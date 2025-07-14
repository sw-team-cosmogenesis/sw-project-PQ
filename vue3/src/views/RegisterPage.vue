<script setup lang="ts">
import { ref } from 'vue'
import { AxiosError } from 'axios'
import { RouterLink, useRouter } from 'vue-router'
import eye from '@/assets/eye.svg'
import eyeSlash from '@/assets/eye-slash.svg'
import axios from 'axios'

const email = ref('')
const emailError = ref(false)

const password = ref('')
const confirmPassword = ref('')
const passwordError = ref(false)

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const router = useRouter()
const error = ref('')
const loginError = ref('')

const validateEmailFormat = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const onEmailInput = () => {
  emailError.value = !validateEmailFormat(email.value)
}

const onConfirmPasswordInput = () => {
  passwordError.value = confirmPassword.value !== password.value
}

const register = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = '两次密码不一致'
    return
  }

  try {
    await axios.post('http://localhost:8000/api/register/', {
      email: email.value,
      password: password.value
    })
    router.push('/login')  // 注册成功跳转登录页
  } catch (err: unknown) {
    const error = err as AxiosError<{ detail?: string }>
    loginError.value = error.response?.data?.detail || '注册失败'
  }
}
</script>

<template>
  <div class="register-page">
    <div class="register-page-header">
      <p class="welcome-text">注册 PopQuiz 账户</p>
    </div>

    <div class="register-box">
      <h2 class="register-title">创建你的 PopQuiz 账户</h2>

      <!-- 邮箱 -->
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

      <!-- 密码 -->
      <div class="field-group password-group">
        <label class="input-label">密码：</label>
        <div class="password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            class="input-field"
            v-model="password"
            @input="onConfirmPasswordInput"
            :class="{ 'input-error': passwordError }"
          />
          <img
            :src="showPassword ? eye : eyeSlash"
            class="eye-icon"
            alt="切换密码可见性"
            @click="() => (showPassword = !showPassword)"
          />
        </div>
      </div>

      <!-- 确认密码 -->
      <div class="field-group password-group">
        <label class="input-label">确认密码：</label>
        <div class="password-wrapper">
          <input
            :type="showConfirmPassword ? 'text' : 'password'"
            class="input-field"
            v-model="confirmPassword"
            @input="onConfirmPasswordInput"
            :class="{ 'input-error': passwordError }"
          />
          <img
            :src="showConfirmPassword ? eye : eyeSlash"
            class="eye-icon"
            alt="切换密码可见性"
            @click="() => (showConfirmPassword = !showConfirmPassword)"
          />
        </div>
        <p class="error-text" :class="{ visible: passwordError }">两次密码不一致</p>
      </div>

      <button class="register-button" @click = "register">注册</button>
      <p class="back-login">
        已有账户？
        <RouterLink to="/login" class="register-link">返回登录</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  height: 80vh;
  padding-right: 10rem;
  padding-bottom: 10rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.register-page-header {
  text-align: center;
}

.welcome-text {
  font-size: 35px;
  color: #333;
  font-family: 'Microsoft YaHei', sans-serif;
  margin-bottom: 1rem;
}

.register-box {
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

.register-title {
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
  height: 0.5rem;
  margin-top: 0.25rem;
  color: transparent;
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

.register-button {
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

.register-button:hover {
  background-color: black;
}

.back-login {
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  margin-top: -0.5rem;
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
