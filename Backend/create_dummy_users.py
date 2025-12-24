import os
import django
import random

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travus.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 한국 이름 리스트
LAST_NAMES = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전']
FIRST_NAMES = [
    '민준', '서준', '예준', '도윤', '시우', '주원', '하준', '지호', '지우', '준서',
    '서연', '서윤', '지우', '서현', '민서', '하은', '하윤', '윤서', '지민', '채원',
    '수빈', '예은', '지원', '소율', '다은', '은서', '가은', '하린', '시은', '수아',
    '준영', '현우', '예성', '태양', '동현', '우진', '승현', '재윤', '건우', '지훈',
    '민재', '승우', '시현', '유진', '현서', '준혁', '태민', '재원', '성민', '상우'
]

# 이메일 도메인
EMAIL_DOMAINS = ['gmail.com', 'naver.com', 'daum.net', 'kakao.com', 'hanmail.net']

# 지역 번호
AREA_CODES = ['010']

print("=== 더미 유저 50명 생성 시작 ===\n")

created_count = 0
password = 'ssafy1234!'  # 통일된 비밀번호

for i in range(1, 51):
    try:
        # 랜덤 이름 생성
        last_name = random.choice(LAST_NAMES)
        first_name = random.choice(FIRST_NAMES)
        full_name = f"{last_name}{first_name}"

        # 유저네임 생성 (중복 방지를 위해 번호 추가)
        username = f"user{i:02d}"

        # 이미 존재하는 유저는 스킵
        if User.objects.filter(username=username).exists():
            print(f"[SKIP] {username} - 이미 존재하는 유저")
            continue

        # 이메일 생성
        email_domain = random.choice(EMAIL_DOMAINS)
        email = f"{username}@{email_domain}"

        # 전화번호 생성 (010-XXXX-XXXX)
        area_code = random.choice(AREA_CODES)
        middle = f"{random.randint(1000, 9999)}"
        last = f"{random.randint(1000, 9999)}"
        phone_number = f"{area_code}-{middle}-{last}"

        # 유저 생성
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # 전화번호 저장 (User 모델에 phone 필드가 있다면)
        if hasattr(user, 'phone'):
            user.phone = phone_number
            user.save()

        created_count += 1
        print(f"[{created_count}/50] {username:10s} | {full_name:6s} | {email:25s} | {phone_number}")

    except Exception as e:
        print(f"[ERROR] user{i:02d} 생성 실패: {e}")
        continue

print(f"\n=== 완료! 총 {created_count}명의 유저가 생성되었습니다 ===")
print(f"\n로그인 정보:")
print(f"  아이디: user01 ~ user50")
print(f"  비밀번호: {password}")
