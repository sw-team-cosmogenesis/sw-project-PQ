<script setup lang="ts">

import LeftSideNavBar from "@/components/LeftSideNavBar.vue";
import { RouterView } from "vue-router";


</script>

<template>
    <LeftSideNavBar />
    <main class="main-content">
      <RouterView />
    </main>
</template>

<style scoped>

.main-content {
  width: 100%;
  height: 100%;
  flex: 1;
  padding: 1.5rem;
  min-height: calc(100vh - 240px); /* 减去顶部导航高度（如有） */
  box-sizing: border-box;
}
</style>
