from django.core.management.base import BaseCommand
from api.models import TravelSpotCategory, TravelSpot, AccessibilityInfo


class Command(BaseCommand):
    help = '샘플 여행지 데이터를 DB에 로드합니다.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('샘플 데이터 로드 시작...'))

        # 카테고리 생성
        cat_tourism, _ = TravelSpotCategory.objects.get_or_create(
            name='관광지',
            defaults={'description': '관광지 관련 여행지', 'icon': '🏛️'}
        )
        cat_culture, _ = TravelSpotCategory.objects.get_or_create(
            name='문화시설',
            defaults={'description': '문화시설 관련 여행지', 'icon': '🎭'}
        )
        cat_leisure, _ = TravelSpotCategory.objects.get_or_create(
            name='레포츠',
            defaults={'description': '레포츠 관련 여행지', 'icon': '⚽'}
        )

        # 여행지 데이터
        spots_data = [
            {
                'content_id': '126508',
                'content_type_id': '12',
                'name': '경복궁',
                'category': cat_tourism,
                'address': '서울특별시 종로구 사직로 161',
                'area_code': '1',
                'sigungu_code': '1',
                'latitude': 37.579617,
                'longitude': 126.977041,
                'description': '조선왕조의 법궁으로 서울의 대표적인 관광지입니다. 무장애 편의시설이 잘 갖춰져 있습니다.',
                'tel': '02-3700-3900',
                'image_url': 'https://images.unsplash.com/photo-1581789164394-8d7a0e9c1d1d',
                'thumbnail_url': 'https://images.unsplash.com/photo-1581789164394-8d7a0e9c1d1d?w=400',
                'rating': 4.8,
                'review_count': 1523,
                'view_count': 45234,
                'bookmark_count': 892,
            },
            {
                'content_id': '264337',
                'content_type_id': '12',
                'name': '남산서울타워',
                'category': cat_tourism,
                'address': '서울특별시 용산구 남산공원길 105',
                'area_code': '1',
                'sigungu_code': '23',
                'latitude': 37.551169,
                'longitude': 126.988227,
                'description': '서울의 랜드마크이자 야경 명소입니다. 엘리베이터와 무장애 시설이 갖춰져 있습니다.',
                'tel': '02-3455-9277',
                'image_url': 'https://images.unsplash.com/photo-1555217851-5f2f3c05394e',
                'thumbnail_url': 'https://images.unsplash.com/photo-1555217851-5f2f3c05394e?w=400',
                'rating': 4.7,
                'review_count': 2341,
                'view_count': 67890,
                'bookmark_count': 1234,
            },
            {
                'content_id': '125405',
                'content_type_id': '12',
                'name': '해운대해수욕장',
                'category': cat_tourism,
                'address': '부산광역시 해운대구 우동',
                'area_code': '6',
                'sigungu_code': '4',
                'latitude': 35.158698,
                'longitude': 129.160384,
                'description': '부산의 대표적인 해수욕장으로 휠체어 접근 가능한 산책로가 있습니다.',
                'tel': '051-749-5700',
                'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19',
                'thumbnail_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400',
                'rating': 4.6,
                'review_count': 3456,
                'view_count': 89012,
                'bookmark_count': 2345,
            },
            {
                'content_id': '264312',
                'content_type_id': '14',
                'name': '국립중앙박물관',
                'category': cat_culture,
                'address': '서울특별시 용산구 서빙고로 137',
                'area_code': '1',
                'sigungu_code': '23',
                'latitude': 37.523926,
                'longitude': 126.980366,
                'description': '한국의 대표적인 박물관으로 완벽한 무장애 시설을 갖추고 있습니다.',
                'tel': '02-2077-9000',
                'image_url': 'https://images.unsplash.com/photo-1581789164394-8d7a0e9c1d1d',
                'thumbnail_url': 'https://images.unsplash.com/photo-1581789164394-8d7a0e9c1d1d?w=400',
                'rating': 4.9,
                'review_count': 987,
                'view_count': 34567,
                'bookmark_count': 678,
            },
            {
                'content_id': '264298',
                'content_type_id': '12',
                'name': '한라산국립공원',
                'category': cat_tourism,
                'address': '제주특별자치도 제주시 1100로 2070-61',
                'area_code': '39',
                'sigungu_code': '1',
                'latitude': 33.362372,
                'longitude': 126.529118,
                'description': '제주도의 상징 한라산으로 일부 코스는 휠체어 접근이 가능합니다.',
                'tel': '064-713-9950',
                'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19',
                'thumbnail_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400',
                'rating': 4.8,
                'review_count': 2156,
                'view_count': 56789,
                'bookmark_count': 1567,
            },
        ]

        for spot_data in spots_data:
            spot, created = TravelSpot.objects.get_or_create(
                content_id=spot_data['content_id'],
                defaults=spot_data
            )
            if created:
                self.stdout.write(f'  + {spot.name} created')

        self.stdout.write(self.style.SUCCESS(f'\nTotal {len(spots_data)} travel spots loaded!'))
