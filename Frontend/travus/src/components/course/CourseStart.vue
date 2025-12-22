<template>
  <div class="course-start">
    <!-- 히어로 섹션 -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="text-section">
          <h1 class="hero-title">
            <span class="highlight-ai">AI</span><span class="highlight-text">코스</span> 플래너
          </h1>
          <p class="hero-subtitle">
            당신이 원하는 여행의 시작<br>
            1분이면 끝! 나만을 위한 여행 코스 추천
          </p>
          <div class="button-group">
            <button class="btn-primary" @click="$emit('next')">
              코스만들기
              <span class="arrow">→</span>
            </button>
          </div>
        </div>

        <div class="illustration-section">
          <img src="@/assets/course3.png" alt="AI 플래너 지도" class="map-image" />
        </div>
      </div>
    </div>

    <!-- 카테고리 탭 (히어로 위에 겹침) -->
    <div class="category-tabs-wrapper">
      <div class="category-tabs">
        <button
          v-for="category in categories"
          :key="category.id"
          class="tab-btn"
          :class="{ active: selectedCategory === category.id }"
          @click="selectedCategory = category.id"
        >
          <span class="tab-icon">{{ category.icon }}</span>
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- Best 30 섹션 -->
    <div class="best30-section">
      <div class="container">

        <!-- 섹션 제목 -->
        <div class="section-header">
          <h2 class="section-title">월간 Best 30</h2>
          <button class="info-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path d="M12 16v-4M12 8h.01" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <!-- 카드 그리드 -->
        <div class="cards-grid">
          <div
            v-for="item in bestItems"
            :key="item.id"
            class="destination-card"
          >
            <div class="card-image">
              <img :src="item.image" :alt="item.name" />
              <button class="accessibility-badge" v-if="item.accessible">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
              </button>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ item.name }}</h3>
              <p class="card-location">{{ item.location }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['next'])

const selectedCategory = ref('my-course')

const categories = [
  { id: 'my-course', name: '나의 여행코스' },
  { id: 'best30', name: '월간Best30' },
  { id: 'regional', name: '지역별 사용자코스' }
]

const bestItems = [
  {
    id: 1,
    name: '소수서원',
    location: '경상북도 영주시',
    image: 'https://via.placeholder.com/400x300',
    accessible: true
  },
  {
    id: 2,
    name: '대진등대',
    location: '강원도 속초시',
    image: 'https://via.placeholder.com/400x300',
    accessible: false
  },
  {
    id: 3,
    name: '대구미술관',
    location: '대구광역시',
    image: 'https://via.placeholder.com/400x300',
    accessible: true
  },
  {
    id: 4,
    name: '청량산',
    location: '경상북도 봉화군',
    image: 'https://via.placeholder.com/400x300',
    accessible: true
  }
]
</script>

<style scoped>
.course-start {
  width: 100%;
  /* background: #5b6fc7; */
}

/* 히어로 섹션 */
.hero-section {
  background: url('@/assets/background.gif') center center / cover no-repeat;
  padding: 140px 2rem 100px;
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  /* background: rgba(91, 111, 199, 0.7); */
  pointer-events: none;
}

.hero-content {
  max-width: 1400px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.text-section {
  color: white;
  padding-left: 4rem;
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 2rem 0;
  letter-spacing: -2px;
}

.highlight-ai {
  color: #00ff88;
  font-style: italic;
}

.highlight-text {
  color: white;
}

.hero-subtitle {
  font-size: 1.5rem;
  line-height: 1.8;
  margin: 0 0 3rem 0;
  opacity: 0.95;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.95);
}

.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}

.btn-primary {
  padding: 1.25rem 3rem;
  font-size: 1.25rem;
  font-weight: 600;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: #4158D0;
  color: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
  background: #3549b8;
}

.arrow {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.btn-primary:hover .arrow {
  transform: translateX(4px);
}

.partner-logos {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  opacity: 0.9;
}

.partner-text {
  font-size: 0.875rem;
  color: white;
  font-weight: 400;
}

.separator {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}

.illustration-section {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  perspective: 1200px;
}

.map-image {
  width: 100%;
  max-width: 800px;
  height: auto;
  display: block;
  filter: drop-shadow(0 20px 60px rgba(0, 0, 0, 0.3));
  margin-top: -150px;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotateY(-5deg);
  }
  50% {
    transform: translateY(-20px) rotateY(5deg);
  }
}

/* 반응형 */
@media (max-width: 1200px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 4rem;
  }

  .illustration-section {
    justify-content: center;
    order: -1;
  }

  .button-group {
    justify-content: center;
  }

  .partner-logos {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 120px 1.5rem 80px;
    min-height: auto;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.125rem;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
    padding: 1rem 2rem;
    font-size: 1.125rem;
  }

  .map-image {
    max-width: 100%;
  }

  .partner-logos {
    font-size: 0.75rem;
  }

  .partner-text {
    font-size: 0.75rem;
  }
}

/* 카테고리 탭 래퍼 (겹침 효과) */
.category-tabs-wrapper {
  position: relative;
  margin-top: -60px;
  z-index: 10;
  padding: 0 2rem;
}

/* 카테고리 탭 */
.category-tabs {
  display: flex;
  justify-content: center;
  gap: 0;
  background: #2c3e7a;
  border-radius: 3px;
  padding: 0.5rem;
  max-width: 1200px;
  margin: 0 auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* Best 30 섹션 */
.best30-section {
  background: #f8f9fa;
  padding: 5rem 0 4rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 3px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.tab-btn.active {
  background: white;
  color: #2c3e7a;
}

.tab-icon {
  font-size: 1.25rem;
}

/* 섹션 헤더 */
.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.info-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e2e8f0;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  color: #4a5568;
  transition: all 0.2s ease;
}

.info-btn:hover {
  background: #cbd5e0;
}

/* 카드 그리드 */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.destination-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.destination-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.destination-card:hover .card-image img {
  transform: scale(1.1);
}

.accessibility-badge {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
}

.accessibility-badge:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

.card-content {
  padding: 1.25rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.card-location {
  font-size: 0.875rem;
  color: #718096;
  margin: 0;
}

/* Best 30 반응형 */
@media (max-width: 1200px) {
  .cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .category-tabs-wrapper {
    margin-top: -40px;
  }

  .best30-section {
    padding: 4rem 0 3rem;
  }

  .category-tabs {
    flex-direction: column;
    max-width: 100%;
  }

  .tab-btn {
    padding: 0.875rem;
  }

  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
