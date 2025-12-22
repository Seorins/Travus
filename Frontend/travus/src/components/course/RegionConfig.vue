<template>
  <div class="region-config">
    <div class="content-card">
      <div class="card-content">
        <div class="text-section">
          <h2 class="title">지역 구성을 선택해주세요</h2>
          <p class="subtitle">2박 3일 여행의 지역 구성을 선택하세요.</p>

          <div class="config-options">
            <button
              class="config-card"
              :class="{ selected: selectedConfig === 1 }"
              @click="selectConfig(1)"
            >
              <div class="config-icon">
                <svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
                  <rect x="10" y="10" width="100" height="60" rx="8" fill="#667eea" opacity="0.2" stroke="#667eea" stroke-width="2"/>
                  <text x="60" y="45" text-anchor="middle" font-size="24" font-weight="bold" fill="#667eea">1</text>
                </svg>
              </div>
              <div class="config-name">한 지역 집중</div>
              <div class="config-desc">
                선택한 지역 중 하나를<br>
                깊이 있게 여행해요
              </div>
            </button>

            <button
              class="config-card"
              :class="{ selected: selectedConfig === 2 }"
              @click="selectConfig(2)"
            >
              <div class="config-icon">
                <svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
                  <rect x="10" y="10" width="45" height="60" rx="8" fill="#667eea" opacity="0.2" stroke="#667eea" stroke-width="2"/>
                  <rect x="65" y="10" width="45" height="60" rx="8" fill="#764ba2" opacity="0.2" stroke="#764ba2" stroke-width="2"/>
                  <text x="32.5" y="45" text-anchor="middle" font-size="20" font-weight="bold" fill="#667eea">1</text>
                  <text x="87.5" y="45" text-anchor="middle" font-size="20" font-weight="bold" fill="#764ba2">2</text>
                </svg>
              </div>
              <div class="config-name">두 지역 조합</div>
              <div class="config-desc">
                선택한 지역 중 두 곳을<br>
                함께 여행해요
              </div>
            </button>
          </div>

          <p class="hint">
            💡 지역 간 이동 시간을 고려하여 추천드려요.
          </p>

          <div class="button-group">
            <button class="btn-back" @click="$emit('back')">
              이전
            </button>
            <button
              class="btn-next"
              :disabled="selectedConfig === null"
              @click="handleNext"
            >
              다음
            </button>
          </div>
        </div>

        <div class="illustration-section">
          <div class="map-illustration">
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <!-- 지도 배경 -->
              <rect width="200" height="200" rx="12" fill="#E8F4F8"/>

              <!-- 경로 -->
              <path d="M 50 100 L 100 60 L 150 100" stroke="#667eea" stroke-width="4" fill="none" stroke-dasharray="5,5" opacity="0.5"/>

              <!-- 위치 마커 1 -->
              <g transform="translate(50, 100)">
                <circle r="20" fill="#667eea" opacity="0.2"/>
                <circle r="12" fill="#667eea"/>
                <circle r="6" fill="white"/>
              </g>

              <!-- 위치 마커 2 -->
              <g transform="translate(100, 60)">
                <circle r="20" fill="#764ba2" opacity="0.2"/>
                <circle r="12" fill="#764ba2"/>
                <circle r="6" fill="white"/>
              </g>

              <!-- 위치 마커 3 -->
              <g transform="translate(150, 100)">
                <circle r="20" fill="#667eea" opacity="0.2"/>
                <circle r="12" fill="#667eea"/>
                <circle r="6" fill="white"/>
              </g>

              <!-- 자동차 아이콘 -->
              <g transform="translate(120, 80)">
                <rect x="-15" y="-8" width="30" height="16" rx="4" fill="white" stroke="#667eea" stroke-width="2"/>
                <rect x="-10" y="-12" width="12" height="8" rx="2" fill="white" stroke="#667eea" stroke-width="2"/>
                <circle cx="-8" cy="8" r="4" fill="#4a5568"/>
                <circle cx="8" cy="8" r="4" fill="#4a5568"/>
              </g>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next', 'back'])

const selectedConfig = ref(null)

const selectConfig = (value) => {
  selectedConfig.value = value
}

const handleNext = () => {
  if (selectedConfig.value !== null) {
    emit('next', selectedConfig.value)
  }
}
</script>

<style scoped>
.region-config {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #E8F4F8 0%, #D4E7F5 100%);
  padding: 100px 20px 40px;
}

.content-card {
  width: 100%;
  max-width: 1200px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
}

.card-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  align-items: center;
}

.text-section {
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  font-size: 1.125rem;
  color: #718096;
  margin: 0 0 2rem 0;
}

.config-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.config-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.5rem;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.config-card:hover {
  border-color: #667eea;
  background: #f7fafc;
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.config-card.selected {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  border-color: #667eea;
  border-width: 3px;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
}

.config-icon {
  margin-bottom: 1.5rem;
  width: 120px;
  height: 80px;
}

.config-icon svg {
  width: 100%;
  height: 100%;
}

.config-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 0.75rem;
}

.config-desc {
  font-size: 0.875rem;
  color: #718096;
  line-height: 1.6;
}

.hint {
  font-size: 0.875rem;
  color: #667eea;
  margin: 0 0 2rem 0;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.btn-back,
.btn-next {
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back {
  background: #f7fafc;
  color: #4a5568;
  border: 2px solid #e2e8f0;
}

.btn-back:hover {
  background: #edf2f7;
}

.btn-next {
  flex: 1;
  background: #667eea;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-next:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-next:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  box-shadow: none;
}

.illustration-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-illustration {
  width: 100%;
  max-width: 200px;
}

.map-illustration svg {
  width: 100%;
  height: auto;
  border-radius: 12px;
}

@media (max-width: 1024px) {
  .card-content {
    grid-template-columns: 1fr;
  }

  .illustration-section {
    display: none;
  }
}

@media (max-width: 768px) {
  .content-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .config-options {
    grid-template-columns: 1fr;
  }

  .config-card {
    padding: 2rem 1rem;
  }
}
</style>
