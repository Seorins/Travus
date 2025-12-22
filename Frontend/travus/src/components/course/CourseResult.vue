<template>
  <div class="course-result">
    <!-- 레퍼런스 그대로: 좌우 분할 레이아웃 (좌측 25~30%, 우측 70~75%) -->
    <div class="result-layout">

      <!-- 좌측 사이드바 - 레퍼런스 그대로 구현 -->
      <aside class="sidebar">
        <!-- 헤더 -->
        <div class="sidebar-header">
          <button class="btn-back" @click="emit('restart')">
            <i class="fa fa-arrow-left"></i>
          </button>
          <h1 class="planner-title">AI코스 플래너</h1>
          <div class="header-actions">
            <button class="btn-icon"><i class="fa fa-bookmark"></i></button>
            <button class="btn-icon"><i class="fa fa-thumbs-up"></i></button>
            <button class="btn-icon"><i class="fa fa-share-alt"></i></button>
          </div>
        </div>

        <!-- 탭 메뉴 - 레퍼런스 그대로 -->
        <div class="tab-menu">
          <button class="tab-item active">여행요약</button>
          <button class="tab-item">세부일정</button>
          <button class="tab-item">연관기사</button>
          <button class="tab-item">여행톡</button>
        </div>

        <!-- 여행 요약 카드 - 레퍼런스 그대로 -->
        <div class="trip-summary-card">
          <div class="summary-badge">
            <span class="badge-day">1박2일</span>
          </div>
          <div class="summary-info">
            <div class="info-item">
              <span class="info-icon">📍</span>
              <span class="info-text">총 이동거리: 14km</span>
            </div>
            <div class="info-item">
              <span class="info-icon">🗺️</span>
              <span class="info-text">여행지역: 대구 - 대구</span>
            </div>
            <div class="info-item">
              <span class="info-icon">🏷️</span>
              <span class="info-text">총 9개 여행지/음식점/카페/숙소 추천</span>
            </div>
          </div>
          <div class="summary-tags">
            <span class="tag">#테마파크</span>
            <span class="tag">#실내여행지</span>
          </div>
        </div>

        <!-- 평점 입력 -->
        <div class="rating-section">
          <span class="rating-label">별점을 남겨주세요.</span>
          <div class="stars">
            <i class="fa fa-star-o"></i>
            <i class="fa fa-star-o"></i>
            <i class="fa fa-star-o"></i>
            <i class="fa fa-star-o"></i>
            <i class="fa fa-star-o"></i>
          </div>
        </div>

        <!-- Day 헤더 -->
        <div class="day-header">
          <h3>Day 1</h3>
          <button class="btn-expand">
            <span>일정편집</span>
            <i class="fa fa-chevron-down"></i>
          </button>
        </div>

        <!-- 장소 리스트 - 레퍼런스 그대로 (세로 스크롤) -->
        <div class="places-list">
          <div
            v-for="(place, index) in currentDayPlaces"
            :key="index"
            class="place-item"
            @click="focusOnMarker(place)"
          >
            <div class="place-number">{{ index + 1 }}</div>
            <div class="place-thumbnail">
              <img
                :src="getPlaceImage(place)"
                :alt="place.name"
                @error="handleImageError"
              />
            </div>
            <div class="place-content">
              <div class="place-category">{{ place.category || '여행지' }}</div>
              <div class="place-name">{{ place.name }}</div>
              <div class="place-address">{{ place.address || '주소 정보 없음' }}</div>
              <button class="btn-detail">더보기 <i class="fa fa-plus"></i></button>
            </div>
          </div>
        </div>
      </aside>

      <!-- 우측 지도 영역 - 레퍼런스 그대로 -->
      <main class="map-area">
        <!-- 카카오맵 -->
        <div id="kakao-map" class="kakao-map"></div>

        <!-- 우측 상단: 날짜 토글 버튼 - 레퍼런스 그대로 위치 -->
        <div class="day-toggle">
          <button
            v-for="(_, index) in itineraryDays"
            :key="index"
            class="day-btn"
            :class="{ active: currentDay === index }"
            @click="switchDay(index)"
          >
            <span class="day-circle" :class="`day${index + 1}`">{{ index + 1 }}</span>
            <span>{{ index + 1 }}일차</span>
          </button>
          <button
            class="day-btn"
            :class="{ active: currentDay === -1 }"
            @click="switchDay(-1)"
          >
            <span class="day-circle all">전체</span>
            <span>{{ itineraryDays.length }}일차</span>
          </button>
        </div>

        <!-- 우측 하단: 다시뽑기 버튼 - 레퍼런스 그대로 위치 -->
        <div class="map-footer">
          <button class="btn-regenerate">
            <i class="fa fa-refresh"></i>
            <span>추천코스가 마음에 들지 않나요?</span>
            <strong>다시뽑기</strong>
            <span class="badge-go">GO</span>
          </button>
        </div>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/services/api'

const props = defineProps({
  courseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['restart'])

// 상태 관리
const itineraryDays = ref([])
const currentDay = ref(0) // 현재 보고 있는 날짜 (0: Day1, 1: Day2, -1: 전체)
const kakaoMap = ref(null)
const markers = ref([])
const polylines = ref([])
const isLoading = ref(true)

// 현재 날짜의 장소들
const currentDayPlaces = computed(() => {
  if (currentDay.value === -1) {
    // 전체 보기
    return itineraryDays.value.flatMap(day => day.places)
  }
  return itineraryDays.value[currentDay.value]?.places || []
})

// 이미지 에러 핸들링
const handleImageError = (e) => {
  e.target.src = 'https://via.placeholder.com/80x80?text=No+Image'
}

// 장소 이미지 가져오기
const getPlaceImage = (place) => {
  if (place.image_url) return place.image_url
  if (place.first_image) return place.first_image
  return 'https://via.placeholder.com/80x80?text=No+Image'
}

// 날짜 전환
const switchDay = (dayIndex) => {
  currentDay.value = dayIndex
  updateMapMarkers()
}

// 카카오맵 SDK 로드
const loadKakaoMapScript = () => {
  return new Promise((resolve, reject) => {
    // 이미 로드되어 있으면 바로 리턴
    if (window.kakao && window.kakao.maps) {
      console.log('✅ 카카오맵 이미 로드됨')
      resolve()
      return
    }

    const apiKey = import.meta.env.VITE_KAKAO_MAP_API_KEY
    console.log('📡 카카오맵 스크립트 로딩 시작, API 키:', apiKey)

    // 기존 스크립트 확인
    const existingScript = document.querySelector('script[src*="dapi.kakao.com"]')
    if (existingScript) {
      console.log('⚠️ 기존 카카오맵 스크립트 제거')
      existingScript.remove()
    }

    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&autoload=false`

    script.onload = () => {
      console.log('✅ 카카오맵 스크립트 다운로드 완료')
      if (window.kakao && window.kakao.maps) {
        window.kakao.maps.load(() => {
          console.log('✅ 카카오맵 API 초기화 완료')
          resolve()
        })
      } else {
        console.error('❌ window.kakao.maps가 없음')
        reject(new Error('Kakao maps API not available'))
      }
    }

    script.onerror = (error) => {
      console.error('❌ 카카오맵 스크립트 로드 실패:', error)
      reject(error)
    }

    document.head.appendChild(script)
    console.log('📄 스크립트 태그 추가됨:', script.src)
  })
}

// 카카오맵 초기화
const initializeKakaoMap = () => {
  const container = document.getElementById('kakao-map')
  if (!container) {
    console.error('❌ 카카오맵 컨테이너를 찾을 수 없습니다')
    return
  }

  console.log('✅ 카카오맵 컨테이너 발견:', container)
  console.log('✅ window.kakao 존재:', !!window.kakao)
  console.log('✅ window.kakao.maps 존재:', !!window.kakao?.maps)

  const options = {
    center: new window.kakao.maps.LatLng(37.5665, 126.9780), // 서울시청
    level: 3 // 확대 레벨 (숫자가 작을수록 확대)
  }

  kakaoMap.value = new window.kakao.maps.Map(container, options)
  console.log('✅ 카카오맵 초기화 완료:', kakaoMap.value)

  // 기본 마커 하나 추가 (테스트용)
  const markerPosition = new window.kakao.maps.LatLng(37.5665, 126.9780)
  const marker = new window.kakao.maps.Marker({
    position: markerPosition
  })
  marker.setMap(kakaoMap.value)
  console.log('✅ 테스트 마커 추가 완료')
}

// 마커 색상 매핑
const getMarkerColor = (dayIndex) => {
  const colors = ['#4A90E2', '#34C759', '#FF9500']
  return colors[dayIndex] || '#4A90E2'
}

// 지도에 마커 및 경로 추가
const updateMapMarkers = () => {
  if (!kakaoMap.value || !itineraryDays.value.length) return

  // 기존 마커 및 폴리라인 제거
  markers.value.forEach(marker => marker.setMap(null))
  polylines.value.forEach(line => line.setMap(null))
  markers.value = []
  polylines.value = []

  const bounds = new window.kakao.maps.LatLngBounds()
  const linePath = []

  // 보여줄 날짜 결정
  const daysToShow = currentDay.value === -1
    ? itineraryDays.value
    : [itineraryDays.value[currentDay.value]]

  let globalIndex = 0

  daysToShow.forEach((day, dayIndex) => {
    const actualDayIndex = currentDay.value === -1 ? dayIndex : currentDay.value

    day.places.forEach((place, placeIndex) => {
      if (!place.latitude || !place.longitude) return

      const position = new window.kakao.maps.LatLng(
        parseFloat(place.latitude),
        parseFloat(place.longitude)
      )

      // 마커 번호 (전체 보기일 때는 연속 번호, 개별 보기일 때는 1부터)
      const markerNumber = currentDay.value === -1 ? globalIndex + 1 : placeIndex + 1
      globalIndex++

      // 커스텀 마커 생성 - 레퍼런스 스타일 그대로
      const markerContent = `
        <div style="
          width: 40px;
          height: 40px;
          background: ${getMarkerColor(actualDayIndex)};
          border: 3px solid white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: 700;
          font-size: 16px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
          cursor: pointer;
        ">
          ${markerNumber}
        </div>
      `

      const customOverlay = new window.kakao.maps.CustomOverlay({
        position: position,
        content: markerContent,
        yAnchor: 0.5
      })

      customOverlay.setMap(kakaoMap.value)
      markers.value.push(customOverlay)
      bounds.extend(position)
      linePath.push(position)

      // 장소 객체에 위치 정보 저장
      place._position = position
    })

    // 경로선 그리기 (각 날짜별로 다른 색상)
    if (linePath.length > 1) {
      const polyline = new window.kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 4,
        strokeColor: getMarkerColor(actualDayIndex),
        strokeOpacity: 0.7,
        strokeStyle: 'solid'
      })

      polyline.setMap(kakaoMap.value)
      polylines.value.push(polyline)
    }
  })

  // 모든 마커가 보이도록 지도 범위 조정
  if (markers.value.length > 0) {
    kakaoMap.value.setBounds(bounds)
  }
}

// 특정 마커에 포커스
const focusOnMarker = (place) => {
  if (!kakaoMap.value || !place._position) return

  kakaoMap.value.setCenter(place._position)
  kakaoMap.value.setLevel(3)
}

// 데이터베이스에서 여행지 데이터 가져오기
const fetchTravelData = async () => {
  try {
    isLoading.value = true

    const regions = props.courseData.regions || []
    const days = props.courseData.duration?.days || 1

    // API 호출
    const response = await api.getTravelSpots({
      area_name: regions.join(','),
      limit: days * 5
    })

    const travelSpots = response.data.results || response.data || []

    // 여행지를 일차별로 분배
    const placesPerDay = Math.ceil(travelSpots.length / days)
    const tempDays = []

    for (let i = 0; i < days; i++) {
      const startIndex = i * placesPerDay
      const endIndex = startIndex + placesPerDay
      const dayPlaces = travelSpots.slice(startIndex, endIndex).map(spot => ({
        id: spot.id,
        name: spot.name,
        address: spot.address || spot.addr1,
        latitude: spot.latitude || spot.mapy,
        longitude: spot.longitude || spot.mapx,
        image_url: spot.image_url,
        first_image: spot.first_image,
        category: getCategoryName(spot.content_type_id)
      }))

      tempDays.push({
        date: `Day ${i + 1}`,
        places: dayPlaces
      })
    }

    itineraryDays.value = tempDays

  } catch (error) {
    console.error('여행 데이터 조회 실패:', error)
    useSampleData()
  } finally {
    isLoading.value = false
  }
}

// 카테고리 이름 변환
const getCategoryName = (contentTypeId) => {
  const categoryMap = {
    12: '여행지',
    14: '문화시설',
    15: '축제',
    25: '여행코스',
    28: '레포츠',
    32: '숙박',
    38: '쇼핑',
    39: '음식점'
  }
  return categoryMap[contentTypeId] || '여행지'
}

// 샘플 데이터
const useSampleData = () => {
  const days = props.courseData.duration?.days || 1
  const tempDays = []

  for (let i = 0; i < days; i++) {
    tempDays.push({
      date: `Day ${i + 1}`,
      places: [
        {
          id: i * 10 + 1,
          name: '아르떼뮤지엄',
          address: '대구광역시 수성구 무학로 42',
          latitude: 35.8714 + (i * 0.01),
          longitude: 128.6014 + (i * 0.01),
          category: '여행지',
          image_url: null
        },
        {
          id: i * 10 + 2,
          name: '라벨라쿠치나',
          address: '대구광역시 수성구 무학로 151',
          latitude: 35.8714 + (i * 0.01) + 0.005,
          longitude: 128.6014 + (i * 0.01) + 0.005,
          category: '음식점',
          image_url: null
        }
      ]
    })
  }

  itineraryDays.value = tempDays
}

// 초기화
onMounted(async () => {
  try {
    console.log('🚀 CourseResult 초기화 시작')
    console.log('📍 API 키:', import.meta.env.VITE_KAKAO_MAP_API_KEY)

    await loadKakaoMapScript()
    console.log('✅ 카카오맵 스크립트 로드 완료')

    initializeKakaoMap()
    console.log('✅ 카카오맵 초기화 완료')

    await fetchTravelData()
    console.log('✅ 여행 데이터 로드 완료')

    updateMapMarkers()
    console.log('✅ 마커 업데이트 완료')

  } catch (error) {
    console.error('❌ 초기화 실패:', error)
    console.error('❌ 에러 상세:', error.message, error.stack)
  }
})

// 날짜 변경 감지
watch(currentDay, () => {
  updateMapMarkers()
})
</script>

<style scoped>
/* 레퍼런스 그대로: 전체 레이아웃 */
.course-result {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: #f5f5f5;
}

.result-layout {
  display: flex;
  height: 100%;
}

/* 레퍼런스 그대로: 좌측 사이드바 (25~30%) */
.sidebar {
  width: 380px;
  height: 100%;
  background: white;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-right: 1px solid #e0e0e0;
}

/* 사이드바 헤더 */
.sidebar-header {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e0e0e0;
  gap: 12px;
}

.btn-back {
  background: none;
  border: none;
  font-size: 18px;
  color: #333;
  cursor: pointer;
  padding: 4px;
}

.planner-title {
  font-size: 18px;
  font-weight: 700;
  color: #000;
  margin: 0;
  flex: 1;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  padding: 4px 8px;
}

/* 탭 메뉴 - 레퍼런스 그대로 */
.tab-menu {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
}

.tab-item {
  flex: 1;
  padding: 12px 8px;
  background: none;
  border: none;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tab-item.active {
  color: #00C73C;
  border-bottom-color: #00C73C;
  font-weight: 600;
}

/* 여행 요약 카드 - 레퍼런스 그대로 */
.trip-summary-card {
  margin: 16px;
  padding: 16px;
  background: #E8F5F1;
  border-radius: 8px;
}

.summary-badge {
  margin-bottom: 12px;
}

.badge-day {
  display: inline-block;
  padding: 4px 12px;
  background: #00C73C;
  color: white;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
}

.summary-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #333;
}

.info-icon {
  font-size: 14px;
}

.summary-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 10px;
  background: white;
  border-radius: 12px;
  font-size: 12px;
  color: #00C73C;
}

/* 평점 섹션 */
.rating-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.rating-label {
  font-size: 13px;
  color: #666;
}

.stars {
  display: flex;
  gap: 4px;
}

.stars i {
  font-size: 16px;
  color: #ddd;
  cursor: pointer;
}

/* Day 헤더 */
.day-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: white;
}

.day-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #000;
  margin: 0;
}

.btn-expand {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  font-size: 13px;
  color: #666;
  cursor: pointer;
}

/* 장소 리스트 - 레퍼런스 그대로 (세로 스크롤) */
.places-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px 16px;
}

.places-list::-webkit-scrollbar {
  width: 6px;
}

.places-list::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.place-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.place-item:hover {
  background: #f9f9f9;
}

.place-number {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #4A90E2;
  color: white;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.place-thumbnail {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  background: #f0f0f0;
}

.place-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.place-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.place-category {
  display: inline-block;
  padding: 2px 8px;
  background: #00C73C;
  color: white;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  align-self: flex-start;
}

.place-name {
  font-size: 15px;
  font-weight: 600;
  color: #000;
  margin-top: 4px;
}

.place-address {
  font-size: 12px;
  color: #888;
  line-height: 1.4;
}

.btn-detail {
  align-self: flex-start;
  margin-top: 4px;
  padding: 4px 8px;
  background: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 11px;
  color: #666;
  cursor: pointer;
}

/* 레퍼런스 그대로: 우측 지도 영역 (70~75%) */
.map-area {
  flex: 1;
  position: relative;
  height: 100%;
}

.kakao-map {
  width: 100%;
  height: 100%;
}

/* 우측 상단: 날짜 토글 - 레퍼런스 그대로 위치 */
.day-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  z-index: 10;
}

.day-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.day-btn.active {
  background: #4A90E2;
  color: white;
  border-color: #4A90E2;
}

.day-circle {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #4A90E2;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 700;
}

.day-circle.day2 {
  background: #34C759;
}

.day-circle.day3 {
  background: #FF9500;
}

.day-circle.all {
  background: #666;
}

.day-btn.active .day-circle {
  background: white;
  color: #4A90E2;
}

/* 우측 하단: 다시뽑기 버튼 - 레퍼런스 그대로 위치 */
.map-footer {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
}

.btn-regenerate {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: white;
  border: 2px solid #00C73C;
  border-radius: 24px;
  font-size: 13px;
  color: #333;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: all 0.2s;
}

.btn-regenerate:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

.btn-regenerate i {
  color: #00C73C;
}

.btn-regenerate strong {
  color: #00C73C;
  font-weight: 700;
}

.badge-go {
  padding: 2px 8px;
  background: #00C73C;
  color: white;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
}

/* 반응형 - 레퍼런스는 데스크톱 기준이므로 모바일은 최소한만 */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    position: absolute;
    z-index: 20;
    max-height: 50vh;
  }

  .map-area {
    width: 100%;
  }
}
</style>
