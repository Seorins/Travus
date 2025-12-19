<template>
  <div class="travel-view">
    <NavigationBar
      :isTTSEnabled="isTTSEnabled"
      @toggle-tts="toggleTTS"
      @font-size-change="handleFontSizeChange"
      @focus="handleTTSFocus"
    />

    <!-- 헤더 섹션 -->
    <section class="travel-header">
      <div class="container">
        <h1 class="page-title">{{ pageTitle }}</h1>
        <p class="page-subtitle">{{ pageSubtitle }}</p>

        <!-- 검색바 -->
        <div class="search-bar">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="여행지를 검색하세요..."
            @keyup.enter="handleSearch"
            class="search-input"
          />
          <button class="search-btn" @click="handleSearch">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- 무장애 검색 섹션 -->
    <section class="filter-section">
      <div class="container">
        <div class="filter-card">
          <!-- 무장애 검색 헤더 -->
          <div class="filter-header" @click="toggleFilterCollapse">
            <h3 class="filter-main-title">무장애 검색</h3>
            <button class="collapse-btn">
              <span v-if="isFilterCollapsed">▼</span>
              <span v-else>▲</span>
            </button>
          </div>

          <!-- 필터 내용 -->
          <div v-show="!isFilterCollapsed" class="filter-content">
            <!-- 무장애 유형 -->
            <div class="filter-row">
              <div class="accessibility-types">
                <button
                  class="accessibility-type-btn"
                  :class="{ active: selectedAccessibilityTypes.includes('wheelchair') }"
                  @click="toggleAccessibilityType('wheelchair')"
                >
                  <div class="icon-wrapper">
                    <img src="@/assets/icon_body.png" alt="지체장애" />
                  </div>
                  <span>지체장애</span>
                </button>

                <button
                  class="accessibility-type-btn"
                  :class="{ active: selectedAccessibilityTypes.includes('visual') }"
                  @click="toggleAccessibilityType('visual')"
                >
                  <div class="icon-wrapper">
                    <img src="@/assets/icon_eye.png" alt="시각장애" />
                  </div>
                  <span>시각장애</span>
                </button>

                <button
                  class="accessibility-type-btn"
                  :class="{ active: selectedAccessibilityTypes.includes('hearing') }"
                  @click="toggleAccessibilityType('hearing')"
                >
                  <div class="icon-wrapper">
                    <img src="@/assets/icon_ear.png" alt="청각장애" />
                  </div>
                  <span>청각장애</span>
                </button>

                <button
                  class="accessibility-type-btn"
                  :class="{ active: selectedAccessibilityTypes.includes('family') }"
                  @click="toggleAccessibilityType('family')"
                >
                  <div class="icon-wrapper">
                    <img src="@/assets/icon_baby.png" alt="영유아 가족" />
                  </div>
                  <span>영유아 가족</span>
                </button>

                <button
                  class="accessibility-type-btn"
                  :class="{ active: selectedAccessibilityTypes.includes('senior') }"
                  @click="toggleAccessibilityType('senior')"
                >
                  <div class="icon-wrapper">
                    <img src="@/assets/icon_old.png" alt="고령자" />
                  </div>
                  <span>고령자</span>
                </button>
              </div>
            </div>

            <!-- 시설 정보 -->
            <div class="filter-row">
              <div class="facility-types">
                <button
                  class="facility-btn"
                  :class="{ active: selectedFacilities.includes('all') }"
                  @click="toggleFacility('all')"
                >
                  전체
                </button>
                <button
                  class="facility-btn"
                  :class="{ active: selectedFacilities.includes('parking') }"
                  @click="toggleFacility('parking')"
                >
                  주차장
                </button>
                <button
                  class="facility-btn"
                  :class="{ active: selectedFacilities.includes('restroom') }"
                  @click="toggleFacility('restroom')"
                >
                  화장실
                </button>
                <button
                  class="facility-btn"
                  :class="{ active: selectedFacilities.includes('elevator') }"
                  @click="toggleFacility('elevator')"
                >
                  승강기
                </button>
                <button
                  class="facility-btn"
                  :class="{ active: selectedFacilities.includes('route') }"
                  @click="toggleFacility('route')"
                >
                  이동경로
                </button>
                <button
                  class="facility-btn"
                  :class="{ active: selectedFacilities.includes('exit') }"
                  @click="toggleFacility('exit')"
                >
                  출입구
                </button>
              </div>
            </div>

            <!-- 지역 선택 및 검색 -->
            <div class="filter-row">
              <div class="region-search-row">
                <div class="region-select-wrapper">
                  <label>지역선택</label>
                  <select v-model="selectedRegion" class="region-select">
                    <option value="">시도 선택</option>
                    <option value="1">서울</option>
                    <option value="6">부산</option>
                    <option value="4">대구</option>
                    <option value="5">인천</option>
                    <option value="2">광주</option>
                    <option value="3">대전</option>
                    <option value="7">울산</option>
                    <option value="39">제주</option>
                    <option value="31">경기</option>
                    <option value="32">강원</option>
                    <option value="33">충북</option>
                    <option value="34">충남</option>
                    <option value="35">경북</option>
                    <option value="36">경남</option>
                    <option value="37">전북</option>
                    <option value="38">전남</option>
                  </select>
                </div>

                <div class="region-select-wrapper">
                  <label>전체</label>
                  <select class="region-select">
                    <option value="">전체</option>
                  </select>
                </div>

                <button class="search-filter-btn" @click="handleFilterSearch">
                  검색
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 로딩 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>데이터를 불러오는 중...</p>
    </div>

    <!-- 여행지 리스트 -->
    <section class="destinations-section" v-else>
      <div class="container">
        <div v-if="destinations.length === 0" class="no-results">
          <p>검색 결과가 없습니다.</p>
        </div>
        <div v-else class="destinations-grid">
          <TravelCard
            v-for="(destination, index) in filteredDestinations"
            :key="index"
            :destination="formatDestination(destination)"
            @click="handleCardClick(destination)"
          />
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination" v-if="totalPages > 1">
          <!-- 이전 그룹 -->
          <button
            class="page-btn nav-btn"
            :disabled="displayedPages[0] === 1"
            @click="changePageGroup(-1)"
            title="이전 그룹"
          >
            ◀◀
          </button>

          <!-- 이전 -->
          <button
            class="page-btn nav-btn"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
            title="이전"
          >
            ◀
          </button>

          <!-- 페이지 번호들 -->
          <button
            v-for="page in displayedPages"
            :key="page"
            class="page-btn"
            :class="{ active: page === currentPage }"
            @click="changePage(page)"
          >
            {{ page }}
          </button>

          <!-- 다음 -->
          <button
            class="page-btn nav-btn"
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
            title="다음"
          >
            ▶
          </button>

          <!-- 다음 그룹 -->
          <button
            class="page-btn nav-btn"
            :disabled="displayedPages[displayedPages.length - 1] === totalPages"
            @click="changePageGroup(1)"
            title="다음 그룹"
          >
            ▶▶
          </button>
        </div>
      </div>
    </section>

    <FooterSection />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import NavigationBar from '@/components/common/NavigationBar.vue'
import FooterSection from '@/components/common/FooterSection.vue'
import TravelCard from '@/components/travel/TravelCard.vue'
import api from '@/services/api'

// 라우트에서 카테고리 가져오기
const route = useRoute()
const contentTypeId = computed(() => route.query.category || '')

// 페이지 타이틀 동적 변경
const pageTitle = computed(() => {
  switch (contentTypeId.value) {
    case '12': return '관광지/명소'
    case '32': return '숙박'
    case '39': return '음식점'
    default: return '여행지 정보'
  }
})

const pageSubtitle = computed(() => {
  switch (contentTypeId.value) {
    case '12': return '전국의 무장애 관광지를 찾아보세요'
    case '32': return '편안한 무장애 숙박시설을 찾아보세요'
    case '39': return '접근 가능한 음식점을 찾아보세요'
    default: return '전국의 다양한 무장애 여행지를 찾아보세요'
  }
})

// TTS 상태
const isTTSEnabled = ref(true)
const synthesis = window.speechSynthesis

const toggleTTS = () => {
  isTTSEnabled.value = !isTTSEnabled.value
  if (!isTTSEnabled.value) {
    synthesis.cancel()
  }
}

const handleFontSizeChange = (size) => {
  document.documentElement.style.fontSize = `${size}px`
}

const handleTTSFocus = (text) => {
  if (isTTSEnabled.value && text) {
    synthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'ko-KR'
    utterance.rate = 0.9
    synthesis.speak(utterance)
  }
}

// 검색 및 필터 상태
const searchQuery = ref('')
const selectedAccessibilityTypes = ref([]) // 무장애 유형 (다중 선택)
const selectedFacilities = ref([]) // 시설 정보 (다중 선택)
const selectedRegion = ref('')
const sortBy = ref('latest')
const isFilterCollapsed = ref(false) // 필터 접기/펼치기 상태

// 데이터 상태
const destinations = ref([])
const loading = ref(false)
const totalCount = ref(0)

// 페이지네이션 상태
const currentPage = ref(1)
const itemsPerPage = 20
const fetchSize = 100 // 이미지 필터링을 고려하여 더 많이 가져오기

const totalPages = computed(() => {
  return Math.ceil(totalCount.value / itemsPerPage)
})

const displayedPages = computed(() => {
  const pages = []
  const maxDisplayed = 5

  // 현재 페이지가 속한 그룹의 시작 페이지 계산
  const groupStart = Math.floor((currentPage.value - 1) / maxDisplayed) * maxDisplayed + 1
  const groupEnd = Math.min(groupStart + maxDisplayed - 1, totalPages.value)

  for (let i = groupStart; i <= groupEnd; i++) {
    pages.push(i)
  }

  return pages
})

// 이미지가 있는 여행지만 필터링하고 페이지당 정확히 itemsPerPage개만 표시
const filteredDestinations = computed(() => {
  const withImages = destinations.value.filter(destination => {
    return destination.firstimage && destination.firstimage.trim() !== ''
  })
  // 최대 itemsPerPage개까지만 반환
  return withImages.slice(0, itemsPerPage)
})

// 여행지 데이터 포맷 변환
const formatDestination = (destination) => {
  return {
    id: destination.contentid || destination.id,
    name: destination.title || destination.name,
    description: destination.addr1 || destination.address || '주소 정보 없음',
    image: destination.firstimage || destination.image_url || 'https://via.placeholder.com/400x300?text=No+Image',
    rating: destination.rating || 0,
    reviews: destination.review_count || 0,
    tags: []
  }
}

// 데이터 로드
const loadDestinations = async () => {
  loading.value = true

  try {
    let response

    if (searchQuery.value) {
      // 키워드 검색
      response = await api.searchTravelSpotsAPI(searchQuery.value, {
        area_code: selectedRegion.value,
        content_type_id: contentTypeId.value,
        page: currentPage.value,
        size: fetchSize
      })
    } else {
      // 지역 기반 목록
      response = await api.getTravelSpotsFromAPI({
        area_code: selectedRegion.value,
        content_type_id: contentTypeId.value,
        page: currentPage.value,
        size: fetchSize
      })
    }

    if (response.data) {
      let results = response.data.results || []

      // 클라이언트 사이드 필터링 (무장애 유형 & 시설)
      if (selectedAccessibilityTypes.value.length > 0 || selectedFacilities.value.length > 0) {
        results = results.filter(item => {
          // 무장애 유형 필터
          if (selectedAccessibilityTypes.value.length > 0) {
            // API 응답에 무장애 정보가 있다고 가정
            // 실제로는 백엔드에서 필터링하는 것이 더 좋음
          }

          // 시설 필터
          if (selectedFacilities.value.length > 0) {
            // API 응답에 시설 정보가 있다고 가정
          }

          return true
        })
      }

      destinations.value = results
      totalCount.value = response.data.count || 0
    }
  } catch (error) {
    console.error('데이터 로드 실패:', error)
    destinations.value = []
    totalCount.value = 0
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadDestinations()
}

const toggleAccessibilityType = (type) => {
  const index = selectedAccessibilityTypes.value.indexOf(type)
  if (index > -1) {
    selectedAccessibilityTypes.value.splice(index, 1)
  } else {
    selectedAccessibilityTypes.value.push(type)
  }
}

const toggleFacility = (facility) => {
  const index = selectedFacilities.value.indexOf(facility)
  if (index > -1) {
    selectedFacilities.value.splice(index, 1)
  } else {
    selectedFacilities.value.push(facility)
  }
}

const toggleFilterCollapse = () => {
  isFilterCollapsed.value = !isFilterCollapsed.value
}

const handleFilterSearch = () => {
  currentPage.value = 1
  loadDestinations()
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadDestinations()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const changePageGroup = (direction) => {
  const maxDisplayed = 5
  let newPage

  if (direction > 0) {
    // 다음 그룹: 현재 표시된 마지막 페이지 + 1
    newPage = displayedPages.value[displayedPages.value.length - 1] + 1
  } else {
    // 이전 그룹: 현재 표시된 첫 페이지 - maxDisplayed
    newPage = displayedPages.value[0] - maxDisplayed
  }

  changePage(newPage)
}

const handleCardClick = (destination) => {
  console.log('Clicked destination:', destination)
  // 상세 페이지로 이동 로직 추가
}

// 카테고리 변경시 데이터 자동 새로고침
watch(() => route.query.category, () => {
  currentPage.value = 1
  selectedRegion.value = ''
  selectedAccessibilityTypes.value = []
  selectedFacilities.value = []
  searchQuery.value = ''
  loadDestinations()
})

onMounted(() => {
  loadDestinations()
})
</script>

<style scoped>
.travel-view {
  min-height: 100vh;
  background: #f9fafb;
}

/* 헤더 섹션 */
.travel-header {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  padding: 4rem 2rem 3rem;
  color: white;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: 3rem;
  font-weight: 900;
  margin: 0 0 1rem 0;
  text-align: center;
}

.page-subtitle {
  font-size: 1.25rem;
  text-align: center;
  margin: 0 0 2rem 0;
  opacity: 0.9;
}

/* 검색바 */
.search-bar {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  background: white;
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  font-size: 1rem;
  outline: none;
  color: #333;
}

.search-btn {
  padding: 1rem 1.5rem;
  background: #111827;
  border: none;
  color: white;
  cursor: pointer;
  transition: background 0.3s ease;
}

.search-btn:hover {
  background: #1f2937;
}

/* 필터 섹션 */
.filter-section {
  background: #f3f4f6;
  padding: 2rem;
}

.filter-card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-header {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background 0.3s ease;
}

.filter-header:hover {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

.filter-main-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.collapse-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: transform 0.3s ease;
}

.filter-content {
  padding: 2rem;
  background: #f9fafb;
}

.filter-row {
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.filter-row:last-child {
  margin-bottom: 0;
}

/* 무장애 유형 버튼 */
.accessibility-types {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.accessibility-type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 1.5rem;
  background: white;
  border: 3px solid #e5e7eb;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.accessibility-type-btn:hover {
  border-color: #9ca3af;
  background: #f9fafb;
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(156, 163, 175, 0.15);
}

.accessibility-type-btn.active {
  border-color: #9ca3af;
  background: #f9fafb;
  position: relative;
}

.accessibility-type-btn.active::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 6px;
  background: #9ca3af;
  border-radius: 3px 3px 0 0;
}

.accessibility-type-btn .icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.accessibility-type-btn .icon-wrapper img {
  width: 50px;
  height: 50px;
  object-fit: contain;
}

.accessibility-type-btn.active .icon-wrapper {
  background: #d1d5db;
}

.accessibility-type-btn span {
  font-size: 1rem;
  font-weight: 700;
  color: #374151;
}

.accessibility-type-btn.active span {
  color: #6b7280;
}

/* 시설 정보 버튼 */
.facility-types {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.facility-btn {
  padding: 0.875rem 2rem;
  background: white;
  border: 2px solid #d1d5db;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: #6b7280;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.facility-btn:hover {
  border-color: #9ca3af;
  background: #f3f4f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.facility-btn.active {
  background: #9ca3af;
  border-color: #9ca3af;
  color: white;
}

/* 지역 선택 및 검색 버튼 */
.region-search-row {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  justify-content: center;
  flex-wrap: wrap;
}

.region-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.region-select-wrapper label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}

.region-select {
  padding: 0.875rem 1.5rem;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  background: white;
  transition: all 0.2s ease;
  min-width: 200px;
}

.region-select:hover {
  border-color: #9ca3af;
}

.region-select:focus {
  outline: none;
  border-color: #6b7280;
  box-shadow: 0 0 0 3px rgba(107, 114, 128, 0.1);
}

.search-filter-btn {
  padding: 0.875rem 3rem;
  background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.search-filter-btn:hover {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.search-filter-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}


/* 로딩 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  min-height: 400px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #111827;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-container p {
  margin-top: 1rem;
  color: #6b7280;
  font-size: 1.1rem;
}

/* 결과 없음 */
.no-results {
  text-align: center;
  padding: 4rem 2rem;
  font-size: 1.2rem;
  color: #6b7280;
}

/* 여행지 리스트 */
.destinations-section {
  padding: 3rem 2rem;
}

.destinations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 3rem;
}

.page-btn {
  padding: 0.75rem 1.25rem;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.page-btn.active {
  background: #111827;
  color: white;
  border-color: #111827;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 반응형 */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .filter-card {
    padding: 1.5rem;
  }

  .filter-main-title {
    font-size: 1.25rem;
  }

  .accessibility-types {
    flex-direction: column;
  }

  .accessibility-type-btn {
    width: 100%;
  }

  .facility-types {
    flex-direction: column;
    gap: 0.75rem;
  }

  .facility-checkbox {
    width: 100%;
  }

  .region-search-row {
    flex-direction: column;
  }

  .region-select {
    width: 100%;
  }

  .search-filter-btn {
    width: 100%;
  }

  .result-info {
    margin-left: 0;
    text-align: center;
  }

  .destinations-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .pagination {
    flex-wrap: wrap;
  }

  .page-btn {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
}
</style>
