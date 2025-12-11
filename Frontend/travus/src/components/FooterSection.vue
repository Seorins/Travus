<template>
  <footer class="footer-section" tabindex="0" @focus="handleFocus">
    <div class="footer-container">
      <!-- 상단 영역: 소셜 아이콘 & 연락처 + 메뉴 -->
      <div class="footer-top">
        <div class="left-section">
          <div class="social-links">
            <a href="#" class="social-icon" aria-label="Naver">N</a>
            <a href="#" class="social-icon" aria-label="Play">▶</a>
            <a href="#" class="social-icon" aria-label="YouTube">▶</a>
            <a href="#" class="social-icon" aria-label="Instagram">📷</a>
            <a href="#" class="social-icon" aria-label="Location">📍</a>
          </div>
          <div class="contact-info">
            <span><strong>T.</strong> 031 293 0128</span>
            <span><strong>M.</strong> admin@travus.com</span>
          </div>
        </div>
        <nav class="top-menu">
          <a href="#" class="menu-item">About Us</a>
          <a href="#" class="menu-item">Work</a>
          <a href="#" class="menu-item">Solution</a>
          <a href="#" class="menu-item">Project</a>
          <a href="#" class="menu-item">Community</a>
        </nav>
      </div>

      <!-- 중간 영역: 메뉴 링크 -->
      <div class="footer-content">
        <div class="footer-links">
          <div class="link-column">
            <h4>About Us</h4>
            <ul>
              <li><a href="#">About Travus</a></li>
              <li><a href="#">Travus 사람들</a></li>
              <li><a href="#">우리의 철학</a></li>
              <li><a href="#">기업문화</a></li>
            </ul>
          </div>

          <div class="link-column">
            <h4>Work</h4>
            <ul>
              <li><a href="#">Portfolio</a></li>
              <li><a href="#">Service</a></li>
              <li><a href="#">AI Image</a></li>
            </ul>
          </div>

          <div class="link-column">
            <h4>Solution</h4>
            <ul>
              <li><a href="#">3D Lab 🔗</a></li>
              <li><a href="#">기업전용 CMS</a></li>
              <li><a href="#">의료전용 CMS</a></li>
              <li><a href="#">팝플전용 CMS</a></li>
              <li><a href="#">기타 솔루션</a></li>
            </ul>
          </div>

          <div class="link-column">
            <h4>Project</h4>
            <ul>
              <li><a href="#">FAQ</a></li>
              <li><a href="#">프로젝트 문의</a></li>
              <li><a href="#">프로젝트 게시판 🔗</a></li>
            </ul>
          </div>

          <div class="link-column">
            <h4>Community</h4>
            <ul>
              <li><a href="#">새소식</a></li>
              <li><a href="#">뉴스레터</a></li>
              <li><a href="#">1:1문의</a></li>
              <li><a href="#">상시채용</a></li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 하단 영역: 뉴스레터 + 큰 로고 -->
      <div class="footer-bottom-section">
        <!-- 뉴스레터 구독 -->
        <div class="newsletter-section">
          <h3 class="newsletter-title">뉴스레터 구독</h3>
          <form class="newsletter-form" @submit.prevent="subscribeNewsletter">
            <input type="email" placeholder="Your email address" class="newsletter-input" />
            <button type="submit" class="newsletter-submit" aria-label="구독하기">→</button>
          </form>
        </div>

        <!-- 큰 로고 -->
        <div class="large-logo">TRAVUS</div>
      </div>

      <!-- 최하단: 회사 정보 -->
      <div class="footer-bottom">
        <div class="copyright">© 2024 TRAVUS</div>
        <div class="footer-tags">
          <span>여성기업</span>
          <span>벤처기업</span>
          <span>기술전환위원증기업</span>
          <span>산업디자인전문기업</span>
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
        <div class="rotating-text">
          <svg viewBox="0 0 200 200" class="circular-text">
            <defs>
              <path
                id="circlePath"
                d="M 100, 100 m -75, 0 a 75,75 0 1,1 150,0 a 75,75 0 1,1 -150,0"
              />
            </defs>
            <text class="rotating-svg-text">
              <textPath href="#circlePath">
                Travus · Travus · Travus · Travus · Travus · Travus ·
              </textPath>
            </text>
          </svg>
        </div>
        <img src="../assets/topbtn.png" alt="Top Button" class="center-character" />
      </button>
    </div>
  </footer>
</template>

<script setup>
const emit = defineEmits(['focus'])

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const subscribeNewsletter = () => {
  alert('뉴스레터 구독이 완료되었습니다!')
}

const handleFocus = (event) => {
  const text =
    event.target.getAttribute('data-text') ||
    event.target.getAttribute('aria-label') ||
    event.target.innerText
  emit('focus', text)
}
</script>

<style scoped>
.footer-section {
  background: #f5f5f5;
  color: #000;
  padding: 3rem 2rem 2rem;
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

/* 상단 영역 - 소셜 아이콘 & 연락처 + 메뉴 */
.footer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ddd;
  margin-bottom: 3rem;
}

.left-section {
  display: flex;
  gap: 3rem;
  align-items: center;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-icon {
  width: 45px;
  height: 45px;
  border: 1px solid #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: #000;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.social-icon:hover {
  background: #000;
  color: #fff;
  transform: translateY(-3px);
}

.contact-info {
  display: flex;
  gap: 2rem;
  font-size: 0.95rem;
}

.contact-info strong {
  font-weight: 700;
}

.top-menu {
  display: flex;
  gap: 3rem;
}

.menu-item {
  text-decoration: none;
  color: #000;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.menu-item:hover {
  color: #666;
}

/* 중간 영역 - 메뉴 링크 */
.footer-content {
  margin-bottom: 3rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 3rem;
}

.link-column h4 {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  color: #000;
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
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
  font-size: 0.95rem;
}

.link-column a:hover {
  color: #000;
  transform: translateX(3px);
}

/* 하단 영역 - 뉴스레터 + 큰 로고 */
.footer-bottom-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-bottom: 3rem;
  border-bottom: 1px solid #ddd;
  margin-bottom: 2rem;
  position: relative;
}

.newsletter-section {
  flex-shrink: 0;
}

.newsletter-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #000;
}

.newsletter-form {
  display: flex;
  max-width: 400px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 25px;
  overflow: hidden;
}

.newsletter-input {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  outline: none;
  font-size: 0.95rem;
}

.newsletter-submit {
  background: #fff;
  border: none;
  padding: 0 1.5rem;
  cursor: pointer;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.newsletter-submit:hover {
  background: #f0f0f0;
}

.large-logo {
  font-size: 8rem;
  font-weight: 900;
  letter-spacing: -0.05em;
  color: #000;
  line-height: 1;
  position: absolute;
  right: 0;
  bottom: 3rem;
}

/* 최하단 - 회사 정보 */
.footer-bottom {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  padding-top: 1rem;
}

.copyright {
  font-size: 0.85rem;
  color: #666;
}

.footer-tags {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.footer-tags span {
  font-size: 0.85rem;
  color: #666;
}

.scroll-to-top {
  position: fixed;
  bottom: 3rem;
  right: 3rem;
  width: 150px;
  height: 150px;
  background: white;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  overflow: visible;
}

.scroll-to-top:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.3);
}


.rotating-text {
  position: absolute;
  width: 100%;
  height: 100%;
  animation: rotate 20s linear infinite;
}

.circular-text {
  width: 100%;
  height: 100%;
}

.rotating-svg-text {
  fill: #9b8854;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 2.5px;
}

.center-character {
  position: relative;
  width: 80px;
  height: 80px;
  z-index: 1;
  object-fit: contain;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .large-logo {
    font-size: 6rem;
    bottom: 2rem;
  }
}

@media (max-width: 1024px) {
  .footer-top {
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
  }

  .top-menu {
    width: 100%;
    justify-content: space-between;
  }

  .footer-links {
    grid-template-columns: repeat(3, 1fr);
  }

  .large-logo {
    font-size: 5rem;
    position: static;
    margin-top: 2rem;
  }

  .footer-bottom-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .left-section {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
  }

  .top-menu {
    flex-direction: column;
    gap: 1rem;
  }

  .footer-links {
    grid-template-columns: 1fr;
  }

  .large-logo {
    font-size: 3rem;
  }

  .scroll-to-top {
    bottom: 2rem;
    right: 2rem;
    width: 80px;
    height: 80px;
  }

  .center-character {
    width: 50px;
    height: 50px;
  }

  .rotating-svg-text {
    font-size: 10px;
    letter-spacing: 1px;
  }
}
</style>
