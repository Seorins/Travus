<template>
  <section class="gradient-text-section" tabindex="0" @focus="handleFocus">
    <div class="text-container">
      <h2 class="main-text" data-text="누구나 쉽고 편리하게 여행을 즐길 수 있도록, TravUs가 함께합니다">
        TravUs는 각자의 속도를 존중하며,<br>
        누구나 편안하게 머물고 자유롭게 나아갈 수 있는 여행을 그립니다.<br>
        따뜻한 기술과 작은 배려가 더해져,<br>
        당신의 여정이 언제나 부드럽게 펼쳐지기를 바랍니다.
      </h2>
    </div>
  </section>
</template>

<script setup>
const emit = defineEmits(['focus'])

const handleFocus = (event) => {
  const text = event.target.getAttribute('data-text') || event.target.innerText
  emit('focus', text)
}
</script>

<style scoped>
.gradient-text-section {
  min-height: 70vh;
  background: linear-gradient(
    to bottom,
    #b4d5fe 0%,
    #bcd6f3 22%,
    #c5d9ee 38%,
    #cedce9 52%,
    #d7dfe4 66%,
    #dfe1df 78%,
    #e5e3df 88%,
    #e9e7e3 94%,
    #edebe8 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 2rem;
  position: relative;
  margin: 0;
  border: none;
}

.gradient-text-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.text-container {
  max-width: 1200px;
  text-align: center;
  z-index: 1;
}

.main-text {
  font-size: 2rem;
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  color: #52423b;
  line-height: 1.5;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  word-break: keep-all;
  letter-spacing: -1px;
}

@media (max-width: 1024px) {
  .main-text {
    font-size: 1.6rem;
  }
}

@media (max-width: 768px) {
  .gradient-text-section {
    min-height: 40vh;
    padding: 3rem 1.5rem;
  }

  .main-text {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .main-text {
    font-size: 1rem;
  }
}
</style>
