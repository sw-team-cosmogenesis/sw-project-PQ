<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'

const emit = defineEmits(['close', 'delete', 'rename'])
const props = defineProps<{ x: number; y: number }>()
const menuRef = ref<HTMLElement | null>(null)

const handleClickOutside = (e: MouseEvent) => {
  if (menuRef.value && !menuRef.value.contains(e.target as Node)) {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<template>
  <div
    class="dropdown-menu"
    :style="{ top: `${y}px`, left: `${x}px` }"
    ref="menuRef"
  >
    <ul>
      <li @click="emit('delete')">删除</li>
    </ul>
  </div>
</template>

<style scoped>
.dropdown-menu {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  z-index: 2000;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  min-width: 120px;
  padding: 0.5rem 0;
}

.dropdown-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-menu li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 14px;
}

.dropdown-menu li:hover {
  background-color: #f0f0f0;
}
</style>
