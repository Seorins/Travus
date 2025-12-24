import os
import django
import random

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travus.settings')
django.setup()

from api.models import Course

print("=== 코스 조회수 추가 시작 ===\n")

# 모든 코스 가져오기
courses = list(Course.objects.all().order_by('-like_count'))
print(f"총 {len(courses)}개의 코스 발견\n")

# 조회수 설정
# 좋아요가 많을수록 조회수도 높게 설정
# 좋아요의 3~10배 정도로 랜덤 설정

for idx, course in enumerate(courses):
    like_count = course.like_count

    # 좋아요 수에 비례하여 조회수 설정
    # 최소: 좋아요 * 3, 최대: 좋아요 * 10
    # 추가로 랜덤 보너스 0~100

    if like_count > 0:
        min_views = like_count * 3
        max_views = like_count * 10
        view_count = random.randint(min_views, max_views) + random.randint(0, 100)
    else:
        # 좋아요가 0이면 조회수는 1~50
        view_count = random.randint(1, 50)

    # 조회수 업데이트
    course.view_count = view_count
    course.save()

    print(f"[{idx+1}/{len(courses)}] {course.title[:35]:35s} - 좋아요: {like_count:3d} | 조회수: {view_count:4d}")

print(f"\n=== 완료! 모든 코스에 조회수가 추가되었습니다 ===")

# 통계
total_views = sum(c.view_count for c in courses)
avg_views = total_views / len(courses) if courses else 0
print(f"\n통계:")
print(f"  총 조회수: {total_views:,}")
print(f"  평균 조회수: {avg_views:.0f}")
print(f"  최고 조회수: {max(c.view_count for c in courses)}")
print(f"  최저 조회수: {min(c.view_count for c in courses)}")
