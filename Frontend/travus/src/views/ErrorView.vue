<template>
  <div class="error-page">
    <div class="error-container">
      <!-- 좌측: 이미지 영역 -->
      <div class="error-left">
        <div class="image-wrapper">
          <img
            :src="errorImage"
            alt="Error"
            class="error-image"
          />
        </div>
      </div>

      <!-- 우측: 텍스트 및 버튼 영역 -->
      <div class="error-right">
        <div class="error-content">
          <div class="error-badge">{{ errorCode }}</div>
          <h1 class="error-title">{{ errorTitle }}</h1>
          <p class="error-message">{{ errorMessage }}</p>

          <div class="error-actions">
            <button @click="goHome" class="btn-home">
              <i class="fa fa-home"></i>
              <span>홈으로 가기</span>
            </button>
            <button @click="goBack" class="btn-back">
              <i class="fa fa-arrow-left"></i>
              <span>이전 페이지</span>
            </button>
          </div>

          <div class="error-suggestions">
            <p class="suggestions-title">이런 경우를 확인해보세요</p>
            <ul class="suggestions-list">
              <li>주소를 정확하게 입력했는지 확인해주세요</li>
              <li>페이지가 이동되었거나 삭제되었을 수 있습니다</li>
              <li>네트워크 연결 상태를 확인해주세요</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import errorImage from '@/assets/error.png'

const router = useRouter()
const route = useRoute()

const errorCode = ref('404')
const errorTitle = ref('페이지를 찾을 수 없습니다')
const errorMessage = ref('요청하신 페이지가 존재하지 않거나 이동되었습니다.')

onMounted(() => {
  // 라우트 쿼리에서 에러 타입 확인
  const errorType = route.query.type || '404'

  if (errorType === '404') {
    errorCode.value = '404'
    errorTitle.value = '페이지를 찾을 수 없습니다'
    errorMessage.value = '요청하신 페이지가 존재하지 않거나 이동되었습니다.'
  } else if (errorType === '500') {
    errorCode.value = '500'
    errorTitle.value = '서버 오류가 발생했습니다'
    errorMessage.value = '일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
  } else if (errorType === 'network') {
    errorCode.value = 'ERR'
    errorTitle.value = '네트워크 오류'
    errorMessage.value = '네트워크 연결을 확인하고 다시 시도해주세요.'
  } else {
    errorCode.value = 'ERR'
    errorTitle.value = '오류가 발생했습니다'
    errorMessage.value = '알 수 없는 오류가 발생했습니다. 다시 시도해주세요.'
  }
})

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  background: #ffffff;
}

.error-container {
  display: flex;
  min-height: 100vh;
  max-width: 1400px;
  margin: 0 auto;
}

/* 좌측 이미지 영역 */
.error-left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 60px;
}

.image-wrapper {
  max-width: 600px;
  width: 100%;
}

.error-image {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.1));
}

/* 우측 텍스트 영역 */
.error-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: white;
}

.error-content {
  max-width: 500px;
  width: 100%;
}

.error-badge {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, #00C73C 0%, #00a832 100%);
  color: white;
  font-size: 28px;
  font-weight: 800;
  border-radius: 12px;
  margin-bottom: 32px;
  box-shadow: 0 4px 16px rgba(0, 199, 60, 0.3);
  letter-spacing: 2px;
}

.error-title {
  font-size: 48px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  line-height: 1.2;
}

.error-message {
  font-size: 18px;
  color: #666;
  line-height: 1.8;
  margin: 0 0 48px 0;
}

.error-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
}

.btn-home,
.btn-back {
  flex: 1;
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.btn-home {
  background: #00C73C;
  color: white;
  box-shadow: 0 4px 16px rgba(0, 199, 60, 0.3);
}

.btn-home:hover {
  background: #00a832;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 199, 60, 0.4);
}

.btn-back {
  background: #f8f9fa;
  color: #333;
  border: 2px solid #e9ecef;
}

.btn-back:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-home i,
.btn-back i {
  font-size: 20px;
}

/* 제안 섹션 */
.error-suggestions {
  padding: 24px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #00C73C;
}

.suggestions-title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  margin: 0 0 16px 0;
}

.suggestions-list {
  margin: 0;
  padding-left: 20px;
  list-style: none;
}

.suggestions-list li {
  position: relative;
  font-size: 14px;
  color: #666;
  line-height: 2;
  padding-left: 20px;
}

.suggestions-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #00C73C;
  font-size: 18px;
  font-weight: bold;
}

/* 반응형 */
@media (max-width: 1024px) {
  .error-container {
    flex-direction: column;
  }

  .error-left,
  .error-right {
    padding: 40px 24px;
  }

  .error-left {
    min-height: 400px;
  }

  .error-title {
    font-size: 36px;
  }

  .error-badge {
    font-size: 24px;
    padding: 10px 20px;
  }
}

@media (max-width: 768px) {
  .error-left {
    min-height: 300px;
    padding: 40px 20px;
  }

  .error-right {
    padding: 40px 20px;
  }

  .error-title {
    font-size: 28px;
  }

  .error-message {
    font-size: 16px;
  }

  .error-badge {
    font-size: 20px;
    padding: 8px 16px;
  }

  .error-actions {
    flex-direction: column;
  }

  .btn-home,
  .btn-back {
    width: 100%;
  }

  .suggestions-list li {
    font-size: 13px;
  }
}
</style>
