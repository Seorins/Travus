import { ref, watch } from 'vue'

/**
 * TTS(Text-to-Speech) 기능을 제공하는 Composable
 */
export function useTTS() {
  const isTTSEnabled = ref(true)
  const isSpeaking = ref(false)

  // SpeechSynthesis 지원 확인
  const isSupported = 'speechSynthesis' in window

  /**
   * 텍스트를 음성으로 읽기
   */
  const speak = (text) => {
    if (!isSupported || !isTTSEnabled.value || !text) return

    // 이전 음성 중지
    window.speechSynthesis.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'ko-KR'
    utterance.rate = 1.0
    utterance.pitch = 1.0
    utterance.volume = 1.0

    utterance.onstart = () => {
      isSpeaking.value = true
    }

    utterance.onend = () => {
      isSpeaking.value = false
    }

    utterance.onerror = () => {
      isSpeaking.value = false
    }

    window.speechSynthesis.speak(utterance)
  }

  /**
   * TTS 중지
   */
  const stop = () => {
    if (isSupported) {
      window.speechSynthesis.cancel()
      isSpeaking.value = false
    }
  }

  /**
   * TTS 토글
   */
  const toggleTTS = () => {
    isTTSEnabled.value = !isTTSEnabled.value
    if (!isTTSEnabled.value) {
      stop()
    }
  }

  // TTS가 비활성화되면 자동으로 중지
  watch(isTTSEnabled, (enabled) => {
    if (!enabled) {
      stop()
    }
  })

  return {
    isTTSEnabled,
    isSpeaking,
    isSupported,
    speak,
    stop,
    toggleTTS
  }
}
