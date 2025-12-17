from django.core.management.base import BaseCommand
from django.utils import timezone
from api.services.tour_api import tour_api_service
from api.models import TravelSpot, TravelSpotCategory, AccessibilityInfo


class Command(BaseCommand):
    help = '공공데이터 API에서 여행지 정보를 가져와 DB에 저장합니다.'

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
            help='가져올 데이터 개수 (기본값: 100)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터를 삭제하고 새로 불러옵니다',
        )

    def handle(self, *args, **options):
        area_code = options.get('area_code')
        num_of_rows = options['num_of_rows']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write(self.style.WARNING('기존 데이터를 삭제하는 중...'))
            TravelSpot.objects.all().delete()
            TravelSpotCategory.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ 기존 데이터 삭제 완료'))

        self.stdout.write(self.style.SUCCESS('공공데이터 API에서 데이터를 가져오는 중...'))

        # API 호출
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

        total_count = response_body.get('totalCount', 0)
        self.stdout.write(self.style.SUCCESS(f'총 {total_count}개 중 {len(item_list)}개의 데이터를 가져왔습니다.'))

        # 카테고리 생성
        created_categories = 0
        category_map = {}

        for item in item_list:
            content_type_id = item.get('contenttypeid', '')
            cat_name = self._get_category_name(content_type_id)

            if cat_name and cat_name not in category_map:
                category, created = TravelSpotCategory.objects.get_or_create(
                    name=cat_name,
                    defaults={
                        'description': f'{cat_name} 관련 여행지'
                    }
                )
                category_map[cat_name] = category
                if created:
                    created_categories += 1

        self.stdout.write(self.style.SUCCESS(f'✓ 카테고리 {created_categories}개 생성'))

        # 여행지 생성
        created_spots = 0
        updated_spots = 0

        for item in item_list:
            content_id = item.get('contentid', '')
            if not content_id:
                continue

            cat_name = self._get_category_name(item.get('contenttypeid', ''))
            category = category_map.get(cat_name)

            # 여행지 생성 또는 업데이트
            travel_spot, created = TravelSpot.objects.update_or_create(
                content_id=content_id,
                defaults={
                    'content_type_id': item.get('contenttypeid', ''),
                    'name': item.get('title', '제목 없음'),
                    'category': category,
                    'address': item.get('addr1', ''),
                    'area_code': item.get('areacode', ''),
                    'sigungu_code': item.get('sigungucode', ''),
                    'latitude': self._to_decimal(item.get('mapy')),
                    'longitude': self._to_decimal(item.get('mapx')),
                    'tel': item.get('tel', ''),
                    'image_url': item.get('firstimage', ''),
                    'thumbnail_url': item.get('firstimage2', ''),
                    'is_active': True,
                    'last_synced_at': timezone.now()
                }
            )

            if created:
                created_spots += 1
            else:
                updated_spots += 1

            # 상세 정보 가져오기 (선택적)
            # self._fetch_detail_info(travel_spot, content_id)

        self.stdout.write(self.style.SUCCESS(f'✓ 여행지 {created_spots}개 생성, {updated_spots}개 업데이트'))
        self.stdout.write(self.style.SUCCESS('데이터 로드 완료!'))

    def _fetch_detail_info(self, travel_spot, content_id):
        """상세 정보 및 무장애 정보 가져오기"""
        # 공통 상세 정보
        detail_result = tour_api_service.get_detail_common(content_id)
        if detail_result and 'response' in detail_result:
            detail_body = detail_result['response'].get('body', {})
            detail_items = detail_body.get('items', {})

            if isinstance(detail_items, dict) and 'item' in detail_items:
                detail_list = detail_items['item']
                if detail_list and len(detail_list) > 0:
                    detail = detail_list[0]
                    travel_spot.description = detail.get('overview', '')
                    travel_spot.homepage = detail.get('homepage', '')
                    travel_spot.save()

        # 무장애 관광 정보
        with_tour_result = tour_api_service.get_detail_with_tour(content_id)
        if with_tour_result and 'response' in with_tour_result:
            with_tour_body = with_tour_result['response'].get('body', {})
            with_tour_items = with_tour_body.get('items', {})

            if isinstance(with_tour_items, dict) and 'item' in with_tour_items:
                with_tour_list = with_tour_items['item']
                if with_tour_list and len(with_tour_list) > 0:
                    with_tour = with_tour_list[0]

                    # AccessibilityInfo 생성
                    AccessibilityInfo.objects.update_or_create(
                        travel_spot=travel_spot,
                        defaults={
                            'parking': with_tour.get('parking', '') == 'Y',
                            'route': with_tour.get('route', '') == 'Y',
                            'public_transport': with_tour.get('publictransport', '') == 'Y',
                            'restroom': with_tour.get('restroom', '') == 'Y',
                            'wheelchair': with_tour.get('wheelchair', '') == 'Y',
                            'exit': with_tour.get('exit', '') == 'Y',
                            'elevator': with_tour.get('elevator', '') == 'Y',
                            'parking_info': with_tour.get('parkinginfo', ''),
                            'route_info': with_tour.get('routeinfo', ''),
                            'restroom_info': with_tour.get('restroominfo', ''),
                        }
                    )

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
