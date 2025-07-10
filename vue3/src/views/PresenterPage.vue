<script setup lang="ts">

import LeftSideNavBar from "@/components/LeftSideNavBar.vue";
import { RouterLink } from "vue-router";


</script>

<template>
    <div class="presenter">
    <LeftSideNavBar />
    <main class="presenter-main">
      <RouterLink to = "/home" />
      <RouterLink to="/presentation"/>
    </main>
  </div>
</template>

<style scoped>
.presenter {
  display: flex;
}

.presenter-main {
  margin-left: 200px; /* 与 SideNavBar 宽度保持一致 */
  padding: 1rem;
  flex: 1;
  min-height: calc(100vh - 64px);
  margin-top: 64px;
}
</style>
