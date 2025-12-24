import os
import django
import random

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travus.settings')
django.setup()

from api.models import Course, CourseLike
from django.contrib.auth import get_user_model

User = get_user_model()

print("=== 코스 소유자 및 좋아요 업데이트 시작 ===\n")

# 모든 유저 가져오기
users = list(User.objects.all())
print(f"총 {len(users)}명의 유저 발견")

if len(users) < 10:
    print("유저가 너무 적습니다. 먼저 더미 유저를 생성해주세요.")
    exit(1)

# 모든 코스 가져오기
courses = list(Course.objects.all())
print(f"총 {len(courses)}개의 코스 발견\n")

# 1. 코스 소유자를 랜덤 유저로 변경 (admin은 유지하되, 일부만)
print("=== 1단계: 코스 소유자 다양화 ===")
admin_course_count = 0
for idx, course in enumerate(courses):
    # 30% 확률로 admin 유지, 70%는 랜덤 유저로 변경
    if random.random() < 0.3:
        # admin 유지 (이미 admin이면 그대로)
        admin_course_count += 1
    else:
        # 랜덤 유저로 변경
        new_owner = random.choice(users)
        course.user = new_owner
        course.save()

    print(f"[{idx+1}/{len(courses)}] {course.title[:30]:30s} - 소유자: {course.user.username}")

print(f"\n총 {admin_course_count}개의 코스가 admin 소유, {len(courses) - admin_course_count}개가 다른 유저 소유\n")

# 2. 기존 좋아요 삭제
print("=== 2단계: 기존 좋아요 데이터 삭제 ===")
deleted_count = CourseLike.objects.all().delete()[0]
print(f"{deleted_count}개의 기존 좋아요 삭제됨\n")

# 3. 새로운 좋아요 데이터 생성 (여러 유저들이 좋아요)
print("=== 3단계: 새로운 좋아요 데이터 생성 ===")
for idx, course in enumerate(courses):
    target_like_count = course.like_count  # 기존에 설정된 좋아요 수

    # 랜덤 유저들을 선택해서 좋아요 추가
    # 좋아요 수만큼 랜덤 유저 선택 (중복 없이)
    like_user_count = min(target_like_count, len(users))
    like_users = random.sample(users, like_user_count)

    created_likes = 0
    for user in like_users:
        try:
            CourseLike.objects.create(
                course=course,
                user=user
            )
            created_likes += 1
        except:
            # 중복 또는 에러 무시
            pass

    # 실제 좋아요 수 업데이트
    actual_like_count = CourseLike.objects.filter(course=course).count()
    course.like_count = actual_like_count
    course.save()

    print(f"[{idx+1}/{len(courses)}] {course.title[:30]:30s} - 좋아요: {actual_like_count}개 (목표: {target_like_count})")

print(f"\n=== 완료! ===")
print(f"- {len(courses)}개의 코스 소유자 다양화 완료")
print(f"- 여러 유저들의 좋아요 데이터 생성 완료")
