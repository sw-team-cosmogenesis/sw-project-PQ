<script setup lang="ts">
import {ref} from 'vue'
import {useRouter, RouterLink} from 'vue-router'
import axios, {type AxiosError} from 'axios'
import eye from '@/assets/eye.svg'
import eyeSlash from '@/assets/eye-slash.svg'

const router = useRouter()

// 表单状态
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const emailError = ref(false)
const loginError = ref('')

// 切换密码显示
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// 邮箱格式校验
const validateEmailFormat = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const onEmailInput = () => {
  emailError.value = !validateEmailFormat(email.value)
}

// 登录逻辑
const login = async () => {
  loginError.value = ''

  if (!validateEmailFormat(email.value)) {
    emailError.value = true
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/api/login/', {
      email: email.value,
      password: password.value,
    })

    const {access, refresh} = res.data

    // 存入 localStorage
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    // 跳转至主界面
    router.push('/presenter/presentations/')
  } catch (err: unknown) {
    const error = err as AxiosError<{ detail?: string }>
    loginError.value = error.response?.data?.detail || '登录失败，请检查邮箱和密码'
  }
}
</script>


<template>
  <div class="login-page">
    <!-- 欢迎文字容器，与登录框并列 -->
    <div class="login-page-header">
      <p class="welcome-text">_(:з」∠) 欢迎回来 ( ° ∀ ° )ﾉ</p>
    </div>

    <div class="login-box">
      <h2 class="login-title">登录你的 PopQuiz 账户</h2>

      <div class="field-group">
        <label class="input-label">邮箱：</label>
        <input
          type="email"
          class="input-field"
          v-model="email"
          @input="onEmailInput"
          :class="{ 'input-error': emailError }"
        />
        <p class="error-text" :class="{ visible: emailError }">邮箱格式有误</p>
      </div>

      <div class="field-group password-group">
        <label class="input-label">密码：</label>
        <div class="password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            class="input-field"
            v-model=password
          />
          <img
            :src="showPassword ? eye : eyeSlash"
            class="eye-icon"
            alt="切换密码可见性"
            @click="togglePasswordVisibility"
          />
        </div>
      </div>
      <p v-if="loginError" class="login-error">{{ loginError }}</p>
      <button class="login-button" @click="login">登录</button>
      <p class="forgot-password">忘记密码?</p>
    </div>
    <p class="register-text">
      新用户？
      <router-link to="/register" class="register-link">点击注册</router-link>
    </p>
  </div>
</template>

<style scoped>
.login-page {
  height: 80vh;
  padding-right: 10rem;
  padding-bottom: 10rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem; /* 控制欢迎文字与登录框之间的距离 */
}

/* 欢迎文字容器 */
.login-page-header {
  text-align: center;
}

.welcome-text {
  font-size: 35px;
  color: #333;
  font-family: 'Microsoft YaHei', sans-serif;
  margin-bottom: 1rem;
}

/* 登录框样式 */
.login-box {
  background-color: white;
  padding: 2.5rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 100px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.login-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: black;
  text-align: center;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.input-label {
  font-size: 14px;
  color: #333;
  margin-bottom: 0.2rem;
  font-weight: bold;
}

.input-field {
  padding: 0.75rem 1rem;
  border: none;
  background-color: #e5e5e5;
  border-radius: 10px;
  font-size: 1rem;
  width: 100%;
  outline: none;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.input-field:focus {
  background-color: white;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.input-error {
  box-shadow: 0 0 0 1px rgb(207, 0, 0);
  background-color: rgba(255, 97, 97, 0.08);
}

.error-text {
  font-size: 0.85rem;
  height: 0.5rem; /* 固定高度，预留空间 */
  margin-top: 0.25rem;
  color: transparent; /* 默认不可见 */
  transition: color 0.3s ease;
}

.error-text.visible {
  color: red;
}

.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-wrapper .input-field {
  padding-right: 2.5rem;
}

.eye-icon {
  position: absolute;
  right: 1rem;
  width: 24px;
  height: 24px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.eye-icon:hover {
  opacity: 1;
}

.login-button {
  margin-top: 1rem;
  background-color: #333333;
  color: white;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 9999px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-button:hover {
  background-color: black;
}

.forgot-password {
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  cursor: pointer;
  margin-top: -0.5rem;
  text-decoration: none; /* 默认无下划线 */
}

.forgot-password:hover {
  text-decoration: underline; /* 鼠标悬停时显示下划线 */
}

.login-error {
  color: red;
  font-size: 0.9rem;
  text-align: center;
  margin-top: -1rem;
  margin-bottom: -1.5rem;
}


.register-text {
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  margin-top: 0.75rem;
}

.register-link {
  color: #007bff;
  text-decoration: none;
  margin-left: 0.25rem;
  font-weight: 500;
}

.register-link:hover {
  text-decoration: underline;
}
</style>
