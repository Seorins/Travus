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
          <label class="input-label">
            <i class="fa-regular fa-user input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="text"
              placeholder="아이디"
              autocomplete="username"
              v-model="form.username"
              @focus="handleFocus"
              aria-label="아이디"
            />
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
              type="text"
              placeholder="생년월일 8자리"
              v-model="form.birth"
              @focus="handleFocus"
              aria-label="생년월일"
            />
          </label>
        </div>

        <div class="signup-row">
          <div class="gender-group">
            <button
              type="button"
              class="gender-btn"
              :class="{ active: form.gender === 'male' }"
              @click="form.gender = 'male'"
              @focus="handleFocus"
              aria-label="남자"
            >
              남자
            </button>
            <button
              type="button"
              class="gender-btn"
              :class="{ active: form.gender === 'female' }"
              @click="form.gender = 'female'"
              @focus="handleFocus"
              aria-label="여자"
            >
              여자
            </button>
            <button
              type="button"
              class="gender-btn"
              :class="{ active: form.gender === 'none' }"
              @click="form.gender = 'none'"
              @focus="handleFocus"
              aria-label="선택안함"
            >
              선택안함
            </button>
          </div>
        </div>


        <div class="signup-row">
          <label class="input-label">
            <i class="fa-solid fa-globe input-icon" aria-hidden="true"></i>
            <select
              class="signup-input"
              v-model="form.country"
              @focus="handleFocus"
              aria-label="국가"
            >
              <option value="KR">대한민국 +82</option>
              <option value="US">미국 +1</option>
              <option value="JP">일본 +81</option>
            </select>
          </label>
        </div>

        <div class="signup-row">
          <label class="input-label">
            <i class="fa-solid fa-mobile-screen input-icon" aria-hidden="true"></i>
            <input
              class="signup-input"
              type="tel"
              placeholder="휴대전화번호"
              autocomplete="tel"
              v-model="form.phone"
              @focus="handleFocus"
              aria-label="휴대전화번호"
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

const { isTTSEnabled, speak, toggleTTS: ttsToggle } = useTTS()
const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
  email: '',
  name: '',
  birth: '',
  gender: 'none',
  country: 'KR',
  phone: ''
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

const handleSubmit = () => {
  errorMessage.value = ''

  if (!form.username || !form.password) {
    errorMessage.value = '아이디와 비밀번호를 입력해 주세요.'
    speak(errorMessage.value)
    return
  }

  const result = authStore.signUp({
    username: form.username.trim(),
    password: form.password,
    name: form.name,
    phone: form.phone,
    email: form.email,
    birth: form.birth.trim(),
    gender: form.gender
  })

  if (!result.ok) {
    errorMessage.value = result.message
    speak(result.message)
    return
  }

  router.push('/login')
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
}

.gender-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
