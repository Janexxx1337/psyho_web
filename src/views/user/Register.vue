<!-- components/Register.vue -->
<template>
  <div class="auth-container">
    <h2>Регистрация</h2>
    <el-form ref="registerForm" :model="registerData" @submit.prevent="handleRegister">
      <el-form-item prop="username">
        <el-input
            v-model="registerData.username"
            placeholder="Имя пользователя"
            clearable
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
            v-model="registerData.password"
            type="password"
            placeholder="Пароль"
            clearable
        />
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input
            v-model="registerData.confirmPassword"
            type="password"
            placeholder="Подтвердите пароль"
            clearable
        />
      </el-form-item>
      <el-button type="primary" :loading="loading" native-type="submit">
        Зарегистрироваться
      </el-button>
      <el-button type="text" @click="goToLogin">Уже есть аккаунт? Вход</el-button>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '@/services/authService';
import { ElMessage } from 'element-plus';

const router = useRouter();
const registerData = ref({
  username: '',
  password: '',
  confirmPassword: '',
});
const loading = ref(false);

const handleRegister = async () => {
  if (registerData.value.password !== registerData.value.confirmPassword) {
    ElMessage.error('Пароли не совпадают');
    return;
  }
  loading.value = true;
  try {
    await authService.register(registerData.value.username, registerData.value.password);
    ElMessage.success('Успешная регистрация');
    await router.push('/login');
  } catch (error) {
    ElMessage.error(error);
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
