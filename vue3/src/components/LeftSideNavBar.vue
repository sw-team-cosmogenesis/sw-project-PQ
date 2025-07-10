<script setup lang="ts">
import { RouterLink } from 'vue-router'
import HomeIcon from '@/assets/home-outline.svg'
import PresentationIcon from "@/assets/presentation-outline.svg";

const navItems = [
  { path: '/presenter/home', label: '主 页', icon: HomeIcon },
  { path: '/presenter/presentation', label: '我的演讲', icon: PresentationIcon },
]
</script>

<template>
  <nav class="side-nav">
    <div class="side-nav__links">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="nav-item"
      :class="{ active: $route.path === item.path }"
    >
      <span class="active-indicator" v-if="$route.path === item.path"></span>

      <!-- 图标 -->
      <img :src="item.icon" alt="icon" class="nav-icon" />

      <!-- 标签 -->
      <span class="nav-label" :class="{active:$route.path === item.path}">{{ item.label }}</span>
    </router-link>
    </div>
  </nav>
</template>


<style scoped>
.side-nav {
  position: fixed;
  top: 84px;
  left: 20px;
  width: 150px; /* 200 × 0.75 */
  height: calc(100vh - 64px);
  background-color: #ffffff;
  padding-top: 1rem;
  box-sizing: border-box;
}

.side-nav__links{
  margin-top: 5rem;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;        /* 垂直居中 */
  justify-content: flex-start; /* 水平靠左对齐 */
  height: 32px;               /* 减小高度 */
  padding: 0 1rem 0 1.5rem;   /* 缩小上下 padding，只保留左右 */
  border-radius: 8px;
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s ease;
  font-size: 17px;
  margin-bottom: 8px;
  gap: 0.5rem;
}

.nav-item:hover {
  background-color: #f2f2f2;
}

.nav-item.active {
  font-weight: bolder;
  background-color: transparent;
}

.nav-item.active:hover {
  background-color: #f2f2f2;
}

.active-indicator {
  position: absolute;
  left: 0;
  top: 4px;
  bottom: 4px;
  width: 2px;
  border-radius: 0 4px 4px 0;
  background-color: #4b1a99;
}

.nav-icon {
  width: 16px;
  height: 16px;
}

.nav-label {
  flex-grow: 1;
}

.nav-label.active {
  flex-grow: 1;
  font-weight: bolder;
}
</style>


