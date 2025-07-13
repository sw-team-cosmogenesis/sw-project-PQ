<script setup lang="ts">
import { ref, computed } from 'vue'

const searchQuery = ref('')
//统计列表中 presentation 的个数
const presentationCount = computed(() => filteredPresentations.value.length)

const presentations = ref([
  { id: 1, title: '如何高效演讲', description: '关于演讲技巧的分享' },
  { id: 2, title: 'AI 与教育', description: '探讨AI在课堂中的应用' },
  { id: 3, title: 'Vue3 项目实战', description: '介绍如何使用 Vue3 构建项目' },
])

const filteredPresentations = computed(() =>
  presentations.value.filter((p) =>
    p.title.includes(searchQuery.value)
  )
)


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
      <div class="search-box">
        <input type="text" v-model="searchQuery" placeholder="搜索演讲..." />
      </div>
    </div>

    <!--统计列表中元素个数-->
    <div class="presentation-count">
    演讲（{{ presentationCount }}）
    </div>

    <!-- 列表区域 -->
    <div class="presentation-list">
      <div
        class="presentation-card"
        v-for="item in filteredPresentations"
        :key="item.id"
      >
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
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
  background-color: black;
  color: white;
}

.btn-outline {
  background-color: #f2f2f2; /* 淡灰色背景 */
  color: black;
  border: none; /* 去掉边框 */
}

/* 搜索框容器 */
.search-box {
  margin-left: auto; /* 将搜索框推向右侧 */
}

/* 搜索框 */
.search-box input {
  padding: 0.4rem 0.75rem;
  font-size: 14px;
  border: none;
  border-radius: 10px; /* 圆角矩形（胶囊形） */
  background-color: #f2f2f2; /* 淡灰色背景 */
  outline: none;
  width: 400px; /* 可选：你可以根据需要调整宽度 */
  height: 42px;
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
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

/* 每个演讲卡片 */
.presentation-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  background-color: #fafafa;
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.05);
}

.presentation-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 16px;
}
</style>
