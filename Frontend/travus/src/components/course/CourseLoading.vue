<template>
  <div class="course-loading">
    <div class="loading-content">
      <div class="robot-animation">
        <svg viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg">
          <!-- 로봇 몸체 -->
          <g class="robot-body">
            <!-- 그림자 -->
            <ellipse cx="100" cy="220" rx="60" ry="12" fill="#E0E7FF" opacity="0.5"/>

            <!-- 머리 -->
            <rect x="70" y="50" width="60" height="70" rx="30" fill="white" stroke="#667eea" stroke-width="3"/>

            <!-- 안테나 -->
            <line x1="100" y1="50" x2="100" y2="35" stroke="#667eea" stroke-width="3" class="antenna"/>
            <circle cx="100" cy="35" r="5" fill="#667eea" class="antenna-tip"/>

            <!-- 눈 (깜빡임) -->
            <g class="eyes">
              <circle cx="85" cy="75" r="6" fill="#667eea"/>
              <circle cx="115" cy="75" r="6" fill="#667eea"/>
            </g>

            <!-- 입 -->
            <path d="M 80 95 Q 100 105 120 95" stroke="#667eea" stroke-width="3" fill="none"/>

            <!-- 몸통 -->
            <rect x="65" y="125" width="70" height="80" rx="10" fill="white" stroke="#667eea" stroke-width="3"/>

            <!-- 팔 -->
            <g class="arms">
              <rect x="50" y="135" width="15" height="40" rx="7" fill="white" stroke="#667eea" stroke-width="2" class="left-arm"/>
              <rect x="135" y="135" width="15" height="40" rx="7" fill="white" stroke="#667eea" stroke-width="2" class="right-arm"/>
            </g>

            <!-- 다리 -->
            <rect x="75" y="205" width="20" height="30" rx="5" fill="white" stroke="#667eea" stroke-width="2"/>
            <rect x="105" y="205" width="20" height="30" rx="5" fill="white" stroke="#667eea" stroke-width="2"/>

            <!-- 디테일 -->
            <circle cx="100" cy="150" r="8" fill="#667eea" opacity="0.3"/>
            <circle cx="100" cy="175" r="5" fill="#667eea" opacity="0.3"/>
          </g>
        </svg>
      </div>

      <h2 class="loading-title">AI가 여행 코스를 생성하고 있어요</h2>
      <p class="loading-message">{{ loadingMessage }}</p>

      <div class="loading-bar">
        <div class="loading-progress"></div>
      </div>

      <div class="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loadingMessages = [
  '선택하신 지역을 분석하고 있어요...',
  '최적의 여행지를 찾고 있어요...',
  '동선을 고려한 일정을 만들고 있어요...',
  '맞춤 여행 코스를 완성하고 있어요...'
]

const loadingMessage = ref(loadingMessages[0])
let messageIndex = 0

onMounted(() => {
  const interval = setInterval(() => {
    messageIndex = (messageIndex + 1) % loadingMessages.length
    loadingMessage.value = loadingMessages[messageIndex]
  }, 2000)

  return () => clearInterval(interval)
})
</script>

<style scoped>
.course-loading {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 20px 40px;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: white;
}

.robot-animation {
  width: 200px;
  height: 250px;
  margin-bottom: 2rem;
}

.robot-animation svg {
  width: 100%;
  height: 100%;
}

/* 로봇 애니메이션 */
.robot-body {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.antenna {
  animation: antenna-wave 2s ease-in-out infinite;
  transform-origin: 100px 50px;
}

@keyframes antenna-wave {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-10deg);
  }
  75% {
    transform: rotate(10deg);
  }
}

.antenna-tip {
  animation: antenna-glow 1.5s ease-in-out infinite;
}

@keyframes antenna-glow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

.eyes {
  animation: blink 4s infinite;
}

@keyframes blink {
  0%, 48%, 52%, 100% {
    transform: scaleY(1);
  }
  50% {
    transform: scaleY(0.1);
  }
}

.left-arm {
  animation: wave-left 2s ease-in-out infinite;
  transform-origin: 57.5px 155px;
}

.right-arm {
  animation: wave-right 2s ease-in-out infinite;
  transform-origin: 142.5px 155px;
}

@keyframes wave-left {
  0%, 100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(-15deg);
  }
}

@keyframes wave-right {
  0%, 100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(15deg);
  }
}

.loading-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
}

.loading-message {
  font-size: 1.125rem;
  margin: 0 0 2rem 0;
  opacity: 0.9;
  min-height: 1.5em;
  animation: fade-in 0.5s ease-in-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 0.9;
  }
}

.loading-bar {
  width: 300px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.loading-progress {
  height: 100%;
  background: white;
  border-radius: 3px;
  animation: progress 2s ease-in-out infinite;
}

@keyframes progress {
  0% {
    width: 0%;
  }
  50% {
    width: 70%;
  }
  100% {
    width: 100%;
  }
}

.loading-dots {
  display: flex;
  gap: 0.5rem;
}

.loading-dots span {
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  animation: dot-bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes dot-bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .robot-animation {
    width: 150px;
    height: 187.5px;
  }

  .loading-title {
    font-size: 1.5rem;
  }

  .loading-message {
    font-size: 1rem;
  }

  .loading-bar {
    width: 250px;
  }
}
</style>
