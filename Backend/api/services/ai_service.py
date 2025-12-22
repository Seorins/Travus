"""
AI 여행 코스 생성 서비스
OpenAI GPT를 사용하여 맞춤형 여행 코스를 생성합니다.
"""
import os
import json
from openai import OpenAI
from django.conf import settings


class AITravelCourseService:
    def __init__(self):
        # OpenAI API 키 설정
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # 또는 "gpt-4" 사용 가능

    def generate_travel_course(self, region_code, region_name, days, themes, available_spots):
        """
        AI를 사용하여 여행 코스를 생성합니다.

        Args:
            region_code (str): 지역 코드 (예: '27' for 대구)
            region_name (str): 지역 이름 (예: '대구')
            days (int): 여행 기간 (일 수)
            themes (list): 선택한 테마 목록 (예: ['자연', '문화'])
            available_spots (list): 데이터베이스에서 가져온 여행지 목록

        Returns:
            dict: {
                'title': str,  # 코스 제목
                'concept': str,  # 코스 컨셉 설명
                'days': [
                    {
                        'day': 1,
                        'places': [
                            {
                                'id': int,
                                'name': str,
                                'category': str,
                                'reason': str  # 선택 이유
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        """

        # 여행지 정보를 AI가 이해할 수 있는 형식으로 변환
        spots_info = self._format_spots_for_ai(available_spots)

        # 프롬프트 생성
        prompt = self._create_prompt(
            region_name=region_name,
            days=days,
            themes=themes,
            spots_info=spots_info
        )

        try:
            # OpenAI API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 한국 여행 전문가입니다. 사용자의 선호도에 맞는 최적의 여행 코스를 만들어주세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,  # 창의성 조절 (0~1, 높을수록 창의적)
                max_tokens=2000,
                response_format={"type": "json_object"}  # JSON 응답 강제
            )

            # 응답 파싱
            ai_response = response.choices[0].message.content
            result = json.loads(ai_response)

            return result

        except Exception as e:
            print(f"❌ AI 코스 생성 실패: {str(e)}")
            # 에러 발생 시 기본 코스 반환
            return self._create_fallback_course(region_name, days, available_spots)

    def _format_spots_for_ai(self, spots):
        """여행지 목록을 AI가 이해하기 쉬운 형식으로 변환"""
        formatted_spots = []

        for spot in spots:
            formatted_spots.append({
                'id': spot.get('id'),
                'name': spot.get('name'),
                'category': spot.get('category', '여행지'),
                'content_type_id': spot.get('content_type_id'),
                'address': spot.get('address', spot.get('addr1', '')),
                'description': spot.get('description', spot.get('overview', ''))[:200],  # 200자로 제한
            })

        return formatted_spots

    def _create_prompt(self, region_name, days, themes, spots_info):
        """AI 프롬프트 생성"""

        theme_str = ', '.join(themes) if themes else '일반 여행'

        prompt = f"""
{region_name} 지역에서 {days}일간의 여행 코스를 만들어주세요.
여행 테마: {theme_str}

다음 여행지 목록에서 선택하여 일정을 짜주세요:

{json.dumps(spots_info, ensure_ascii=False, indent=2)}

요구사항:
1. 하루에 방문할 장소는 3~5곳으로 제한
2. 여행지(관광지), 음식점, 숙소를 균형있게 배치
3. 동선을 고려하여 효율적으로 배치
4. 각 장소 선택 이유를 간단히 설명
5. 코스 전체의 컨셉과 매력적인 제목을 만들어주세요

응답 형식 (반드시 JSON으로):
{{
    "title": "코스 제목 (창의적이고 매력적으로)",
    "concept": "코스 컨셉 설명 (2-3문장)",
    "days": [
        {{
            "day": 1,
            "places": [
                {{
                    "id": 여행지ID,
                    "name": "여행지명",
                    "category": "카테고리",
                    "reason": "선택 이유"
                }}
            ]
        }}
    ]
}}
"""
        return prompt

    def _create_fallback_course(self, region_name, days, spots):
        """AI 실패 시 기본 코스 생성"""

        # 카테고리별로 분류
        attractions = [s for s in spots if s.get('content_type_id') == '12'][:days * 2]
        restaurants = [s for s in spots if s.get('content_type_id') == '39'][:days * 2]
        accommodations = [s for s in spots if s.get('content_type_id') == '32'][:max(1, days - 1)]

        result = {
            "title": f"{region_name} {days}일 여행 코스",
            "concept": f"{region_name}의 주요 명소를 돌아보는 {days}일 여행 코스입니다.",
            "days": []
        }

        for day in range(days):
            day_places = []

            # 여행지 2개
            if day * 2 < len(attractions):
                for i in range(2):
                    if day * 2 + i < len(attractions):
                        spot = attractions[day * 2 + i]
                        day_places.append({
                            "id": spot['id'],
                            "name": spot['name'],
                            "category": "여행지",
                            "reason": f"{region_name}의 대표 관광지"
                        })

            # 음식점 1개
            if day < len(restaurants):
                spot = restaurants[day]
                day_places.append({
                    "id": spot['id'],
                    "name": spot['name'],
                    "category": "음식점",
                    "reason": "현지 맛집"
                })

            # 마지막 날 제외하고 숙소 추가
            if day < days - 1 and day < len(accommodations):
                spot = accommodations[day]
                day_places.append({
                    "id": spot['id'],
                    "name": spot['name'],
                    "category": "숙소",
                    "reason": "편안한 휴식"
                })

            result["days"].append({
                "day": day + 1,
                "places": day_places
            })

        return result


# 싱글톤 인스턴스
ai_travel_service = AITravelCourseService()
