<script setup lang="ts">
import { ref } from 'vue'
import ProfileBox from './ProfileBox.vue'

const showDropdown = ref(false)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}
</script>

<template>
  <nav class="top-nav">
    <!-- 左侧 Logo -->
    <div class="logo-area">
      <img src="@/assets/logo.svg" alt="Logo" class="logo-img" />
      <span class="site-name">AI Pop Quiz</span>
    </div>

    <!-- 右侧头像及弹出框 -->
    <div class="avatar-area">
      <img
        src="../assets/avatar.jpg"
        alt="Avatar"
        class="avatar-img"
        @click="toggleDropdown"
      />

      <!-- 弹出框组件 -->
      <ProfileBox
        :visible="showDropdown"
        @close="showDropdown = false"
      />
    </div>
  </nav>
</template>


<style scoped>
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 84px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 50;
}

.logo-area {
  display: flex;
  align-items: center;
}

.logo-img {
  height: 32px;
  width: auto;
}

.site-name {
  margin-left: 8px;
  font-weight: bold;
  font-size: 18px;
  color: #2d2d2d;
}

.avatar-area {
  position: relative;
}

.avatar-img {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  border: 1px solid #d1d5db;
  cursor: pointer;
  object-fit: cover;
}
</style>
