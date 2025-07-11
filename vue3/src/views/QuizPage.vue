<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from '@/utils/request'
import QuizCard from '../components/QuizCard.vue'  // 你的题卡组件路径

interface QuizItem {
  uuid: string | number
  question_text: string
  options: (string | number)[]
}

interface Answer {
  quizId: string | number
  answerIndex: number
  answerText: string | number
}

const quizList = ref<QuizItem[]>([])
const currentQuizIndex = ref(0)
const loading = ref(true)
const error = ref('')
const answers = ref<Answer[]>([])

const currentQuiz = computed(() => quizList.value[currentQuizIndex.value])

const fetchQuizzes = async () => {
  try {
    const res = await axios.get('popquiz/')
    console.log("数据请求成功:" + res.data)
    quizList.value = res.data
  } catch (err) {
    error.value = '题目加载失败'
    console.log(error)
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = (answer: Answer) => {
  answers.value.push(answer)
  currentQuizIndex.value += 1
}

onMounted(fetchQuizzes)
</script>

<template>
    <div class="quiz-page">
    <div v-if="loading">题目加载中...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="currentQuizIndex < quizList.length" class="quiz-wrapper">
      <QuizCard
        :question="currentQuiz.question_text"
        :options="currentQuiz.options"
        :quiz-id="currentQuiz.uuid"
        @submit="handleSubmit"
      />
    </div>
    <div v-else class="quiz-wrapper">
      <h2>你已完成全部题目!</h2>
      <ul>
        <li v-for="(answer, index) in answers" :key="index">
          第 {{ index + 1 }} 题：选项 {{ answer.answerText }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.quiz-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-width: 40rem;
  box-sizing: border-box;
  padding: 2rem 10vw 2rem 2rem;
}

.quiz-wrapper {
  width: 100%;
  max-width: 600px;
}

/* 题目完成后的样式 */
h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

ul {
  list-style-type: disc;
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
}
</style>
