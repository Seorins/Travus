<template>
  <div class="login-view">
    <NavigationBar
      :is-t-t-s-enabled="isTTSEnabled"
      @toggle-tts="toggleTTS"
      @focus="handleFocus"
    />
    <div class="login-card">
      <h1 class="login-title">로그인</h1>

      <form class="login-form" @submit.prevent="handleSubmit">
        <input
          class="login-input"
          type="text"
          placeholder="아이디 또는 전화번호"
          autocomplete="username"
          v-model="form.username"
          @focus="handleFocus"
          aria-label="아이디 또는 전화번호"
        />
        <input
          class="login-input"
          type="password"
          placeholder="비밀번호"
          autocomplete="current-password"
          v-model="form.password"
          @focus="handleFocus"
          aria-label="비밀번호"
        />

        <div class="login-options">
          <label class="keep-login">
            <input type="checkbox" v-model="form.keep" />
            <span @focus="handleFocus" tabindex="0">로그인 상태 유지</span>
          </label>
        </div>

        <button
          class="login-submit"
          type="submit"
          @focus="handleFocus"
          aria-label="로그인"
        >
          로그인
        </button>

        <p v-if="errorMessage" class="login-error" role="alert">
          {{ errorMessage }}
        </p>

        
        <div class="login-links">
          <button
            class="text-link"
            type="button"
            @focus="handleFocus"
            aria-label="비밀번호 찾기"
          >
            비밀번호 찾기
          </button>
          <span class="link-separator">|</span>
          <button
            class="text-link"
            type="button"
            @focus="handleFocus"
            aria-label="아이디 찾기"
          >
            아이디 찾기
          </button>
          <span class="link-separator">|</span>
          <router-link class="text-link" to="/signup" @focus="handleFocus" aria-label="회원가입">
            회원가입
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTTS } from '@/composables/useTTS'
import { useAuthStore } from '@/stores/auth'
import NavigationBar from '@/components/common/NavigationBar.vue'
import axios from 'axios'

const { isTTSEnabled, speak, toggleTTS: ttsToggle } = useTTS()
const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
  keep: true,
  ipSecurity: true
})

const errorMessage = ref('')

const toggleTTS = () => {
  ttsToggle()
  speak(isTTSEnabled.value ? 'TTS가 켜졌습니다' : 'TTS가 꺼졌습니다')
}

const handleFocus = (payload) => {
  const text = typeof payload === 'string'
    ? payload
    : payload?.target?.innerText ||
      payload?.target?.getAttribute('aria-label') ||
      payload?.target?.getAttribute('placeholder') ||
      ''

  if (text && isTTSEnabled.value) {
    speak(text)
  }
}

const handleSubmit = async () => {
  errorMessage.value = ''

  try {
    // 백엔드 로그인 API 호출
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
    const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
      username: form.username.trim(),
      password: form.password
    })

    // JWT 토큰 저장
    const { access, refresh, user } = response.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    // auth store 업데이트 (로컬 상태 동기화)
    authStore.currentUser = user
    authStore.isLoggedIn = true

    speak('로그인 성공')
    router.push('/')
  } catch (error) {
    console.error('로그인 실패:', error)

    const message = error.response?.data?.error ||
                   error.response?.data?.detail ||
                   '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.'

    errorMessage.value = message
    speak(message)
  }
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  padding: 6rem 1rem 2rem;
}

.login-card {
  width: 640px;
  max-width: 100%;
  background: #ffffff;
  border-radius: 20px;
  padding: 3.6rem 3.4rem 3rem;
  box-shadow: 0 24px 50px rgba(15, 23, 42, 0.18);
}

.login-title {
  margin: 0 0 1.5rem;
  font-size: 2.4rem;
  font-weight: 700;
  color: #111827;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

.login-input {
  width: 100%;
  padding: 1.4rem 1.5rem;
  border-radius: 12px;
  border: 1.6px solid #d1d5db;
  font-size: 1.2rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.login-input:focus {
  outline: none;
  border-color: #a08077;
  box-shadow: 0 0 0 2px rgba(47, 158, 68, 0.15);
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.1rem;
  color: #4b5563;
  margin: 0.2rem 0 0.4rem;
}

.keep-login {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.ip-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.ip-label {
  font-weight: 600;
  color: #4b5563;
}

.ip-checkbox {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.toggle-pill {
  min-width: 70px;
  height: 32px;
  padding: 0 0.5rem;
  border-radius: 999px;
  background: #2f9e44;
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  font-weight: 700;
  transition: background 0.2s ease;
}

.ip-checkbox:not(:checked) + .toggle-pill {
  background: #9ca3af;
}

.login-submit {
  width: 100%;
  padding: 1.35rem 1.5rem;
  border: none;
  border-radius: 12px;
  background: #a08077;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  cursor: pointer;
}

.login-error {
  margin: 0;
  color: #ef4444;
  font-size: 1rem;
}

.login-divider {
  position: relative;
  text-align: center;
  font-size: 1rem;
  color: #9ca3af;
  margin: 0.4rem 0 0.1rem;
}

.login-divider::before,
.login-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 34%;
  height: 1px;
  background: #e5e7eb;
}

.login-divider::before {
  left: 0;
}

.login-divider::after {
  right: 0;
}

.passkey-button {
  width: 100%;
  padding: 1.2rem 1.5rem;
  border-radius: 12px;
  border: 1.6px solid #2f9e44;
  background: #ffffff;
  color: #2f9e44;
  font-weight: 700;
  cursor: pointer;
}

.login-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.6rem;
  font-size: 1rem;
  color: #6b7280;
}

.text-link {
  border: none;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  text-decoration: none;
}

.text-link:hover {
  color: #2f9e44;
}

.link-separator {
  color: #d1d5db;
}

@media (max-width: 480px) {
  .login-card {
    padding: 2.8rem 2.2rem 2.4rem;
  }
}
</style>
