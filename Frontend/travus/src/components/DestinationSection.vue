<template>
  <section class="destination-section" tabindex="0" @focus="handleFocus">
    <div class="destination-container">
      <div class="destination-header">
        <p class="question-text">떠나고 싶은 여행지가 있나요?</p>
        <h2 class="main-title" data-text="What We Travel">What We Travel</h2>
      </div>

      <div class="destinations-grid">
        <!-- 첫 번째 줄 -->
        <div class="destination-row scroll-left">
          <div
            v-for="(dest, index) in firstRow"
            :key="`row1-${index}`"
            class="destination-item"
            :tabindex="0"
            @focus="handleItemFocus($event, dest)"
          >
            <span class="icon">{{ dest.icon }}</span>
            <span class="destination-name">{{ dest.name }}</span>
          </div>
          <!-- 복제본 -->
          <div
            v-for="(dest, index) in firstRow"
            :key="`row1-clone-${index}`"
            class="destination-item"
            aria-hidden="true"
          >
            <span class="icon">{{ dest.icon }}</span>
            <span class="destination-name">{{ dest.name }}</span>
          </div>
        </div>

        <!-- 두 번째 줄 -->
        <div class="destination-row scroll-right">
          <div
            v-for="(dest, index) in secondRow"
            :key="`row2-${index}`"
            class="destination-item"
            :tabindex="0"
            @focus="handleItemFocus($event, dest)"
          >
            <span class="icon">{{ dest.icon }}</span>
            <span class="destination-name">{{ dest.name }}</span>
          </div>
          <!-- 복제본 -->
          <div
            v-for="(dest, index) in secondRow"
            :key="`row2-clone-${index}`"
            class="destination-item"
            aria-hidden="true"
          >
            <span class="icon">{{ dest.icon }}</span>
            <span class="destination-name">{{ dest.name }}</span>
          </div>
        </div>

        <!-- 세 번째 줄 -->
        <div class="destination-row scroll-left">
          <div
            v-for="(dest, index) in thirdRow"
            :key="`row3-${index}`"
            class="destination-item"
            :tabindex="0"
            @focus="handleItemFocus($event, dest)"
          >
            <span class="icon">{{ dest.icon }}</span>
            <span class="destination-name">{{ dest.name }}</span>
          </div>
          <!-- 복제본 -->
          <div
            v-for="(dest, index) in thirdRow"
            :key="`row3-clone-${index}`"
            class="destination-item"
            aria-hidden="true"
          >
            <span class="icon">{{ dest.icon }}</span>
            <span class="destination-name">{{ dest.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['focus'])

// 여행지 데이터 (아이콘 + 이름)
const firstRow = ref([
  { name: '#AI 맞춤 CMS개발', icon: '⚙️' },
  { name: '#반응형홈페이지', icon: '📱' },
  { name: '#병원홈페이지', icon: '🛡️' },
  { name: '#마케팅운영', icon: '' },
  { name: '#웹 접근성', icon: '💻' },
  { name: '#CRM통합', icon: '' },
  { name: '#데이터 분석', icon: '📊' }
])

const secondRow = ref([
  { name: '#콘텐츠기획', icon: '' },
  { name: '#SNS콘텐츠', icon: '💡' },
  { name: '#기업홈페이지제작', icon: '' },
  { name: '#3D 모델링', icon: '' },
  { name: '#AI 챗봇', icon: '🤖' },
  { name: '#SEO 최적화', icon: '' }
])

const thirdRow = ref([
  { name: '#UI/UX디자인', icon: '' },
  { name: '#브랜딩', icon: '' },
  { name: '#반응형 웹', icon: '' },
  { name: '#모바일앱', icon: '📲' },
  { name: '#전자상거래', icon: '' },
  { name: '#클라우드', icon: '' }
])

const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}

const handleItemFocus = (event, dest) => {
  emit('focus', dest.name)
}
</script>

<style scoped>
.destination-section {
  height: 100vh;
  background: #1a1a1a;
  padding: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.destination-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.destination-container {
  max-width: 100%;
  width: 100%;
}

.destination-header {
  text-align: center;
  margin-bottom: 5rem;
  padding: 0 2rem;
}

.question-text {
  font-size: 1.2rem;
  color: #ff6b35;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.main-title {
  font-size: 5rem;
  font-weight: 900;
  color: #ff6b35;
  letter-spacing: -0.02em;
}

.destinations-grid {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.destination-row {
  display: flex;
  gap: 2rem;
  white-space: nowrap;
}

.scroll-left {
  animation: scrollLeft 40s linear infinite;
}

.scroll-right {
  animation: scrollRight 40s linear infinite;
}

.destination-row:hover {
  animation-play-state: paused;
}

.destination-item {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0 3rem;
  font-size: 2.2rem;
  font-weight: 600;
  color: #fff;
  transition: all 0.3s ease;
  flex-shrink: 0;
  cursor: pointer;
  background: transparent;
  border: none;
  border-right: 1px solid #333;
}

.destination-item:last-child {
  border-right: none;
}

.destination-item:hover {
  color: #ff6b35;
}

.destination-item:focus {
  outline: 2px solid #ffd700;
  outline-offset: 5px;
  color: #ff6b35;
}

.icon {
  font-size: 2.5rem;
}

.destination-name {
  font-weight: 600;
  white-space: nowrap;
}

@keyframes scrollLeft {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

@keyframes scrollRight {
  0% {
    transform: translateX(-50%);
  }
  100% {
    transform: translateX(0);
  }
}

@media (max-width: 1024px) {
  .main-title {
    font-size: 3.5rem;
  }

  .destination-item {
    font-size: 1.4rem;
    padding: 1.2rem 2rem;
  }

  .icon {
    font-size: 1.6rem;
  }
}

@media (max-width: 768px) {
  .question-text {
    font-size: 1rem;
  }

  .main-title {
    font-size: 2.5rem;
  }

  .destination-item {
    font-size: 1.1rem;
    padding: 1rem 1.5rem;
  }

  .icon {
    font-size: 1.3rem;
  }

  .destinations-grid {
    gap: 2rem;
  }
}
</style>
