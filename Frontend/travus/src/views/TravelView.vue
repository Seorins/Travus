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
        <h1 class="page-title">여행지 정보</h1>
        <p class="page-subtitle">전국의 다양한 무장애 여행지를 찾아보세요</p>

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

    <!-- 필터 섹션 -->
    <section class="filter-section">
      <div class="container">
        <div class="filter-container">
          <!-- 지역 필터 -->
          <div class="filter-group">
            <label class="filter-label">지역</label>
            <select v-model="selectedRegion" @change="handleFilterChange" class="filter-select">
              <option value="">전체</option>
              <option value="1">서울</option>
              <option value="6">부산</option>
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

          <!-- 정렬 -->
          <div class="filter-group">
            <label class="filter-label">정렬</label>
            <select v-model="sortBy" @change="handleSort" class="filter-select">
              <option value="latest">최신순</option>
              <option value="name">이름순</option>
            </select>
          </div>

          <!-- 결과 수 -->
          <div class="result-count">
            총 <strong>{{ totalCount }}</strong>개
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
            v-for="(destination, index) in destinations"
            :key="index"
            :destination="formatDestination(destination)"
            @click="handleCardClick(destination)"
          />
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination" v-if="totalPages > 1">
          <button
            class="page-btn"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            이전
          </button>

          <button
            v-for="page in displayedPages"
            :key="page"
            class="page-btn"
            :class="{ active: page === currentPage }"
            @click="changePage(page)"
          >
            {{ page }}
          </button>

          <button
            class="page-btn"
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
          >
            다음
          </button>
        </div>
      </div>
    </section>

    <FooterSection />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavigationBar from '@/components/common/NavigationBar.vue'
import FooterSection from '@/components/common/FooterSection.vue'
import TravelCard from '@/components/travel/TravelCard.vue'
import api from '@/services/api'

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
const selectedRegion = ref('')
const sortBy = ref('latest')

// 데이터 상태
const destinations = ref([])
const loading = ref(false)
const totalCount = ref(0)

// 페이지네이션 상태
const currentPage = ref(1)
const itemsPerPage = 20

const totalPages = computed(() => {
  return Math.ceil(totalCount.value / itemsPerPage)
})

const displayedPages = computed(() => {
  const pages = []
  const maxDisplayed = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxDisplayed / 2))
  let end = Math.min(totalPages.value, start + maxDisplayed - 1)

  if (end - start + 1 < maxDisplayed) {
    start = Math.max(1, end - maxDisplayed + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
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
        page: currentPage.value,
        size: itemsPerPage
      })
    } else {
      // 지역 기반 목록
      response = await api.getTravelSpotsFromAPI({
        area_code: selectedRegion.value,
        page: currentPage.value,
        size: itemsPerPage
      })
    }

    if (response.data) {
      destinations.value = response.data.results || []
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

const handleFilterChange = () => {
  currentPage.value = 1
  loadDestinations()
}

const handleSort = () => {
  // 정렬 로직 (클라이언트 사이드)
  if (sortBy.value === 'name') {
    destinations.value.sort((a, b) => (a.title || a.name).localeCompare(b.title || b.name))
  }
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadDestinations()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handleCardClick = (destination) => {
  console.log('Clicked destination:', destination)
  // 상세 페이지로 이동 로직 추가
}

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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  background: #667eea;
  border: none;
  color: white;
  cursor: pointer;
  transition: background 0.3s ease;
}

.search-btn:hover {
  background: #5568d3;
}

/* 필터 섹션 */
.filter-section {
  background: white;
  padding: 2rem;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filter-container {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  background: white;
  min-width: 150px;
  transition: all 0.2s ease;
}

.filter-select:hover {
  border-color: #9ca3af;
}

.filter-select:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
  border-color: #667eea;
}

.result-count {
  margin-left: auto;
  font-size: 1rem;
  color: #6b7280;
}

.result-count strong {
  color: #667eea;
  font-size: 1.25rem;
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
  border-top-color: #667eea;
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
  background: #667eea;
  color: white;
  border-color: #667eea;
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

  .filter-container {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select {
    min-width: 100%;
  }

  .result-count {
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
