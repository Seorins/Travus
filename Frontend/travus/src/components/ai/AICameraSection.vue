<template>
  <section class="ai-camera-section" tabindex="0" @focus="handleFocus">
    <div class="ai-camera-container">
      <div class="content-wrapper">
        <div class="text-content">
          <h2 class="section-title" data-text="AI 카메라로 여행하기">
            AI 카메라로 여행하기
          </h2>
          <p class="section-subtitle">Explore with AI Camera</p>

          <div class="feature-description">
            <p class="main-text">QR을 찍고 AI와 함께 여행지를 탐색하세요</p>

            <ul class="feature-list">
              <li tabindex="0" @focus="handleFeatureFocus">
                <span class="feature-icon">📸</span>
                <div class="feature-text">
                  <strong>실시간 이미지 인식</strong>
                  <p>카메라로 찍은 여행지를 AI가 즉시 분석하고 설명합니다</p>
                </div>
              </li>
              <li tabindex="0" @focus="handleFeatureFocus">
                <span class="feature-icon">🗣️</span>
                <div class="feature-text">
                  <strong>음성 안내</strong>
                  <p>시각장애인을 위한 상세한 음성 설명을 제공합니다</p>
                </div>
              </li>
              <li tabindex="0" @focus="handleFeatureFocus">
                <span class="feature-icon">🔍</span>
                <div class="feature-text">
                  <strong>상세 정보 제공</strong>
                  <p>역사, 문화, 접근성 정보를 AI가 분석하여 제공합니다</p>
                </div>
              </li>
              <li tabindex="0" @focus="handleFeatureFocus">
                <span class="feature-icon">💬</span>
                <div class="feature-text">
                  <strong>대화형 안내</strong>
                  <p>궁금한 점을 물어보면 AI가 실시간으로 답변합니다</p>
                </div>
              </li>
            </ul>

            <button class="cta-button" tabindex="0" @focus="handleFocus">
              지금 체험하기 →
            </button>
          </div>
        </div>

        <div class="phone-mockup">
          <div class="phone-container">
            <div class="phone-frame">
              <div class="phone-screen">
                <div class="screen-content">
                  <div class="camera-interface">
                    <div class="camera-header">
                      <span class="camera-title">TravUs AI Camera</span>
                      <span class="camera-status">●</span>
                    </div>
                    <div class="camera-viewfinder">
                      <div class="scan-line"></div>
                      <div class="focus-box"></div>
                      <div class="qr-icon">📷</div>
                    </div>
                    <div class="camera-info">
                      <p>QR 코드를 스캔하거나</p>
                      <p>여행지를 촬영하세요</p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="phone-notch"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const emit = defineEmits(['focus'])

const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}

const handleFeatureFocus = (event) => {
  const strong = event.currentTarget.querySelector('strong')
  const p = event.currentTarget.querySelector('p')
  const text = `${strong?.innerText}. ${p?.innerText}`
  emit('focus', text)
}
</script>

<style scoped>
.ai-camera-section {
  min-height: 100vh;
  background: url('@/assets/ai-camera-bg.png') center/cover no-repeat;
  padding: 6rem 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-camera-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.ai-camera-container {
  max-width: 1400px;
  width: 100%;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.text-content {
  color: #2d3748;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.section-subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  opacity: 0.8;
  margin-bottom: 2rem;
}

.main-text {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 2rem;
  line-height: 1.4;
  color: #ffffff;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
}

.feature-list li {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.feature-list li:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateX(10px);
}

.feature-list li:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
  background: rgba(255, 255, 255, 1);
}

.feature-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.feature-text strong {
  display: block;
  font-size: 1.3rem;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.feature-text p {
  color: #4a5568;
  line-height: 1.6;
  margin: 0;
}

.cta-button {
  background: #667eea; /* 보라색 단색 */
  color: white;
  border: none;
  padding: 1.2rem 2.5rem;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.cta-button:focus {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
}

.phone-mockup {
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1000px;
}

.phone-container {
  animation: phoneRotate 6s ease-in-out infinite;
  transform-style: preserve-3d;
}

.phone-frame {
  width: 320px;
  height: 650px;
  background: #1a1a1a;
  border-radius: 40px;
  padding: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
}

.phone-notch {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 30px;
  background: #1a1a1a;
  border-radius: 0 0 20px 20px;
  z-index: 10;
}

.phone-screen {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 32px;
  overflow: hidden;
}

.screen-content {
  width: 100%;
  height: 100%;
  background: #667eea; /* 보라색 단색 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-interface {
  color: white;
  text-align: center;
  width: 100%;
  padding: 2rem;
}

.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.camera-title {
  font-weight: 600;
  font-size: 1.1rem;
}

.camera-status {
  color: #ff4444;
  animation: blink 2s infinite;
}

.camera-viewfinder {
  width: 100%;
  height: 300px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
  position: relative;
  margin-bottom: 1.5rem;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, #00ff00, transparent);
  animation: scan 2s ease-in-out infinite;
}

.focus-box {
  width: 150px;
  height: 150px;
  border: 3px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  position: relative;
  animation: focusPulse 2s ease-in-out infinite;
}

.focus-box::before,
.focus-box::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border: 3px solid white;
}

.focus-box::before {
  top: -3px;
  left: -3px;
  border-right: none;
  border-bottom: none;
}

.focus-box::after {
  bottom: -3px;
  right: -3px;
  border-left: none;
  border-top: none;
}

.qr-icon {
  font-size: 4rem;
  position: absolute;
}

.camera-info p {
  margin: 0.25rem 0;
  font-size: 1rem;
  opacity: 0.9;
}

/* 애니메이션 */
@keyframes phoneRotate {
  0%,
  100% {
    transform: rotateY(-5deg) rotateX(2deg);
  }
  50% {
    transform: rotateY(5deg) rotateX(-2deg);
  }
}

@keyframes scan {
  0% {
    top: 0;
  }
  100% {
    top: 100%;
  }
}

@keyframes focusPulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

@keyframes blink {
  0%,
  50%,
  100% {
    opacity: 1;
  }
  25%,
  75% {
    opacity: 0.3;
  }
}

@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .phone-container {
    transform: scale(0.8);
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }

  .main-text {
    font-size: 1.4rem;
  }

  .phone-frame {
    width: 280px;
    height: 570px;
  }
}
</style>
