from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Course, CourseSpot, TravelSpot, CourseLike
from random import randint, choice, sample
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = '테스트용 더미 코스 데이터 생성'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='생성할 코스 개수 (기본값: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']

        # 기존 사용자 가져오기 (없으면 생성)
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING('사용자가 없습니다. 테스트 사용자를 생성합니다.'))
            for i in range(5):
                user = User.objects.create_user(
                    username=f'testuser{i+1}',
                    password='testpass123',
                    first_name=f'테스터{i+1}',
                    email=f'test{i+1}@example.com'
                )
                users.append(user)
            self.stdout.write(self.style.SUCCESS(f'{len(users)}명의 테스트 사용자를 생성했습니다.'))

        # 여행지 데이터 가져오기
        travel_spots_by_area = {}
        for area_code in ['1', '2', '3', '4', '5', '6', '31', '32', '39']:
            spots = list(TravelSpot.objects.filter(area_code=area_code)[:50])
            if spots:
                travel_spots_by_area[area_code] = spots

        if not travel_spots_by_area:
            self.stdout.write(self.style.ERROR('여행지 데이터가 없습니다. 먼저 여행지를 등록하세요.'))
            return

        # 코스 제목 템플릿
        title_templates = [
            '{region} 당일치기 여행',
            '{region} 1박2일 여행 코스',
            '{region} 문화탐방 코스',
            '{region} 맛집 투어',
            '{region} 힐링 여행',
            '{region} 가족 여행 코스',
            '{region} 데이트 코스',
            '{region} 사진 명소 투어',
            '{region} 역사 탐방',
            '{region} 자연 힐링 코스'
        ]

        region_names = {
            '1': '서울', '2': '인천', '3': '대전', '4': '대구',
            '5': '광주', '6': '부산', '31': '경기', '32': '강원', '39': '제주'
        }

        created_count = 0
        for i in range(count):
            # 랜덤 지역 선택
            area_code = choice(list(travel_spots_by_area.keys()))
            region_name = region_names.get(area_code, '지역')
            spots_pool = travel_spots_by_area[area_code]

            # 랜덤 사용자 선택
            user = choice(users)

            # 코스 기본 정보
            title = choice(title_templates).format(region=region_name)
            description = f'{region_name}의 아름다운 명소를 둘러보는 추천 여행 코스입니다.'

            # 랜덤 날짜 (최근 60일 이내)
            days_ago = randint(0, 60)
            created_at = datetime.now() - timedelta(days=days_ago)

            # 공개 여부 (80% 공개)
            is_public = randint(1, 10) <= 8

            # 코스 생성
            course = Course.objects.create(
                user=user,
                title=title,
                description=description,
                is_public=is_public,
                like_count=randint(0, 50),
                view_count=randint(0, 200),
                created_at=created_at
            )

            # 코스에 여행지 추가 (3~6개)
            num_spots = randint(3, 6)
            selected_spots = sample(spots_pool, min(num_spots, len(spots_pool)))

            for order, spot in enumerate(selected_spots, 1):
                CourseSpot.objects.create(
                    course=course,
                    travel_spot=spot,
                    order=order,
                    memo=''
                )

            # 랜덤 좋아요 추가 (일부 사용자만)
            like_users = sample(users, min(randint(0, len(users)), len(users)))
            for like_user in like_users:
                CourseLike.objects.create(user=like_user, course=course)

            created_count += 1

            if created_count % 10 == 0:
                self.stdout.write(f'{created_count}개 코스 생성 중...')

        self.stdout.write(
            self.style.SUCCESS(f'✅ 총 {created_count}개의 더미 코스를 생성했습니다!')
        )
