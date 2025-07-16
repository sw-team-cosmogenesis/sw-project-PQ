import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
})

// 请求拦截：自动加 Authorization
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：token过期尝试刷新
api.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config
    if (
      err.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refresh_token')
    ) {
      originalRequest._retry = true
      try {
        const refreshRes = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: localStorage.getItem('refresh_token'),
        })
        localStorage.setItem('access_token', refreshRes.data.access)
        originalRequest.headers.Authorization = `Bearer ${refreshRes.data.access}`
        return api(originalRequest)
      } catch (refreshErr) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
        return Promise.reject(refreshErr)
      }
    }
    return Promise.reject(err)
  }
)

export default api
