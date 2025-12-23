# AI 여행 코스 생성 기능 구현 완료

## 구현 완료 항목

### ✅ Backend 구현

#### 1. AI 코스 생성 서비스 (`Backend/api/services/ai_course_generator.py`)
- GMS API를 통한 OpenAI GPT-4o-mini 호출
- 여행 기간별 순서 패턴 정의
  - 당일치기: 6개 (여행-여행-식당-여행-여행-식당)
  - 1박 2일: 12개 (Day 1, Day 2 각각 6개)
  - 2박 3일: 18개 (Day 1, 2, 3 각각 6개)
- 시스템 프롬프트 및 사용자 프롬프트 자동 생성
- AI 응답 검증 로직 (ID 존재 여부, 순서 패턴 준수 확인)
- 동선 최적화 (위도/경도 기반)

#### 2. Django 설정 (`Backend/travus/settings.py`)
```python
GMS_API_KEY = 'S14P02EA02-e78f608f-87c7-4534-a076-6916104b3bdc'
GMS_API_URL = 'https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions'
GMS_MODEL = 'gpt-4o-mini'
```

#### 3. CourseViewSet API 엔드포인트 (`Backend/api/views.py`)
```python
POST /api/courses/generate_ai_course/

Request Body:
{
  "region": "서울",           // 지역명
  "area_code": "1",          // 지역 코드
  "duration": "1박 2일",     // 여행 기간
  "themes": ["역사·문화"]    // 테마 (선택사항)
}

Response:
{
  "title": "AI가 생성한 코스 제목",
  "description": "코스 설명",
  "itinerary": [
    {
      "day": 1,
      "order": 1,
      "type": "travel",
      "id": 123,
      "spot_detail": { /* TravelSpot 상세 정보 */ }
    },
    ...
  ]
}
```

**주요 기능:**
- DB에서 해당 지역의 여행지 조회 (이미지, 위치 정보 필수)
- 여행지/음식점 충분성 검증
- AI 코스 생성 요청
- 생성된 ID로 상세 정보 조회 및 응답

---

### ✅ Frontend 구현

#### 1. API 서비스 추가 (`Frontend/travus/src/services/api.js`)
```javascript
// AI 코스 생성
generateAICourse(data) {
  return apiClient.post('/courses/generate_ai_course/', data, {
    timeout: 60000 // AI 응답 대기 60초
  })
}

// 코스 저장
saveCourse(data) {
  return apiClient.post('/courses/', data)
}
```

#### 2. CourseView 업데이트 (`Frontend/travus/src/views/CourseView.vue`)
**주요 변경사항:**
- 지역 코드 매핑 추가 (서울: "1", 부산: "6" 등)
- `generateCourse()` 함수를 실제 AI API 호출로 변경
- 응답 데이터를 day별로 그룹핑 및 정렬
- 에러 처리 (타임아웃, 데이터 부족, API 오류)

**데이터 흐름:**
```
사용자 선택 → AI API 호출 → 응답 가공 → CourseResult 렌더링
```

#### 3. CourseResult 저장 기능 (`Frontend/travus/src/components/course/CourseResult.vue`)
- 저장 버튼 추가 (북마크 아이콘 → 저장 아이콘)
- `saveCourse()` 함수 구현
- 저장 상태 관리 (isSaving, isSaved)
- 인증 오류 처리

---

## 데이터 흐름 전체 구조

```
┌─────────────┐
│   사용자     │
└──────┬──────┘
       │ 1. 지역, 기간, 테마 선택
       ▼
┌─────────────────────┐
│  CourseView.vue     │
│  generateCourse()   │
└──────┬──────────────┘
       │ 2. API 호출
       ▼
┌──────────────────────────────────┐
│  Backend - CourseViewSet         │
│  generate_ai_course()            │
│                                  │
│  ① DB 조회 (해당 지역 여행지)    │
│  ② 데이터 충분성 검증            │
│  ③ AI 서비스 호출                │
└──────┬───────────────────────────┘
       │ 3. AI 요청
       ▼
┌──────────────────────────────────┐
│  ai_course_generator.py          │
│                                  │
│  ① 시스템 프롬프트 생성          │
│  ② 사용자 프롬프트 생성          │
│  ③ GMS API 호출 (OpenAI)        │
│  ④ 응답 검증                     │
└──────┬───────────────────────────┘
       │ 4. AI 응답
       ▼
┌──────────────────────────────────┐
│  GMS API (SSAFY OpenAI Gateway) │
│  GPT-4o-mini                     │
└──────┬───────────────────────────┘
       │ 5. 생성된 코스 (ID만)
       ▼
┌──────────────────────────────────┐
│  Backend - generate_ai_course()  │
│                                  │
│  ① ID 목록 추출                  │
│  ② DB에서 상세 정보 조회         │
│  ③ itinerary에 상세 정보 추가   │
└──────┬───────────────────────────┘
       │ 6. 완성된 응답
       ▼
┌──────────────────────────────────┐
│  CourseView.vue                  │
│                                  │
│  ① day별 그룹핑                  │
│  ② 순서별 정렬                   │
│  ③ generatedCourse에 저장        │
└──────┬───────────────────────────┘
       │ 7. 렌더링
       ▼
┌──────────────────────────────────┐
│  CourseResult.vue                │
│                                  │
│  - 카카오맵 표시                 │
│  - 마커 및 경로선                │
│  - 장소 리스트                   │
│  - 저장 버튼                     │
└──────────────────────────────────┘
```

---

## 테스트 방법

### 1. Backend 서버 실행
```bash
cd Backend
python manage.py runserver
```

### 2. Frontend 서버 실행
```bash
cd Frontend/travus
npm run dev
```

### 3. 테스트 시나리오

#### 시나리오 1: 당일치기 코스 생성
1. CourseView 접속 (`/course`)
2. "코스만들기" 클릭
3. 지역 선택: **서울**
4. 여행 기간: **당일치기**
5. 테마 선택: **역사·문화**, **카페** (선택사항)
6. 로딩 화면 → 결과 화면

**예상 결과:**
- 6개 장소 (여행 4개, 식당 2개)
- 서울 지역 내 장소들
- 카카오맵에 마커 표시

#### 시나리오 2: 1박 2일 코스 생성
1. 지역 선택: **부산**
2. 여행 기간: **1박 2일**
3. 테마 선택: **바다**, **음식**
4. 결과 확인

**예상 결과:**
- Day 1: 6개 장소
- Day 2: 6개 장소
- 총 12개 장소
- Day 토글 버튼으로 전환 가능

#### 시나리오 3: 2박 3일 코스 생성
1. 지역 선택: **제주**
2. 여행 기간: **2박 3일**
3. 지역 구성: **한 지역 집중**
4. 테마 선택: **자연**, **액티비티**
5. 결과 확인

**예상 결과:**
- Day 1, 2, 3 각각 6개 장소
- 총 18개 장소

#### 시나리오 4: 코스 저장
1. 코스 생성 완료 후
2. 우측 상단 **저장 버튼** (💾) 클릭
3. 로그인 상태 확인
   - 로그인 O: "코스가 저장되었습니다!" 알림
   - 로그인 X: "로그인이 필요합니다." 알림

---

## 에러 처리

### Backend 에러

| 에러 | 원인 | 해결 방법 |
|------|------|-----------|
| `지역, 지역코드, 여행 기간은 필수입니다` | 필수 파라미터 누락 | Request Body 확인 |
| `해당 지역의 여행지가 부족합니다` | DB에 데이터 부족 | 해당 지역 여행지 추가 필요 |
| `해당 지역의 음식점이 부족합니다` | DB에 음식점 부족 | content_type_id=39인 데이터 추가 |
| `AI 응답 시간 초과` | GMS API 지연 | 재시도 또는 타임아웃 증가 |
| `AI API 호출 중 오류` | 네트워크 오류 | 인터넷 연결 확인 |

### Frontend 에러

| 에러 | 원인 | 해결 방법 |
|------|------|-----------|
| `지역 정보를 찾을 수 없습니다` | regionCodeMap 누락 | 지역 코드 매핑 확인 |
| `요청 시간이 초과되었습니다` | 60초 초과 | 재시도 |
| `로그인이 필요합니다` | 인증 토큰 없음 | 로그인 후 저장 |

---

## 환경 변수 확인

### Backend (`.env`)
```env
GMS_API_KEY=S14P02EA02-e78f608f-87c7-4534-a076-6916104b3bdc
```

### Frontend (`.env`)
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_KAKAO_MAP_API_KEY=YOUR_KAKAO_MAP_KEY
```

---

## 향후 개선 사항

### 1. CourseSpot 자동 저장
현재는 Course만 저장되고, CourseSpot은 저장되지 않음.

**개선 방안:**
```python
# Backend/api/serializers.py에 추가
class CourseCreateSerializer(serializers.ModelSerializer):
    course_spots = CourseSpotSerializer(many=True)

    def create(self, validated_data):
        spots_data = validated_data.pop('course_spots')
        course = Course.objects.create(**validated_data)

        for spot_data in spots_data:
            CourseSpot.objects.create(course=course, **spot_data)

        return course
```

### 2. 숙박 시설 추가
현재는 여행지와 음식점만 포함.

**개선 방안:**
- content_type_id=32 (숙박) 데이터 추가
- 1박 2일, 2박 3일에 accommodation 추가
- 순서 패턴 수정

### 3. 다시뽑기 기능
"다시뽑기" 버튼 클릭 시 같은 조건으로 재생성.

**개선 방안:**
```javascript
const regenerateCourse = async () => {
  currentStep.value = 'loading'
  await generateCourse(selectedThemes.value)
}
```

### 4. 테마 기반 필터링 강화
AI가 테마를 더 잘 반영하도록 프롬프트 개선.

**개선 방안:**
- 여행지 DB에 theme 필드 추가
- AI에게 전달할 때 테마별로 분류
- 시스템 프롬프트에 테마 중요도 강조

---

## 파일 구조

```
travus/
├── Backend/
│   ├── api/
│   │   ├── services/
│   │   │   └── ai_course_generator.py ✨ NEW
│   │   ├── models.py
│   │   ├── views.py (수정: generate_ai_course 추가)
│   │   └── serializers.py
│   └── travus/
│       └── settings.py (수정: GMS_API_KEY 추가)
│
├── Frontend/
│   └── travus/
│       ├── src/
│       │   ├── services/
│       │   │   └── api.js (수정: generateAICourse, saveCourse 추가)
│       │   ├── views/
│       │   │   └── CourseView.vue (수정: AI API 연동)
│       │   └── components/
│       │       └── course/
│       │           └── CourseResult.vue (수정: 저장 기능 추가)
│
└── docs/
    ├── AI_RECOMMENDATION_DESIGN.md ✨ NEW
    └── AI_COURSE_IMPLEMENTATION_SUMMARY.md ✨ NEW (이 파일)
```

---

## 구현 완료!

모든 기능이 정상적으로 구현되었습니다. 테스트를 진행해보시고, 문제가 있으면 말씀해주세요!
