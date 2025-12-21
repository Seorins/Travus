<template>
  <div class="travel-detail-page">
    <NavigationBar />

    <main class="main-content">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>여행지 정보를 불러오는 중...</p>
      </div>

      <!-- 에러 상태 -->
      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="$router.push('/travel')" class="back-btn">목록으로 돌아가기</button>
      </div>

      <!-- 상세 정보 -->
      <div v-else-if="destination" class="detail-content">
        <div class="container">
          <!-- 헤더 섹션 -->
          <div class="header-section">
            <div class="header-top">
              <span class="category-badge">여행지</span>
              <div class="actions">
                <button class="action-btn" @click="openShareModal">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8M16 6l-4-4-4 4M12 2v13" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button class="action-btn">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
            <h1 class="page-title">{{ destination?.title || '로딩 중...' }}</h1>
          </div>

          <!-- 탭 메뉴 -->
          <div class="tab-menu">
            <button class="tab-item active">사진보기</button>
            <button class="tab-item">상세정보</button>
            <button class="tab-item">댓글</button>
            <button class="tab-item">추천여행</button>
          </div>

          <!-- 메인 이미지 -->
          <div class="main-image-section">
            <div class="image-container">
              <img
                v-if="images.length > 0"
                :src="images[0].originimgurl || images[0].smallimageurl || 'https://via.placeholder.com/1200x600'"
                :alt="destination.title"
              />
              <img
                v-else
                :src="destination.firstimage || destination.firstimage2 || 'https://via.placeholder.com/1200x600'"
                :alt="destination.title"
              />
              <div class="image-counter">{{ images.length > 0 ? `1/${images.length}` : '1/1' }}</div>
            </div>
          </div>

          <!-- 상세 설명 -->
          <div class="description-section">
            <h2 class="section-title">상세정보</h2>
            <p class="description-text" v-if="destination.overview">
              {{ destination.overview }}
            </p>
            <p class="description-text no-content" v-else>
              상세 설명이 준비 중입니다.
            </p>
          </div>

          <!-- 지도 -->
          <div class="map-section">
            <div id="kakao-map" class="kakao-map"></div>
          </div>

          <!-- 기본 정보 그리드 -->
          <div class="info-grid-section">
            <div class="info-grid-item" v-if="destination.tel">
              <span class="info-key">문의/안내</span>
              <span class="info-value">{{ destination.tel }}</span>
            </div>
            <div class="info-grid-item" v-if="destination.addr1">
              <span class="info-key">주소</span>
              <span class="info-value">{{ destination.addr1 }}</span>
            </div>
            <div class="info-grid-item" v-if="detailIntro && detailIntro.usetime">
              <span class="info-key">이용시간</span>
              <span class="info-value">{{ detailIntro.usetime }}</span>
            </div>
            <div class="info-grid-item" v-if="detailIntro && detailIntro.restdate">
              <span class="info-key">쉬는날</span>
              <span class="info-value">{{ detailIntro.restdate }}</span>
            </div>
            <div class="info-grid-item" v-if="detailIntro && detailIntro.parking">
              <span class="info-key">주차시설</span>
              <span class="info-value">{{ detailIntro.parking }}</span>
            </div>
            <div class="info-grid-item" v-if="detailIntro && detailIntro.infocenter">
              <span class="info-key">문의 및 안내</span>
              <span class="info-value">{{ detailIntro.infocenter }}</span>
            </div>
            <div class="info-grid-item" v-if="destination.homepage">
              <span class="info-key">홈페이지</span>
              <div class="info-value" v-html="destination.homepage"></div>
            </div>
            <div class="info-grid-item">
              <span class="info-key">지역</span>
              <span class="info-value">{{ getRegionName(destination.areacode) }}</span>
            </div>
          </div>

          <!-- 태그 -->
          <div class="tags-section">
            <span class="tag">#{{ getRegionName(destination.areacode) }}</span>
            <span class="tag">#관광지</span>
            <span class="tag">#무장애여행</span>
          </div>

          <!-- AI 요약 섹션 -->
          <div class="ai-summary-section">
            <div class="ai-summary-header">
              <div class="ai-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
              </div>
              <h3 class="ai-summary-title">AI가 빠르게 요약해주는 사용자 후기!</h3>
            </div>
            <div class="ai-summary-content">
              <p>이 여행지는 {{ getRegionName(destination.areacode) }} 지역의 대표적인 관광명소로, 접근성이 좋고 다양한 편의시설을 갖추고 있습니다. 무장애 관광을 위한 시설이 잘 마련되어 있어 모든 분들이 편안하게 여행을 즐기실 수 있습니다.</p>
            </div>
          </div>

          <!-- 무장애 정보 -->
          <div class="accessibility-section">
            <h2 class="section-title">무장애 관광 정보</h2>
            <div class="accessibility-grid">
              <div class="accessibility-card">
                <div class="accessibility-icon">♿</div>
                <h3 class="accessibility-title">휠체어 접근</h3>
                <p class="accessibility-text">{{ accessibilityInfo.wheelchair }}</p>
              </div>
              <div class="accessibility-card">
                <div class="accessibility-icon">🅿️</div>
                <h3 class="accessibility-title">주차 시설</h3>
                <p class="accessibility-text">{{ accessibilityInfo.parking }}</p>
              </div>
              <div class="accessibility-card">
                <div class="accessibility-icon">🚻</div>
                <h3 class="accessibility-title">장애인 화장실</h3>
                <p class="accessibility-text">{{ accessibilityInfo.restroom }}</p>
              </div>
              <div class="accessibility-card">
                <div class="accessibility-icon">👁️</div>
                <h3 class="accessibility-title">시각장애인 안내</h3>
                <p class="accessibility-text">{{ accessibilityInfo.visual }}</p>
              </div>
            </div>
          </div>

          <!-- 추천 여행지 -->
          <div class="recommendations-section" v-if="recommendations.length > 0">
            <h2 class="section-title">{{ getRegionName(destination.areacode) }} 추천 여행지</h2>
            <div class="recommendation-grid">
              <div
                v-for="rec in recommendations"
                :key="rec.contentid"
                class="recommendation-card"
                @click="handleRecommendationClick(rec)"
              >
                <div class="recommendation-image">
                  <img
                    :src="rec.firstimage || rec.firstimage2 || 'https://via.placeholder.com/300x200'"
                    :alt="rec.title"
                  />
                </div>
                <div class="recommendation-info">
                  <h3 class="recommendation-title">{{ rec.title }}</h3>
                  <p class="recommendation-location">{{ getRegionName(rec.areacode) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 공유 모달 -->
    <div v-if="showShareModal" class="modal-overlay" @click="closeShareModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>여행지 공유하기</h3>
          <button class="modal-close-btn" @click="closeShareModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p class="share-description">아래 링크를 복사하여 공유해보세요!</p>
          <div class="url-container">
            <input
              ref="urlInput"
              type="text"
              :value="currentUrl"
              readonly
              class="url-input"
            />
            <button @click="copyToClipboard" class="copy-btn">
              {{ copySuccess ? '복사됨!' : '복사' }}
            </button>
          </div>
          <p v-if="copySuccess" class="copy-success-message">✓ 링크가 클립보드에 복사되었습니다</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavigationBar from '@/components/common/NavigationBar.vue'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const isLoading = ref(true)
const error = ref(null)
const destination = ref(null)
const detailIntro = ref(null)
const detailInfo = ref(null)
const images = ref([])
const recommendations = ref([])
const accessibilityInfo = ref({
  wheelchair: '정보 준비 중입니다',
  parking: '정보 준비 중입니다',
  restroom: '정보 준비 중입니다',
  visual: '정보 준비 중입니다'
})

// 공유 모달 관련
const showShareModal = ref(false)
const copySuccess = ref(false)
const urlInput = ref(null)
const currentUrl = ref('')

const regionMap = {
  '1': '서울',
  '2': '인천',
  '3': '대전',
  '4': '대구',
  '5': '광주',
  '6': '부산',
  '7': '울산',
  '8': '세종',
  '31': '경기',
  '32': '강원',
  '33': '충북',
  '34': '충남',
  '35': '경북',
  '36': '경남',
  '37': '전북',
  '38': '전남',
  '39': '제주'
}

const getRegionName = (areacode) => {
  return regionMap[areacode] || '기타'
}

// 같은 지역 추천 여행지 가져오기
const fetchRecommendations = async (areaCode, currentContentId) => {
  try {
    console.log('📍 같은 지역 추천 여행지 조회:', areaCode)

    // 같은 지역의 관광지 가져오기
    const response = await api.getTravelSpots({
      area_code: areaCode,
      content_type_id: '12', // 관광지만
      page_size: 20 // 충분히 가져와서 랜덤 선택
    })

    if (response.data && response.data.results) {
      // 현재 여행지 제외
      let filtered = response.data.results.filter(item => item.content_id !== currentContentId)

      // 이미지가 있는 것만 필터링
      filtered = filtered.filter(item => item.image_url)

      // 랜덤 셔플 (Fisher-Yates)
      const shuffled = [...filtered]
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
      }

      // 최대 6개만 선택
      recommendations.value = shuffled.slice(0, 6).map(item => ({
        contentid: item.content_id,
        title: item.name,
        addr1: item.address,
        areacode: item.area_code,
        firstimage: item.image_url,
        firstimage2: item.thumbnail_url
      }))

      console.log(`✅ ${recommendations.value.length}개 추천 여행지 로드 완료`)
    }
  } catch (error) {
    console.error('❌ 추천 여행지 로드 실패:', error)
    recommendations.value = []
  }
}

const initKakaoMap = () => {
  if (!destination.value || !destination.value.mapy || !destination.value.mapx) {
    console.error('좌표 정보가 없습니다')
    return
  }

  const container = document.getElementById('kakao-map')
  const options = {
    center: new window.kakao.maps.LatLng(destination.value.mapy, destination.value.mapx),
    level: 3
  }

  const map = new window.kakao.maps.Map(container, options)
  const markerPosition = new window.kakao.maps.LatLng(destination.value.mapy, destination.value.mapx)
  const marker = new window.kakao.maps.Marker({ position: markerPosition })
  marker.setMap(map)

  const infowindow = new window.kakao.maps.InfoWindow({
    content: `<div style="padding:10px;font-size:14px;text-align:center;min-width:150px;">${destination.value.title}</div>`
  })
  infowindow.open(map, marker)
}

const loadKakaoMapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      resolve()
      return
    }

    const apiKey = import.meta.env.VITE_KAKAO_MAP_API_KEY
    if (!apiKey) {
      console.warn('카카오맵 API 키가 설정되지 않았습니다.')
      reject(new Error('카카오맵 API 키가 없습니다'))
      return
    }

    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&autoload=false`
    script.onload = () => {
      if (window.kakao && window.kakao.maps) {
        window.kakao.maps.load(() => resolve())
      } else {
        reject(new Error('카카오맵 스크립트 로딩 실패'))
      }
    }
    script.onerror = (error) => {
      console.error('카카오맵 스크립트 로딩 에러:', error)
      reject(error)
    }
    document.head.appendChild(script)
  })
}

const fetchDestinationDetail = async () => {
  try {
    isLoading.value = true
    error.value = null
    const contentId = route.params.id
    console.log('📍 DB에서 content_id로 여행지 조회:', contentId)

    // DB에서 content_id로 여행지 조회
    const response = await api.getTravelSpotByContentId(contentId)
    console.log('✅ DB 응답:', response.data)

    const travelSpot = response.data

    // DB 응답을 기존 API 응답 형식에 맞게 매핑
    destination.value = {
      contentid: travelSpot.content_id,
      contenttypeid: travelSpot.content_type_id,
      title: travelSpot.name,
      addr1: travelSpot.address,
      areacode: travelSpot.area_code,
      sigungucode: travelSpot.sigungu_code,
      mapy: travelSpot.latitude,
      mapx: travelSpot.longitude,
      overview: travelSpot.description,
      tel: travelSpot.tel,
      homepage: travelSpot.homepage,
      firstimage: travelSpot.image_url,
      firstimage2: travelSpot.thumbnail_url,
      // 무장애 정보가 있으면 포함
      accessibility: travelSpot.accessibility
    }

    console.log('✅ 여행지 정보 로드 완료:', destination.value.title)

    // 무장애 정보 매핑 (DB에서 가져온 데이터 사용)
    if (travelSpot.accessibility) {
      const acc = travelSpot.accessibility
      accessibilityInfo.value = {
        wheelchair: acc.wheelchair ? '휠체어 이용 가능' : acc.wheelchair_info || '정보 없음',
        parking: acc.parking ? '장애인 주차장 있음' : acc.parking_info || '정보 없음',
        restroom: acc.restroom ? '장애인 화장실 있음' : acc.restroom_info || '정보 없음',
        visual: acc.audio_guide ? '음성 안내 제공' : '정보 없음'
      }
    }

    // 이미지 정보 설정 (DB의 image_url 사용)
    if (travelSpot.image_url) {
      images.value = [{
        originimgurl: travelSpot.image_url,
        smallimageurl: travelSpot.thumbnail_url
      }]
    }

    // 같은 지역 추천 여행지 가져오기
    await fetchRecommendations(travelSpot.area_code, contentId)

    // 지도 초기화 (데이터 로딩 완료 후)
    if (destination.value.mapx && destination.value.mapy) {
      try {
        await loadKakaoMapScript()
        setTimeout(() => initKakaoMap(), 100)
      } catch (mapError) {
        console.warn('지도 로딩 실패:', mapError)
      }
    }

  } catch (err) {
    console.error('Failed to fetch destination detail:', err)
    error.value = err.message || '여행지 정보를 불러오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDestinationDetail()
})

// 추천 여행지 클릭 핸들러
const handleRecommendationClick = (rec) => {
  router.push(`/travel/${rec.contentid}`)
}

// 공유 모달 열기
const openShareModal = () => {
  currentUrl.value = window.location.href
  showShareModal.value = true
  copySuccess.value = false
}

// 공유 모달 닫기
const closeShareModal = () => {
  showShareModal.value = false
  copySuccess.value = false
}

// URL 복사
const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(currentUrl.value)
    copySuccess.value = true

    // 3초 후 복사 성공 메시지 숨기기
    setTimeout(() => {
      copySuccess.value = false
    }, 3000)
  } catch (err) {
    console.error('Failed to copy:', err)
    // Fallback: input 선택 후 복사
    if (urlInput.value) {
      urlInput.value.select()
      document.execCommand('copy')
      copySuccess.value = true

      setTimeout(() => {
        copySuccess.value = false
      }, 3000)
    }
  }
}

// route.params.id가 변경될 때마다 데이터 다시 가져오기
watch(() => route.params.id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    console.log('Route changed from', oldId, 'to', newId)
    // 기존 데이터 초기화
    destination.value = null
    detailIntro.value = null
    detailInfo.value = null
    images.value = []
    recommendations.value = []
    // 새 데이터 가져오기
    fetchDestinationDetail()
  }
})
</script>

<style scoped>
.travel-detail-page {
  width: 100%;
  min-height: 100vh;
  background: #ffffff;
}

.main-content {
  padding-top: 80px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* 로딩 & 에러 */
.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 2rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 헤더 섹션 */
.header-section {
  padding: 2rem 0 1.5rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.category-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: #374151;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f9fafb;
  border-color: #667eea;
}

.action-btn svg {
  color: #6b7280;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

/* 탭 메뉴 */
.tab-menu {
  display: flex;
  gap: 1rem;
  border-bottom: 2px solid #e5e7eb;
  margin-bottom: 2rem;
}

.tab-item {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.tab-item.active {
  color: #667eea;
  font-weight: 600;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #667eea;
}

/* 메인 이미지 */
.main-image-section {
  margin-bottom: 3rem;
}

.image-container {
  position: relative;
  width: 100%;
  height: 600px;
  border-radius: 12px;
  overflow: hidden;
  background: #f3f4f6; /* 이미지 로딩 전/없을 때 배경색 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* cover → contain으로 변경 (화질 유지, 전체 이미지 표시) */
  background: #ffffff;
}

.image-counter {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* 섹션 타이틀 */
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 1.5rem 0;
}

/* 상세 설명 */
.description-section {
  margin-bottom: 3rem;
}

.description-text {
  font-size: 1rem;
  line-height: 1.8;
  color: #374151;
  margin: 0;
}

.no-content {
  color: #9ca3af;
  font-style: italic;
}

/* 지도 */
.map-section {
  margin-bottom: 3rem;
}

.kakao-map {
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
}

/* 정보 그리드 */
.info-grid-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 2rem;
  background: #f9fafb;
  border-radius: 12px;
}

.info-grid-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-key {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
}

.info-value {
  font-size: 1rem;
  color: #111827;
  line-height: 1.6;
}

.info-value :deep(a) {
  color: #667eea;
  text-decoration: none;
}

/* 태그 */
.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 3rem;
}

.tag {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* AI 요약 */
.ai-summary-section {
  padding: 2rem;
  background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
  border-radius: 12px;
  margin-bottom: 3rem;
}

.ai-summary-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.ai-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #3b82f6;
  color: white;
  border-radius: 12px;
}

.ai-summary-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e40af;
  margin: 0;
}

.ai-summary-content p {
  font-size: 1rem;
  line-height: 1.8;
  color: #1e3a8a;
  margin: 0;
}

/* 무장애 정보 */
.accessibility-section {
  margin-bottom: 3rem;
}

.accessibility-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.accessibility-card {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  text-align: center;
}

.accessibility-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.accessibility-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.75rem 0;
}

.accessibility-text {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

/* 추천 여행지 */
.recommendations-section {
  margin-bottom: 3rem;
}

.recommendation-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.recommendation-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.recommendation-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.recommendation-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recommendation-info {
  padding: 1.25rem;
}

.recommendation-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.recommendation-location {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

/* 공유 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
}

.modal-close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.modal-body {
  padding: 1.5rem;
}

.share-description {
  margin: 0 0 1rem;
  color: #6b7280;
  font-size: 0.95rem;
}

.url-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.url-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #374151;
  background: #f9fafb;
  font-family: monospace;
  transition: border-color 0.2s;
}

.url-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
}

.copy-btn {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.copy-btn:hover {
  background: #5568d3;
  transform: translateY(-1px);
}

.copy-btn:active {
  transform: translateY(0);
}

.copy-success-message {
  color: #10b981;
  font-size: 0.9rem;
  margin: 0.5rem 0 0;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
}

/* 반응형 */
@media (max-width: 1024px) {
  .info-grid-section {
    grid-template-columns: 1fr;
  }

  .accessibility-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .recommendation-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.75rem;
  }

  .image-container {
    height: 400px;
  }

  .accessibility-grid,
  .recommendation-grid {
    grid-template-columns: 1fr;
  }

  .tab-menu {
    overflow-x: auto;
  }

  .tab-item {
    white-space: nowrap;
  }
}
</style>
