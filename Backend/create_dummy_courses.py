import os
import django
import random
from datetime import datetime, timedelta

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travus.settings')
django.setup()

from api.models import TravelSpot, Course, CourseSpot
from django.contrib.auth import get_user_model

User = get_user_model()

# 코스 제목 템플릿
COURSE_TITLES = [
    "{region} 맛집 투어 {days}일",
    "{region} 문화유산 탐방 {days}일",
    "{region} 자연 힐링 여행 {days}일",
    "{region} 핫플레이스 {days}일",
    "{region} 당일치기 여행",
    "{region} 가족 여행 코스 {days}일",
    "{region} 커플 데이트 코스",
    "{region} 사진 맛집 투어 {days}일",
    "{region} 역사 탐방 {days}일",
    "{region} 먹방 여행 {days}일",
]

DESCRIPTIONS = [
    "인스타그램 감성 가득한 여행 코스입니다!",
    "현지인 추천 맛집과 명소를 담았습니다.",
    "가족과 함께 즐기기 좋은 코스예요.",
    "연인과 함께 로맨틱한 여행을 즐겨보세요.",
    "힐링이 필요할 때 추천하는 코스입니다.",
    "사진 찍기 좋은 장소들로 구성했어요!",
    "먹방 여행자를 위한 특별한 코스입니다.",
    "역사와 문화를 느낄 수 있는 여행이에요.",
    "자연과 함께하는 힐링 여행 코스입니다.",
    "SNS에서 핫한 장소들만 모았어요!",
]

REGIONS = {
    '1': '서울',
    '2': '인천',
    '3': '대전',
    '4': '대구',
    '5': '광주',
    '6': '부산',
    '7': '울산',
    '31': '경기',
    '32': '강원',
    '39': '제주'
}

# 이미지가 있는 여행지만 가져오기
spots_with_images = list(TravelSpot.objects.exclude(image_url='').exclude(image_url__isnull=True))

print(f"총 {len(spots_with_images)}개의 이미지 있는 여행지 발견")

# admin 유저 가져오기
try:
    user = User.objects.get(username='admin')
    print(f"코스 생성 유저: {user.username}")
except User.DoesNotExist:
    print("에러: 'admin' 유저가 없습니다. 먼저 admin 유저를 생성해주세요.")
    exit(1)
except Exception as e:
    print(f"유저 조회 실패: {e}")
    exit(1)

# 50개의 코스 생성
created_count = 0
for i in range(50):
    try:
        # 랜덤으로 일정 결정 (1~3일)
        days = random.randint(1, 3)

        # 랜덤 지역 선택
        region_code = random.choice(list(REGIONS.keys()))
        region_name = REGIONS[region_code]

        # 해당 지역의 이미지 있는 여행지들 필터링
        region_spots = [s for s in spots_with_images if s.area_code == region_code]

        # 해당 지역에 여행지가 충분하지 않으면 전체에서 선택
        if len(region_spots) < days * 3:
            region_spots = spots_with_images

        # 코스 제목 생성
        title_template = random.choice(COURSE_TITLES)
        title = title_template.format(region=region_name, days=days)

        # 코스 생성
        course = Course.objects.create(
            user=user,
            title=title,
            description=random.choice(DESCRIPTIONS),
            is_public=True,
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )

        # 각 날짜별로 여행지 추가 (하루에 3-5개)
        order = 1
        used_spots = set()

        for day in range(days):
            spots_per_day = random.randint(3, 5)

            for _ in range(spots_per_day):
                # 중복되지 않은 여행지 선택
                available_spots = [s for s in region_spots if s.id not in used_spots]
                if not available_spots:
                    break

                spot = random.choice(available_spots)
                used_spots.add(spot.id)

                # CourseSpot 생성
                CourseSpot.objects.create(
                    course=course,
                    travel_spot=spot,
                    order=order,
                    memo=f"Day {day + 1} - {order}번째 장소"
                )
                order += 1

        created_count += 1
        print(f"[{created_count}/50] 코스 생성 완료: {title} ({order-1}개 장소)")

    except Exception as e:
        print(f"코스 생성 실패 ({i+1}번째): {e}")
        continue

print(f"\n✅ 총 {created_count}개의 더미 코스가 생성되었습니다!")
