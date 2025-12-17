import json
import time
from django.core.management.base import BaseCommand
from api.services.tour_api import tour_api_service


class Command(BaseCommand):
    help = '공공데이터 API에서 여행지 정보를 가져와 fixture JSON 파일로 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--area-code',
            type=str,
            help='지역 코드 (예: 1=서울, 6=부산, 39=제주)',
        )
        parser.add_argument(
            '--num-of-rows',
            type=int,
            default=100,
            help='페이지당 가져올 데이터 개수 (기본값: 100)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='전체 데이터를 모두 가져옵니다 (페이지네이션 자동)',
        )
        parser.add_argument(
            '--with-details',
            action='store_true',
            help='상세 정보와 무장애 정보도 함께 가져옵니다 (시간이 오래 걸림)',
        )
        parser.add_argument(
            '--output',
            type=str,
            default='api/fixtures/tour_data.json',
            help='출력 파일 경로 (기본값: api/fixtures/tour_data.json)',
        )

    def handle(self, *args, **options):
        area_code = options.get('area_code')
        num_of_rows = options['num_of_rows']
        fetch_all = options['all']
        with_details = options['with_details']
        output_path = options['output']

        self.stdout.write(self.style.SUCCESS('공공데이터 API에서 데이터를 가져오는 중...'))
        if with_details:
            self.stdout.write(self.style.WARNING('상세 정보도 가져옵니다. 시간이 오래 걸릴 수 있습니다.'))

        all_items = []
        page_no = 1

        if fetch_all:
            # 전체 데이터 가져오기
            while True:
                self.stdout.write(f'페이지 {page_no} 가져오는 중...')

                result = tour_api_service.get_area_based_list(
                    area_code=area_code,
                    num_of_rows=num_of_rows,
                    page_no=page_no
                )

                if not result or 'response' not in result:
                    self.stdout.write(self.style.ERROR(f'페이지 {page_no} API 응답 실패'))
                    break

                response_body = result['response'].get('body', {})
                total_count = response_body.get('totalCount', 0)
                items = response_body.get('items', {})

                # items가 딕셔너리이고 'item' 키가 있으면 그것을 사용
                if isinstance(items, dict) and 'item' in items:
                    item_list = items['item']
                else:
                    item_list = []

                if not item_list:
                    self.stdout.write(f'페이지 {page_no}: 데이터 없음 (종료)')
                    break

                all_items.extend(item_list)
                self.stdout.write(self.style.SUCCESS(f'페이지 {page_no}: {len(item_list)}개 가져옴 (누적: {len(all_items)}/{total_count})'))

                # 모든 데이터를 가져왔으면 종료
                if len(all_items) >= total_count:
                    break

                page_no += 1

            item_list = all_items
        else:
            # 단일 페이지만 가져오기
            result = tour_api_service.get_area_based_list(
                area_code=area_code,
                num_of_rows=num_of_rows
            )

            if not result or 'response' not in result:
                self.stdout.write(self.style.ERROR('API 응답 실패'))
                self.stdout.write(f'응답: {result}')
                return

            response_body = result['response'].get('body', {})
            items = response_body.get('items', {})

            # items가 딕셔너리이고 'item' 키가 있으면 그것을 사용
            if isinstance(items, dict) and 'item' in items:
                item_list = items['item']
            else:
                item_list = []

        if not item_list:
            self.stdout.write(self.style.WARNING('데이터가 없습니다.'))
            return

        self.stdout.write(self.style.SUCCESS(f'총 {len(item_list)}개의 데이터를 가져왔습니다.'))

        # 상세 정보 가져오기
        if with_details:
            self.stdout.write(self.style.SUCCESS('상세 정보를 가져오는 중...'))
            self.stdout.write(self.style.WARNING('API Rate Limit 방지를 위해 요청 사이 0.5초 대기'))

            for idx, item in enumerate(item_list, 1):
                content_id = item.get('contentid', '')
                if not content_id:
                    continue

                self.stdout.write(f'[{idx}/{len(item_list)}] {item.get("title", "")} 상세 정보 가져오는 중...')

                try:
                    # 공통 상세 정보
                    detail_result = tour_api_service.get_detail_common(content_id)
                    if detail_result and 'response' in detail_result:
                        detail_body = detail_result['response'].get('body', {})
                        detail_items = detail_body.get('items', {})
                        if isinstance(detail_items, dict) and 'item' in detail_items:
                            detail_list = detail_items['item']
                            if detail_list and len(detail_list) > 0:
                                detail = detail_list[0]
                                item['overview'] = detail.get('overview', '')
                                item['homepage'] = detail.get('homepage', '')

                    time.sleep(0.5)  # 0.5초 대기

                    # 무장애 관광 정보
                    with_tour_result = tour_api_service.get_detail_with_tour(content_id)
                    if with_tour_result and 'response' in with_tour_result:
                        with_tour_body = with_tour_result['response'].get('body', {})
                        with_tour_items = with_tour_body.get('items', {})
                        if isinstance(with_tour_items, dict) and 'item' in with_tour_items:
                            with_tour_list = with_tour_items['item']
                            if with_tour_list and len(with_tour_list) > 0:
                                with_tour = with_tour_list[0]
                                item['accessibility'] = {
                                    'parking': with_tour.get('parking', ''),
                                    'route': with_tour.get('route', ''),
                                    'publictransport': with_tour.get('publictransport', ''),
                                    'restroom': with_tour.get('restroom', ''),
                                    'wheelchair': with_tour.get('wheelchair', ''),
                                    'exit': with_tour.get('exit', ''),
                                    'elevator': with_tour.get('elevator', ''),
                                    'parkinginfo': with_tour.get('parkinginfo', ''),
                                    'routeinfo': with_tour.get('routeinfo', ''),
                                }

                    time.sleep(0.5)  # 0.5초 대기

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ⚠ 상세 정보 가져오기 실패: {e}'))
                    continue

            self.stdout.write(self.style.SUCCESS('상세 정보 가져오기 완료!'))

        # Fixture 형식으로 변환
        fixtures = []

        # 카테고리 먼저 생성
        categories = set()
        for item in item_list:
            cat_name = self._get_category_name(item.get('contenttypeid', ''))
            if cat_name:
                categories.add(cat_name)

        # 카테고리 fixture
        for idx, cat_name in enumerate(sorted(categories), start=1):
            fixtures.append({
                "model": "api.travelspotcategory",
                "pk": idx,
                "fields": {
                    "name": cat_name,
                    "description": f"{cat_name} 관련 여행지",
                    "icon": ""
                }
            })

        category_map = {name: idx for idx, name in enumerate(sorted(categories), start=1)}

        # TravelSpot fixture
        for idx, item in enumerate(item_list, start=1):
            cat_name = self._get_category_name(item.get('contenttypeid', ''))
            category_id = category_map.get(cat_name) if cat_name else None

            fixture_item = {
                "model": "api.travelspot",
                "pk": idx,
                "fields": {
                    "content_id": item.get('contentid', ''),
                    "content_type_id": item.get('contenttypeid', ''),
                    "name": item.get('title', '제목 없음'),
                    "category": category_id,
                    "address": item.get('addr1', ''),
                    "area_code": item.get('areacode', ''),
                    "sigungu_code": item.get('sigungucode', ''),
                    "latitude": self._to_decimal(item.get('mapy')),
                    "longitude": self._to_decimal(item.get('mapx')),
                    "description": item.get('overview', ''),
                    "tel": item.get('tel', ''),
                    "homepage": item.get('homepage', ''),
                    "image_url": item.get('firstimage', ''),
                    "thumbnail_url": item.get('firstimage2', ''),
                    "rating": 0.00,
                    "review_count": 0,
                    "view_count": 0,
                    "bookmark_count": 0,
                    "is_active": True,
                    "last_synced_at": None
                }
            }
            fixtures.append(fixture_item)

            # 무장애 정보가 있으면 AccessibilityInfo도 추가
            if 'accessibility' in item and item['accessibility']:
                acc = item['accessibility']
                accessibility_fixture = {
                    "model": "api.accessibilityinfo",
                    "pk": idx,
                    "fields": {
                        "travel_spot": idx,
                        "parking": acc.get('parking', '') == 'Y',
                        "route": acc.get('route', '') == 'Y',
                        "public_transport": acc.get('publictransport', '') == 'Y',
                        "restroom": acc.get('restroom', '') == 'Y',
                        "wheelchair": acc.get('wheelchair', '') == 'Y',
                        "exit": acc.get('exit', '') == 'Y',
                        "elevator": acc.get('elevator', '') == 'Y',
                        "audio_guide": False,
                        "parking_info": acc.get('parkinginfo', ''),
                        "route_info": acc.get('routeinfo', ''),
                        "restroom_info": '',
                        "wheelchair_info": '',
                        "exit_info": '',
                        "elevator_info": '',
                        "braile_block": False,
                        "help_dog": False,
                        "guide_system": False,
                        "stroller": False,
                        "lactation_room": False
                    }
                }
                fixtures.append(accessibility_fixture)

        # JSON 파일로 저장
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'✓ {output_path} 파일로 저장되었습니다.'))
        self.stdout.write(self.style.SUCCESS(f'총 {len(fixtures)}개의 fixture 생성 (카테고리 {len(categories)}개 + 여행지 {len(item_list)}개)'))

    def _get_category_name(self, content_type_id):
        """콘텐츠 타입 ID를 카테고리명으로 변환"""
        category_map = {
            '12': '관광지',
            '14': '문화시설',
            '15': '축제/공연/행사',
            '25': '여행코스',
            '28': '레포츠',
            '32': '숙박',
            '38': '쇼핑',
            '39': '음식점'
        }
        return category_map.get(str(content_type_id), '기타')

    def _to_decimal(self, value):
        """문자열을 Decimal로 변환 (실패시 None)"""
        if not value:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
