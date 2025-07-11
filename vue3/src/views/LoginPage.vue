<script setup lang="ts">
import { ref } from 'vue'
import eye from '@/assets/eye.svg'
import eyeSlash from '@/assets/eye-slash.svg'

const showPassword = ref(false)

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// 邮箱检测
const email = ref('')
const emailError = ref(false)

const validateEmailFormat = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const onEmailInput = () => {
  emailError.value = !validateEmailFormat(email.value)
}
</script>

<template>
  <div class="login-page">
    <!-- 欢迎文字容器，与登录框并列 -->
    <div class="login-page-header">
      <p class="welcome-text">_(:з」∠) 欢迎回来  ( ° ∀ ° )ﾉ</p>
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
          />
          <img
            :src="showPassword ? eyeSlash : eye"
            class="eye-icon"
            alt="切换密码可见性"
            @click="togglePasswordVisibility"
          />
        </div>
      </div>

      <button class="login-button">登录</button>
      <p class="forgot-password">忘记密码?</p>
    </div>
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
</style>
