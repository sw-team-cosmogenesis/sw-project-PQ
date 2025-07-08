<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

// 接收由父组件传来的控制显示的 props
const props = defineProps<{
  visible: boolean
}>()

const emits = defineEmits<{
  (e: 'close'): void
}>()

const dropdownRef = ref<HTMLElement | null>(null)

function handleClickOutside(event: MouseEvent) {
  if (
    props.visible &&
    dropdownRef.value &&
    !dropdownRef.value.contains(event.target as Node)
  ) {
    emits('close')
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <transition name="fade">
    <div
      v-if="visible"
      ref="dropdownRef"
      class="absolute top-12 right-0 bg-white rounded-lg shadow-lg border border-gray-200 w-48 py-2 z-50"
    >
      <ul class="text-sm text-gray-700">
        <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer">个人中心</li>
        <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer">设置</li>
        <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer">退出登录</li>
      </ul>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
