<template>
  <div class="region-select">
    <div class="background-illustration"></div>
    <div class="content-card">
      <div class="card-content">
        <div class="text-section">
          <p class="subtitle">어디로 떠나볼까요?</p>
          <h2 class="title">떠나고 싶은 지역을 <br/> <span class="nxttitle">선택해주세요</span> </h2>

          <div class="regions-grid">
            <button
              v-for="region in regions"
              :key="region.code"
              class="region-btn"
              :class="{ selected: selectedRegions.includes(region.code) }"
              @click="toggleRegion(region.code)"
            >
              {{ region.name }}
            </button>
          </div>

          <p class="hint">
            지역을 기반으로 TRAVUS가 동선을 고려해 추천해드려요.
          </p>

          <div class="button-group">
            <button class="btn-back" @click="$emit('back')">
              이전
            </button>
            <button
              class="btn-next"
              :disabled="selectedRegions.length === 0"
              @click="handleNext"
            >
              다음
            </button>
          </div>
        </div>

      </div>
    </div>
    <div class="character-wrapper">
      <img src='@/assets/select1.png' alt="TravUs AI 캐릭터" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next', 'back'])

const regions = [
  { code: '1', name: '서울' },
  { code: '6', name: '부산' },
  { code: '4', name: '대구' },
  { code: '2', name: '인천' },
  { code: '5', name: '광주' },
  { code: '3', name: '대전' },
  { code: '7', name: '울산' },
  { code: '8', name: '세종' },
  { code: '31', name: '경기' },
  { code: '32', name: '강원' },
  { code: '33', name: '충북' },
  { code: '34', name: '충남' },
  { code: '37', name: '전북' },
  { code: '38', name: '전남' },
  { code: '35', name: '경북' },
  { code: '36', name: '경남' },
  { code: '39', name: '제주' }
]

const selectedRegions = ref([])

const toggleRegion = (code) => {
  const index = selectedRegions.value.indexOf(code)
  if (index > -1) {
    selectedRegions.value.splice(index, 1)
  } else {
    selectedRegions.value.push(code)
  }
}

const handleNext = () => {
  if (selectedRegions.value.length > 0) {
    emit('next', selectedRegions.value)
  }
}
</script>

<style scoped>
.region-select {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #9fc5f8;
  padding: 100px 20px 40px;
  position: relative;
  overflow: hidden;
}

.background-illustration {
  position: absolute;
  inset: 0;
  background-image: url('/cloud-bg.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  z-index: 0;
}

.content-card {
  width: 100%;
  max-width: 800px;
  min-height: 700px;
  background: white;
  border-radius: 5px;
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

.nxttitle {
  font-size: 2rem;
  font-weight: lighter;
  color: #1a202c;
  /* margin: 0 0 2rem 0; */
}

.card-content {
  display: block;
}

.subtitle {
  font-size: 1.125rem;
  color: #718096;
}

.regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
  margin-top: 2rem;
}

.region-btn {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 400;
  border: 2px solid #e2e8f0;
  background: #e2e8f0;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #4a5568;
}

.region-btn:hover {
  border-color: #667eea;
  background: #f7fafc;
}

.region-btn.selected {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.character-wrapper {
  position: absolute;
  right: 6%;
  bottom: 8%;
  z-index: 1;
  pointer-events: none; 
}

.character-wrapper img {
  width: 250px;   
  height: auto;
  opacity: 0.95;
}

.hint {
  font-size: 0.875rem;
  color: #a0aec0;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 10px;
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

  .regions-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .region-btn {
    padding: 0.75rem;
    font-size: 0.875rem;
  }
}
</style>
