<template>
  <section class="target-section" tabindex="0" @focus="handleFocus">
    <div class="target-container">
      <h2 class="section-title" data-text="여행 대상 섹션">
        여행 대상 섹션
      </h2>
      <p class="section-description">이 섹션은 나중에 구현될 예정입니다.</p>
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
.target-section {
  width: 100%;
  min-height: 100vh;
  background: #ff6b35;
  padding: 4rem 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.target-section:focus {
  outline: 3px solid #ffd700;
  outline-offset: -3px;
}

.target-container {
  max-width: 1200px;
  width: 100%;
  text-align: center;
}

.section-title {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.section-description {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 300;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }

  .section-description {
    font-size: 1.2rem;
  }
}
</style>
