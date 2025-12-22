<template>
  <section class="travel-target-section" ref="sectionRef">
    <div class="container">
      <!-- 상단 헤더 -->
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

      <!-- 여행지 리스트 -->
      <div class="destinations-list">
        <div
          v-for="(item, index) in travelItems"
          :key="index"
          class="destination-item"
          :class="item.colorClass"
          ref="itemRefs"
        >
          <div class="item-number">{{ String(index + 1).padStart(2, '0') }}</div>
          <div class="item-content">
            <div class="item-header">
              <span class="category">{{ item.category }}</span>
              <h3 class="item-title">{{ item.title }}</h3>
            </div>
            <div class="features-list">
              <span
                v-for="(feature, idx) in item.features"
                :key="idx"
                class="feature-tag"
              >
                {{ feature }}
              </span>
            </div>
          </div>
          <div class="item-icon">
            <div class="icon-circle" :class="item.colorClass"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const sectionRef = ref(null)
const itemRefs = ref([])

const travelItems = [
  {
    category: 'BEACH TOUR',
    title: '해변 여행',
    features: ['부산 해운대', '강릉 경포대', '제주 협재 해수욕장', '양양 서핑', '속초 해변', '포항 호미곶'],
    colorClass: 'blue',
  },
  {
    category: 'MOUNTAIN HIKING',
    title: '등산 & 트레킹',
    features: ['설악산', '지리산', '북한산', '한라산', '계룡산', '내장산'],
    colorClass: 'green',
  },
  {
    category: 'CULTURAL HERITAGE',
    title: '문화 유산 투어',
    features: ['경주 불국사', '경복궁', '창덕궁', '수원 화성', '하회마을', '종묘'],
    colorClass: 'purple',
  },
  {
    category: 'FOOD TOUR',
    title: '맛집 탐방',
    features: ['전주 한옥마을', '서울 망원동', '부산 광안리', '대구 동성로', '제주 흑돼지', '강릉 초당두부'],
    colorClass: 'red',
  },
  {
    category: 'CITY TOUR',
    title: '도시 여행',
    features: ['서울 명동', '부산 해운대', '인천 차이나타운', '대전 엑스포', '광주 양림동', '대구 김광석길'],
    colorClass: 'orange',
  },
  {
    category: 'NATURE & HEALING',
    title: '자연 & 힐링',
    features: ['제주 올레길', '보성 녹차밭', '담양 죽녹원', '순천만 습지', '태안 안면도', '가평 아침고요수목원'],
    colorClass: 'teal',
  },
  {
    category: 'ISLAND TRIP',
    title: '섬 여행',
    features: ['제주도', '울릉도', '거제도', '남해도', '진도', '완도'],
    colorClass: 'pink',
  },
  {
    category: 'WINTER SPORTS',
    title: '겨울 스포츠',
    features: ['평창 스키장', '강원 보드', '무주 리조트', '용평 스키', '하이원', '비발디파크'],
    colorClass: 'yellow',
  }
]

onMounted(() => {
  // 각 아이템에 스크롤 트리거 애니메이션 적용
  itemRefs.value.forEach((item, index) => {
    if (!item) return

    gsap.fromTo(
      item,
      {
        opacity: 0.2,
        y: 100,
        scale: 0.9
      },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: item,
          start: 'top 80%',
          end: 'top 30%',
          scrub: 0.5,
          toggleActions: 'play none none reverse'
        }
      }
    )

    // 아이콘 회전 애니메이션
    const iconCircle = item.querySelector('.icon-circle')
    if (iconCircle) {
      gsap.fromTo(
        iconCircle,
        {
          scale: 0,
          rotation: -180
        },
        {
          scale: 1,
          rotation: 0,
          duration: 1,
          ease: 'back.out(1.7)',
          scrollTrigger: {
            trigger: item,
            start: 'top 70%',
            end: 'top 40%',
            scrub: 0.5
          }
        }
      )
    }
  })
})

onUnmounted(() => {
  ScrollTrigger.getAll().forEach(trigger => trigger.kill())
})
</script>

<style scoped>
.travel-target-section {
  background: #f5f5f5;
  min-height: 100vh;
  padding: 5rem 2rem;
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 상단 헤더 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4rem;
}

.text-box {
  color: #111827;
}

.subtitle {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  opacity: 0.9;
  letter-spacing: 2px;
}

.title {
  font-size: 3.5rem;
  font-weight: 900;
  font-family: 'Poppins', sans-serif;
  margin: 0;
}

.main-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  background: #ffffff;
  border-radius: 50px;
  text-decoration: none;
  border: 2px solid rgba(154, 182, 243, 0.45);
  color: #8aa6e8;
  font-weight: 600;
  transition: all 0.3s ease;
}

.main-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(154, 182, 243, 0.35);
}

.arrow {
  font-size: 1.5rem;
}

/* 여행지 리스트 */
.destinations-list {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.destination-item {
  display: grid;
  grid-template-columns: 80px 1fr 120px;
  gap: 2rem;
  align-items: center;
  padding: 2.5rem;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
  border-radius: 20px;
  border: 2px solid rgba(17, 24, 39, 0.08);
  transition: all 0.3s ease;
  opacity: 0.2;
}

.destination-item:hover {
  background: rgba(255, 255, 255, 0.85);
  border-color: rgba(154, 182, 243, 0.35);
  transform: translateX(10px);
}

.item-number {
  font-size: 3rem;
  font-weight: 900;
  color: rgba(31, 41, 55, 0.35);
  font-family: 'Poppins', sans-serif;
}

.item-content {
  flex: 1;
}

.item-header {
  margin-bottom: 1rem;
}

.category {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 2px;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.item-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0.5rem 0 0 0;
}

.features-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.feature-tag {
  padding: 0.4rem 1rem;
  background: rgba(154, 182, 243, 0.18);
  border-radius: 20px;
  font-size: 0.85rem;
  color: #1f2937;
  font-weight: 500;
}

.item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(154, 182, 243, 0.22);
  border: 3px solid #9ab6f3;
  position: relative;
}

.icon-circle::before {
  content: '→';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5rem;
  color: #1f2937;
  font-weight: 900;
}

/* 색상별 테마 */
.destination-item.blue:hover { border-color: #3498db; }
.destination-item.green:hover { border-color: #2ecc71; }
.destination-item.purple:hover { border-color: #9b59b6; }
.destination-item.red:hover { border-color: #e74c3c; }
.destination-item.orange:hover { border-color: #f39c12; }
.destination-item.teal:hover { border-color: #1abc9c; }
.destination-item.pink:hover { border-color: #ff69b4; }
.destination-item.yellow:hover { border-color: #f1c40f; }

/* 반응형 */
@media (max-width: 1024px) {
  .title {
    font-size: 2.5rem;
  }

  .destination-item {
    grid-template-columns: 60px 1fr 80px;
    gap: 1.5rem;
    padding: 2rem;
  }

  .item-number {
    font-size: 2rem;
  }

  .item-title {
    font-size: 1.5rem;
  }

  .icon-circle {
    width: 70px;
    height: 70px;
  }

  .icon-circle::before {
    font-size: 1.8rem;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 3rem;
  }

  .title {
    font-size: 2rem;
  }

  .destination-item {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1.5rem;
  }

  .item-number {
    font-size: 1.5rem;
  }

  .item-title {
    font-size: 1.3rem;
  }

  .icon-circle {
    width: 60px;
    height: 60px;
  }

  .icon-circle::before {
    font-size: 1.5rem;
  }

  .feature-tag {
    font-size: 0.75rem;
    padding: 0.3rem 0.8rem;
  }
}
</style>
