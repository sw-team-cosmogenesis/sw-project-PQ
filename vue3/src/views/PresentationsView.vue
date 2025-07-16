<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import {RouterLink} from 'vue-router'
import api from '@/utils/api.ts'
const isFocused = ref(false)

const clearSearch = () => {
  searchQuery.value = ''
}

interface presentation {
  uuid: string
  title: string
  description: string
  updated_at: string  // 假设后端返回的是 ISO 格式时间字符串
}

// 日期格式化函数
const formatDate = (isoString: string) => {
  const date = new Date(isoString)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `编辑于 ${year}年${month}月${day}日`
}

const searchQuery = ref('')

const presentations = ref<presentation[]>([])
const filteredPresentations = computed(() =>
  presentations.value.filter((p) =>
    p.title.includes(searchQuery.value)
  )
)
const presentationCount = computed(() => filteredPresentations.value.length)

// 页面加载时从后端拉取数据
onMounted(async () => {
  try {
    const res = await api.get('http://localhost:8000/api/presentations/')
    presentations.value = res.data
  } catch (err) {
    console.error('获取演讲列表失败:', err)
  }
})

</script>

<template>
  <div class="presentation-container">

    <h1 class="page-title">我的演讲</h1>

    <div class="toolbar">
      <div class="left-controls">
        <div class="button-group">
          <button class="btn btn-primary">新建演讲</button>
          <button class="btn btn-outline">临时占位</button>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-box" :class="{ focused: isFocused }">
        <img src="@/assets/search.svg" class="search-icon-left" alt="搜索"/>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索演讲..."
          @focus="isFocused = true"
          @blur="isFocused = false"
        />
        <img
          v-if="searchQuery"
          src="@/assets/x.svg"
          class="search-icon-clear"
          alt="清除"
          @click="clearSearch"
        />
      </div>
    </div>

    <!--统计列表中元素个数-->
    <div class="presentation-count">
      演讲（{{ presentationCount }}）
    </div>

    <!-- 列表区域 -->
    <div class="presentation-list">
      <div
        class="presentation-wrapper"
        v-for="item in filteredPresentations"
        :key="item.uuid"
      >
        <router-link
          :to="`/presentation/${item.uuid}`"
          class="presentation-link"
        >
          <div class="presentation-card"></div>
          <div class="presentation-meta">
            <h3 class="presentation-title">{{ item.title }}</h3>
            <p class="presentation-time">{{ formatDate(item.updated_at) }}</p>
          </div>
        </router-link>
        <img
          src="@/assets/dots-horizontal.svg"
          alt="更多操作"
          class="dot-icon"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.presentation-container {
  width: 100%;
  height: 100%;
  padding: 1.5rem;
  box-sizing: border-box;
}

/* 页面标题 */
.page-title {
  font-size: 2rem;
  font-weight: normal;
  margin-bottom: 1.5rem;
  color: #222;
}

/* 工具栏整体 */
.toolbar {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

/* 左侧标题 + 按钮区域 */
.left-controls {
  display: flex;
  align-items: center;
}

/* 按钮组 */
.button-group {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  font-size: 16px;
  border-radius: 9999px;
  cursor: pointer;
  border: 1px solid black;
  transition: background-color 0.2s ease;
}

.btn-primary {
  background-color: rgba(0, 0, 0, 0.83);
  color: white;
}

.btn-primary:hover {
  background-color: rgb(0, 0, 0);
}

.btn-outline {
  background-color: rgba(205, 205, 205, 0.33); /* 淡灰色背景 */
  color: black;
  border: none; /* 去掉边框 */
}

.btn-outline:hover {
  background-color: rgba(205, 205, 205, 0.75); /* 淡灰色背景 */
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  background-color: #f2f2f2;
  border-radius: 10px;
  height: 42px;
  width: 400px;
  padding: 0 2.5rem;
  transition: background-color 0.2s ease, box-shadow 0.2s ease, border 0.2s ease;
  margin-left: auto;
}

.search-box input {
  flex: 1;
  font-size: 14px;
  border: none;
  background: transparent;
  outline: none;
  height: 100%;
  color: #333;
  padding: 0;
  caret-color: #333;
}

.search-icon-left {
  position: absolute;
  left: 0.75rem;
  width: 18px;
  height: 18px;
  opacity: 0.6;
}

.search-icon-clear {
  position: absolute;
  right: 0.75rem;
  width: 16px;
  height: 16px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.search-icon-clear:hover {
  opacity: 1;
}

/* 聚焦状态样式 */
.search-box.focused {
  background-color: white;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
  border: 1px solid #004080;
}

/* 聚焦时隐藏 placeholder */
.search-box.focused input::placeholder {
  color: transparent;
}

/*列表元素个数*/
.presentation-count {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 0.75rem;
  color: #333;
}

/* 演讲卡片列表布局 */
.presentation-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.presentation-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

/* 每个演讲卡片 */
.presentation-card {
  min-height: 180px;
  border: 1px solid #ccc;
  border-radius: 16px;
  background-color: white;
  transition: box-shadow 0.2s ease;
  flex: 1;
}

.presentation-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.presentation-meta {
  text-align: left;
  padding: 0 0.25rem;
}


.presentation-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #111;
  margin: 0;
}

.presentation-time {
  font-size: 0.9rem;
  color: #777;
  margin: 0.2rem 0 0;
}

.presentation-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 16px;
}

.dot-icon {
  position: absolute;
  right: 0.5rem;
  bottom: 1.5rem;
  width: 20px;
  height: 20px;
  opacity: 0;
  transition: opacity 0.2s ease, filter 0.2s ease;
  cursor: pointer;
}

/* 父元素悬停时图标显现 */
.presentation-wrapper:hover .dot-icon {
  opacity: 0.7;
}

.presentation-link {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  flex: 1;
}

.presentation-link:hover {
  background-color: transparent; /* 禁止悬停背景 */
}
</style>
