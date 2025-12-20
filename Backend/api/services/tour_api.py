import requests
import logging
from django.conf import settings
from typing import Dict, List, Optional
from urllib.parse import quote

# 로깅 설정 (print 대신 사용 권장)
logger = logging.getLogger(__name__)


class TourAPIService:
    """한국관광공사 무장애 여행 API 서비스 (TourAPI 4.0 기준)"""

    def __init__(self):
        self.base_url = settings.TOUR_API_BASE_URL
        self.api_key = settings.TOUR_API_KEY
        self.mobile_os = settings.TOUR_API_MOBILE_OS
        self.mobile_app = settings.TOUR_API_MOBILE_APP

    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        API 요청 공통 메서드

        공공데이터 포털 API의 특성상 serviceKey를 URL에 직접 포함시키고,
        나머지 파라미터는 requests의 params로 전달하여 이중 인코딩 방지
        """
        # ServiceKey 처리: 이미 인코딩되어 있는지 확인 후 처리
        if '%' in self.api_key:
            # 이미 인코딩된 키라면 그대로 사용
            service_key = self.api_key
        else:
            # 디코딩된 키라면 인코딩 수행
            service_key = quote(self.api_key, safe='')

        # URL에 serviceKey 직접 포함 (이중 인코딩 방지)
        url = f"{self.base_url}/{endpoint}?serviceKey={service_key}"

        # 기본 파라미터 설정
        default_params = {
            'MobileOS': self.mobile_os,
            'MobileApp': self.mobile_app,
            '_type': 'json',
            'numOfRows': 20,
            'pageNo': 1
        }

        # 파라미터 병합 (사용자 파라미터가 우선)
        request_params = {**default_params, **params}

        try:
            logger.info(f"=== Making TourAPI request ===")
            logger.info(f"Endpoint: {endpoint}")
            logger.info(f"Parameters: {request_params}")

            response = requests.get(url, params=request_params, timeout=10)

            # 최종 요청 URL 로깅
            logger.info(f"Final URL: {response.url}")

            response.raise_for_status()
            json_response = response.json()

            # 응답 구조 간단히 로깅
            if 'response' in json_response:
                body = json_response.get('response', {}).get('body', {})
                total_count = body.get('totalCount', 'N/A')
                logger.info(f"Response totalCount: {total_count}")

            return json_response

        except requests.exceptions.RequestException as e:
            logger.error(f"TourAPI Request Failed: {e}")
            logger.error(f"Failed URL: {url}")
            return None
        except ValueError as e:  # JSON Decode Error
            logger.error(f"TourAPI JSON Decode Failed: {e}")
            return None

    def _normalize_response(self, response: Optional[Dict]) -> List[Dict]:
        """
        응답 데이터를 항상 List 형태로 반환하도록 정규화하는 헬퍼 메서드.
        TourAPI는 결과가 1개면 Dict, 2개 이상이면 List로 반환하는데,
        이를 항상 List로 통일하여 프론트엔드의 Array.isArray 체크를 줄임.
        """
        if not response:
            return []

        try:
            body = response.get('response', {}).get('body', {})
            items = body.get('items', {})

            # 데이터가 아예 없는 경우 (items가 빈 문자열로 올 때가 있음)
            if not items:
                return []

            item_list = items.get('item', [])

            # 결과가 1개일 경우 dict로 오고, 여러개일 경우 list로 옴 -> 무조건 list로 변환
            if isinstance(item_list, dict):
                return [item_list]
            return item_list if isinstance(item_list, list) else []

        except (AttributeError, TypeError):
            return []

    def get_area_based_list(
        self,
        area_code: Optional[str] = None,
        sigungu_code: Optional[str] = None,
        content_type_id: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 20
    ) -> Optional[Dict]:
        """
        지역 기반 관광정보 조회

        원본 응답이 필요한 경우(totalCount 등)가 있으므로 정규화 선택적 적용
        """
        params = {
            'pageNo': page_no,
            'numOfRows': num_of_rows,
            'arrange': 'A',  # A=제목순, C=수정일순, D=생성일순
        }

        if area_code:
            params['areaCode'] = area_code
        if sigungu_code:
            params['sigunguCode'] = sigungu_code
        if content_type_id:
            params['contentTypeId'] = content_type_id

        return self._make_request('areaBasedList2', params)

    def get_detail_common(self, content_id: str) -> Optional[Dict]:
        """
        공통정보 상세 조회

        기본 정보와 contenttypeid를 가져오는 핵심 메서드
        """
        logger.info(f"=== get_detail_common called with content_id: {content_id} ===")
        params = {
            'contentId': content_id,
            'defaultYN': 'Y',
            'firstImageYN': 'Y',
            'areacodeYN': 'Y',
            'addrinfoYN': 'Y',
            'mapinfoYN': 'Y',
            'overviewYN': 'Y',
        }

        result = self._make_request('detailCommon2', params)

        if result and 'response' in result:
            items = result.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            if isinstance(items, dict):
                logger.info(f"API returned title: {items.get('title', 'NO TITLE')}, contentid: {items.get('contentid', 'NO ID')}")
            elif isinstance(items, list) and len(items) > 0:
                logger.info(f"API returned title: {items[0].get('title', 'NO TITLE')}, contentid: {items[0].get('contentid', 'NO ID')}")

        return result

    def get_detail_intro(self, content_id: str, content_type_id: str) -> Optional[Dict]:
        """
        소개 정보 조회 (detailIntro2)

        주의: content_type_id는 필수 파라미터입니다.
        기본값을 제거하여 호출하는 쪽에서 반드시 올바른 타입을 전달하도록 강제합니다.
        - 12: 관광지
        - 32: 숙박
        - 39: 음식점
        - 15: 행사/공연/축제
        """
        params = {
            'contentId': content_id,
            'contentTypeId': content_type_id,
        }

        return self._make_request('detailIntro2', params)

    def get_detail_info(self, content_id: str, content_type_id: str) -> Optional[Dict]:
        """
        반복 정보 조회 (detailInfo2)

        주의: content_type_id는 필수 파라미터입니다.
        각 타입별로 다른 구조의 데이터를 반환하므로 정확한 타입 전달이 중요합니다.
        """
        params = {
            'contentId': content_id,
            'contentTypeId': content_type_id,
        }

        return self._make_request('detailInfo2', params)

    def get_detail_image(self, content_id: str) -> Optional[Dict]:
        """이미지 정보 조회 (detailImage2)"""
        params = {
            'contentId': content_id,
            'imageYN': 'Y',
            'subImageYN': 'Y',  # 서브 이미지 포함
            'numOfRows': 100,
        }

        return self._make_request('detailImage2', params)

    def get_detail_with_tour(self, content_id: str) -> Optional[Dict]:
        """
        무장애 관광정보 상세 조회

        주의: TourAPI 4.0 기준 무장애 정보는 'detailWithTour1'입니다.
        API 문서를 확인하여 엔드포인트가 맞는지 검증이 필요합니다.
        """
        params = {
            'contentId': content_id,
        }

        # detailWithTour1로 변경 (TourAPI 4.0 표준)
        return self._make_request('detailWithTour1', params)

    def search_keyword(
        self,
        keyword: str,
        area_code: Optional[str] = None,
        content_type_id: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 20
    ) -> Optional[Dict]:
        """키워드 검색"""
        params = {
            'keyword': keyword,
            'pageNo': page_no,
            'numOfRows': num_of_rows,
            'arrange': 'A',
        }

        if area_code:
            params['areaCode'] = area_code
        if content_type_id:
            params['contentTypeId'] = content_type_id

        return self._make_request('searchKeyword2', params)

    def get_area_code(self, area_code: Optional[str] = None) -> Optional[Dict]:
        """지역코드 조회"""
        params = {
            'numOfRows': 100,
        }

        if area_code:
            params['areaCode'] = area_code

        return self._make_request('areaCode2', params)


# 싱글톤 인스턴스
tour_api_service = TourAPIService()
