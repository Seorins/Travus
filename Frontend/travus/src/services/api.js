import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 응답 인터셉터 (에러 처리)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  // 공공데이터 API에서 여행지 가져오기
  getTravelSpotsFromAPI(params = {}) {
    return apiClient.get('/travel-spots/from_api/', { params })
  },

  // 공공데이터 API 키워드 검색
  searchTravelSpotsAPI(keyword, params = {}) {
    return apiClient.get('/travel-spots/search_api/', {
      params: { keyword, ...params }
    })
  },

  // DB에서 여행지 목록 가져오기
  getTravelSpots(params = {}) {
    return apiClient.get('/travel-spots/', { params })
  },

  // 여행지 상세 정보
  getTravelSpotDetail(id) {
    return apiClient.get(`/travel-spots/${id}/`)
  },

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

  // 리뷰 목록
  getReviews(travelSpotId) {
    return apiClient.get('/reviews/', {
      params: { travel_spot: travelSpotId }
    })
  },

  // 리뷰 작성
  createReview(data) {
    return apiClient.post('/reviews/', data)
  }
}
