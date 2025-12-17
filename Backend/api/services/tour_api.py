import requests
from django.conf import settings
from typing import Dict, List, Optional
from urllib.parse import quote


class TourAPIService:
    """한국관광공사 무장애 여행 API 서비스"""

    def __init__(self):
        self.base_url = settings.TOUR_API_BASE_URL
        self.api_key = settings.TOUR_API_KEY
        self.mobile_os = settings.TOUR_API_MOBILE_OS
        self.mobile_app = settings.TOUR_API_MOBILE_APP

    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """API 요청 공통 메서드"""
        # API 키가 이미 인코딩되어 있으면 그대로, 아니면 인코딩
        # %가 포함되어 있으면 이미 인코딩된 것으로 판단
        if '%' in self.api_key:
            # 이미 인코딩된 키 - 그대로 사용
            url = f"{self.base_url}/{endpoint}?serviceKey={self.api_key}"
        else:
            # 인코딩 안된 키 - 인코딩 필요
            encoded_key = quote(self.api_key, safe='')
            url = f"{self.base_url}/{endpoint}?serviceKey={encoded_key}"

        # 기본 파라미터 추가 (serviceKey 제외)
        default_params = {
            'MobileOS': self.mobile_os,
            'MobileApp': self.mobile_app,
            '_type': 'json',
            'numOfRows': 20,
            'pageNo': 1
        }

        # 사용자 파라미터 병합
        request_params = {**default_params, **params}

        try:
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 실패: {e}")
            print(f"요청 URL: {response.url if 'response' in locals() else url}")
            return None

    def get_area_based_list(
        self,
        area_code: Optional[str] = None,
        sigungu_code: Optional[str] = None,
        content_type_id: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 20
    ) -> Optional[Dict]:
        """지역 기반 관광정보 조회"""
        params = {
            'pageNo': page_no,
            'numOfRows': num_of_rows,
        }

        if area_code:
            params['areaCode'] = area_code
        if sigungu_code:
            params['sigunguCode'] = sigungu_code
        if content_type_id:
            params['contentTypeId'] = content_type_id

        return self._make_request('areaBasedList2', params)

    def get_detail_common(self, content_id: str) -> Optional[Dict]:
        """공통정보 상세 조회"""
        params = {
            'contentId': content_id,
            'defaultYN': 'Y',
            'firstImageYN': 'Y',
            'areacodeYN': 'Y',
            'addrinfoYN': 'Y',
            'mapinfoYN': 'Y',
            'overviewYN': 'Y',
        }

        return self._make_request('detailCommon2', params)

    def get_detail_with_tour(self, content_id: str) -> Optional[Dict]:
        """무장애 관광정보 상세 조회"""
        params = {
            'contentId': content_id,
        }

        return self._make_request('detailWithTour2', params)

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
