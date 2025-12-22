<template>
  <div class="comments-view">
    <NavigationBar />
    <div class="container">
      <h1>내가 쓴 댓글</h1>
      <p class="empty">아직 작성한 댓글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import NavigationBar from '@/components/common/NavigationBar.vue'
</script>

<style scoped>
.comments-view {
  min-height: 100vh;
  background: #f7f9fb;
}
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 6rem 1.25rem 2rem;
}
.empty {
  margin-top: 1rem;
  color: #6b7280;
}
</style>
