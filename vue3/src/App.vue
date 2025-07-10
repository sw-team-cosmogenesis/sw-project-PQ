<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import QuizPage from "@/views/QuizPage.vue";
import TopNavBar from "@/components/TopNavBar.vue";
</script>

<template>
  <div class="app-container">
    <TopNavBar/>
    <main  class="app-main-container">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh; /* 让整体高度占满屏幕 */
  width: 70vw;
}

.app-main-container {
  flex: 1; /* 填充顶部以外的空间 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中（可选） */
  padding-top: 4rem;       /* 防止被顶部栏遮住 */
}
</style>
