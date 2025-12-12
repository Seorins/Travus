<template>
  <section
    class="ar-room-section"
    ref="sectionRef"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    @mousemove="handleMouseMove"
    @mousedown="handleMouseDown"
    tabindex="0"
    @focus="handleFocus"
  >
    <div class="ar-room-container">
      <!-- 헤더 -->
      <div class="ar-room-header">
        <h2 class="ar-room-title">AR ROOM</h2>
        <p class="ar-room-subtitle">
          포스터가 내 방에 어울릴까?<br />
          AR ROOM에서 내 공간을 테스트 해보세요.
        </p>
      </div>

      <!-- 드래그 가능한 카드 캐러셀 -->
      <div class="carousel-track" ref="trackRef" :style="trackStyle">
        <!-- 카드 1 -->
        <div class="ar-card" :tabindex="0" @focus="handleCardFocus($event, destinations[0])">
          <div class="card-thumbnail" :style="{ backgroundImage: `url(${destinations[0].image})` }">
            <div class="card-overlay"></div>
          </div>
          <div class="card-info">
            <h3 class="card-title">{{ destinations[0].name }}</h3>
            <p class="card-description">{{ destinations[0].description }}</p>
          </div>
        </div>

        <!-- 카드 2 -->
        <div class="ar-card" :tabindex="0" @focus="handleCardFocus($event, destinations[1])">
          <div class="card-thumbnail" :style="{ backgroundImage: `url(${destinations[1].image})` }">
            <div class="card-overlay"></div>
          </div>
          <div class="card-info">
            <h3 class="card-title">{{ destinations[1].name }}</h3>
            <p class="card-description">{{ destinations[1].description }}</p>
          </div>
        </div>

        <!-- 카드 3 -->
        <div class="ar-card" :tabindex="0" @focus="handleCardFocus($event, destinations[2])">
          <div class="card-thumbnail" :style="{ backgroundImage: `url(${destinations[2].image})` }">
            <div class="card-overlay"></div>
          </div>
          <div class="card-info">
            <h3 class="card-title">{{ destinations[2].name }}</h3>
            <p class="card-description">{{ destinations[2].description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 커스텀 드래그 커서 -->
    <div
      class="custom-cursor"
      ref="cursorRef"
      :class="{ active: showCursor, dragging: isDragging }"
      :style="cursorStyle"
    >
      <span>{{ isDragging ? 'Dragging' : 'Drag' }}</span>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['focus'])

// Refs
const sectionRef = ref(null)
const trackRef = ref(null)
const cursorRef = ref(null)

// 상태
const showCursor = ref(false)
const isDragging = ref(false)
const currentX = ref(0)
const targetX = ref(0)
const startX = ref(0)
const scrollLeft = ref(0)

// 커서 위치
const cursorX = ref(0)
const cursorY = ref(0)

// 목업 데이터
const destinations = ref([
  {
    name: '이 포스터 하나로 제가 원하던 공간이 완성되었어요 :)',
    description: 'AR ROOM으로 미리 확인해보세요',
    image: 'https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?w=800&h=1000&fit=crop'
  },
  {
    name: '우리 집 거실이 갤러리처럼 변했어요',
    description: 'AR ROOM 등록하기',
    image: 'https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=800&h=1000&fit=crop'
  },
  {
    name: 'AR ROOM으로 완성한 나만의 공간',
    description: '내 공간에 어울리는 포스터 찾기',
    image: 'https://images.unsplash.com/photo-1615799999673-a1b6d6cb0b2f?w=800&h=1000&fit=crop'
  }
])

// Computed styles
const trackStyle = computed(() => ({
  transform: `translateX(${currentX.value}px)`,
  transition: isDragging.value ? 'none' : 'transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
}))

const cursorStyle = computed(() => ({
  transform: `translate(${cursorX.value}px, ${cursorY.value}px)`
}))

// 마우스 엔터
const handleMouseEnter = () => {
  showCursor.value = true
}

// 마우스 리브
const handleMouseLeave = () => {
  showCursor.value = false
  if (isDragging.value) {
    handleMouseUp()
  }
}

// 마우스 무브 (커서 따라가기)
const handleMouseMove = (e) => {
  if (!sectionRef.value) return

  // fixed position이므로 전체 화면 기준
  cursorX.value = e.clientX - 60 // 커서 중앙 정렬 (120px / 2)
  cursorY.value = e.clientY - 60

  if (isDragging.value) {
    const dx = e.clientX - startX.value
    targetX.value = scrollLeft.value + dx

    // 드래그 범위 제한
    const maxScroll = 0
    const minScroll = -(trackRef.value.scrollWidth - sectionRef.value.clientWidth) + 200

    targetX.value = Math.max(minScroll, Math.min(maxScroll, targetX.value))
    currentX.value = targetX.value
  }
}

// 마우스 다운 (드래그 시작)
const handleMouseDown = (e) => {
  isDragging.value = true
  startX.value = e.clientX
  scrollLeft.value = currentX.value

  if (sectionRef.value) {
    sectionRef.value.style.cursor = 'none'
  }
}

// 마우스 업 (드래그 종료 & 스냅)
const handleMouseUp = () => {
  if (!isDragging.value) return

  isDragging.value = false

  // 스냅 로직: 가장 가까운 카드로 스냅
  const cardWidth = 700 // 카드 너비 + 간격
  const snapIndex = Math.round(-currentX.value / cardWidth)
  const snapPosition = -snapIndex * cardWidth

  // 범위 제한
  const maxSnap = 0
  const minSnap = -(destinations.value.length - 1) * cardWidth

  targetX.value = Math.max(minSnap, Math.min(maxSnap, snapPosition))
  currentX.value = targetX.value
}

// 포커스 핸들러
const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}

const handleCardFocus = (event, dest) => {
  const text = `${dest.name}. ${dest.description}`
  emit('focus', text)
}

// 마운트
onMounted(() => {
  document.addEventListener('mouseup', handleMouseUp)
})

// 언마운트
onUnmounted(() => {
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>

<style scoped>
.ar-room-section {
  min-height: 100vh;
  background: #000000;
  padding: 4rem 0;
  position: relative;
  overflow: hidden;
  cursor: none !important;
}

.ar-room-section * {
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
  color: #FF6A00;
  margin-bottom: 1rem;
  letter-spacing: -2px;
  text-transform: uppercase;
}

.ar-room-subtitle {
  font-size: 1.2rem;
  color: #ffffff;
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

/* 커스텀 커서 */
.custom-cursor {
  position: fixed;
  width: 120px;
  height: 120px;
  background: #FF6A00;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 9999;
  opacity: 0;
  transition: opacity 0.2s ease;
  will-change: transform;
}

.custom-cursor.active {
  opacity: 0.95;
}

.custom-cursor.dragging {
  transform: scale(1.15);
  background: #ff8533;
  transition: transform 0.2s ease;
}

.custom-cursor span {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
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
