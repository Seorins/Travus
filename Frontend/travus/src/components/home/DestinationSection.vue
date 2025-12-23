<template>
  <section
    class="ar-room-section"
    :class="{ 'hide-cursor': showCursor }"
    ref="sectionRef"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    @mousemove="handleMouseMove"
    @mousedown="handleMouseDown"
    tabindex="0"
  >
    <div class="ar-room-container">
      <div class="ar-room-header">
        <h2 class="ar-room-title">AR ROOM</h2>
        <p class="ar-room-subtitle">
          포스터가 내 방에 어울릴까?<br />
          AR ROOM에서 내 공간을 테스트 해보세요.
        </p>
      </div>

      <div class="carousel-track" ref="trackRef" :style="trackStyle">
        <div
          class="ar-card"
          v-for="(d, i) in destinations"
          :key="i"
        >
          <div
            class="card-thumbnail"
            :style="{ backgroundImage: `url(${d.image})` }"
          />
          <div class="card-info">
            <h3 class="card-title">{{ d.name }}</h3>
            <p class="card-description">{{ d.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 🔥 커스텀 커서는 body로 이동 -->
  <Teleport to="body">
    <div
      class="custom-cursor"
      :class="{ active: showCursor, dragging: isDragging }"
      :style="cursorStyle"
    >
      <span v-if="!isDragging">← DRAG →</span>
      <span v-else>RELEASE</span>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const sectionRef = ref(null)
const trackRef = ref(null)

const showCursor = ref(false)
const isDragging = ref(false)

const cursorX = ref(0)
const cursorY = ref(0)

const startX = ref(0)
const currentX = ref(0)
const scrollLeft = ref(0)
const velocity = ref(0)
const lastX = ref(0)
const lastTime = ref(0)

const destinations = ref([
  {
    name: '이 포스터 하나로 제가 원하던 공간이 완성되었어요 :)',
    description: 'AR ROOM으로 미리 확인해보세요',
    image: 'https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead'
  },
  {
    name: '우리 집 거실이 갤러리처럼 변했어요',
    description: 'AR ROOM 등록하기',
    image: 'https://images.unsplash.com/photo-1513519245088-0e12902e35ca'
  },
  {
    name: 'AR ROOM으로 완성한 나만의 공간',
    description: '내 공간에 어울리는 포스터 찾기',
    image: 'https://images.unsplash.com/photo-1615799999673-a1b6d6cb0b2f'
  },
  {
    name: '침실을 나만의 감성 공간으로',
    description: 'AR ROOM에서 먼저 체험하기',
    image: 'https://images.unsplash.com/photo-1596636604876-d4e4c34f4b47'
  },
  {
    name: '사무실에도 어울리는 포스터',
    description: '업무 공간 꾸미기',
    image: 'https://images.unsplash.com/photo-1582571183281-e2a73903c93a'
  },
  {
    name: '카페 같은 내 공간 만들기',
    description: 'AR로 미리 배치해보기',
    image: 'https://images.unsplash.com/photo-1513519245088-0e12902e35ca'
  },
  {
    name: '빈티지 감성으로 채우는 방',
    description: '나만의 갤러리 벽 완성',
    image: 'https://images.unsplash.com/photo-1615799998603-7c6270a45196'
  },
  {
    name: '모던한 공간의 완성',
    description: 'AR ROOM에서 확인하기',
    image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe'
  }
])

const trackStyle = computed(() => ({
  transform: `translateX(${currentX.value}px)`,
  transition: isDragging.value ? 'none' : 'transform 1.2s cubic-bezier(0.19, 1, 0.22, 1)'
}))

const cursorStyle = computed(() => ({
  left: `${cursorX.value}px`,
  top: `${cursorY.value}px`
}))

const handleMouseEnter = () => {
  showCursor.value = true
}

const handleMouseLeave = () => {
  showCursor.value = false
  isDragging.value = false
}

const handleMouseMove = (e) => {
  // 🔥 커서 딜레이 (고급 UX)
  cursorX.value += (e.clientX - 60 - cursorX.value) * 0.2
  cursorY.value += (e.clientY - 60 - cursorY.value) * 0.2

  if (!isDragging.value) return

  const now = Date.now()
  const dx = e.clientX - startX.value

  // 속도 계산 (관성 효과용)
  if (lastTime.value) {
    const dt = now - lastTime.value
    velocity.value = (e.clientX - lastX.value) / (dt || 1)
  }

  lastX.value = e.clientX
  lastTime.value = now

  // 스크롤 범위 제한
  const maxScroll = 0
  const minScroll = -(trackRef.value?.scrollWidth - window.innerWidth + 200) || -2000

  const newX = scrollLeft.value + dx
  currentX.value = Math.max(minScroll, Math.min(maxScroll, newX))
}

const handleMouseDown = (e) => {
  isDragging.value = true
  startX.value = e.clientX
  scrollLeft.value = currentX.value
  velocity.value = 0
  lastX.value = e.clientX
  lastTime.value = Date.now()
}

const handleMouseUp = () => {
  if (!isDragging.value) return
  isDragging.value = false

  // 🔥 관성 스크롤 효과
  const applyInertia = () => {
    if (Math.abs(velocity.value) < 0.1) {
      velocity.value = 0
      return
    }

    const maxScroll = 0
    const minScroll = -(trackRef.value?.scrollWidth - window.innerWidth + 200) || -2000

    currentX.value += velocity.value * 15
    currentX.value = Math.max(minScroll, Math.min(maxScroll, currentX.value))

    velocity.value *= 0.92 // 감속
    requestAnimationFrame(applyInertia)
  }

  if (Math.abs(velocity.value) > 0.5) {
    applyInertia()
  }
}

onMounted(() => {
  document.addEventListener('mouseup', handleMouseUp)
})

onUnmounted(() => {
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>


<style scoped>
.ar-room-section {
  min-height: 120vh;
  height: auto;
  background: #ffffff;
  padding: 8rem 0 10rem 0;
  position: relative;
  overflow: hidden;
  /* cursor: none !important; */
  display: flex;
  align-items: center;
}

.ar-room-section.hide-cursor,
.ar-room-section.hide-cursor * {
  cursor: none !important;
}

.ar-room-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.ar-room-container {
  max-width: 100%;
  position: relative;
}

/* 헤더 */
.ar-room-header {
  padding: 0 4rem;
  margin-bottom: 4rem;
  position: relative;
  z-index: 5;
}

.ar-room-title {
  font-size: 4rem;
  font-weight: 900;
  color: #394b9e;
  margin-bottom: 1rem;
  letter-spacing: -2px;
  text-transform: uppercase;
}

.ar-room-subtitle {
  font-size: 1.2rem;
  color: #000000;
  line-height: 1.8;
  font-weight: 300;
}

/* 캐러셀 트랙 */
.carousel-track {
  display: flex;
  gap: 4rem;
  padding: 0 4rem;
  will-change: transform;
  user-select: none;
}

/* AR 카드 */
.ar-card {
  flex-shrink: 0;
  width: 660px;
  background: #1a1a1a;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

.ar-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 30px 80px rgba(255, 106, 0, 0.3);
}

.ar-card:focus {
  outline: 4px solid #FF6A00;
  outline-offset: 6px;
  transform: translateY(-10px) scale(1.02);
}

/* 카드 썸네일 */
.card-thumbnail {
  width: 100%;
  height: 400px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.4) 100%
  );
}

/* 카드 정보 */
.card-info {
  padding: 2rem;
  background: #1a1a1a;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.card-description {
  font-size: 1rem;
  color: #FF6A00;
  font-weight: 500;
}

.ar-room-section.hide-cursor,
.ar-room-section.hide-cursor * {
  cursor: none !important;
}

.custom-cursor {
  position: fixed;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #ff6a00;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: transform 0.25s ease, background 0.25s ease;
  z-index: 9999;
}

.custom-cursor.active {
  opacity: 0.95;
  visibility: visible;
}

.custom-cursor.dragging {
  background: #fff;
  transform: scale(1.3) rotate(-5deg);
}

.custom-cursor span {
  font-weight: 700;
  letter-spacing: 1px;
  color: #000;
}


/* 반응형 */
@media (max-width: 1400px) {
  .ar-card {
    width: 560px;
  }

  .card-thumbnail {
    height: 420px;
  }
}

@media (max-width: 1024px) {
  .ar-room-title {
    font-size: 3rem;
  }

  .ar-card {
    width: 480px;
  }

  .card-thumbnail {
    height: 360px;
  }

  .carousel-track {
    gap: 2rem;
  }
}

@media (max-width: 768px) {
  .ar-room-section {
    cursor: auto;
  }

  .custom-cursor {
    display: none;
  }

  .ar-room-title {
    font-size: 2.5rem;
  }

  .ar-room-subtitle {
    font-size: 1rem;
  }

  .ar-card {
    width: 90vw;
  }

  .card-thumbnail {
    height: 300px;
  }

  .card-info {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.2rem;
  }
}
</style>
