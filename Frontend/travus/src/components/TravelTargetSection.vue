<template>
  <section class="service-section" tabindex="0" @focus="handleFocus">
    <div class="service-container">
      <!-- 상단 텍스트 & 버튼 -->
      <div class="section-header">
        <div class="text-box">
          <p class="subtitle">우리는 이런 일을 해요</p>
          <h2 class="title">Creative Service</h2>
        </div>
        <a href="#" class="main-btn">
          <span>메뉴 더보기</span>
          <span class="arrow">→</span>
        </a>
      </div>

      <!-- 카드 슬라이드 섹션 -->
      <div class="carousel-container" ref="circleContainer">
        <!-- 왼쪽 중앙 텍스트 (고정) -->
        <div class="intro-text">
          <div class="text-content">
            <p>
              생각의 경계를 넘어서는<br />
              유연한 사고와 혁신적인 발상으로<br />
              무한한 가능성을 만들어요.
            </p>
          </div>
        </div>

        <!-- 카드 슬라이더 -->
        <div class="cards-wrapper" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">

          <!-- 카드 1: 브랜딩 디자인 -->
          <div class="card-item">
            <div class="service-card">
              <div class="card-header">
                <p class="card-label">Branding Design</p>
                <p class="card-title">브랜드 및 아이덴티티 디자인</p>
              </div>
              <div class="card-body">
                <ul class="service-list">
                  <li>브랜드 전략</li>
                  <li>브랜딩 자산 개발</li>
                  <li>Visual Identity</li>
                  <li>BX Design</li>
                  <li>Brand Guidelines</li>
                  <li>Naming & Storytelling</li>
                </ul>
                <div class="card-icon pink"></div>
              </div>
            </div>
          </div>

          <!-- 카드 2: UI/UX 디자인 -->
          <div class="card-item">
            <div class="service-card">
              <div class="card-header">
                <p class="card-label">UI/UX Design</p>
                <p class="card-title">UI/UX 디자인</p>
              </div>
              <div class="card-body">
                <ul class="service-list">
                  <li>반응형 홈페이지</li>
                  <li>적응형 홈페이지</li>
                  <li>Interaction Design</li>
                  <li>사용성 테스트</li>
                  <li>Visual Design</li>
                  <li>접근성 디자인</li>
                </ul>
                <div class="card-icon purple"></div>
              </div>
            </div>
          </div>

          <!-- 카드 3: 웹 & 모바일 -->
          <div class="card-item">
            <div class="service-card">
              <div class="card-header">
                <p class="card-label">Digital Services</p>
                <p class="card-title">웹 & 모바일 시스템 개발</p>
              </div>
              <div class="card-body">
                <ul class="service-list">
                  <li>프론트엔드 개발</li>
                  <li>HTML, CSS, JavaScript</li>
                  <li>백엔드 개발</li>
                  <li>AI 기술 개발</li>
                  <li>Mobile App</li>
                  <li>보안(SSL, 인증, 취약점)</li>
                </ul>
                <div class="card-icon red"></div>
              </div>
            </div>
          </div>

          <!-- 카드 4: 모션 그래픽 -->
          <div class="card-item">
            <div class="service-card">
              <div class="card-header">
                <p class="card-label">Digital Marketing</p>
                <p class="card-title">모션 그래픽 및 비주얼 콘텐츠</p>
              </div>
              <div class="card-body">
                <ul class="service-list">
                  <li>2D/3D Motion Graphic</li>
                  <li>스토리보드 및 기획</li>
                  <li>3D 카탈로그 / 3D 쇼룸</li>
                  <li>Visual Effects</li>
                  <li>브랜드 캐릭터 개발</li>
                  <li>인터랙티브 비주얼 콘텐츠</li>
                </ul>
                <div class="card-icon blue"></div>
              </div>
            </div>
          </div>

          <!-- 카드 5: 디지털 마케팅 -->
          <div class="card-item">
            <div class="service-card">
              <div class="card-header">
                <p class="card-label">Creative Consulting</p>
                <p class="card-title">디지털 마케팅 및 캠페인</p>
              </div>
              <div class="card-body">
                <ul class="service-list">
                  <li>검색 엔진 최적화 (SEO)</li>
                  <li>마케팅 콘텐츠 제작</li>
                  <li>소셜 미디어 마케팅</li>
                  <li>모바일 최적화 광고</li>
                  <li>Newsletters</li>
                  <li>Web Analytics</li>
                </ul>
                <div class="card-icon yellow"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 하단 로봇 이미지 (옵션) -->
      <div class="robot-character">
        <img src="../assets/topbtn.png" alt="Robot Character" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['focus'])

const currentIndex = ref(0)
const totalItems = 5 // 카드 5개
let isScrolling = false

const circleContainer = ref(null)

const handleWheel = (e) => {
  e.preventDefault()

  // 마지막 카드에서 아래로 스크롤 시 이벤트 리스너 제거하고 페이지 스크롤 허용
  if (currentIndex.value === totalItems - 1 && e.deltaY > 0) {
    circleContainer.value.removeEventListener('wheel', handleWheel)
    return
  }

  if (isScrolling) return
  isScrolling = true

  if (e.deltaY > 0 && currentIndex.value < totalItems - 1) {
    // 스크롤 다운 → 다음 카드
    currentIndex.value++
  } else if (e.deltaY < 0 && currentIndex.value > 0) {
    // 스크롤 업 → 이전 카드
    currentIndex.value--
  }

  setTimeout(() => {
    isScrolling = false
  }, 600)
}


const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}

onMounted(() => {
  circleContainer.value.addEventListener('wheel', handleWheel, { passive: false })
})

onUnmounted(() => {
  circleContainer.value?.removeEventListener('wheel', handleWheel)
})

</script>


<style scoped>
.service-section {
  background: #ff6714;
  min-height: 100vh;
  max-height: 100vh;
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

/* 캐러셀 컨테이너 */
.carousel-container {
  position: relative;
  width: 100%;
  height: 650px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4rem;
  overflow: hidden;
}

/* 왼쪽 중앙 텍스트 (고정) */
.intro-text {
  flex-shrink: 0;
  width: 450px;
  text-align: left;
  z-index: 10;
}

.text-content {
  color: white;
  font-size: 1.8rem;
  line-height: 1.8;
  font-weight: 400;
}

/* 카드 슬라이더 래퍼 */
.cards-wrapper {
  display: flex;
  flex-shrink: 0;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  width: 420px;
  height: 100%;
}

/* 카드 아이템 */
.card-item {
  flex-shrink: 0;
  width: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.service-card {
  background: white;
  border-radius: 25px;
  padding: 2rem;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
  height: 420px;
  width: 100%;
  transition: all 0.3s ease;
  overflow: hidden;
}

.service-card:hover {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.card-header {
  background: #1a1a1a;
  margin: -2rem -2rem 1.5rem -2rem;
  padding: 1.5rem 2rem;
  border-radius: 25px 25px 0 0;
}

.card-label {
  font-size: 0.75rem;
  color: #ff6714;
  margin-bottom: 0.5rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
}

.card-body {
  position: relative;
}

.service-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.service-list li {
  font-size: 0.8rem;
  color: #666;
  position: relative;
  padding-left: 0.8rem;
}

.service-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #ff6714;
  font-size: 0.7rem;
}

.card-icon {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  position: absolute;
  bottom: -10px;
  right: 10px;
  opacity: 0.25;
}

.card-icon.pink {
  background: linear-gradient(135deg, #ff6b9d 0%, #c239b3 100%);
}

.card-icon.purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon.red {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon.blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon.yellow {
  background: linear-gradient(135deg, #fdeb71 0%, #f8d800 100%);
}

/* 로봇 캐릭터 */
.robot-character {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  z-index: 10;
}

.robot-character img {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.2));
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
@media (max-width: 1200px) {
  .carousel-container {
    gap: 2rem;
  }

  .intro-text {
    width: 350px;
  }

  .text-content {
    font-size: 1.4rem;
  }

  .cards-wrapper {
    width: 380px;
  }

  .card-item {
    width: 380px;
  }

  .service-card {
    height: 380px;
  }
}

@media (max-width: 1024px) {
  .title {
    font-size: 3rem;
  }

  .carousel-container {
    flex-direction: column;
    gap: 2rem;
    height: auto;
  }

  .intro-text {
    width: 100%;
    text-align: center;
  }

  .text-content {
    font-size: 1.2rem;
  }

  .cards-wrapper {
    width: 100%;
  }

  .card-item {
    width: 100%;
  }

  .service-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 2rem;
  }

  .title {
    font-size: 2.5rem;
  }

  .text-content {
    font-size: 1rem;
  }

  .card-icon {
    width: 80px;
    height: 80px;
  }

  .service-card {
    padding: 1.5rem;
    height: 350px;
  }

  .card-title {
    font-size: 1.2rem;
  }
}
</style>
