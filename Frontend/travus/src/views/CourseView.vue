<template>
  <div class="course-view">
    <NavigationBar />

    <!-- ① 시작 화면 -->
    <CourseStart
      v-if="currentStep === 'start'"
      @next="goToRegionSelect"
    />

    <!-- ② 지역 선택 -->
    <RegionSelect
      v-if="currentStep === 'region'"
      @next="goToDurationSelect"
      @back="currentStep = 'start'"
    />

    <!-- ③ 여행 기간 선택 -->
    <DurationSelect
      v-if="currentStep === 'duration'"
      @next="goToRegionConfigOrTheme"
      @back="currentStep = 'region'"
    />

    <!-- ④ 지역 구성 선택 (2박 3일만) -->
    <RegionConfig
      v-if="currentStep === 'regionConfig'"
      @next="goToThemeSelect"
      @back="currentStep = 'duration'"
    />

    <!-- ⑤ 여행 테마 선택 -->
    <ThemeSelect
      v-if="currentStep === 'theme'"
      @next="generateCourse"
      @back="goBackFromTheme"
    />

    <!-- ⑥ 로딩 화면 -->
    <CourseLoading
      v-if="currentStep === 'loading'"
    />

    <!-- ⑦ 여행 결과 -->
    <CourseResult
      v-if="currentStep === 'result'"
      :course-data="generatedCourse"
      @restart="restartCourse"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavigationBar from '@/components/common/NavigationBar.vue'
import CourseStart from '@/components/course/CourseStart.vue'
import RegionSelect from '@/components/course/RegionSelect.vue'
import DurationSelect from '@/components/course/DurationSelect.vue'
import RegionConfig from '@/components/course/RegionConfig.vue'
import ThemeSelect from '@/components/course/ThemeSelect.vue'
import CourseLoading from '@/components/course/CourseLoading.vue'
import CourseResult from '@/components/course/CourseResult.vue'

const currentStep = ref('start')
const selectedRegions = ref([])
const selectedDuration = ref(null)
const selectedRegionCount = ref(null)
const selectedThemes = ref([])
const generatedCourse = ref(null)

const goToRegionSelect = () => {
  currentStep.value = 'region'
}

const goToDurationSelect = (regions) => {
  selectedRegions.value = regions
  currentStep.value = 'duration'
}

const goToRegionConfigOrTheme = (duration) => {
  selectedDuration.value = duration

  // 2박 3일이면 지역 구성 선택으로
  if (duration.days === 3) {
    currentStep.value = 'regionConfig'
  } else {
    currentStep.value = 'theme'
  }
}

const goToThemeSelect = (regionCount) => {
  selectedRegionCount.value = regionCount
  currentStep.value = 'theme'
}

const goBackFromTheme = () => {
  if (selectedDuration.value?.days === 3) {
    currentStep.value = 'regionConfig'
  } else {
    currentStep.value = 'duration'
  }
}

const generateCourse = async (themes) => {
  selectedThemes.value = themes
  currentStep.value = 'loading'

  // TODO: AI 여행 코스 생성 API 호출
  // 임시로 3초 후 결과 화면으로 이동
  setTimeout(() => {
    // TODO: 실제 API 응답 데이터로 대체
    generatedCourse.value = {
      title: '서린님을 위한 여행코스',
      regions: selectedRegions.value,
      duration: selectedDuration.value,
      themes: selectedThemes.value,
      days: [] // 실제 일정 데이터
    }
    currentStep.value = 'result'
  }, 3000)
}

const restartCourse = () => {
  currentStep.value = 'start'
  selectedRegions.value = []
  selectedDuration.value = null
  selectedRegionCount.value = null
  selectedThemes.value = []
  generatedCourse.value = null
}
</script>

<style scoped>
.course-view {
  width: 100%;
  min-height: 100vh;
  background: #ffffff;
}
</style>
