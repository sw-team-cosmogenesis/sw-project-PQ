<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps<{
  question: string,
  options: Array<string | number>,
  quizId: string | number  // 可选的题目ID
}>()

const emits = defineEmits(['submit'])

const selectedIndex = ref<number | null>(null)

const selectOption = (index: number) => {
  selectedIndex.value = index
}

const submit = () => {
  if (selectedIndex.value !== null) {
    emits('submit', {
      quizId: props.quizId,
      answerIndex: selectedIndex.value,
      answerText: props.options[selectedIndex.value]
    })
    selectedIndex.value = null
  }
}

</script>

<template>
<div class="quiz-card">
    <h2 class="question">{{ question }}</h2>
    <ul class="options">
      <li
        v-for="(option, index) in options"
        :key="index"
        :class="{ selected: selectedIndex === index }"
        @click="selectOption(index)"
      >
        {{ option }}
      </li>
    </ul>
    <button v-if="selectedIndex !== null" @click="submit" class="submit-btn">
      提交
    </button>
  </div>
</template>

<style scoped>
.quiz-card {
  width: 100%;                     /* 宽度占满容器 */
  max-width: 500px;                /* 限制最大宽度 */
  min-width: 300px;    /* 最小宽度 */
  min-height: 400px;   /* 最小高度 */
  margin: 0 auto;                  /* ✅ 水平居中 */
  padding: 1.5rem;
  border-radius: 12px;
  background: #f8f9fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.question {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
.options {
  list-style: none;
  padding: 0;
}
.options li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.options li.selected {
  background: #dbeafe;
  border-color: #3b82f6;
}
.submit-btn {
  display: block;
  margin: 1rem auto 0 auto;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>
