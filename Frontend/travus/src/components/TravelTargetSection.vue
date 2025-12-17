<template>
  <section class="service-section" tabindex="0" @focus="handleFocus">
    <div class="service-container">
      <!-- 상단 텍스트 & 버튼 -->
      <div class="section-header">
        <div class="text-box">
          <p class="subtitle">여행지 추천</p>
          <h2 class="title">Travel Destinations</h2>
        </div>
        <a href="#" class="main-btn">
          <span>더 보기</span>
          <span class="arrow">→</span>
        </a>
      </div>

      <!-- CircularGallery -->
      <div class="gallery-wrapper">
        <CircularGallery
          :items="travelItems"
          :bend="2"
          :textColor="'#ffffff'"
          :borderRadius="0.08"
          :scrollEase="0.05"
          :scrollSpeed="1.5"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import CircularGallery from './CircularGallery.vue'

const emit = defineEmits(['focus'])

const travelItems = [
  {
    category: 'BEACH TOUR',
    title: '해변 여행',
    features: ['부산 해운대', '강릉 경포대', '제주 협재 해수욕장', '양양 서핑', '속초 해변', '포항 호미곶'],
    colorClass: 'blue',
    text: '해변 여행'
  },
  {
    category: 'MOUNTAIN HIKING',
    title: '등산 & 트레킹',
    features: ['설악산', '지리산', '북한산', '한라산', '계룡산', '내장산'],
    colorClass: 'green',
    text: '등산 & 트레킹'
  },
  {
    category: 'CULTURAL HERITAGE',
    title: '문화 유산 투어',
    features: ['경주 불국사', '경복궁', '창덕궁', '수원 화성', '하회마을', '종묘'],
    colorClass: 'purple',
    text: '문화 유산'
  },
  {
    category: 'FOOD TOUR',
    title: '맛집 탐방',
    features: ['전주 한옥마을', '서울 망원동', '부산 광안리', '대구 동성로', '제주 흑돼지', '강릉 초당두부'],
    colorClass: 'red',
    text: '맛집 탐방'
  },
  {
    category: 'CITY TOUR',
    title: '도시 여행',
    features: ['서울 명동', '부산 해운대', '인천 차이나타운', '대전 엑스포', '광주 양림동', '대구 김광석길'],
    colorClass: 'orange',
    text: '도시 여행'
  },
  {
    category: 'NATURE & HEALING',
    title: '자연 & 힐링',
    features: ['제주 올레길', '보성 녹차밭', '담양 죽녹원', '순천만 습지', '태안 안면도', '가평 아침고요수목원'],
    colorClass: 'teal',
    text: '자연 & 힐링'
  },
  {
    category: 'ISLAND TRIP',
    title: '섬 여행',
    features: ['제주도', '울릉도', '거제도', '남해도', '진도', '완도'],
    colorClass: 'pink',
    text: '섬 여행'
  },
  {
    category: 'WINTER SPORTS',
    title: '겨울 스포츠',
    features: ['평창 스키장', '강원 보드', '무주 리조트', '용평 스키', '하이원', '비발디파크'],
    colorClass: 'yellow',
    text: '겨울 스포츠'
  }
]

const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}
</script>


<style scoped>
.service-section {
  background: #ff6714;
  min-height: 100vh;
  padding: 3rem 2rem;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.service-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.service-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}

/* 상단 헤더 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  animation: fadeInDown 0.8s ease;
}

.text-box {
  color: white;
}

.subtitle {
  font-size: 1rem;
  margin-bottom: 0.3rem;
  opacity: 0.9;
}

.title {
  font-size: 3rem;
  font-weight: 900;
  font-family: 'Poppins', sans-serif;
}

.main-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  background: white;
  border-radius: 50px;
  text-decoration: none;
  color: #ff6714;
  font-weight: 600;
  transition: all 0.3s ease;
}

.main-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.arrow {
  font-size: 1.5rem;
}

/* Gallery Wrapper */
.gallery-wrapper {
  width: 100%;
  height: 700px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 애니메이션 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 */
@media (max-width: 1024px) {
  .title {
    font-size: 2.5rem;
  }

  .gallery-wrapper {
    height: 500px;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 1.5rem;
  }

  .title {
    font-size: 2rem;
  }

  .gallery-wrapper {
    height: 400px;
  }
}
</style>
