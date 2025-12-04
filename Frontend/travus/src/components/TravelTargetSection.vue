<template>
  <section class="target-section" tabindex="0" @focus="handleFocus">
    <div class="target-container">
      <div class="target-header">
        <h2 class="section-title" data-text="누구를 위한 서비스인가요?">
          Creative Service
        </h2>
        <button class="service-btn">무엇 대해가?</button>
      </div>

      <div class="main-content-area">
        <h3 class="main-text">
          생각의 경계를 넘어서는<br />
          유연한 사고와 혁신적인 방식으로<br />
          무한한 가능성을 만들어요.
        </h3>

        <div class="character-icon-main">🤖</div>
      </div>

      <!-- 카드 슬라이더 (3개 동시 표시) -->
      <div class="cards-slider-wrapper">
        <div class="cards-display">
          <!-- 왼쪽 카드 -->
          <div
            v-if="currentIndex > 0"
            class="card-item card-left"
            :tabindex="0"
            @focus="handleCardFocus($event, cards[currentIndex - 1])"
          >
            <div class="card-header">
              <h4>{{ cards[currentIndex - 1].category }}</h4>
              <h3>{{ cards[currentIndex - 1].title }}</h3>
            </div>
            <ul class="card-list">
              <li v-for="(item, idx) in cards[currentIndex - 1].items" :key="idx">{{ item }}</li>
            </ul>
            <div class="card-shape" :style="{ background: cards[currentIndex - 1].color }"></div>
          </div>

          <!-- 중앙 카드 (활성) -->
          <div
            class="card-item card-center active"
            :tabindex="0"
            @focus="handleCardFocus($event, cards[currentIndex])"
          >
            <div class="card-header">
              <h4>{{ cards[currentIndex].category }}</h4>
              <h3>{{ cards[currentIndex].title }}</h3>
            </div>
            <ul class="card-list">
              <li v-for="(item, idx) in cards[currentIndex].items" :key="idx">{{ item }}</li>
            </ul>
            <div class="card-shape" :style="{ background: cards[currentIndex].color }"></div>
          </div>

          <!-- 오른쪽 카드 -->
          <div
            v-if="currentIndex < cards.length - 1"
            class="card-item card-right"
            :tabindex="0"
            @focus="handleCardFocus($event, cards[currentIndex + 1])"
          >
            <div class="card-header">
              <h4>{{ cards[currentIndex + 1].category }}</h4>
              <h3>{{ cards[currentIndex + 1].title }}</h3>
            </div>
            <ul class="card-list">
              <li v-for="(item, idx) in cards[currentIndex + 1].items" :key="idx">{{ item }}</li>
            </ul>
            <div class="card-shape" :style="{ background: cards[currentIndex + 1].color }"></div>
          </div>
        </div>
      </div>

      <!-- 인디케이터 (네비게이션 제거) -->
      <div class="slider-nav">
        <div class="indicators">
          <span
            v-for="(card, index) in cards"
            :key="index"
            class="dot"
            :class="{ active: currentIndex === index }"
          ></span>
        </div>
      </div>

      <p class="scroll-hint">스크롤해서 카드를 넘겨보세요 ↓</p>

      <div class="character-bottom">
        <div class="character-icon">🐯</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const emit = defineEmits(['focus'])

const cards = ref([
  {
    category: 'UX/UI 디자인 및 개발',
    title: '브랜드 앤 아이덴터티 디자인',
    items: ['브랜드 관리', '디자인 가이드 제작', 'Visual Identity', 'UX Design', 'Brand Guidelines', 'Naming & Storytelling'],
    color: '#a8e6cf'
  },
  {
    category: 'UI/UX 디자인',
    title: 'UI/UX 디자인',
    items: ['인재형 솔루션', '비즈니 솔루션', 'Interaction Design', 'Visual Design', '서포트 디자인', '코드핀 디자인'],
    color: '#ffd3a5'
  },
  {
    category: '유성 크레딧 및 마켓금',
    title: '유성 크레딧 및 마켓금 콘텐츠',
    items: ['감각 체형 부문의 대조의', '추집 레디어(창창)', 'Newsletter', 'SEO/AI Creative Graphics', 'Visual Identity', 'HTML/CSS 법플의', 'UI/UX 초점', 'web Analytics'],
    color: '#a1c4fd'
  },
  {
    category: '디지털 마케팅 및 캠페인',
    title: '디지털 마케팅 및 캠페인',
    items: ['감정 체형 부문의 대조의', '추집 레디어 잠금가2', 'Newsletter', 'web Analytics', 'SEO/AI Creative Graphics', 'HTML/CSS 법플의'],
    color: '#fbc2eb'
  }
])

const currentIndex = ref(0)
const sliderRef = ref(null)

const handleFocus = (event) => {
  const text = event.target.innerText || event.target.getAttribute('aria-label')
  emit('focus', text)
}

const handleCardFocus = (event, card) => {
  const text = `${card.title}. ${card.items.join(', ')}`
  emit('focus', text)
}

onMounted(() => {
  const section = document.querySelector('.target-section')

  if (!section) return

  const totalCards = cards.value.length
  // 각 카드마다 100vh씩 스크롤
  const scrollDistance = window.innerHeight * totalCards

  ScrollTrigger.create({
    trigger: section,
    start: 'top top',
    end: `+=${scrollDistance}`,
    pin: true,
    pinSpacing: false, // 공백 제거
    scrub: 1,
    anticipatePin: 1,
    onUpdate: (self) => {
      const progress = self.progress
      // 현재 카드 인덱스 (0, 1, 2, 3)
      const newIndex = Math.min(totalCards - 1, Math.floor(progress * totalCards))
      currentIndex.value = newIndex
    }
  })
})

onUnmounted(() => {
  ScrollTrigger.getAll().forEach((trigger) => trigger.kill())
})
</script>

<style scoped>
.target-section {
  width: 100%;
  height: 100vh;
  background: #ff6b35;
  padding: 4rem 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.target-container {
  max-width: 1400px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.target-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  color: white;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.service-btn {
  background: white;
  color: #ff6b35;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.service-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.main-content-area {
  text-align: center;
  margin-bottom: 4rem;
  position: relative;
}

.main-text {
  font-size: 2.2rem;
  font-weight: 700;
  color: white;
  line-height: 1.5;
  margin-bottom: 2rem;
}

.character-icon-main {
  font-size: 8rem;
  filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
  animation: float 3s ease-in-out infinite;
}

/* 카드 슬라이더 */
.cards-slider-wrapper {
  width: 100%;
  margin-bottom: 3rem;
  padding: 2rem 0;
  perspective: 1500px;
}

.cards-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  position: relative;
  height: 500px;
}

.card-item {
  width: 400px;
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  overflow: hidden;
}

/* 왼쪽 카드 */
.card-left {
  left: 10%;
  opacity: 0.6;
  transform: translateX(-100px) rotateY(15deg) scale(0.85);
  z-index: 1;
}

/* 중앙 카드 (활성) */
.card-center {
  left: 50%;
  transform: translateX(-50%) rotateY(0deg) scale(1);
  opacity: 1;
  z-index: 3;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* 오른쪽 카드 */
.card-right {
  right: 10%;
  opacity: 0.6;
  transform: translateX(100px) rotateY(-15deg) scale(0.85);
  z-index: 1;
}

.card-item:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
}

.card-header {
  margin-bottom: 2rem;
}

.card-header h4 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.card-header h3 {
  font-size: 1.6rem;
  color: #2d3748;
  font-weight: 700;
  margin: 0;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;
  position: relative;
  z-index: 2;
}

.card-list li {
  padding: 0.6rem 0;
  color: #4a5568;
  font-size: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-list li:last-child {
  border-bottom: none;
}

.card-shape {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  opacity: 0.3;
  z-index: 1;
}

/* 네비게이션 */
.slider-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.indicators {
  display: flex;
  gap: 0.8rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot:hover {
  background: rgba(255, 255, 255, 0.8);
}

.dot.active {
  background: white;
  width: 35px;
  border-radius: 6px;
}

.character-bottom {
  text-align: center;
}

.character-icon {
  font-size: 4rem;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.3));
}

.scroll-hint {
  text-align: center;
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  margin-top: 2rem;
  opacity: 0.8;
  animation: bounce 2s infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.8rem;
  }

  .main-text {
    font-size: 1.5rem;
  }

  .character-icon-main {
    font-size: 5rem;
  }

  .cards-track {
    padding: 0 1rem;
  }

  .card-item {
    min-width: 300px;
  }
}
</style>
