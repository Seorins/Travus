<template>
  <div class="course-loading">
    <div class="loading-content">
      <div class="loading-animation">
        <img src="@/assets/loading.png" alt="로딩 중" class="loading-img" />
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

.loading-animation {
  width: 300px;
  height: 300x;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  animation: float-spin 3s ease-in-out infinite;
}

@keyframes float-spin {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
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
  .loading-animation {
    width: 180px;
    height: 180px;
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
