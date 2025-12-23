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
    signUp({ username, password, name, phone, email = '', birth = '', gender = '' }) {
      const exists = this.users.some((user) => user.username === username)
      if (exists) {
        return { ok: false, message: '이미 가입된 아이디입니다.' }
      }

      this.users.push({
        username: username.trim(),
        password,
        name,
        phone,
        email,
        birth: (birth || '').trim(),
        gender
      })
      saveState(this)
      return { ok: true }
    },
    login(username, password, remember = true) {
      const user = this.users.find(
        (item) => item.username === username && item.password === password
      )

      if (!user) {
        return { ok: false, message: '아이디와 비밀번호가 올바르지 않습니다.' }
      }

      this.currentUser = {
        username: user.username,
        name: user.name,
        phone: user.phone,
        email: user.email,
        birth: user.birth,
        gender: user.gender
      }
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
    },
    updateProfile(payload) {
      if (!this.currentUser) {
        return { ok: false, message: '로그인 후 이용해 주세요.' }
      }

      const index = this.users.findIndex((user) => user.username === this.currentUser.username)
      if (index === -1) {
        return { ok: false, message: '사용자 정보를 찾을 수 없습니다.' }
      }

      const updated = {
        ...this.users[index],
        ...payload,
        username: this.users[index].username
      }

      this.users.splice(index, 1, updated)
      this.currentUser = { ...this.currentUser, ...payload }
      saveState(this)
      return { ok: true }
    }
  }
})
