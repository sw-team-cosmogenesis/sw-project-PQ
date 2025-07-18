<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import api from "@/utils/api.ts";

const route = useRoute()
const presentationUuid = route.params.uuid as string

const selectedFile = ref<File | null>(null)
const fileType = ref('ppt')

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement | null
  if (!target || !target.files || target.files.length === 0) {
    selectedFile.value = null
    return
  }
  selectedFile.value = target.files[0]
}

const uploadFile = async () => {
  if (!selectedFile.value) return alert('请选择文件')

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('type', fileType.value)
  formData.append('title', selectedFile.value.name)
  formData.append('presentation_uuid', presentationUuid)
  try {
    await api.post('http://localhost:8000/api/upload-media/', formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    alert('上传成功')
  } catch (error) {
    alert('上传失败')
    console.error(error)
  }
}
</script>

<template>
  <div class="upload-panel">
    <label>选择文件：
      <input type="file" @change="onFileChange" />
    </label>

    <label>材料类型：
      <select v-model="fileType">
        <option value="ppt">PPT</option>
        <option value="video">视频</option>
        <option value="audio">音频</option>
        <option value="image">图片</option>
        <option value="pdf">PDF</option>
        <option value="other">其他</option>
      </select>
    </label>

    <button @click="uploadFile">上传材料</button>
  </div>
</template>

<style scoped>
.upload-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 1em;
}
</style>
