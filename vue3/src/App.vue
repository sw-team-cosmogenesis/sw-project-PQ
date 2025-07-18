<script setup lang="ts">
import {RouterView } from 'vue-router'
import { useRoute } from 'vue-router'
import TopNavBar from "@/components/TopNavBar.vue";

const route = useRoute()
// 在登陆和注册页面隐藏顶部栏

</script>

<template class="background">
  <div>
    <TopNavBar v-if="!route.meta.hideNavbar"/>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>

.main{
  width: 80vw;
  height: 80vh;
  margin-top: 50px;
}
</style>
