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
        <p class="page-subtitle">전국의 다양한 여행지를 찾아보세요</p>

        <!-- 검색바 -->
        <div class="search-bar">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="여행지를 검색하세요..."
            @input="handleSearch"
            class="search-input"
          />
          <button class="search-btn">
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
              <option value="서울">서울</option>
              <option value="부산">부산</option>
              <option value="제주">제주</option>
              <option value="경기">경기</option>
              <option value="강원">강원</option>
              <option value="충북">충북</option>
              <option value="충남">충남</option>
              <option value="경북">경북</option>
              <option value="경남">경남</option>
              <option value="전북">전북</option>
              <option value="전남">전남</option>
            </select>
          </div>

          <!-- 카테고리 필터 -->
          <div class="filter-group">
            <label class="filter-label">카테고리</label>
            <select v-model="selectedCategory" @change="handleFilterChange" class="filter-select">
              <option value="">전체</option>
              <option value="beach">해변</option>
              <option value="mountain">산/등산</option>
              <option value="culture">문화유산</option>
              <option value="food">맛집</option>
              <option value="city">도시</option>
              <option value="nature">자연/힐링</option>
              <option value="island">섬</option>
              <option value="winter">겨울스포츠</option>
            </select>
          </div>

          <!-- 정렬 -->
          <div class="filter-group">
            <label class="filter-label">정렬</label>
            <select v-model="sortBy" @change="handleSort" class="filter-select">
              <option value="latest">최신순</option>
              <option value="popular">인기순</option>
              <option value="name">이름순</option>
            </select>
          </div>

          <!-- 결과 수 -->
          <div class="result-count">
            총 <strong>{{ filteredDestinations.length }}</strong>개
          </div>
        </div>
      </div>
    </section>

    <!-- 여행지 리스트 -->
    <section class="destinations-section">
      <div class="container">
        <div class="destinations-grid">
          <TravelCard
            v-for="(destination, index) in paginatedDestinations"
            :key="index"
            :destination="destination"
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

// Import images
import avatar1 from '@/assets/avatar1.png'
import avatar2 from '@/assets/avatar2.png'
import avatar3 from '@/assets/avatar3.png'
import mainImg from '@/assets/main.png'
import footImg from '@/assets/footimg.jpg'
import char3 from '@/assets/char3.png'
import topbtn from '@/assets/topbtn.png'

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
const selectedCategory = ref('')
const sortBy = ref('latest')

// 페이지네이션 상태
const currentPage = ref(1)
const itemsPerPage = 12

// 샘플 여행지 데이터
const destinations = ref([
  {
    id: 1,
    name: '부산 해운대',
    region: '부산',
    category: 'beach',
    image: mainImg,
    description: '아름다운 해변과 도시의 조화',
    tags: ['해변', '서핑', '야경'],
    rating: 4.8,
    reviews: 1234
  },
  {
    id: 2,
    name: '제주 한라산',
    region: '제주',
    category: 'mountain',
    image: avatar1,
    description: '제주도의 상징, 백록담이 있는 명산',
    tags: ['등산', '자연', '트레킹'],
    rating: 4.9,
    reviews: 2156
  },
  {
    id: 3,
    name: '경주 불국사',
    region: '경북',
    category: 'culture',
    image: avatar2,
    description: '신라 천년의 역사가 살아있는 곳',
    tags: ['문화재', '사찰', '역사'],
    rating: 4.7,
    reviews: 987
  },
  {
    id: 4,
    name: '전주 한옥마을',
    region: '전북',
    category: 'food',
    image: avatar3,
    description: '전통과 맛이 어우러진 곳',
    tags: ['한옥', '맛집', '전통'],
    rating: 4.6,
    reviews: 1567
  },
  {
    id: 5,
    name: '서울 경복궁',
    region: '서울',
    category: 'culture',
    image: char3,
    description: '조선왕조의 법궁',
    tags: ['궁궐', '역사', '문화'],
    rating: 4.8,
    reviews: 3421
  },
  {
    id: 6,
    name: '강릉 경포대',
    region: '강원',
    category: 'beach',
    image: topbtn,
    description: '동해안의 아름다운 해변',
    tags: ['해변', '일출', '카페'],
    rating: 4.5,
    reviews: 892
  },
  {
    id: 7,
    name: '설악산',
    region: '강원',
    category: 'mountain',
    image: footImg,
    description: '사계절 아름다운 명산',
    tags: ['등산', '단풍', '케이블카'],
    rating: 4.9,
    reviews: 2345
  },
  {
    id: 8,
    name: '여수 밤바다',
    region: '전남',
    category: 'city',
    image: mainImg,
    description: '낭만적인 해안도시',
    tags: ['야경', '맛집', '해변'],
    rating: 4.7,
    reviews: 1678
  }
])

// 필터링된 여행지
const filteredDestinations = computed(() => {
  let result = destinations.value

  // 검색어 필터
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(dest =>
      dest.name.toLowerCase().includes(query) ||
      dest.description.toLowerCase().includes(query) ||
      dest.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  // 지역 필터
  if (selectedRegion.value) {
    result = result.filter(dest => dest.region === selectedRegion.value)
  }

  // 카테고리 필터
  if (selectedCategory.value) {
    result = result.filter(dest => dest.category === selectedCategory.value)
  }

  // 정렬
  if (sortBy.value === 'popular') {
    result = [...result].sort((a, b) => b.rating - a.rating)
  } else if (sortBy.value === 'name') {
    result = [...result].sort((a, b) => a.name.localeCompare(b.name))
  }

  return result
})

// 페이지네이션
const totalPages = computed(() => {
  return Math.ceil(filteredDestinations.value.length / itemsPerPage)
})

const paginatedDestinations = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredDestinations.value.slice(start, end)
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

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleFilterChange = () => {
  currentPage.value = 1
}

const handleSort = () => {
  currentPage.value = 1
}

const handleCardClick = (destination) => {
  console.log('Clicked destination:', destination)
  // 상세 페이지로 이동 로직 추가
}

onMounted(() => {
  // 데이터 로딩 로직 추가 가능
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
