import { defineStore } from 'pinia'

const STORAGE_KEY = 'travus-auth'

const loadState = () => {
  if (typeof window === 'undefined') {
    return { users: [], currentUser: null, isLoggedIn: false }
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return { users: [], currentUser: null, isLoggedIn: false }
    }

    const parsed = JSON.parse(raw)
    return {
      users: Array.isArray(parsed.users) ? parsed.users : [],
      currentUser: parsed.currentUser || null,
      isLoggedIn: Boolean(parsed.isLoggedIn)
    }
  } catch {
    return { users: [], currentUser: null, isLoggedIn: false }
  }
}

const saveState = (state, storage = window.localStorage) => {
  if (typeof window === 'undefined') return

  const payload = {
    users: state.users,
    currentUser: state.currentUser,
    isLoggedIn: state.isLoggedIn
  }

  storage.setItem(STORAGE_KEY, JSON.stringify(payload))
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    ...loadState()
  }),
  actions: {
    signUp({ username, password, name, phone }) {
      const exists = this.users.some((user) => user.username === username)
      if (exists) {
        return { ok: false, message: '이미 가입된 아이디입니다.' }
      }

      this.users.push({ username, password, name, phone })
      saveState(this)
      return { ok: true }
    },
    login(username, password, remember = true) {
      const user = this.users.find(
        (item) => item.username === username && item.password === password
      )

      if (!user) {
        return { ok: false, message: '아이디 또는 비밀번호가 올바르지 않습니다.' }
      }

      this.currentUser = { username: user.username, name: user.name, phone: user.phone }
      this.isLoggedIn = true

      if (typeof window !== 'undefined') {
        const storage = remember ? window.localStorage : window.sessionStorage
        if (!remember) {
          window.localStorage.removeItem(STORAGE_KEY)
        }
        saveState(this, storage)
      }

      return { ok: true }
    },
    logout() {
      this.currentUser = null
      this.isLoggedIn = false
      if (typeof window !== 'undefined') {
        window.localStorage.removeItem(STORAGE_KEY)
        window.sessionStorage.removeItem(STORAGE_KEY)
      }
    }
  }
})
