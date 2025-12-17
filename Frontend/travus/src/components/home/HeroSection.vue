<template>
  <section class="hero-section" tabindex="0" @focus="handleFocus">
    <div class="hero-slider">
      <transition name="fade" mode="out-in">
        <div
          :key="currentSlide"
          class="hero-slide"
          :style="{ backgroundImage: `url(${slides[currentSlide].image})` }"
        >
          <div class="hero-overlay"></div>
          <div class="hero-content">
            <h2 class="hero-title" data-text="모두를 위한 여행, TravUs">
              {{ slides[currentSlide].title }}
            </h2>
            <p class="hero-subtitle">{{ slides[currentSlide].subtitle }}</p>
          </div>
        </div>
      </transition>
    </div>

    <!-- 슬라이드 인디케이터 -->
    <div class="slide-indicators">
      <button
        v-for="(slide, index) in slides"
        :key="index"
        class="indicator"
        :class="{ active: currentSlide === index }"
        @click="goToSlide(index)"
        :tabindex="0"
        @focus="handleFocus"
        :aria-label="`슬라이드 ${index + 1}로 이동`"
      ></button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['focus'])

// 목업 슬라이드 데이터
const slides = ref([
  {
    title: '모두를 위한 여행, TravUs',
    subtitle: '장애의 경계를 넘어서는 유연한 사고와 혁신적인 방식으로 무한한 가능성을 만들어요.',
    image: 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1920&h=1080&fit=crop'
  },
  {
    title: '접근 가능한 여행의 시작',
    subtitle: '모든 사람이 평등하게 여행을 즐길 수 있는 세상을 만듭니다.',
    image: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1920&h=1080&fit=crop'
  },
  {
    title: 'AI와 함께하는 스마트 여행',
    subtitle: '인공지능 기술로 더욱 편리하고 안전한 여행을 제공합니다.',
    image: 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1920&h=1080&fit=crop'
  }
])

const currentSlide = ref(0)
let slideInterval = null

const goToSlide = (index) => {
  currentSlide.value = index
}

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.value.length
}

const handleFocus = (event) => {
  const text =
    event.target.getAttribute('data-text') ||
    event.target.innerText ||
    event.target.getAttribute('aria-label')
  emit('focus', text)
}

onMounted(() => {
  // 자동 슬라이드 (5초마다)
  slideInterval = setInterval(nextSlide, 5000)
})

onUnmounted(() => {
  if (slideInterval) {
    clearInterval(slideInterval)
  }
})
</script>

<style scoped>
.hero-section {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.hero-slider {
  width: 100%;
  height: 100%;
}

.hero-slide {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7); /* 단색 오버레이 */
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  padding: 2rem;
  max-width: 1200px;
  animation: fadeInUp 1s ease-out;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  line-height: 1.6;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
  opacity: 0.95;
}

.slide-indicators {
  position: absolute;
  bottom: 3rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 1rem;
  z-index: 10;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: 2px solid white;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.indicator:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.2);
}

.indicator:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
}

.indicator.active {
  background: white;
  width: 40px;
  border-radius: 6px;
}

/* 페이드 트랜지션 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 애니메이션 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .slide-indicators {
    bottom: 2rem;
  }
}
</style>
