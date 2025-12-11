<template>
  <section class="image-banner-section">
    <img src="@/assets/footimg.jpg" alt="Travus Banner" class="full-banner-image" />
  </section>
</template>

<script setup>

</script>

<style scoped>
.image-banner-section {
  width: 100%;
  height: auto;
  position: relative;
  overflow: hidden;
  padding: 0;
  margin: 0;
  display: block;
  line-height: 0;
  border: none;
  margin-top: -1px;
}

.full-banner-image {
  width: 100%;
  height: auto;
  object-fit: cover;
  object-position: top;
  display: block;
}

@media (max-width: 768px) {
  .image-banner-section {
    height: 60vh;
  }
}
</style>
