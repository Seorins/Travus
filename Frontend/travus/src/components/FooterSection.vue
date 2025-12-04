<template>
  <footer class="footer-section" tabindex="0" @focus="handleFocus">
    <div class="footer-container">
      <!-- 상단 영역 -->
      <div class="footer-top">
        <div class="footer-hero">
          <div class="footer-characters">
            <span class="character" v-for="char in characters" :key="char.id">{{ char.emoji }}</span>
          </div>
          <h2 class="footer-title" data-text="함께 떠나요, TravUs와 함께">
            함께 떠나요, TravUs와 함께
          </h2>
          <p class="footer-tagline">모두가 평등하게 여행을 즐기는 그날까지</p>
        </div>
      </div>

      <!-- 중간 영역 -->
      <div class="footer-content">
        <div class="footer-brand">
          <h3 class="brand-name">TravUs</h3>
          <p class="brand-description">
            접근성을 최우선으로 하는 여행 플랫폼으로, 모든 사람이 자유롭게 여행할 수 있는 세상을
            만듭니다.
          </p>
        </div>

        <div class="footer-links">
          <div class="link-column" tabindex="0" @focus="handleColumnFocus">
            <h4>서비스</h4>
            <ul>
              <li><a href="#" tabindex="0" @focus="handleFocus">여행지 검색</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">AI 카메라</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">접근성 정보</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">커뮤니티</a></li>
            </ul>
          </div>

          <div class="link-column" tabindex="0" @focus="handleColumnFocus">
            <h4>회사 소개</h4>
            <ul>
              <li><a href="#" tabindex="0" @focus="handleFocus">About Us</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">팀 소개</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">채용 정보</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">보도자료</a></li>
            </ul>
          </div>

          <div class="link-column" tabindex="0" @focus="handleColumnFocus">
            <h4>고객 지원</h4>
            <ul>
              <li><a href="#" tabindex="0" @focus="handleFocus">FAQ</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">1:1 문의</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">이용 가이드</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">접근성 지원</a></li>
            </ul>
          </div>

          <div class="link-column" tabindex="0" @focus="handleColumnFocus">
            <h4>법적 고지</h4>
            <ul>
              <li><a href="#" tabindex="0" @focus="handleFocus">이용약관</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">개인정보처리방침</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">접근성 정책</a></li>
              <li><a href="#" tabindex="0" @focus="handleFocus">위치기반서비스</a></li>
            </ul>
          </div>
        </div>
      </div>

      <!-- SNS 링크 -->
      <div class="footer-social">
        <a
          href="#"
          class="social-link"
          tabindex="0"
          @focus="handleFocus"
          aria-label="Facebook 페이지"
        >
          <span class="social-icon">📘</span>
        </a>
        <a
          href="#"
          class="social-link"
          tabindex="0"
          @focus="handleFocus"
          aria-label="Instagram 페이지"
        >
          <span class="social-icon">📷</span>
        </a>
        <a href="#" class="social-link" tabindex="0" @focus="handleFocus" aria-label="YouTube 채널">
          <span class="social-icon">▶️</span>
        </a>
        <a href="#" class="social-link" tabindex="0" @focus="handleFocus" aria-label="Twitter 계정">
          <span class="social-icon">🐦</span>
        </a>
      </div>

      <!-- 하단 영역 -->
      <div class="footer-bottom">
        <div class="company-info">
          <p>© 2025 TravUs. All rights reserved.</p>
          <p>대표: TravUs Team | 사업자등록번호: 000-00-00000</p>
          <p>주소: 서울특별시 강남구 테헤란로 123</p>
          <p>이메일: contact@travus.com | 전화: 02-1234-5678</p>
        </div>
      </div>

      <!-- 맨 위로 버튼 -->
      <button
        class="scroll-to-top"
        @click="scrollToTop"
        tabindex="0"
        @focus="handleFocus"
        aria-label="맨 위로 이동"
      >
        ↑
      </button>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['focus'])

// 목업 캐릭터 데이터
const characters = ref([
  { id: 1, emoji: '🚶' },
  { id: 2, emoji: '🧑‍🦽' },
  { id: 3, emoji: '👨‍🦯' },
  { id: 4, emoji: '👨‍👩‍👧‍👦' },
  { id: 5, emoji: '🧓' },
  { id: 6, emoji: '👶' }
])

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const handleFocus = (event) => {
  const text =
    event.target.getAttribute('data-text') ||
    event.target.getAttribute('aria-label') ||
    event.target.innerText
  emit('focus', text)
}

const handleColumnFocus = (event) => {
  const h4 = event.currentTarget.querySelector('h4')
  const links = Array.from(event.currentTarget.querySelectorAll('a')).map((a) => a.innerText)
  const text = `${h4?.innerText}. ${links.join(', ')}`
  emit('focus', text)
}
</script>

<style scoped>
.footer-section {
  background: #2d2d2d; /* 진한 회색 단색 */
  color: white;
  padding: 4rem 2rem 2rem;
  position: relative;
}

.footer-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
}

.footer-top {
  text-align: center;
  margin-bottom: 4rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-characters {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.character {
  font-size: 3rem;
  animation: bounce 2s ease-in-out infinite;
  display: inline-block;
}

.character:nth-child(1) {
  animation-delay: 0s;
}
.character:nth-child(2) {
  animation-delay: 0.2s;
}
.character:nth-child(3) {
  animation-delay: 0.4s;
}
.character:nth-child(4) {
  animation-delay: 0.6s;
}
.character:nth-child(5) {
  animation-delay: 0.8s;
}
.character:nth-child(6) {
  animation-delay: 1s;
}

.footer-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #667eea; /* 보라색 단색 */
}

.footer-tagline {
  font-size: 1.3rem;
  opacity: 0.8;
}

.footer-content {
  display: grid;
  grid-template-columns: 1.5fr 2fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer-brand {
  max-width: 400px;
}

.brand-name {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: white;
}

.brand-description {
  line-height: 1.8;
  opacity: 0.8;
  font-size: 1.1rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.link-column {
  transition: transform 0.3s ease;
}

.link-column:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
  transform: translateY(-5px);
}

.link-column h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #667eea;
  font-weight: 700;
}

.link-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.link-column li {
  margin-bottom: 0.75rem;
}

.link-column a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
}

.link-column a:hover {
  color: white;
  transform: translateX(5px);
}

.link-column a:focus {
  outline: 2px solid #ffd700;
  outline-offset: 2px;
  color: white;
}

.footer-social {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 3rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.social-link {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  text-decoration: none;
}

.social-link:hover {
  background: #667eea; /* 보라색 단색 */
  transform: translateY(-5px);
}

.social-link:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
  background: #667eea; /* 보라색 단색 */
}

.social-icon {
  font-size: 1.8rem;
}

.footer-bottom {
  text-align: center;
}

.company-info {
  opacity: 0.7;
  font-size: 0.9rem;
  line-height: 1.8;
}

.company-info p {
  margin: 0.25rem 0;
}

.scroll-to-top {
  position: fixed;
  bottom: 3rem;
  right: 3rem;
  width: 60px;
  height: 60px;
  background: #667eea; /* 보라색 단색 */
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  z-index: 100;
}

.scroll-to-top:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
}

.scroll-to-top:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .footer-links {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .footer-title {
    font-size: 1.8rem;
  }

  .footer-tagline {
    font-size: 1.1rem;
  }

  .footer-links {
    grid-template-columns: 1fr;
  }

  .character {
    font-size: 2rem;
  }

  .scroll-to-top {
    bottom: 2rem;
    right: 2rem;
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
}
</style>
