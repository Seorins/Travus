<template>
  <div class="travel-card" :class="colorClass">
    <div class="card-header">
      <p class="card-category">{{ category }}</p>
      <h3 class="card-title">{{ title }}</h3>
    </div>
    <div class="card-body">
      <ul class="feature-list">
        <li v-for="(feature, index) in features" :key="index">{{ feature }}</li>
      </ul>
      <div class="card-icon"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  category: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  features: {
    type: Array,
    required: true
  },
  colorClass: {
    type: String,
    default: 'pink'
  }
})
</script>

<style scoped>
.travel-card {
  background: white;
  border-radius: 25px;
  padding: 0;
  width: 420px;
  height: 500px;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-header {
  background: #1a1a1a;
  padding: 2rem;
  border-radius: 25px 25px 0 0;
}

.card-category {
  font-size: 0.75rem;
  color: #ff6714;
  margin-bottom: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  line-height: 1.4;
}

.card-body {
  position: relative;
  padding: 2rem;
  flex: 1;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.feature-list li {
  font-size: 0.9rem;
  color: #666;
  position: relative;
  padding-left: 1rem;
  line-height: 1.6;
}

.feature-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #ff6714;
  font-size: 1rem;
  font-weight: bold;
}

.card-icon {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  position: absolute;
  bottom: 0;
  right: 15px;
  opacity: 0.2;
}

.travel-card.pink .card-icon {
  background: linear-gradient(135deg, #ff6b9d 0%, #c239b3 100%);
}

.travel-card.purple .card-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.travel-card.red .card-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.travel-card.blue .card-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.travel-card.yellow .card-icon {
  background: linear-gradient(135deg, #fdeb71 0%, #f8d800 100%);
}

.travel-card.green .card-icon {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.travel-card.orange .card-icon {
  background: linear-gradient(135deg, #ffa751 0%, #ffe259 100%);
}

.travel-card.teal .card-icon {
  background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
}
</style>
