<template>
  <div class="theme-select">
    <div class="content-card">
      <div class="card-content">
        <h2 class="title">어떤 테마의 여행을 원하시나요?</h2>
        <p class="subtitle">원하는 테마를 모두 선택해주세요. (중복 선택 가능)</p>

        <div class="themes-grid">
          <button
            v-for="theme in themes"
            :key="theme.id"
            class="theme-card"
            :class="{ selected: selectedThemes.includes(theme.id) }"
            @click="toggleTheme(theme.id)"
          >
            <div class="theme-icon">{{ theme.icon }}</div>
            <div class="theme-name">{{ theme.name }}</div>
          </button>
        </div>

        <p class="hint">
          💡 선택한 테마에 맞는 여행지를 추천해드려요.
        </p>

        <div class="button-group">
          <button class="btn-back" @click="$emit('back')">
            이전
          </button>
          <button
            class="btn-next"
            :disabled="selectedThemes.length === 0"
            @click="handleNext"
          >
            여행 코스 생성하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next', 'back'])

const themes = [
  { id: 'mountain', name: '산', icon: '🏔️' },
  { id: 'sea', name: '바다', icon: '🌊' },
  { id: 'indoor', name: '실내여행지', icon: '🏛️' },
  { id: 'activity', name: '액티비티', icon: '🎯' },
  { id: 'culture', name: '문화/역사', icon: '🏛️' },
  { id: 'theme_park', name: '테마파크', icon: '🎢' },
  { id: 'cafe', name: '카페', icon: '☕' },
  { id: 'market', name: '전통시장', icon: '🏪' },
  { id: 'festival', name: '축제', icon: '🎉' }
]

const selectedThemes = ref([])

const toggleTheme = (id) => {
  const index = selectedThemes.value.indexOf(id)
  if (index > -1) {
    selectedThemes.value.splice(index, 1)
  } else {
    selectedThemes.value.push(id)
  }
}

const handleNext = () => {
  if (selectedThemes.value.length > 0) {
    emit('next', selectedThemes.value)
  }
}
</script>

<style scoped>
.theme-select {
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
  max-width: 1000px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
}

.card-content {
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
  text-align: center;
}

.subtitle {
  font-size: 1.125rem;
  color: #718096;
  margin: 0 0 2.5rem 0;
  text-align: center;
}

.themes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.theme-card {
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
  min-height: 140px;
}

.theme-card:hover {
  border-color: #667eea;
  background: #f7fafc;
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.theme-card.selected {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.theme-card.selected .theme-icon,
.theme-card.selected .theme-name {
  color: white;
}

.theme-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  filter: grayscale(0);
  transition: filter 0.3s ease;
}

.theme-card:not(.selected) .theme-icon {
  filter: grayscale(0.3);
}

.theme-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
}

.hint {
  font-size: 0.875rem;
  color: #667eea;
  margin: 0 0 2rem 0;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  text-align: center;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-next:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
}

.btn-next:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  box-shadow: none;
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

  .themes-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .theme-card {
    padding: 1.5rem 0.75rem;
    min-height: 120px;
  }

  .theme-icon {
    font-size: 2.5rem;
  }

  .theme-name {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .themes-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
