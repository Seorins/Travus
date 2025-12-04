<template>
  <section class="destination-section" tabindex="0" @focus="handleFocus">
    <div class="destination-container">
      <div class="destination-header">
        <h2 class="section-title" data-text="추천 여행지">추천 여행지</h2>
        <p class="section-subtitle">Recommended Destinations</p>
      </div>

      <div class="destinations-grid">
        <!-- 첫 번째 줄: 왼쪽으로 흐름 -->
        <div class="destination-row" data-direction="left">
          <div
            v-for="(dest, index) in firstRow"
            :key="`row1-${index}`"
            class="destination-card"
            :tabindex="0"
            @focus="handleCardFocus($event, dest)"
          >
            <div class="card-image" :style="{ backgroundImage: `url(${dest.image})` }">
              <div class="card-overlay"></div>
              <div class="card-badge">{{ dest.badge }}</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ dest.name }}</h3>
              <p class="card-description">{{ dest.description }}</p>
              <div class="card-tags">
                <span v-for="(tag, tIndex) in dest.tags" :key="tIndex" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          <!-- 복제본 (무한 스크롤 효과) -->
          <div
            v-for="(dest, index) in firstRow"
            :key="`row1-clone-${index}`"
            class="destination-card"
            aria-hidden="true"
          >
            <div class="card-image" :style="{ backgroundImage: `url(${dest.image})` }">
              <div class="card-overlay"></div>
              <div class="card-badge">{{ dest.badge }}</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ dest.name }}</h3>
              <p class="card-description">{{ dest.description }}</p>
              <div class="card-tags">
                <span v-for="(tag, tIndex) in dest.tags" :key="tIndex" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 두 번째 줄: 오른쪽으로 흐름 -->
        <div class="destination-row" data-direction="right">
          <div
            v-for="(dest, index) in secondRow"
            :key="`row2-${index}`"
            class="destination-card"
            :tabindex="0"
            @focus="handleCardFocus($event, dest)"
          >
            <div class="card-image" :style="{ backgroundImage: `url(${dest.image})` }">
              <div class="card-overlay"></div>
              <div class="card-badge">{{ dest.badge }}</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ dest.name }}</h3>
              <p class="card-description">{{ dest.description }}</p>
              <div class="card-tags">
                <span v-for="(tag, tIndex) in dest.tags" :key="tIndex" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          <!-- 복제본 -->
          <div
            v-for="(dest, index) in secondRow"
            :key="`row2-clone-${index}`"
            class="destination-card"
            aria-hidden="true"
          >
            <div class="card-image" :style="{ backgroundImage: `url(${dest.image})` }">
              <div class="card-overlay"></div>
              <div class="card-badge">{{ dest.badge }}</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ dest.name }}</h3>
              <p class="card-description">{{ dest.description }}</p>
              <div class="card-tags">
                <span v-for="(tag, tIndex) in dest.tags" :key="tIndex" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 세 번째 줄: 왼쪽으로 흐름 -->
        <div class="destination-row" data-direction="left">
          <div
            v-for="(dest, index) in thirdRow"
            :key="`row3-${index}`"
            class="destination-card"
            :tabindex="0"
            @focus="handleCardFocus($event, dest)"
          >
            <div class="card-image" :style="{ backgroundImage: `url(${dest.image})` }">
              <div class="card-overlay"></div>
              <div class="card-badge">{{ dest.badge }}</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ dest.name }}</h3>
              <p class="card-description">{{ dest.description }}</p>
              <div class="card-tags">
                <span v-for="(tag, tIndex) in dest.tags" :key="tIndex" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          <!-- 복제본 -->
          <div
            v-for="(dest, index) in thirdRow"
            :key="`row3-clone-${index}`"
            class="destination-card"
            aria-hidden="true"
          >
            <div class="card-image" :style="{ backgroundImage: `url(${dest.image})` }">
              <div class="card-overlay"></div>
              <div class="card-badge">{{ dest.badge }}</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ dest.name }}</h3>
              <p class="card-description">{{ dest.description }}</p>
              <div class="card-tags">
                <span v-for="(tag, tIndex) in dest.tags" :key="tIndex" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['focus'])

// 목업 여행지 데이터
const firstRow = ref([
  {
    name: '경복궁',
    description: '조선시대의 정궁으로 한국의 역사와 문화를 체험할 수 있습니다.',
    image: 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=600&h=400&fit=crop',
    badge: '서울',
    tags: ['휠체어 접근', '음성 안내', '무료 입장']
  },
  {
    name: '제주 한라산',
    description: '아름다운 자연경관과 다양한 등산 코스를 제공합니다.',
    image: 'https://images.unsplash.com/photo-1599899315207-e6d8d67e0ee0?w=600&h=400&fit=crop',
    badge: '제주',
    tags: ['자연', '트레킹', '전망대']
  },
  {
    name: '부산 해운대',
    description: '국내 최대 해수욕장으로 다양한 편의시설을 갖추고 있습니다.',
    image: 'https://images.unsplash.com/photo-1538485399081-7191377e8241?w=600&h=400&fit=crop',
    badge: '부산',
    tags: ['해변', '접근성 우수', '휠체어 대여']
  }
])

const secondRow = ref([
  {
    name: '강릉 정동진',
    description: '동해의 일출을 감상할 수 있는 아름다운 해변입니다.',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&h=400&fit=crop',
    badge: '강릉',
    tags: ['일출', '기차역', '포토존']
  },
  {
    name: '전주 한옥마을',
    description: '전통 한옥과 맛있는 음식을 경험할 수 있습니다.',
    image: 'https://images.unsplash.com/photo-1578193661550-3d84b4e0d3b6?w=600&h=400&fit=crop',
    badge: '전주',
    tags: ['문화체험', '전통음식', '접근성']
  },
  {
    name: '속초 설악산',
    description: '웅장한 산세와 계절마다 다른 아름다움을 자랑합니다.',
    image: 'https://images.unsplash.com/photo-1516380544158-a3d1e62a1f9c?w=600&h=400&fit=crop',
    badge: '속초',
    tags: ['국립공원', '케이블카', '단풍']
  }
])

const thirdRow = ref([
  {
    name: '경주 불국사',
    description: '유네스코 세계문화유산으로 지정된 천년 고찰입니다.',
    image: 'https://images.unsplash.com/photo-1516799315-7ea247f58c51?w=600&h=400&fit=crop',
    badge: '경주',
    tags: ['문화재', '사찰', '역사']
  },
  {
    name: '여수 오동도',
    description: '동백꽃과 아름다운 바다 풍경을 즐길 수 있습니다.',
    image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&h=400&fit=crop',
    badge: '여수',
    tags: ['섬', '산책로', '야경']
  },
  {
    name: '인천 차이나타운',
    description: '이국적인 분위기와 맛있는 중화요리를 경험할 수 있습니다.',
    image: 'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=600&h=400&fit=crop',
    badge: '인천',
    tags: ['문화거리', '음식', '관광명소']
  }
])

const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}

const handleCardFocus = (event, dest) => {
  const text = `${dest.name}. ${dest.description}. ${dest.tags.join(', ')}`
  emit('focus', text)
}
</script>

<style scoped>
.destination-section {
  min-height: 100vh;
  background: #2d3748; /* 진한 회색 단색 */
  padding: 6rem 0;
  overflow: hidden;
}

.destination-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.destination-container {
  max-width: 100%;
}

.destination-header {
  text-align: center;
  margin-bottom: 4rem;
  color: white;
  padding: 0 2rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  opacity: 0.8;
}

.destinations-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.destination-row {
  display: flex;
  gap: 2rem;
  padding: 0 2rem;
}

.destination-row[data-direction='left'] {
  animation: scrollLeft 40s linear infinite;
}

.destination-row[data-direction='right'] {
  animation: scrollRight 40s linear infinite;
}

.destination-row:hover {
  animation-play-state: paused;
}

.destination-card {
  min-width: 400px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.destination-card:hover {
  transform: translateY(-10px);
}

.destination-card:focus {
  outline: 4px solid #ffd700;
  outline-offset: 4px;
  transform: translateY(-10px) scale(1.02);
}

.card-image {
  width: 100%;
  height: 250px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2); /* 단색 오버레이 */
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.95);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.card-content {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.75rem;
}

.card-description {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #667eea; /* 보라색 단색 */
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
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

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }

  .section-subtitle {
    font-size: 1.2rem;
  }

  .destination-card {
    min-width: 300px;
  }

  .card-image {
    height: 200px;
  }
}
</style>
