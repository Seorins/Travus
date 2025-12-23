<template>
  <div class="mypage-view">
    <NavigationBar
      :is-t-t-s-enabled="isTTSEnabled"
      @toggle-tts="toggleTTS"
      @focus="handleFocus"
    />

    <section class="profile-card">
      <div class="profile-top">
        <div class="profile-left">
          <div class="avatar-circle">
            <span class="avatar-icon">👤</span>
          </div>
          <div class="profile-info">
            <h2 class="name">{{ displayName }}</h2>
            <p class="username">@{{ user?.username }}</p>
            <p class="phone" v-if="user?.phone">☎ {{ user.phone }}</p>
          </div>
        </div>

        <div>
          <span class="label">내가 쓴 댓글</span>
          <button class="stat stat-button" type="button" @click="goMyComments" @focus="handleFocus">
            <span class="value">0개</span>
          </button>
        </div>

        <div class="profile-actions">
          <button class="edit-link" type="button" @click="goPersonalInfo" @focus="handleFocus">
            개인정보 수정
          </button>
          
        </div>
      </div>
    </section>

    <section class="reservation">
      <h3>북마크</h3>
      <div class="chips">
        <button
          v-for="chip in chipItems"
          :key="chip.key"
          class="chip"
          :class="{ active: chip.key === activeChip }"
          @click="setActiveChip(chip.key)"
          @focus="handleFocus"
        >
          {{ chip.label }}
        </button>
      </div>
      <div class="empty">
        <div class="empty-icon">📄</div>
        <p>현재 북마크 기록이 없습니다.</p>
      </div>
    </section>

    <footer class="mypage-footer">
      <button class="logout-btn" @click="handleLogout" @focus="handleFocus">로그아웃</button>
    </footer>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import NavigationBar from '@/components/common/NavigationBar.vue'
import { useAuthStore } from '@/stores/auth'
import { useTTS } from '@/composables/useTTS'

const authStore = useAuthStore()
const router = useRouter()
const user = computed(() => authStore.currentUser)
const displayName = computed(() => user.value?.name || user.value?.username || '여행자')
const { isTTSEnabled, speak, toggleTTS } = useTTS()
const activeChip = ref('전체')
const chipItems = [
  { key: '전체', label: '전체(0)' },
  { key: '수도권', label: '수도권(0)' },
  { key: '경상북도', label: '경상북도(0)' },
  { key: '경상남도', label: '경상남도(0)' },
  { key: '충청북도', label: '충청북도(0)' },
  { key: '충청남도', label: '충청남도(0)' },
  { key: '제주', label: '제주(0)' }
]

const goPersonalInfo = () => {
  router.push('/mypage/info')
}

const goMyComments = () => {
  router.push('/mypage/comments')
}

const setActiveChip = (key) => {
  activeChip.value = key
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const handleFocus = (payload) => {
  const text =
    typeof payload === 'string'
      ? payload
      : payload?.target?.innerText ||
        payload?.target?.getAttribute('aria-label') ||
        payload?.target?.getAttribute('placeholder') ||
        ''

  if (text && isTTSEnabled.value) {
    speak(text)
  }
}
</script>

<style scoped>
.mypage-view {
  min-height: 100vh;
  background: #f7f9fb;
  padding: 6rem 1.25rem 2.5rem;
}

.profile-card {
  max-width: 1100px;
  margin: 0 auto 2rem;
  background: #ffffff;
  border-radius: 20px;
  padding: 1.75rem 2rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
}

.profile-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.profile-left {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.profile-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.avatar-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #e8f0fe;
  display: grid;
  place-items: center;
  font-size: 2rem;
  color: #1f2937;
}

.profile-info .name {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.profile-info .username {
  margin: 0.1rem 0;
  color: #6b7280;
}

.profile-info .phone {
  margin: 0;
  color: #4b5563;
  font-weight: 600;
}

.stat {
  text-align: center;
}

.stat-button {
  background: none;
  border: none;
  padding: 0.35rem 0.6rem;
  cursor: pointer;
}

.label {
  display: block;
  color: #6b7280;
  margin-bottom: 0.15rem;
}

.value {
  display: block;
  color: #a08077;
  font-weight: 800;
  font-size: 1.05rem;
  text-decoration: underline;   /* 밑줄 */
  text-underline-offset: 4px;   /* 글씨랑 간격 */
}

.edit-link {
  padding: 0.45rem 1rem;
  border-radius: 12px;
  border: 1.5px solid #a08077;
  background: transparent;
  color: #a08077;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-link:hover {
  background: #fff6f0;
}

.reservation {
  max-width: 1100px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 14px;
  padding: 1.4rem 1.6rem 2rem;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.06);
}

.reservation h3 {
  margin: 0 0 0.8rem;
  font-size: 1.2rem;
  color: #111827;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 1.1rem;
}

.chip {
  border: 1.5px solid #d1d5db;
  background: #ffffff;
  border-radius: 999px;
  padding: 0.5rem 0.9rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #374151;
}

.chip.active {
  border-color: #a08077;
  color: #a08077;
  font-weight: 700;
  background: #fff6f0;
}

.chip:hover {
  border-color: #a1766a;
  color: #a1766a;
}

.empty {
  border-top: 1px solid #e5e7eb;
  padding: 1.6rem 0.4rem 0.6rem;
  text-align: center;
  color: #9ca3af;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 0.4rem;
}

.mypage-footer {
  max-width: 1100px;
  margin: 1rem auto 0;
  display: flex;
  justify-content: flex-end;
  padding: 0 0.25rem;
}

.logout-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  border: 1.5px solid #ef4444;
  background: #ffffff;
  color: #ef4444;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #fef2f2;
}

@media (max-width: 768px) {
  .profile-card {
    padding: 1.4rem;
  }

  .profile-top {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
