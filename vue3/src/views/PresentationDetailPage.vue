<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import AudienceDetailView from "@/components/AudienceDetailView.vue";
import OrganizerDetailView from "@/components/OrganizerDetailView.vue";
import EditView from "@/views/EditView.vue";

interface Presentation{
  title:string,
  description:string,
}

// 获取当前路径中的 uuid
const route = useRoute()
const uuid = route.params.uuid as string

const userRole = ref<'audience' | 'presenter' | 'organizer' | null>(null)
const presentation = ref<Presentation>({ title: '',description: '',  })

// 加载数据
onMounted(async () => {
  try {
    const res = await axios.get(`/api/presentations/${uuid}/detail/`)
    presentation.value = res.data.presentation
    userRole.value = res.data.role  // 后端根据用户返回角色
  } catch (err) {
    console.error('获取详情失败', err)
  }
})
</script>

<template>
    <div v-if="presentation">
    <h1>{{ presentation.title }}</h1>
    <p>{{ presentation.description }}</p>

    <div v-if="userRole === 'audience'">
      <!-- 展示观众的作答与反馈 -->
      <AudienceDetailView :presentation="presentation" />
    </div>

    <div v-else-if="userRole === 'presenter'">
      <!-- 上传资源 & 查看观众反馈 -->
      <EditView :presentation="presentation" />
    </div>

    <div v-else-if="userRole === 'organizer'">
      <!-- 组织者视图 -->
      <OrganizerDetailView :presentation="presentation" />
    </div>

    <div v-else>
      <p>无访问权限</p>
    </div>
  </div>
</template>

<style scoped>

</style>
