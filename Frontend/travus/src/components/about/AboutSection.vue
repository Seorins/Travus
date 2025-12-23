<template>
  <section class="about-container">
    <!-- 배경 큰 글씨 -->
    <div class="background-text">TRAVUS</div>

    <!-- 왼쪽 텍스트 영역 -->
    <div class="left-area">

      <h1 class="title">
        <span class="travus-text">TRAVUS</span>의 뜻이<br />
        무엇인가요?
      </h1>

      <!-- 말풍선 -->
      <div class="bubble-list">
        <div class="bubble-row left">
          <img class="bubble-avatar" src="@/assets/avatar1.png" alt="avatar" />
          <div class="left-bubble">새로 나온 버스 이름인가요?</div>
        </div>
        <div class="bubble-row right">
          <div class="right-bubble">새로운 여행 플랫폼인가요?</div>
          <img class="bubble-avatar" src="@/assets/avatar3.png" alt="avatar" />
        </div>
        <div class="bubble-row left">
          <img class="bubble-avatar" src="@/assets/avatar2.png" alt="avatar" />
          <div class="left-bubble">트래버스 출발합니다~</div>
        </div>
      </div>

      <p class="description"><strong>
        'TravUs'는 'Travel(여행)'과 'Us(우리)'가 합쳐진 이름으로,<br />
        <span>우리 모두를 위한 여행</span>이라는 뜻을 담고 있습니다.<br /><br />
        누구나 불편함 없이 여행을 즐길 수 있도록 길을 만드는 작은 시작이 되고자 하는 마음이 담겨 있어요.<br />
        TravUs는 우리 모두의 여행을 위한 이름이기도 합니다.<br /><br />
        여러분도 오늘부터 TravUs와 함께해요!
      </strong>
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
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 120px 120px;
  background-color: #b4d5fe;
  min-height: 120vh;
  box-sizing: border-box;
  overflow: hidden;
}


.background-text {
  position: absolute;
  font-size: 160px;
  font-weight: 800;
  color: rgba(119, 120, 160, 0.12);
  top: 24%;
  left: 60%;
  transform: translate(-50%, -50%);
  z-index: 0;
  pointer-events: none;
  white-space: nowrap;
  letter-spacing: 3px;
  font-family: 'Arial Rounded MT Bold', 'Nunito', 'Quicksand', 'Helvetica Neue', Arial, sans-serif;
}

.left-area {
  width: 60%;
  position: relative;
  z-index: 1;
}

.title {
  font-size: 56px;
  font-weight: 700;
  line-height: 1.3;
  color: #5f6f8d;
  margin-bottom: 40px;
}

/* travus 글씨배경 */
.travus-text{
  background-color: #5f6f8d;
  color: #b4d5fe;
  padding: 0px 5px;
}

.bubble-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
  max-width: 100%;
  padding: 30px;
}

.bubble-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bubble-row.left {
  justify-content: flex-start;
}

.bubble-row.right {
  justify-content: flex-end;
}

.bubble-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center top;
  flex-shrink: 0;
  box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
  background-color: #5b6880;
}

.left-bubble {
  background: white;
  display: inline-block;
  padding: 16px 24px;
  border-radius: 20px;
  width: fit-content;
  font-size: 18px;
  font-weight: 500;
  color: #5f6f8d;
  box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
  animation: float 3s ease-in-out infinite;
  position: relative;
  font-weight: bold;
}

.left-bubble::after {
  content: '';
  position: absolute;
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid white;
}

.right-bubble {
  background: white;
  display: inline-block;
  padding: 16px 24px;
  border-radius: 20px;
  width: fit-content;
  font-size: 18px;
  font-weight: 500;
  color: #5f6f8d;
  box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
  animation: float 3s ease-in-out infinite;
  position: relative;
  font-weight: bold;
}

.right-bubble::after {
  content: '';
  position: absolute;
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-left: 8px solid white;
}

.description {
  font-size: 19px;
  line-height: 1.8;
  color: #5f6f8d;
  letter-spacing: -0.5px;
}

.description span{
  background-color: #5f6f8d;
  color: white;
  padding: 2px 5px;
}
.right-area {
  width: 50%;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 1;
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
