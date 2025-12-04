<template>
  <nav class="navbar" :style="{ fontSize: `${fontSize}px` }">
    <div class="navbar-container">
      <!-- 로고 -->
      <div class="navbar-logo" tabindex="0" @focus="handleFocus">
        <h1>TravUs</h1>
      </div>

      <!-- 컨트롤 버튼 그룹 -->
      <div class="navbar-controls">
        <!-- 글자 크기 조절 -->
        <div class="font-size-controls">
          <button
            class="control-btn"
            @click="decreaseFontSize"
            tabindex="0"
            @focus="handleFocus"
            aria-label="글자 크기 줄이기"
          >
            <span class="icon">-</span>
          </button>
          <button
            class="control-btn"
            @click="increaseFontSize"
            tabindex="0"
            @focus="handleFocus"
            aria-label="글자 크기 키우기"
          >
            <span class="icon">+</span>
          </button>
        </div>

        <!-- TTS 토글 -->
        <button
          class="control-btn tts-btn"
          :class="{ active: isTTSEnabled }"
          @click="toggleTTS"
          tabindex="0"
          @focus="handleFocus"
          :aria-label="isTTSEnabled ? 'TTS 끄기' : 'TTS 켜기'"
        >
          <span class="icon">{{ isTTSEnabled ? '🔊' : '🔇' }}</span>
          <span class="label">TTS {{ isTTSEnabled ? 'ON' : 'OFF' }}</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  isTTSEnabled: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['toggle-tts', 'font-size-change', 'focus'])

const fontSize = ref(16)
const minFontSize = 12
const maxFontSize = 24

const increaseFontSize = () => {
  if (fontSize.value < maxFontSize) {
    fontSize.value += 2
    emit('font-size-change', fontSize.value)
  }
}

const decreaseFontSize = () => {
  if (fontSize.value > minFontSize) {
    fontSize.value -= 2
    emit('font-size-change', fontSize.value)
  }
}

const toggleTTS = () => {
  emit('toggle-tts')
}

const handleFocus = (event) => {
  const text = event.target.innerText || event.target.getAttribute('aria-label')
  emit('focus', text)
}
</script>

<style scoped>
.navbar {
  position: relative;
  background: #5a67d8; /* 보라색 단색 */
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo h1 {
  color: white;
  font-size: 2em;
  font-weight: 700;
  margin: 0;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.navbar-logo h1:hover,
.navbar-logo:focus h1 {
  transform: scale(1.05);
  outline: 2px solid rgba(255, 255, 255, 0.5);
  outline-offset: 4px;
  border-radius: 8px;
}

.navbar-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.font-size-controls {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem;
  border-radius: 8px;
}

.control-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  color: #667eea;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 44px;
  min-height: 44px;
  justify-content: center;
}

.control-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.control-btn:focus {
  outline: 3px solid #ffd700;
  outline-offset: 2px;
}

.control-btn:active {
  transform: translateY(0);
}

.tts-btn.active {
  background: #5a67d8;
  color: white;
}

.tts-btn.active:hover {
  background: #4c51bf;
}

.icon {
  font-size: 1.2em;
}

.label {
  font-size: 0.9em;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 1rem;
  }

  .label {
    display: none;
  }
}
</style>
