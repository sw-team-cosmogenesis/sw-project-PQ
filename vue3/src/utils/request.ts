import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,  // 使用环境变量
  timeout: 2000,
})

export default instance
