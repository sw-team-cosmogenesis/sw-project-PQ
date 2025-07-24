<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {useRoute} from 'vue-router'
import api from '@/utils/api'

// 读取演讲 UUID
const route = useRoute()
const uuid = route.params.uuid as string

// 标题编辑相关
const presentationTitle = ref('加载中...')
const isEditingTitle = ref(false)
const editedTitle = ref('')

// 获取演讲详情
const fetchPresentation = async () => {
  try {
    const res = await api.get(`/presentations/${uuid}/`)
    console.log(res.data)
    presentationTitle.value = res.data.title
  } catch (error) {
    console.error('获取演讲失败:', error)
  }
}

// 保存标题修改
const saveTitle = async () => {
  try {
    await api.patch(`/presentations/${uuid}/`, {
      title: editedTitle.value
    })
    presentationTitle.value = editedTitle.value
    isEditingTitle.value = false
  } catch (error) {
    console.error('标题修改失败:', error)
  }
}

const startEditing = () => {
  editedTitle.value = presentationTitle.value
  isEditingTitle.value = true
}

// 资料列表，初始为空数组
const materials = ref<Array<{
  uuid: string
  title: string
  file: string
  type: string
}>>([])

// 读取相关资料列表
const fetchMaterials = async () => {
  try {
    // 获取指定演讲的所有media文件
    const res = await api.get(`/upload-media/`, {
      params: {presentation: uuid}
    })
    // 假设后端支持用 ?presentation=uuid 来过滤
    materials.value = res.data.results || res.data  // 视后端分页结构调整
  } catch (error) {
    console.error('获取资料失败:', error)
  }
}

// 上传资料相关
const fileInput = ref<HTMLInputElement | null>(null)

const triggerUpload = () => {
  fileInput.value?.click()
}

const uploadMaterial = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const file = target.files[0]
  const formData = new FormData()
  console.log(formData)
  formData.append('file', file)
  formData.append('presentation_uuid', uuid)

  try {
    await api.post(`/upload-media/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    alert('上传成功！')
    target.value = '' // 清空 input
    await fetchMaterials()
  } catch (err) {
    console.error('上传失败:', err)
    alert('上传失败，请重试')
  }
}

onMounted(() => {
  fetchPresentation()
  fetchMaterials()
})
</script>

<template>
  <div class="edit-view">
    <!-- 顶部标题栏 -->
    <div class="top-bar">
      <h2 v-if="!isEditingTitle" @click="startEditing" class="title-display">
        {{ presentationTitle }}
        <span class="edit-tip">(点击修改)</span>
      </h2>
      <div v-else class="edit-title">
        <input v-model="editedTitle" class="title-input"/>
        <button @click="saveTitle" class="save-btn">保存</button>
      </div>
    </div>

    <!-- 主体区域 -->
    <div class="content-area">
      <!-- 右侧资料栏 -->
      <div class="sidebar">
        <div class="sidebar-header">
          <div class="sidebar-title">
            <h3>相关资料</h3>
            <img
              src="@/assets/upload.svg"
              alt="上传"
              class="upload-icon"
              @click="triggerUpload"
            />
          </div>
          <input
            ref="fileInput"
            type="file"
            style="display: none"
            @change="uploadMaterial"
          />
        </div>
        <ul class="material-list">
          <li v-for="material in materials" :key="material.uuid">
            <a :href="material.file" target="_blank" rel="noopener noreferrer">
              {{ material.title }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.edit-view {
  display: flex;
  flex-direction: column;
}

.top-bar {
  padding: 1rem 2rem;
  border-bottom: 1px solid #ccc;
}

.title-display {
  font-size: 1.5rem;
  cursor: pointer;
}

.edit-tip {
  font-size: 0.875rem;
  color: #888;
  margin-left: 0.5rem;
}

.edit-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-input {
  font-size: 1.25rem;
  padding: 0.25rem 0.5rem;
}

.save-btn {
  padding: 0.25rem 0.75rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
}

.content-area {
  flex: 1;
  display: flex;
  padding: 1rem 2rem;
}

/* 右侧资料栏 */
.sidebar {
  margin-left: auto;
  width: 260px;
  border-left: 1px solid #ddd;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
}
.sidebar-title {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* 图标和文字之间的间距 */
}
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.upload-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.material-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.material-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}
</style>
