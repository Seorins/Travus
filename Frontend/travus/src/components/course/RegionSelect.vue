<template>
  <div class="region-select">
    <!-- 배경 이미지 -->
    <div class="background-wrapper"></div>

    <!-- 구름 애니메이션 -->
    <div class="clouds-container">
      <img src="@/assets/img_cloud1.png" alt="cloud" class="cloud cloud1" />
      <img src="@/assets/img_cloud2.png" alt="cloud" class="cloud cloud2" />
      <img src="@/assets/img_cloud4.png" alt="cloud" class="cloud cloud4" />
      <img src="@/assets/img_cloud5.png" alt="cloud" class="cloud cloud5" />
    </div>

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
              :class="{ selected: selectedRegion === region.code }"
              @click="selectRegion(region.code)"
            >
              {{ region.name }}
            </button>
          </div>

          <p class="hint">
            하나의 지역을 선택하시면 TRAVUS가 동선을 고려해 추천해드려요.
          </p>

          <div class="button-group">
            <button class="btn-back" @click="emit('back')">
              이전
            </button>
            <button
              class="btn-next"
              :disabled="!selectedRegion"
              @click="handleNext"
            >
              다음
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- 캐릭터 -->
    <div class="character-wrapper">
      <img src='@/assets/select1.png' alt="TravUs AI 캐릭터" class="character-img" />
      <div class="character-shadow"></div>
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

// 단일 선택으로 변경
const selectedRegion = ref(null)

const selectRegion = (code) => {
  // 이미 선택된 지역을 다시 클릭하면 선택 해제
  if (selectedRegion.value === code) {
    selectedRegion.value = null
  } else {
    selectedRegion.value = code
  }
}

const handleNext = () => {
  if (selectedRegion.value) {
    // 배열 형태로 전달 (기존 API 호환성 유지)
    emit('next', [selectedRegion.value])
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
  padding: 100px 20px 40px;
  position: relative;
  overflow: hidden;
  background: linear-gradient(to bottom, #87CEEB 0%, #A0D3F0 50%, #B8DFF5 100%);
}

/* 배경 이미지 - course_background 사용 */
.background-wrapper {
  position: absolute;
  inset: 0;
  background-image: url('@/assets/course_background.png');
  background-repeat: no-repeat;
  background-position: bottom right;
  background-size: auto 100%;
  z-index: 0;
}

.background-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 30%;
  background: linear-gradient(to bottom, #87CEEB 0%, #9fc5f8 50%, transparent 100%);
  z-index: 1;
}

/* 구름 애니메이션 */
.clouds-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.cloud {
  position: absolute;
  opacity: 0;
  animation: cloudFloat 3s ease-out forwards;
}

.cloud1 {
  top: 10%;
  left: 10%;
  width: 120px;
  animation-delay: 0.2s;
}

.cloud2 {
  top: 20%;
  right: 15%;
  width: 150px;
  animation-delay: 0.5s;
}

.cloud4 {
  top: 50%;
  left: 5%;
  width: 100px;
  animation-delay: 0.8s;
}

.cloud5 {
  top: 60%;
  right: 10%;
  width: 130px;
  animation-delay: 1.1s;
}

@keyframes cloudFloat {
  0% {
    opacity: 0;
    transform: translateY(-50px);
  }
  100% {
    opacity: 0.8;
    transform: translateY(0);
  }
}

.content-card {
  width: 100%;
  max-width: 800px;
  min-height: 700px;
  background: white;
  border-radius: 5px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
}

.card-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.text-section {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.subtitle {
  font-size: 1.125rem;
  color: #718096;
  margin-bottom: 0.5rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.nxttitle {
  font-size: 2rem;
  font-weight: 300;
  color: #1a202c;
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

/* 캐릭터 */
.character-wrapper {
  position: absolute;
  right: 6%;
  bottom: 8%;
  z-index: 3;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.character-img {
  width: 250px;
  height: auto;
  position: relative;
  z-index: 2;
  animation: floatCharacter 3s ease-in-out infinite;
  margin-bottom: -50px;
}

.character-shadow {
  width: 180px;
  height: 30px;
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.1) 40%, transparent 70%);
  border-radius: 50%;
  z-index: 1;
  filter: blur(8px);
}

@keyframes floatCharacter {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
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
  margin-top: auto;
  padding-top: 2rem;
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
  .character-wrapper {
    right: 3%;
    bottom: 5%;
  }

  .character-img {
    width: 200px;
  }

  .character-shadow {
    width: 150px;
  }

  .cloud1, .cloud2, .cloud4, .cloud5 {
    width: 80px;
  }
}

@media (max-width: 768px) {
  .content-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .nxttitle {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .regions-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .region-btn {
    width: 70px;
    height: 70px;
    font-size: 0.875rem;
  }

  .character-wrapper {
    display: none;
  }

  .cloud {
    width: 60px !important;
  }
}
</style>
