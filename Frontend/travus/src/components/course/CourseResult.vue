<template>
  <div class="course-result">
    <div class="result-container">
      <!-- 헤더 -->
      <div class="result-header">
        <h1 class="course-title">{{ courseData?.title || '맞춤 여행 코스' }}</h1>
        <div class="header-actions">
          <button class="btn-save">
            <span class="icon">💾</span>
            코스 저장하기
          </button>
          <button class="btn-restart" @click="$emit('restart')">
            <span class="icon">🔄</span>
            새로 만들기
          </button>
        </div>
      </div>

      <!-- 여행 요약 정보 -->
      <div class="trip-summary">
        <div class="summary-item">
          <span class="summary-label">지역</span>
          <span class="summary-value">{{ regionNames }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">기간</span>
          <span class="summary-value">{{ durationText }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">테마</span>
          <span class="summary-value">{{ themeNames }}</span>
        </div>
      </div>

      <!-- 지도 + 일정 -->
      <div class="content-grid">
        <!-- 지도 영역 -->
        <div class="map-section">
          <div class="map-container">
            <div id="map" class="map"></div>
          </div>

          <div class="map-legend">
            <div class="legend-item">
              <span class="legend-marker day1"></span>
              <span>1일차</span>
            </div>
            <div class="legend-item" v-if="courseData?.duration?.days >= 2">
              <span class="legend-marker day2"></span>
              <span>2일차</span>
            </div>
            <div class="legend-item" v-if="courseData?.duration?.days >= 3">
              <span class="legend-marker day3"></span>
              <span>3일차</span>
            </div>
          </div>
        </div>

        <!-- 일정 영역 -->
        <div class="itinerary-section">
          <h3 class="section-title">여행 일정</h3>

          <div class="days-list">
            <div
              v-for="(day, index) in sampleDays"
              :key="index"
              class="day-card"
            >
              <div class="day-header">
                <span class="day-badge" :class="`day${index + 1}`">
                  Day {{ index + 1 }}
                </span>
                <span class="day-date">{{ day.date }}</span>
              </div>

              <div class="places-list">
                <div
                  v-for="(place, placeIndex) in day.places"
                  :key="placeIndex"
                  class="place-item"
                >
                  <div class="place-number">{{ placeIndex + 1 }}</div>
                  <div class="place-info">
                    <div class="place-name">{{ place.name }}</div>
                    <div class="place-time">{{ place.time }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button class="btn-view-detail">
            상세 일정 보기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  courseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['restart'])

// 임시 샘플 데이터
const sampleDays = ref([
  {
    date: '2024.01.15 (월)',
    places: [
      { name: '경복궁', time: '09:00 - 11:00' },
      { name: '북촌 한옥마을', time: '11:30 - 13:00' },
      { name: '인사동', time: '14:00 - 16:00' },
      { name: '청계천', time: '16:30 - 18:00' }
    ]
  },
  {
    date: '2024.01.16 (화)',
    places: [
      { name: 'N서울타워', time: '10:00 - 12:00' },
      { name: '남산 한옥마을', time: '13:00 - 15:00' },
      { name: '명동', time: '15:30 - 18:00' }
    ]
  }
])

const regionNames = computed(() => {
  if (!props.courseData?.regions) return ''
  return props.courseData.regions.join(', ')
})

const durationText = computed(() => {
  const duration = props.courseData?.duration
  if (!duration) return ''
  return duration.name
})

const themeNames = computed(() => {
  if (!props.courseData?.themes) return ''
  const themeMap = {
    mountain: '산',
    sea: '바다',
    indoor: '실내여행지',
    activity: '액티비티',
    culture: '문화/역사',
    theme_park: '테마파크',
    cafe: '카페',
    market: '전통시장',
    festival: '축제'
  }
  return props.courseData.themes.map(t => themeMap[t] || t).join(', ')
})

onMounted(() => {
  // TODO: 카카오맵 API 초기화
  console.log('지도 초기화 예정')
})
</script>

<style scoped>
.course-result {
  width: 100%;
  min-height: 100vh;
  background: #f7fafc;
  padding: 100px 20px 40px;
}

.result-container {
  max-width: 1400px;
  margin: 0 auto;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.course-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn-save,
.btn-restart {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-save {
  background: #667eea;
  color: white;
}

.btn-save:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

.btn-restart {
  background: white;
  color: #4a5568;
  border: 2px solid #e2e8f0;
}

.btn-restart:hover {
  background: #f7fafc;
}

.trip-summary {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.summary-label {
  font-size: 0.875rem;
  color: #718096;
  font-weight: 500;
}

.summary-value {
  font-size: 1.125rem;
  color: #1a202c;
  font-weight: 600;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.map-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.map-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.map {
  width: 100%;
  height: 600px;
  background: linear-gradient(135deg, #E8F4F8 0%, #D4E7F5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #718096;
  font-size: 1.125rem;
}

.map::before {
  content: '🗺️ 지도가 표시됩니다';
}

.map-legend {
  display: flex;
  gap: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.legend-marker {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.legend-marker.day1 {
  background: #667eea;
}

.legend-marker.day2 {
  background: #764ba2;
}

.legend-marker.day3 {
  background: #f093fb;
}

.itinerary-section {
  display: flex;
  flex-direction: column;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
}

.days-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.days-list::-webkit-scrollbar {
  width: 6px;
}

.days-list::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 3px;
}

.days-list::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.days-list::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

.day-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.day-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f7fafc;
}

.day-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
}

.day-badge.day1 {
  background: #667eea;
}

.day-badge.day2 {
  background: #764ba2;
}

.day-badge.day3 {
  background: #f093fb;
}

.day-date {
  font-size: 0.875rem;
  color: #718096;
}

.places-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.place-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.place-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  border-radius: 50%;
  font-weight: 600;
  color: #667eea;
  flex-shrink: 0;
}

.place-info {
  flex: 1;
}

.place-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.25rem;
}

.place-time {
  font-size: 0.875rem;
  color: #718096;
}

.btn-view-detail {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-view-detail:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .map {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .result-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .course-title {
    font-size: 1.5rem;
  }

  .header-actions {
    width: 100%;
  }

  .btn-save,
  .btn-restart {
    flex: 1;
  }

  .trip-summary {
    flex-direction: column;
    gap: 1rem;
  }

  .days-list {
    max-height: none;
  }
}
</style>
