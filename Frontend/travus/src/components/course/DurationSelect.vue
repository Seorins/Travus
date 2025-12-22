<template>
  <div class="duration-select">
    <div class="content-card">
      <div class="card-content">
        <div class="text-section">
          <h2 class="title">여행 기간을 선택해주세요</h2>
          <p class="subtitle">당일치기부터 2박 3일까지 선택할 수 있어요.</p>

          <div class="duration-options">
            <button
              v-for="option in durationOptions"
              :key="option.value"
              class="duration-card"
              :class="{ selected: selectedDuration === option.value }"
              @click="selectDuration(option.value)"
            >
              <div class="icon">{{ option.icon }}</div>
              <div class="duration-name">{{ option.name }}</div>
              <div class="duration-desc">{{ option.description }}</div>
            </button>
          </div>

          <div class="button-group">
            <button class="btn-back" @click="$emit('back')">
              이전
            </button>
            <button
              class="btn-next"
              :disabled="selectedDuration === null"
              @click="handleNext"
            >
              다음
            </button>
          </div>
        </div>

        <div class="illustration-section">
          <div class="calendar-illustration">
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <!-- 달력 -->
              <rect x="20" y="30" width="160" height="150" rx="10" fill="white" stroke="#667eea" stroke-width="3"/>

              <!-- 달력 헤더 -->
              <rect x="20" y="30" width="160" height="40" rx="10" fill="#667eea"/>
              <rect x="20" y="50" width="160" height="20" fill="#667eea"/>

              <!-- 요일 -->
              <line x1="20" y1="80" x2="180" y2="80" stroke="#e2e8f0" stroke-width="2"/>

              <!-- 날짜 그리드 -->
              <g fill="#cbd5e0" font-size="12" font-weight="600">
                <circle cx="45" cy="100" r="4"/>
                <circle cx="70" cy="100" r="4"/>
                <circle cx="95" cy="100" r="4"/>
                <circle cx="120" cy="100" r="4"/>
                <circle cx="145" cy="100" r="4"/>

                <circle cx="45" cy="125" r="4"/>
                <circle cx="70" cy="125" r="4"/>
                <circle cx="95" cy="125" r="4"/>
                <circle cx="120" cy="125" r="4"/>
                <circle cx="145" cy="125" r="4"/>
              </g>

              <!-- 선택된 날짜들 -->
              <circle cx="95" cy="150" r="12" fill="#667eea" opacity="0.3"/>
              <circle cx="120" cy="150" r="12" fill="#667eea" opacity="0.3"/>
              <circle cx="145" cy="150" r="12" fill="#667eea" opacity="0.3"/>

              <!-- 시계 아이콘 -->
              <g transform="translate(155, 25)">
                <circle cx="0" cy="0" r="15" fill="white" opacity="0.3"/>
                <circle cx="0" cy="0" r="12" fill="white" stroke="#5568d3" stroke-width="2"/>
                <line x1="0" y1="0" x2="0" y2="-6" stroke="#5568d3" stroke-width="2"/>
                <line x1="0" y1="0" x2="4" y2="0" stroke="#5568d3" stroke-width="2"/>
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

const durationOptions = [
  {
    value: 'day',
    name: '당일치기',
    description: '하루 동안 즐기는 여행',
    icon: '☀️',
    days: 1
  },
  {
    value: '1night',
    name: '1박 2일',
    description: '여유로운 주말 여행',
    icon: '🌙',
    days: 2
  },
  {
    value: '2nights',
    name: '2박 3일',
    description: '알찬 휴가 여행',
    icon: '⭐',
    days: 3
  }
]

const selectedDuration = ref(null)

const selectDuration = (value) => {
  selectedDuration.value = value
}

const handleNext = () => {
  if (selectedDuration.value !== null) {
    const selected = durationOptions.find(opt => opt.value === selectedDuration.value)
    emit('next', selected)
  }
}
</script>

<style scoped>
.duration-select {
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

.duration-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.duration-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.duration-card:hover {
  border-color: #667eea;
  background: #f7fafc;
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.duration-card.selected {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.duration-card.selected .icon,
.duration-card.selected .duration-name,
.duration-card.selected .duration-desc {
  color: white;
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.duration-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 0.5rem;
}

.duration-desc {
  font-size: 0.875rem;
  color: #718096;
  line-height: 1.4;
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

.calendar-illustration {
  width: 100%;
  max-width: 200px;
}

.calendar-illustration svg {
  width: 100%;
  height: auto;
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

  .duration-options {
    grid-template-columns: 1fr;
  }

  .duration-card {
    padding: 1.5rem 1rem;
  }
}
</style>
