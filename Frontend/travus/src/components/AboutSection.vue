<template>
  <section class="about-container">
    <!-- 왼쪽 텍스트 영역 -->
    <div class="left-area">

      <h1 class="title">
        <span class="travus-text">TRAVUS</span>의 뜻이<br />
        무엇인가요?
      </h1>

      <!-- 말풍선 -->
      <div class="bubble-list">
        <div class="bubble">혹시 대표님 이름인가요?</div>
        <div class="bubble">고진진 이름이랑 비슷하네요!</div>
        <div class="bubble">소이정씨 택배왔습니다~</div>
      </div>

      <p class="description">
        소이정의 뜻이 정확하게 뭐냐고 물으시는 분들이 정말 많아요~<br /><br />
        ‘소이정’은 ‘(소작은 소, 정이로울 이, 정할 정)’
        <strong>적지 않다 소작소이이다.</strong> 라는 뜻을 가진 한자입니다.<br /><br />
        작은 시작으로 큰 뜻을 이루고자 하는 마음이 담겨있습니다.<br />
        소이정은 우리의 뜻이기도, 우리 모두의 이름이기도 합니다.<br /><br />
        여러분도 오늘부터 소이정과 함께해요!
      </p>
    </div>

    <!-- 오른쪽 이미지 -->
    <div class="right-area">
      <img class="char-img" src="@/assets/main.png" alt="char Character" />
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.about-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 80px 120px;
  background-color: #f0c9bd;
  min-height: 100vh;
  box-sizing: border-box;
}


.left-area {
  width: 60%;
}

.title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.3;
  color: #a08077;
  margin-bottom: 40px;
}

.travus-text{
  background-color: #a08077;
  color: #f0c9bd;
  padding: 0px 5px;
}

.bubble-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 35px;
}

.bubble {
  background: white;
  display: inline-block;
  padding: 12px 20px;
  border-radius: 20px;
  width: fit-content;
  font-size: 16px;
  font-weight: 500;
  color: #444;
  box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
  animation: float 3s ease-in-out infinite;
}

.description {
  font-size: 17px;
  line-height: 1.8;
  color: #5c3a32;
}

.right-area {
  width: 50%;
  display: flex;
  justify-content: center;
}

.char-img {
  width: 550px;
  height: auto;
  object-fit: contain;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}
</style>
