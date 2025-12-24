import os
import django
import random

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travus.settings')
django.setup()

from api.models import Course, CourseLike
from django.contrib.auth import get_user_model

User = get_user_model()

# admin 유저 가져오기
try:
    admin_user = User.objects.get(username='admin')
    print(f"좋아요 생성 유저: {admin_user.username}")
except User.DoesNotExist:
    print("에러: 'admin' 유저가 없습니다.")
    exit(1)

# 모든 코스 가져오기
courses = list(Course.objects.all().order_by('id'))
print(f"총 {len(courses)}개의 코스 발견")

if len(courses) == 0:
    print("코스가 없습니다!")
    exit(1)

# 좋아요 개수를 다양하게 분포시키기
# Best 30에 들어갈 코스들은 좋아요를 많이 (50~150개)
# 나머지는 적게 (0~30개)

like_count_distribution = []

# 상위 30개는 높은 좋아요
for i in range(min(30, len(courses))):
    like_count_distribution.append(random.randint(50, 150))

# 나머지는 낮은 좋아요
for i in range(len(courses) - min(30, len(courses))):
    like_count_distribution.append(random.randint(0, 30))

# 섞기
random.shuffle(like_count_distribution)

# 각 코스에 좋아요 개수 설정
for idx, course in enumerate(courses):
    like_count = like_count_distribution[idx]

    # like_count 필드 직접 업데이트
    course.like_count = like_count
    course.save()

    print(f"[{idx+1}/{len(courses)}] {course.title[:30]}... - 좋아요: {like_count}개")

print(f"\n완료! 모든 코스에 좋아요가 추가되었습니다.")

# Best 30 확인
print("\n=== 좋아요 TOP 30 ===")
top_courses = Course.objects.all().order_by('-like_count')[:30]
for idx, course in enumerate(top_courses):
    print(f"{idx+1}. {course.title} - {course.like_count}개")
