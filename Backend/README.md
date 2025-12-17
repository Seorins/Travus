# TravUs Backend - Django REST Framework

무장애 여행 서비스 TravUs의 백엔드 API 서버입니다.

## 설정 완료 내역

### 1. 환경 변수 설정 (.env)
- ✅ `.env` 파일 생성 완료
- ✅ 한국관광공사 공공데이터 API 키 설정
- ✅ Django 기본 설정 (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- ✅ CORS 설정 (Frontend 연동)
- ✅ Redis 캐시 설정

### 2. 데이터베이스 모델 설계 (api/models.py)

설계서 ERD 기반으로 다음 8개 모델 생성 완료:

#### User (사용자)
- AbstractUser 상속
- 장애 유형 (DISABILITY_CHOICES)
- 선호 접근성 옵션 (JSONField)
- 전화번호, 가입일, 수정일

#### TravelSpotCategory (여행지 카테고리)
- 카테고리명, 설명, 아이콘

#### TravelSpot (여행지 정보)
- 공공데이터 API 필드 (content_id, content_type_id)
- 기본 정보 (이름, 카테고리, 설명)
- 위치 정보 (주소, 지역코드, 시군구코드, 위도, 경도)
- 연락처 (전화번호, 홈페이지)
- 이미지 (대표 이미지, 썸네일)
- 통계 (평점, 리뷰 수, 조회수, 북마크 수)
- 메타 정보 (활성화 여부, 마지막 동기화 시간)

#### AccessibilityInfo (무장애 관광 정보)
- TravelSpot와 1:1 관계
- 접근성 시설 (주차장, 화장실, 휠체어, 승강기, 음성안내 등)
- 각 시설별 상세 정보 (TextField)
- 기타 정보 (점자블록, 안내견, 유모차, 수유실 등)

#### Bookmark (북마크)
- User-TravelSpot 관계
- 메모 기능
- unique_together 제약조건

#### Course (여행 코스)
- 사용자 생성 여행 코스
- 총 거리, 예상 소요시간
- 공개 설정, 좋아요, 조회수

#### CourseSpot (코스 내 여행지)
- Course-TravelSpot 다대다 관계 중간 테이블
- 순서, 메모, 체류 시간

#### Review (리뷰)
- User-TravelSpot 리뷰
- 평점, 접근성 평점
- 이미지 (JSONField 배열)
- 좋아요 수

### 3. Django 설정 (travus/settings.py)

✅ 환경 변수 로드 (python-dotenv)
✅ REST Framework 설정
✅ CORS 설정
✅ 커스텀 User 모델 설정 (AUTH_USER_MODEL)
✅ 한국어/서울 시간대 설정
✅ 공공데이터 API 설정
✅ Redis 캐시 설정

### 4. Django Admin 설정 (api/admin.py)

✅ 모든 모델 Admin 등록
✅ 한글 verbose_name 설정
✅ 검색, 필터, 정렬 기능
✅ 읽기 전용 필드 설정

### 5. 패키지 설치 (requirements.txt)

추가된 패키지:
- `django-cors-headers` - CORS 처리
- `python-dotenv` - 환경 변수 관리
- `redis` - 캐시 시스템

## 다음 단계

### 마이그레이션 (사용자가 직접 실행)

```bash
# 가상환경 활성화
source venv/Scripts/activate  # Windows Git Bash
# 또는
venv\Scripts\activate  # Windows CMD

# 패키지 설치
pip install -r requirements.txt

# 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 실행
python manage.py migrate

# 관리자 계정 생성
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```

### API 개발 예정 작업

1. **Serializers 생성** (`api/serializers.py`)
   - 각 모델에 대한 Serializer 클래스
   - 중첩 Serializer (AccessibilityInfo, CourseSpot 등)

2. **ViewSets 생성** (`api/views.py`)
   - TravelSpotViewSet
   - BookmarkViewSet
   - CourseViewSet
   - ReviewViewSet

3. **공공데이터 API 연동** (`api/services/tour_api.py`)
   - 지역 기반 여행지 목록 조회
   - 무장애 정보 조회
   - 키워드 검색
   - 데이터 동기화 스크립트

4. **URL 설정** (`api/urls.py`, `travus/urls.py`)
   - Router 설정
   - API 엔드포인트 구성

## 공공데이터 API 정보

- **서비스명**: 한국관광공사_무장애여행정보서비스
- **Base URL**: http://apis.data.go.kr/B551011/KorWithService1
- **인증키**: .env 파일에 설정됨 (TOUR_API_KEY)

### 주요 API 엔드포인트

1. `areaBasedList1` - 지역 기반 관광정보 조회
2. `detailWithTour1` - 무장애 관광정보 조회
3. `detailCommon1` - 공통정보 조회
4. `searchKeyword1` - 키워드 검색

## 디렉토리 구조

```
Backend/
├── .env                    # 환경 변수 (gitignore에 추가)
├── manage.py
├── requirements.txt
├── travus/
│   ├── settings.py        # Django 설정
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── models.py          # 데이터베이스 모델
    ├── admin.py           # Django Admin 설정
    ├── serializers.py     # (생성 예정)
    ├── views.py           # (생성 예정)
    └── urls.py            # (생성 예정)
```

## 주의사항

- `.env` 파일은 절대 Git에 커밋하지 않습니다
- API 키는 외부에 노출되지 않도록 관리합니다
- 마이그레이션은 사용자가 직접 실행해야 합니다
