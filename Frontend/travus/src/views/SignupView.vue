<template>
  <div class="signup-view">
    <NavigationBar
      :is-t-t-s-enabled="isTTSEnabled"
      @toggle-tts="toggleTTS"
      @focus="handleFocus"
    />
    <div class="signup-card">
      <form class="signup-form" @submit.prevent="handleSubmit">
        <div class="signup-row">
          <label class="input-label" :class="{ 'input-error': usernameError, 'input-success': usernameAvailable }">
            <i class="fa-regular fa-user input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="text"
              placeholder="아이디"
              autocomplete="username"
              v-model="form.username"
              @input="checkUsername"
              @focus="handleFocus"
              aria-label="아이디"
            />
            <span v-if="checkingUsername" class="input-suffix">확인중...</span>
            <span v-else-if="usernameAvailable" class="input-suffix success">사용 가능</span>
            <span v-else-if="usernameError" class="input-suffix error">{{ usernameError }}</span>
          </label>
        </div>

        <div class="signup-row">
          <label class="input-label">
            <i class="fa-regular fa-lock input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="password"
              placeholder="비밀번호"
              autocomplete="new-password"
              v-model="form.password"
              @focus="handleFocus"
              aria-label="비밀번호"
            />
          </label>
        </div>

        <div class="signup-row">
          <label class="input-label">
            <i class="fa-regular fa-envelope input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="email"
              placeholder="[선택] 이메일주소 (비밀번호 찾기 등 본인 확인용)"
              autocomplete="email"
              v-model="form.email"
              @focus="handleFocus"
              aria-label="이메일"
            />
          </label>
        </div>

        <div class="signup-row">
          <label class="input-label">
            <i class="fa-regular fa-id-card input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="text"
              placeholder="이름"
              autocomplete="name"
              v-model="form.name"
              @focus="handleFocus"
              aria-label="이름"
            />
          </label>
        </div>

        <div class="signup-row">
          <label class="input-label">
            <i class="fa-regular fa-calendar input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="date"
              v-model="form.birth"
              @focus="handleFocus"
              aria-label="생년월일"
              max="9999-12-31"
            />
          </label>
        </div>

        <div class="signup-row">
          <div class="gender-group">
            <button
              type="button"
              class="gender-btn"
              :class="{ active: form.gender === 'M' }"
              @click="form.gender = 'M'"
              @focus="handleFocus"
              aria-label="남자"
            >
              남자
            </button>
            <button
              type="button"
              class="gender-btn"
              :class="{ active: form.gender === 'F' }"
              @click="form.gender = 'F'"
              @focus="handleFocus"
              aria-label="여자"
            >
              여자
            </button>
          </div>
        </div>


        <div class="signup-row">
          <label class="input-label">
            <i class="fa-solid fa-mobile-screen input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="tel"
              placeholder="휴대전화번호 (예: 01012345678)"
              autocomplete="tel"
              v-model="form.phone"
              @focus="handleFocus"
              aria-label="휴대전화번호"
              maxlength="11"
            />
          </label>
        </div>

        <p v-if="errorMessage" class="signup-error" role="alert">
          {{ errorMessage }}
        </p>

        <button class="signup-submit" type="submit" @focus="handleFocus" aria-label="가입하기">
          가입하기
        </button>
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
  email: '',
  name: '',
  birth: '',
  gender: '',
  phone: ''
})

const errorMessage = ref('')
const checkingUsername = ref(false)
const usernameAvailable = ref(false)
const usernameError = ref('')
let usernameCheckTimeout = null

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

// 아이디 중복 체크
const checkUsername = async () => {
  const username = form.username.trim()

  // 초기화
  usernameAvailable.value = false
  usernameError.value = ''

  if (!username) {
    return
  }

  // 아이디 유효성 검사 (4-20자, 영문+숫자)
  if (username.length < 4 || username.length > 20) {
    usernameError.value = '4-20자로 입력해주세요'
    return
  }

  if (!/^[a-zA-Z0-9]+$/.test(username)) {
    usernameError.value = '영문과 숫자만 사용 가능합니다'
    return
  }

  // 디바운스: 500ms 후에 API 호출
  clearTimeout(usernameCheckTimeout)
  usernameCheckTimeout = setTimeout(async () => {
    try {
      checkingUsername.value = true
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

      // 백엔드에 아이디 중복 체크 API 호출
      const response = await axios.get(`${API_BASE_URL}/auth/check-username/`, {
        params: { username }
      })

      if (response.data.available) {
        usernameAvailable.value = true
        usernameError.value = ''
      } else {
        usernameAvailable.value = false
        usernameError.value = '이미 사용중인 아이디입니다'
      }
    } catch (error) {
      console.error('아이디 중복 체크 실패:', error)
      // 중복 체크 실패 시 무시 (서버 에러)
      usernameError.value = ''
    } finally {
      checkingUsername.value = false
    }
  }, 500)
}

const handleSubmit = async () => {
  errorMessage.value = ''

  // 필수 입력 검증
  if (!form.username || !form.password) {
    errorMessage.value = '아이디와 비밀번호를 입력해 주세요.'
    speak(errorMessage.value)
    return
  }

  if (!form.name) {
    errorMessage.value = '이름을 입력해 주세요.'
    speak(errorMessage.value)
    return
  }

  if (!form.phone) {
    errorMessage.value = '휴대전화번호를 입력해 주세요.'
    speak(errorMessage.value)
    return
  }

  if (!form.gender) {
    errorMessage.value = '성별을 선택해 주세요.'
    speak(errorMessage.value)
    return
  }

  // 아이디 사용 가능 여부 확인
  if (!usernameAvailable.value) {
    errorMessage.value = '사용 가능한 아이디인지 확인해주세요.'
    speak(errorMessage.value)
    return
  }

  try {
    // 백엔드 회원가입 API 호출
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
    const response = await axios.post(`${API_BASE_URL}/auth/signup/`, {
      username: form.username.trim(),
      password: form.password,
      name: form.name,
      phone: form.phone,
      email: form.email || '',
      birth: form.birth || '',
      gender: form.gender
    })

    speak('회원가입이 완료되었습니다')
    router.push('/login')
  } catch (error) {
    console.error('회원가입 실패:', error)

    const message = error.response?.data?.error ||
                   error.response?.data?.username?.[0] ||
                   error.response?.data?.detail ||
                   '회원가입에 실패했습니다. 다시 시도해주세요.'

    errorMessage.value = message
    speak(message)
  }
}
</script>

<style scoped>
.signup-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  padding: 6rem 1rem 2rem;
}

.signup-card {
  width: 540px;
  max-width: 100%;
  background: #ffffff;
  border-radius: 18px;
  padding: 2.2rem 2.2rem 2rem;
  box-shadow: 0 24px 50px rgba(15, 23, 42, 0.18);
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.signup-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  border: 1.5px solid #d1d5db;
  border-radius: 10px;
  padding: 0.75rem 0.9rem;
  transition: border-color 0.2s;
}

.input-label.input-error {
  border-color: #ef4444;
}

.input-label.input-success {
  border-color: #10b981;
}

.input-icon {
  font-size: 1.1rem;
  width: 1.2rem;
  text-align: center;
}

.signup-input {
  flex: 1;
  border: none;
  font-size: 0.95rem;
  background: transparent;
}

.signup-input:focus {
  outline: none;
}

.input-suffix {
  color: #9ca3af;
  font-size: 0.85rem;
  white-space: nowrap;
}

.input-suffix.success {
  color: #10b981;
  font-weight: 600;
}

.input-suffix.error {
  color: #ef4444;
  font-weight: 600;
}

.gender-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.gender-btn {
  padding: 0.6rem 0;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  background: #ffffff;
  cursor: pointer;
  font-size: 0.9rem;
}

.gender-btn.active {
  border-color: #a08077;
  color: #a08077;
  font-weight: 700;
}

.signup-error {
  margin: 0.2rem 0 0;
  color: #ef4444;
  font-size: 0.9rem;
}

.signup-submit {
  margin-top: 0.6rem;
  padding: 0.85rem 1rem;
  border: none;
  border-radius: 10px;
  background: #a08077;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
}

@media (max-width: 480px) {
  .signup-card {
    padding: 1.8rem 1.4rem 1.6rem;
  }
}
</style>
