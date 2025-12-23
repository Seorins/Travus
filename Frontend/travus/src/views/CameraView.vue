<template>
  <div class="camera-page" :style="{ fontSize: `${baseFontSize}px` }">
    <NavigationBar
      :is-t-t-s-enabled="isTTSEnabled"
      @toggle-tts="toggleTTS"
      @font-size-change="handleFontSizeChange"
      @focus="handleFocus"
    />

    <main class="camera-main">
      <section class="camera-hero">
        <div class="hero-text">
          <h1>AI 카메라로 여행지를 바로 분석해요</h1>
          <p class="subtitle">
            카메라를 켜고 여행지를 비추면 즉시 분석하고 정보를 알려줘요!
          </p>
          <div class="hero-actions">
            <button class="primary-btn" @click="startCamera" @focus="handleFocus">카메라 켜기</button>
            <label class="ghost-btn" for="imageUpload" @focus="handleFocus">사진 업로드</label>
            <input id="imageUpload" type="file" accept="image/*" class="sr-only" @change="handleFileUpload" />
          </div>
          <p class="status" :class="{ error: errorMessage }">
            {{ errorMessage || statusMessage }}
          </p>
        </div>
        <div class="hero-visual">
          <div class="floating-card">
            <div class="card-header">
              <span>Travus AI Camera</span>
              <span class="dot live"></span>
            </div>
            <div class="card-body">
              <p>실시간 분석</p>
              <h3>GPT가 여행지를 설명합니다</h3>
            </div>
          </div>
          <div class="floating-card secondary">
            <div class="card-header">
              <span>대화 모드</span>
              <span class="dot idle"></span>
            </div>
            <div class="card-body">
              <p>궁금한 점을 물어보세요</p>
              <h3>여행지 정보 · 접근성 · 추천 코스</h3>
            </div>
          </div>
        </div>
      </section>

      <section class="camera-body">
        <div class="camera-panel">
          <div class="viewer">
            <video ref="videoRef" autoplay playsinline muted class="video-feed"></video>
            <div v-if="!isStreaming" class="video-placeholder">
              <p>카메라를 켜면 여기에 실시간 영상이 표시됩니다.</p>
              <button class="primary-btn" @click="startCamera" @focus="handleFocus">카메라 시작</button>
            </div>
          </div>

          <div class="controls">
            <button class="ghost-btn" @click="startCamera" @focus="handleFocus">다시 연결</button>
            <button class="primary-btn" :disabled="captureDisabled" @click="capturePhoto" @focus="handleFocus">
              {{ analysisLoading ? '분석 중...' : '캡처 및 분석' }}
            </button>
            <button class="ghost-btn danger" @click="stopCamera" @focus="handleFocus">카메라 끄기</button>
          </div>

          <div class="preview" v-if="capturedImage">
            <p class="preview-label">캡처 이미지</p>
            <img :src="capturedImage" alt="Captured" />
          </div>
        </div>

        <div class="insight-panel">
          <div class="insight-card">
            <div class="card-title">
              <span>분석 결과</span>
              <span v-if="analysisLoading" class="pill">Analyzing</span>
            </div>
            <p v-if="!analysisResult && !analysisLoading" class="placeholder-text">
              사진을 캡처하거나 업로드하면 여행지를 설명해줘요!
            </p>
            <div v-else class="result-box">
              <p class="result-text">{{ analysisResult }}</p>
            </div>
          </div>

          <div class="insight-card">
            <div class="card-title">
              <span>AI에게 질문하기</span>
            </div>
            <div class="chat-box">
              <textarea
                v-model="question"
                rows="3"
                placeholder="궁금한 점을 입력하세요. 예) 휠체어 접근성은 어떤가요?"
                @focus="handleFocus"
              />
              <div class="voice-controls">
                <button
                  class="ghost-btn"
                  :class="{ danger: isRecording }"
                  :disabled="transcriptionLoading"
                  @click="toggleRecording"
                  @focus="handleFocus"
                >
                  {{ isRecording ? '녹음 중지' : ' 음성으로 질문' }}
                </button>
                <span class="pill" v-if="isRecording">녹음 중</span>
                <span class="pill muted" v-else-if="transcriptionLoading">음성 변환 중</span>
              </div>
              <p v-if="voiceError" class="error-text">{{ voiceError }}</p>
              <div class="chat-actions">
                <button class="primary-btn" :disabled="chatLoading || !question.trim()" @click="askQuestion" @focus="handleFocus">
                  {{ chatLoading ? '응답 생성 중...' : '질문하기' }}
                </button>
              </div>
              <div v-if="chatAnswer" class="chat-answer">
                <p class="answer-label">🔊 답변</p>
                <p>{{ chatAnswer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <canvas ref="canvasRef" class="sr-only"></canvas>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import NavigationBar from '@/components/common/NavigationBar.vue'
import { useTTS } from '@/composables/useTTS'
import api from '@/services/api'

const { isTTSEnabled, speak, toggleTTS: ttsToggle } = useTTS()
const baseFontSize = ref(16)

const videoRef = ref(null)
const canvasRef = ref(null)
const stream = ref(null)
const isStreaming = ref(false)

const capturedImage = ref('')
const analysisResult = ref('')
const chatAnswer = ref('')
const statusMessage = ref('카메라를 켜서 여행지를 비춰주세요.')
const errorMessage = ref('')
const analysisLoading = ref(false)
const chatLoading = ref(false)
const question = ref('')
const travelName = ref('')
const isRecording = ref(false)
const transcriptionLoading = ref(false)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const voiceError = ref('')

const handleFocus = (text) => {
  const spoken = typeof text === 'string' ? text : (text?.target?.innerText || text?.target?.value)
  if (spoken && isTTSEnabled.value) {
    speak(spoken)
  }
}

const toggleTTS = () => {
  ttsToggle()
  speak(isTTSEnabled.value ? 'TTS가 켜졌습니다' : 'TTS가 꺼졌습니다')
}

const handleFontSizeChange = (size) => {
  baseFontSize.value = size
  speak(`글자 크기가 ${size}포인트로 변경되었습니다`)
}

const startCamera = async () => {
  errorMessage.value = ''
  try {
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' },
      audio: false
    })
    stream.value = mediaStream
    if (videoRef.value) {
      videoRef.value.srcObject = mediaStream
    }
    isStreaming.value = true
    statusMessage.value = '카메라가 켜졌어요. 화면을 비추고 캡처를 눌러보세요.'
  } catch (error) {
    console.error(error)
    errorMessage.value = '카메라 권한을 확인하고 다시 시도해주세요.'
    statusMessage.value = ''
  }
}

const stopCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach((track) => track.stop())
  }
  isStreaming.value = false
  stream.value = null
  statusMessage.value = '카메라가 꺼졌습니다.'
}

const captureDisabled = computed(() => !isStreaming.value || analysisLoading.value)

const capturePhoto = () => {
  if (!videoRef.value) return

  const video = videoRef.value
  const canvas = canvasRef.value
  const width = video.videoWidth || 720
  const height = video.videoHeight || 480

  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video, 0, 0, width, height)

  canvas.toBlob(async (blob) => {
    if (!blob) return
    if (capturedImage.value) {
      URL.revokeObjectURL(capturedImage.value)
    }
    capturedImage.value = URL.createObjectURL(blob)
    const file = new File([blob], 'capture.png', { type: 'image/png' })
    await sendForAnalysis(file)
  }, 'image/png')
}

const handleFileUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return
  if (capturedImage.value) {
    URL.revokeObjectURL(capturedImage.value)
  }
  capturedImage.value = URL.createObjectURL(file)
  await sendForAnalysis(file)
}

const sendForAnalysis = async (file) => {
  analysisLoading.value = true
  analysisResult.value = ''
  chatAnswer.value = ''
  errorMessage.value = ''
  statusMessage.value = '이미지 분석 중입니다...'
  try {
    const formData = new FormData()
    formData.append('image', file)
    const { data } = await api.analyzeImage(formData)
    analysisResult.value = data?.result || '분석 결과를 가져오지 못했습니다.'
    travelName.value = data?.travel_name || ''
    statusMessage.value = '분석이 완료됐습니다. 궁금한 점을 물어보세요.'
    if (analysisResult.value && isTTSEnabled.value) {
      speak(analysisResult.value)
    }
  } catch (error) {
    console.error(error)
    const serverMessage =
      error?.response?.data?.detail ||
      error?.response?.data?.error ||
      error.message
    errorMessage.value = serverMessage || '이미지 분석 중 오류가 발생했습니다.'
    analysisResult.value = errorMessage.value  // 결과 영역에도 바로 표시
    statusMessage.value = ''
  } finally {
    analysisLoading.value = false
  }
}

const askQuestion = async () => {
  if (!question.value.trim()) return
  chatLoading.value = true
  chatAnswer.value = ''
  errorMessage.value = ''
  try {
    const payload = {
      question: question.value,
      travel_name: travelName.value || '이 장소'
    }
    const { data } = await api.chatAI(payload)
    chatAnswer.value = data?.answer || '답변을 가져오지 못했습니다.'
    if (chatAnswer.value && isTTSEnabled.value) {
      speak(chatAnswer.value)
    }
  } catch (error) {
    console.error(error)
    const serverMessage =
      error?.response?.data?.error || error?.response?.data?.detail || error.message
    errorMessage.value = serverMessage || 'AI 답변을 불러오는 중 문제가 발생했습니다.'
  } finally {
    chatLoading.value = false
  }
}

const toggleRecording = async () => {
  voiceError.value = ''
  if (isRecording.value) {
    stopRecording()
    return
  }
  if (!navigator.mediaDevices?.getUserMedia) {
    voiceError.value = '마이크를 사용할 수 없습니다.'
    return
  }
  try {
    const micStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const recorder = new MediaRecorder(micStream)
    mediaRecorder.value = recorder
    audioChunks.value = []

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.value.push(e.data)
      }
    }

    recorder.onstop = async () => {
      micStream.getTracks().forEach((t) => t.stop())
      if (!audioChunks.value.length) return
      const blob = new Blob(audioChunks.value, { type: 'audio/webm' })
      await sendAudioForTranscription(blob)
    }

    recorder.start()
    isRecording.value = true
    statusMessage.value = '녹음 중입니다. 질문을 말씀해 주세요.'
    if (isTTSEnabled.value) speak('녹음이 시작되었습니다. 질문을 말씀해 주세요.')
  } catch (error) {
    console.error(error)
    voiceError.value = '마이크 권한을 확인해주세요.'
  }
}

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
  }
  isRecording.value = false
}

const sendAudioForTranscription = async (blob) => {
  transcriptionLoading.value = true
  try {
    const file = new File([blob], 'voice.webm', { type: 'audio/webm' })
    const formData = new FormData()
    formData.append('audio', file)
    const { data } = await api.transcribeAudio(formData)
    if (data?.text) {
      question.value = data.text
      statusMessage.value = '음성이 텍스트로 변환되었습니다.'
      if (isTTSEnabled.value) speak('질문을 텍스트로 변환했습니다.')
      // 변환된 질문을 자동으로 전송
      await askQuestion()
    } else {
      voiceError.value = '음성을 변환하지 못했습니다.'
    }
  } catch (error) {
    console.error(error)
    const serverMessage =
      error?.response?.data?.detail ||
      error?.response?.data?.error ||
      error.message
    voiceError.value = serverMessage || '음성 변환 중 문제가 발생했습니다.'
  } finally {
    transcriptionLoading.value = false
    isRecording.value = false
  }
}

onBeforeUnmount(() => {
  stopCamera()
  if (capturedImage.value) {
    URL.revokeObjectURL(capturedImage.value)
  }
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
  }
})
</script>

<style scoped>
.camera-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #c8e9ff, #f6edff);
  color: #0f172a;
}

.camera-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 8rem 1.5rem 3rem;
}

.camera-hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 2rem;
  align-items: center;
  margin-bottom: 2.5rem;
}

.hero-text h1 {
  font-size: 2.6rem;
  margin: 0.75rem 0;
  line-height: 1.2;
  color: #0f172a;
}

.hero-text .subtitle {
  color: #344054;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 0.75rem;
  margin: 1.5rem 0;
  flex-wrap: wrap;
}

.status {
  color: #475467;
  font-size: 0.95rem;
}

.status.error {
  color: #f04438;
}

.eyebrow {
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #2d7dd2;
}

.hero-visual {
  position: relative;
  min-height: 260px;
}

.floating-card {
  background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.12), transparent 55%), #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1rem 1.25rem;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.35);
  position: absolute;
  width: 90%;
  left: 5%;
  animation: float 6s ease-in-out infinite;
  color: #e5e7eb;
}

.floating-card.secondary {
  top: 140px;
  right: 0;
  left: auto;
  width: 88%;
  animation-delay: 1.5s;
  background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.1), transparent 55%), #111827;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
  color: #cbd5e1;
}

.card-body h3 {
  margin: 0.25rem 0 0;
  font-size: 1.25rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  display: inline-block;
}

.dot.live {
  background: #22c55e;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.8);
}

.dot.idle {
  background: #fbbf24;
  box-shadow: 0 0 8px rgba(251, 191, 36, 0.6);
}

.camera-body {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 1.5rem;
}

.camera-panel,
.insight-panel {
  background: #fdfefe;
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 18px;
  padding: 1.5rem;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
}

.viewer {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: linear-gradient(135deg, #e6f3ff, #f9f5ff);
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(15, 23, 42, 0.06);
}

.video-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #0f172a;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.5), transparent 40%),
    radial-gradient(circle at 70% 60%, rgba(255, 255, 255, 0.4), transparent 35%);
  text-align: center;
}

.controls {
  display: flex;
  gap: 0.75rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.preview {
  margin-top: 1rem;
}

.preview img {
  width: 100%;
  border-radius: 12px;
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.preview-label {
  margin-bottom: 0.35rem;
  color: #0f172a;
  font-size: 0.95rem;
}

.insight-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.insight-card {
  background: #fdfefe;
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 14px;
  padding: 1rem 1.25rem;
}

.card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.3rem 0.8rem;
  border-radius: 999px;
  background: rgba(45, 125, 210, 0.12);
  color: #2d7dd2;
  font-size: 0.85rem;
}

.pill.muted {
  background: rgba(148, 163, 184, 0.15);
  color: #475467;
}

.placeholder-text {
  color: #667085;
}

.result-box {
  background: rgba(245, 249, 255, 0.9);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 12px;
  padding: 1rem;
  color: #0f172a;
  line-height: 1.6;
  white-space: pre-line;
}

.chat-box textarea {
  width: 100%;
  background: #f8fafc;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 10px;
  padding: 0.75rem;
  color: #0f172a;
  resize: none;
}

.chat-box textarea:focus {
  outline: 2px solid #2d7dd2;
  border-color: transparent;
}

.chat-actions {
  margin-top: 0.75rem;
  display: flex;
  justify-content: flex-end;
}

.chat-answer {
  margin-top: 0.75rem;
  background: rgba(229, 249, 245, 0.9);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 10px;
  padding: 0.75rem;
  color: #0f172a;
  line-height: 1.5;
}

.answer-label {
  font-size: 0.9rem;
  color: #0f172a;
  margin-bottom: 0.25rem;
}

.voice-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.error-text {
  color: #f04438;
  margin-top: 0.25rem;
  font-size: 0.9rem;
}

.primary-btn,
.ghost-btn {
  border: none;
  border-radius: 12px;
  padding: 0.8rem 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.primary-btn {
  background: linear-gradient(135deg, #52b9ff, #88e0ff);
  color: #0b1224;
  box-shadow: 0 10px 25px rgba(82, 185, 255, 0.35);
}

.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.ghost-btn {
  background: #f5f7fb;
  color: #0f172a;
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.ghost-btn.danger {
  color: #f04438;
  border-color: rgba(240, 68, 56, 0.25);
}

.ghost-btn:hover,
.primary-btn:hover {
  transform: translateY(-1px);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 1024px) {
  .camera-hero,
  .camera-body {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 200px;
  }

  .floating-card,
  .floating-card.secondary {
    position: relative;
    width: 100%;
    left: 0;
    top: 0;
    animation: none;
    margin-top: 1rem;
  }
}

@media (max-width: 640px) {
  .hero-text h1 {
    font-size: 2rem;
  }

  .controls {
    flex-direction: column;
  }

  .primary-btn,
  .ghost-btn {
    width: 100%;
    text-align: center;
  }
}
</style>
