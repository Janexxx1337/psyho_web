<!-- components/Login.vue -->
<template>
  <div class="auth-container">
    <h2>Вход</h2>
    <el-form ref="loginForm" :model="loginData" @submit.prevent="handleLogin">
      <el-form-item prop="username">
        <el-input
            v-model="loginData.username"
            placeholder="Имя пользователя"
            clearable
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
            v-model="loginData.password"
            type="password"
            placeholder="Пароль"
            clearable
        />
      </el-form-item>
      <el-button type="primary" :loading="loading" native-type="submit">
        Войти
      </el-button>
      <el-button type="text" @click="goToRegister">Нет аккаунта? Регистрация</el-button>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '@/services/authService';
import { ElMessage } from 'element-plus';

const router = useRouter();
const loginData = ref({
  username: '',
  password: '',
});
const loading = ref(false);

const handleLogin = async () => {
  loading.value = true;
  try {
    await authService.login(loginData.value.username, loginData.value.password);
    ElMessage.success('Успешный вход');
    router.push('/');
  } catch (error) {
    ElMessage.error(error);
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
