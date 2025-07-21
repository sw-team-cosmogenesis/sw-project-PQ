<script setup lang="ts">
import { useRouter, useRoute, RouterLink } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goBack = () => {
  router.push('/presentations')
}
</script>

<template>
  <nav class="side-nav">
    <!-- 返回按钮 -->
    <button class="top-btn" @click="goBack">← 返回</button>

    <!-- 导航按钮 -->
    <div class="side-nav__links">
      <RouterLink
        :to="{ name: 'EditView', params: { uuid: route.params.uuid } }"
        class="nav-item"
        :class="{ active: $route.name === 'PresentationEdit' || $route.name === 'PresentationDefault' }"
      >
        <span class="active-indicator" v-if="$route.name === 'PresentationEdit' || $route.name === 'PresentationDefault'"></span>
        <span class="nav-label">编辑</span>
      </RouterLink>

      <RouterLink
        :to="{ name: 'ResultView', params: { uuid: route.params.uuid } }"
        class="nav-item"
        :class="{ active: $route.name === 'PresentationResult' }"
      >
        <span class="active-indicator" v-if="$route.name === 'PresentationResult'"></span>
        <span class="nav-label">结果</span>
      </RouterLink>
    </div>
  </nav>
</template>

<style scoped>
.side-nav {
  position: fixed;
  top: 84px;
  left: 20px;
  width: 150px;
  height: calc(100vh - 64px);
  background-color: #ffffff;
  padding-top: 1rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.top-btn {
  margin: 1rem auto 2rem;
  background: none;
  border: none;
  color: #4b1a99;
  font-weight: bold;
  cursor: pointer;
  font-size: 14px;
}

.side-nav__links {
  margin-top: 1rem;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 32px;
  padding: 0 1rem 0 1.5rem;
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

.nav-label {
  flex-grow: 1;
}

.nav-label.active {
  font-weight: bolder;
}
</style>
