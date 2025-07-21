<script setup lang="ts">
import {RouterView}  from 'vue-router';
import PresenterLeftSidebar from '@/components/PresenterLeftSidebar.vue'
</script>

<template>

    <PresenterLeftSidebar />
    <div class="main-content">
      <router-view />
    </div>
</template>

<style scoped>
.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
