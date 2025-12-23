import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 요청 인터셉터 (JWT 토큰 자동 추가)
apiClient.interceptors.request.use(
  (config) => {
    // localStorage에서 토큰 가져오기
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 응답 인터셉터 (에러 처리)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  // ==========================================
  // 메인 API (DB 기반) - 우선 사용
  // ==========================================

  // DB에서 여행지 목록 가져오기
  getTravelSpots(params = {}) {
    return apiClient.get('/travel-spots/', { params })
  },

  // 여행지 상세 정보 (DB PK 기준)
  getTravelSpotDetail(id) {
    return apiClient.get(`/travel-spots/${id}/`)
  },

  // content_id로 여행지 조회 (공공데이터 API ID 기준)
  getTravelSpotByContentId(contentId) {
    return apiClient.get('/travel-spots/by_content_id/', {
      params: { content_id: contentId }
    })
  },

  // ==========================================
  // 레거시 API (실시간 공공데이터 - 필요시만 사용)
  // ==========================================

  // 공공데이터 API에서 여행지 가져오기 (목록 또는 상세)
  getTravelSpotsFromAPI(params = {}) {
    return apiClient.get('/travel-spots/from_api/', { params })
  },

  // 공공데이터 API 키워드 검색
  searchTravelSpotsAPI(keyword, params = {}) {
    return apiClient.get('/travel-spots/search_api/', {
      params: { keyword, ...params }
    })
  },

  // 공공데이터 API 특정 여행지 기본 정보 (detailCommon1)
  getTravelSpotDetailCommon(contentId, contentTypeId = null) {
    const params = { content_id: contentId }
    if (contentTypeId) {
      params.content_type_id = contentTypeId
    }
    return apiClient.get('/travel-spots/detail_common/', { params })
  },

  // 공공데이터 API 소개 정보 (detailIntro2)
  getTravelSpotDetailIntro(contentId, contentTypeId = 12) {
    return apiClient.get('/travel-spots/detail_intro/', {
      params: {
        content_id: contentId,
        content_type_id: contentTypeId
      }
    })
  },

  // 공공데이터 API 반복 정보 (detailInfo2)
  getTravelSpotDetailInfo(contentId, contentTypeId = 12) {
    return apiClient.get('/travel-spots/detail_info/', {
      params: {
        content_id: contentId,
        content_type_id: contentTypeId
      }
    })
  },

  // 공공데이터 API 이미지 정보 (detailImage2)
  getTravelSpotDetailImages(contentId) {
    return apiClient.get('/travel-spots/detail_image/', {
      params: { content_id: contentId }
    })
  },

  // 공공데이터 API 무장애 여행정보 (detailWithTour1)
  getTravelSpotDetailWithTour(contentId) {
    return apiClient.get('/travel-spots/detail_with_tour/', {
      params: { content_id: contentId }
    })
  },

  // 공공데이터 API 지역코드 조회 (areaCode2)
  getAreaCodes(areaCode = null) {
    const params = {}
    if (areaCode) params.area_code = areaCode
    return apiClient.get('/travel-spots/area_code/', { params })
  },

  // 공공데이터 API 서비스분류코드 조회 (categoryCode2)
  getCategoryCodes(params = {}) {
    return apiClient.get('/travel-spots/category_code/', { params })
  },

  // 공공데이터 API 위치기반 관광정보 조회 (locationBasedList2)
  getTravelSpotsByLocation(mapx, mapy, params = {}) {
    return apiClient.get('/travel-spots/location_based/', {
      params: { mapx, mapy, ...params }
    })
  },

  // ==========================================
  // 기타 엔드포인트
  // ==========================================

  // 카테고리 목록
  getCategories() {
    return apiClient.get('/categories/')
  },

  // 북마크 목록
  getBookmarks() {
    return apiClient.get('/bookmarks/')
  },

  // 북마크 추가
  createBookmark(data) {
    return apiClient.post('/bookmarks/', data)
  },

  // 북마크 삭제
  deleteBookmark(id) {
    return apiClient.delete(`/bookmarks/${id}/`)
  },

  // 코스 목록
  getCourses(params = {}) {
    return apiClient.get('/courses/', { params })
  },

  // 코스 상세
  getCourseDetail(id) {
    return apiClient.get(`/courses/${id}/`)
  },

  // AI 코스 생성
  generateAICourse(data) {
    return apiClient.post('/courses/generate_ai_course/', data, {
      timeout: 60000 // AI 응답을 위해 타임아웃 60초로 증가
    })
  },

  // 코스 저장
  saveCourse(data) {
    return apiClient.post('/courses/', data)
  },

  // 코스 좋아요 토글
  toggleCourseLike(courseId) {
    return apiClient.post(`/courses/${courseId}/toggle_like/`)
  },

  // 코스 좋아요 상태 조회
  getCourseLikeStatus(courseId) {
    return apiClient.get(`/courses/${courseId}/like_status/`)
  },

  // 리뷰 목록
  getReviews(travelSpotId) {
    return apiClient.get('/reviews/', {
      params: { travel_spot: travelSpotId }
    })
  },

  // 리뷰 작성
  createReview(data) {
    return apiClient.post('/reviews/', data)
  },

  // 코스 댓글 관련
  getCourseComments(courseId) {
    return apiClient.get(`/courses/${courseId}/comments/`)
  },

  createCourseComment(courseId, data) {
    return apiClient.post(`/courses/${courseId}/comments/`, data)
  },

  deleteCourseComment(commentId) {
    return apiClient.delete(`/comments/${commentId}/`)
  },

  // 현재 사용자 정보
  getCurrentUser() {
    return apiClient.get('/auth/me/')
  }
}
