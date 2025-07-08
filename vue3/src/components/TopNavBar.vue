<script setup lang="ts">
import { ref } from 'vue'
import ProfileBox from './ProfileBox.vue'

const showDropdown = ref(false)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}
</script>

<template>
  <nav class="fixed top-0 left-0 w-full h-16 flex items-center justify-between px-6 shadow-md bg-white z-50">
    <!-- 左侧 Logo -->
    <div class="flex items-center">
      <img src="@/assets/logo.svg" alt="Logo" class="h-8 w-auto" />
      <span class="ml-2 font-bold text-lg text-gray-800">AI Pop Quiz</span>
    </div>

    <!-- 右侧头像及弹出框 -->
    <div class="relative">
      <img
        src=""
        alt="Avatar"
        class="h-10 w-10 rounded-full cursor-pointer border border-gray-300"
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

</style>
