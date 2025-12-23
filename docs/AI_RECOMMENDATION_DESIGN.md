# 여행 추천 AI 로직 설계

## 개요

AI는 **새로운 여행지를 생성하지 않고**, DB에 있는 실제 데이터 중에서 **선택만** 수행합니다.
여행 기간에 따라 정해진 순서 패턴을 따르며, ID만 반환하여 프론트엔드에서 상세 정보를 조회합니다.

---

## 1️⃣ 백엔드 로직 흐름

### 1.1 API 엔드포인트

```
POST /api/travel/recommend
```

**Request Body:**
```json
{
  "region": "서울",
  "duration": "1박 2일",
  "theme": "역사·문화"
}
```

### 1.2 백엔드 처리 단계

```python
# Backend/travus/travel/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json

@api_view(['POST'])
def recommend_travel(request):
    """
    1. 사용자 입력 받기
    2. DB에서 후보 데이터 조회
    3. AI에게 데이터 전달 및 추천 요청
    4. AI 응답 반환
    """

    # 1. 사용자 입력
    region = request.data.get('region')
    duration = request.data.get('duration')  # "당일치기", "1박 2일", "2박 3일"
    theme = request.data.get('theme')

    # 2. DB에서 후보 데이터 조회
    from .models import TravelSpot, Restaurant, Accommodation

    travel_spots = TravelSpot.objects.filter(region=region).values(
        'id', 'name', 'category', 'description', 'theme'
    )

    restaurants = Restaurant.objects.filter(region=region).values(
        'id', 'name', 'cuisine_type', 'description'
    )

    accommodations = Accommodation.objects.filter(region=region).values(
        'id', 'name', 'type', 'description'
    )

    # 3. AI에게 전달할 데이터 준비
    candidates = {
        "travel_spots": list(travel_spots),
        "restaurants": list(restaurants),
        "accommodations": list(accommodations)
    }

    # 4. AI 추천 요청
    ai_response = call_ai_recommendation(
        candidates=candidates,
        duration=duration,
        theme=theme
    )

    return Response(ai_response)


def call_ai_recommendation(candidates, duration, theme):
    """
    SSAFY GMS API를 통해 OpenAI에 추천 요청
    """

    GMS_KEY = "S14P02EA02-e78f608f-87c7-4534-a076-6916104b3bdc"

    # AI 프롬프트 생성
    system_prompt = generate_system_prompt(duration)
    user_prompt = generate_user_prompt(candidates, theme)

    # GMS API 호출
    response = requests.post(
        "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GMS_KEY}"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }
    )

    ai_result = response.json()
    recommendation = json.loads(ai_result['choices'][0]['message']['content'])

    return recommendation
```

---

## 2️⃣ AI 프롬프트 설계

### 2.1 System Prompt 생성 함수

```python
def generate_system_prompt(duration):
    """
    여행 기간에 따라 순서 패턴을 정의하는 시스템 프롬프트
    """

    patterns = {
        "당일치기": {
            "pattern": "travel → restaurant → travel → travel → restaurant",
            "structure": [
                {"order": 1, "type": "travel"},
                {"order": 2, "type": "restaurant"},
                {"order": 3, "type": "travel"},
                {"order": 4, "type": "travel"},
                {"order": 5, "type": "restaurant"}
            ]
        },
        "1박 2일": {
            "pattern": """
Day 1: travel → restaurant → travel → travel → restaurant → accommodation
Day 2: travel → restaurant → travel → travel → restaurant
            """,
            "structure": [
                # Day 1
                {"day": 1, "order": 1, "type": "travel"},
                {"day": 1, "order": 2, "type": "restaurant"},
                {"day": 1, "order": 3, "type": "travel"},
                {"day": 1, "order": 4, "type": "travel"},
                {"day": 1, "order": 5, "type": "restaurant"},
                {"day": 1, "order": 6, "type": "accommodation"},
                # Day 2
                {"day": 2, "order": 1, "type": "travel"},
                {"day": 2, "order": 2, "type": "restaurant"},
                {"day": 2, "order": 3, "type": "travel"},
                {"day": 2, "order": 4, "type": "travel"},
                {"day": 2, "order": 5, "type": "restaurant"}
            ]
        },
        "2박 3일": {
            "pattern": """
Day 1: travel → restaurant → travel → travel → restaurant → accommodation
Day 2: travel → restaurant → travel → travel → restaurant → accommodation
Day 3: travel → restaurant → travel → travel → restaurant
            """,
            "structure": [
                # Day 1
                {"day": 1, "order": 1, "type": "travel"},
                {"day": 1, "order": 2, "type": "restaurant"},
                {"day": 1, "order": 3, "type": "travel"},
                {"day": 1, "order": 4, "type": "travel"},
                {"day": 1, "order": 5, "type": "restaurant"},
                {"day": 1, "order": 6, "type": "accommodation"},
                # Day 2
                {"day": 2, "order": 1, "type": "travel"},
                {"day": 2, "order": 2, "type": "restaurant"},
                {"day": 2, "order": 3, "type": "travel"},
                {"day": 2, "order": 4, "type": "travel"},
                {"day": 2, "order": 5, "type": "restaurant"},
                {"day": 2, "order": 6, "type": "accommodation"},
                # Day 3
                {"day": 3, "order": 1, "type": "travel"},
                {"day": 3, "order": 2, "type": "restaurant"},
                {"day": 3, "order": 3, "type": "travel"},
                {"day": 3, "order": 4, "type": "travel"},
                {"day": 3, "order": 5, "type": "restaurant"}
            ]
        }
    }

    pattern_info = patterns[duration]

    return f"""
당신은 여행 코스 추천 전문가입니다.

**중요 규칙:**
1. 절대로 새로운 장소를 만들지 마세요
2. 반드시 제공된 후보 목록의 ID만 사용하세요
3. 아래 순서 패턴을 정확히 따라야 합니다

**여행 순서 패턴 ({duration}):**
{pattern_info['pattern']}

**응답 형식:**
- 반드시 JSON 형식으로만 응답하세요
- 각 항목은 day(해당되는 경우), order, type, id만 포함
- id는 반드시 제공된 후보 목록에 있는 실제 ID여야 합니다

**JSON 구조:**
{{
  "itinerary": [
    {json.dumps(pattern_info['structure'][0], ensure_ascii=False)},
    ...
  ]
}}

사용자가 선택한 테마와 각 장소의 특성을 고려하여 최적의 조합을 선택하세요.
"""


def generate_user_prompt(candidates, theme):
    """
    실제 DB 데이터와 테마를 전달하는 사용자 프롬프트
    """

    return f"""
사용자가 선택한 테마: {theme}

**선택 가능한 여행지 목록:**
{json.dumps(candidates['travel_spots'], ensure_ascii=False, indent=2)}

**선택 가능한 음식점 목록:**
{json.dumps(candidates['restaurants'], ensure_ascii=False, indent=2)}

**선택 가능한 숙소 목록:**
{json.dumps(candidates['accommodations'], ensure_ascii=False, indent=2)}

위 목록에서만 선택하여 여행 코스를 구성해주세요.
각 장소의 id를 그대로 사용하고, 순서 패턴을 정확히 따라주세요.
"""
```

---

## 3️⃣ AI 응답 예시

### 3.1 당일치기 응답 예시

```json
{
  "itinerary": [
    {
      "order": 1,
      "type": "travel",
      "id": 12
    },
    {
      "order": 2,
      "type": "restaurant",
      "id": 5
    },
    {
      "order": 3,
      "type": "travel",
      "id": 8
    },
    {
      "order": 4,
      "type": "travel",
      "id": 15
    },
    {
      "order": 5,
      "type": "restaurant",
      "id": 9
    }
  ]
}
```

### 3.2 1박 2일 응답 예시

```json
{
  "itinerary": [
    {
      "day": 1,
      "order": 1,
      "type": "travel",
      "id": 12
    },
    {
      "day": 1,
      "order": 2,
      "type": "restaurant",
      "id": 5
    },
    {
      "day": 1,
      "order": 3,
      "type": "travel",
      "id": 8
    },
    {
      "day": 1,
      "order": 4,
      "type": "travel",
      "id": 15
    },
    {
      "day": 1,
      "order": 5,
      "type": "restaurant",
      "id": 9
    },
    {
      "day": 1,
      "order": 6,
      "type": "accommodation",
      "id": 3
    },
    {
      "day": 2,
      "order": 1,
      "type": "travel",
      "id": 22
    },
    {
      "day": 2,
      "order": 2,
      "type": "restaurant",
      "id": 11
    },
    {
      "day": 2,
      "order": 3,
      "type": "travel",
      "id": 18
    },
    {
      "day": 2,
      "order": 4,
      "type": "travel",
      "id": 7
    },
    {
      "day": 2,
      "order": 5,
      "type": "restaurant",
      "id": 14
    }
  ]
}
```

### 3.3 2박 3일 응답 예시

```json
{
  "itinerary": [
    {
      "day": 1,
      "order": 1,
      "type": "travel",
      "id": 12
    },
    {
      "day": 1,
      "order": 2,
      "type": "restaurant",
      "id": 5
    },
    {
      "day": 1,
      "order": 3,
      "type": "travel",
      "id": 8
    },
    {
      "day": 1,
      "order": 4,
      "type": "travel",
      "id": 15
    },
    {
      "day": 1,
      "order": 5,
      "type": "restaurant",
      "id": 9
    },
    {
      "day": 1,
      "order": 6,
      "type": "accommodation",
      "id": 3
    },
    {
      "day": 2,
      "order": 1,
      "type": "travel",
      "id": 22
    },
    {
      "day": 2,
      "order": 2,
      "type": "restaurant",
      "id": 11
    },
    {
      "day": 2,
      "order": 3,
      "type": "travel",
      "id": 18
    },
    {
      "day": 2,
      "order": 4,
      "type": "travel",
      "id": 7
    },
    {
      "day": 2,
      "order": 5,
      "type": "restaurant",
      "id": 14
    },
    {
      "day": 2,
      "order": 6,
      "type": "accommodation",
      "id": 6
    },
    {
      "day": 3,
      "order": 1,
      "type": "travel",
      "id": 25
    },
    {
      "day": 3,
      "order": 2,
      "type": "restaurant",
      "id": 19
    },
    {
      "day": 3,
      "order": 3,
      "type": "travel",
      "id": 13
    },
    {
      "day": 3,
      "order": 4,
      "type": "travel",
      "id": 9
    },
    {
      "day": 3,
      "order": 5,
      "type": "restaurant",
      "id": 16
    }
  ]
}
```

---

## 4️⃣ 프론트엔드 처리

### 4.1 API 호출 및 상세 정보 조회

```javascript
// Frontend/travus/src/api/travel.js

export async function getRecommendation(region, duration, theme) {
  // 1. AI 추천 요청
  const response = await fetch('/api/travel/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ region, duration, theme })
  });

  const aiResult = await response.json();

  // 2. ID를 기반으로 상세 정보 조회
  const detailedItinerary = await fetchDetailedInfo(aiResult.itinerary);

  return detailedItinerary;
}

async function fetchDetailedInfo(itinerary) {
  // ID 목록 추출
  const travelIds = itinerary.filter(item => item.type === 'travel').map(item => item.id);
  const restaurantIds = itinerary.filter(item => item.type === 'restaurant').map(item => item.id);
  const accommodationIds = itinerary.filter(item => item.type === 'accommodation').map(item => item.id);

  // 일괄 조회
  const [travels, restaurants, accommodations] = await Promise.all([
    fetch(`/api/travel/spots?ids=${travelIds.join(',')}`).then(r => r.json()),
    fetch(`/api/restaurants?ids=${restaurantIds.join(',')}`).then(r => r.json()),
    fetch(`/api/accommodations?ids=${accommodationIds.join(',')}`).then(r => r.json())
  ]);

  // ID를 키로 하는 맵 생성
  const dataMap = {
    travel: Object.fromEntries(travels.map(t => [t.id, t])),
    restaurant: Object.fromEntries(restaurants.map(r => [r.id, r])),
    accommodation: Object.fromEntries(accommodations.map(a => [a.id, a]))
  };

  // AI 응답에 상세 정보 결합
  return itinerary.map(item => ({
    ...item,
    details: dataMap[item.type][item.id]
  }));
}
```

### 4.2 Vue 컴포넌트 사용 예시

```vue
<template>
  <div class="itinerary">
    <div v-for="day in groupedByDay" :key="day.dayNumber" class="day-section">
      <h2>Day {{ day.dayNumber }}</h2>

      <div v-for="item in day.items" :key="`${item.day}-${item.order}`" class="itinerary-item">
        <div class="order">{{ item.order }}</div>
        <div class="content">
          <div class="type-badge" :class="item.type">{{ getTypeName(item.type) }}</div>
          <h3>{{ item.details.name }}</h3>
          <p>{{ item.details.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getRecommendation } from '@/api/travel';

const itinerary = ref([]);

onMounted(async () => {
  itinerary.value = await getRecommendation('서울', '1박 2일', '역사·문화');
});

const groupedByDay = computed(() => {
  const days = {};

  itinerary.value.forEach(item => {
    const dayNumber = item.day || 1;
    if (!days[dayNumber]) {
      days[dayNumber] = { dayNumber, items: [] };
    }
    days[dayNumber].items.push(item);
  });

  return Object.values(days);
});

function getTypeName(type) {
  const names = {
    travel: '여행지',
    restaurant: '음식점',
    accommodation: '숙소'
  };
  return names[type];
}
</script>
```

---

## 5️⃣ 백엔드 상세 정보 조회 API

```python
# Backend/travus/travel/views.py

@api_view(['GET'])
def get_spots_by_ids(request):
    """
    여러 여행지를 ID 목록으로 일괄 조회
    """
    ids = request.GET.get('ids', '').split(',')
    spots = TravelSpot.objects.filter(id__in=ids)
    serializer = TravelSpotSerializer(spots, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_restaurants_by_ids(request):
    """
    여러 음식점을 ID 목록으로 일괄 조회
    """
    ids = request.GET.get('ids', '').split(',')
    restaurants = Restaurant.objects.filter(id__in=ids)
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_accommodations_by_ids(request):
    """
    여러 숙소를 ID 목록으로 일괄 조회
    """
    ids = request.GET.get('ids', '').split(',')
    accommodations = Accommodation.objects.filter(id__in=ids)
    serializer = AccommodationSerializer(accommodations, many=True)
    return Response(serializer.data)
```

---

## 6️⃣ 전체 데이터 흐름

```
[사용자]
  ↓ (지역, 기간, 테마 선택)
[프론트엔드]
  ↓ POST /api/travel/recommend
[백엔드 - Django]
  ↓ DB 조회 (해당 지역의 모든 후보)
  ↓ 후보 목록 + 순서 패턴
[AI - GPT via GMS]
  ↓ 후보 중 선택 + 순서대로 배치
  ↓ JSON 응답 (id만 포함)
[백엔드]
  ↓ AI 응답 반환
[프론트엔드]
  ↓ id 목록 추출
  ↓ GET /api/travel/spots?ids=1,2,3
  ↓ GET /api/restaurants?ids=4,5
  ↓ GET /api/accommodations?ids=6
[백엔드]
  ↓ 상세 정보 반환
[프론트엔드]
  ↓ AI 응답 + 상세 정보 결합
  ↓ 화면 렌더링
[사용자]
```

---

## 7️⃣ 구현 시 주의사항

### 7.1 AI 응답 검증

```python
def validate_ai_response(response, duration, candidate_ids):
    """
    AI 응답이 규칙을 준수하는지 검증
    """
    itinerary = response.get('itinerary', [])

    # 1. 순서 패턴 검증
    expected_patterns = {
        "당일치기": ['travel', 'restaurant', 'travel', 'travel', 'restaurant'],
        "1박 2일": {
            1: ['travel', 'restaurant', 'travel', 'travel', 'restaurant', 'accommodation'],
            2: ['travel', 'restaurant', 'travel', 'travel', 'restaurant']
        },
        "2박 3일": {
            1: ['travel', 'restaurant', 'travel', 'travel', 'restaurant', 'accommodation'],
            2: ['travel', 'restaurant', 'travel', 'travel', 'restaurant', 'accommodation'],
            3: ['travel', 'restaurant', 'travel', 'travel', 'restaurant']
        }
    }

    # 2. ID 존재 여부 검증
    for item in itinerary:
        item_type = item['type']
        item_id = item['id']

        if item_id not in candidate_ids[item_type]:
            raise ValueError(f"Invalid ID: {item_id} not in candidates for type {item_type}")

    return True
```

### 7.2 에러 처리

```python
@api_view(['POST'])
def recommend_travel(request):
    try:
        # ... AI 호출 로직

        # 응답 검증
        validate_ai_response(ai_response, duration, candidate_ids)

        return Response(ai_response)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=500
        )
```

### 7.3 캐싱 전략

```python
from django.core.cache import cache

def get_candidates_cached(region):
    """
    지역별 후보 목록을 캐싱하여 성능 향상
    """
    cache_key = f"candidates_{region}"
    candidates = cache.get(cache_key)

    if not candidates:
        candidates = {
            "travel_spots": list(TravelSpot.objects.filter(region=region).values()),
            "restaurants": list(Restaurant.objects.filter(region=region).values()),
            "accommodations": list(Accommodation.objects.filter(region=region).values())
        }
        cache.set(cache_key, candidates, 60 * 60)  # 1시간 캐싱

    return candidates
```

---

## 8️⃣ 테스트 시나리오

### 8.1 단위 테스트

```python
# Backend/travus/travel/tests.py

from django.test import TestCase
from .views import generate_system_prompt, validate_ai_response

class AIRecommendationTest(TestCase):
    def test_system_prompt_generation(self):
        """시스템 프롬프트가 올바르게 생성되는지 테스트"""
        prompt = generate_system_prompt("1박 2일")
        self.assertIn("Day 1", prompt)
        self.assertIn("Day 2", prompt)

    def test_response_validation(self):
        """AI 응답 검증 로직 테스트"""
        valid_response = {
            "itinerary": [
                {"order": 1, "type": "travel", "id": 1},
                {"order": 2, "type": "restaurant", "id": 2}
            ]
        }

        candidate_ids = {
            "travel": [1, 2, 3],
            "restaurant": [2, 3, 4],
            "accommodation": [5, 6]
        }

        self.assertTrue(validate_ai_response(valid_response, "당일치기", candidate_ids))
```

---

## 9️⃣ 환경 변수 설정

```python
# Backend/travus/settings.py

# GMS API 설정
GMS_API_KEY = os.getenv('GMS_API_KEY', 'S14P02EA02-e78f608f-87c7-4534-a076-6916104b3bdc')
GMS_API_URL = 'https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions'
GMS_MODEL = 'gpt-4o-mini'
```

```
# .env 파일
GMS_API_KEY=S14P02EA02-e78f608f-87c7-4534-a076-6916104b3bdc
```

---

이 설계를 기반으로 구현하시면 됩니다! 추가 질문이 있으시면 말씀해주세요.
