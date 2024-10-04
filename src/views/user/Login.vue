<!-- components/Login.vue -->
<template>
  <div class="auth-page">
    <el-card class="auth-container">
      <h2>Вход</h2>
      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="rules"
        @submit.prevent="handleLogin"
        label-position="top"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="Имя пользователя"
            clearable
            prefix-icon="user"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="Пароль"
            clearable
            prefix-icon="lock"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            native-type="submit"
            round
            block
          >
            Войти
          </el-button>
        </el-form-item>
      </el-form>
      <p class="switch-auth">
        Нет аккаунта?
        <el-link type="primary" @click="goToRegister">Регистрация</el-link>
      </p>
    </el-card>
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

  const rules = {
    username: [
      {
        required: true,
        message: 'Пожалуйста, введите имя пользователя',
        trigger: 'blur',
      },
    ],
    password: [
      {
        required: true,
        message: 'Пожалуйста, введите пароль',
        trigger: 'blur',
      },
    ],
  };

  const loginForm = ref(null);

  const handleLogin = async () => {
    await loginForm.value.validate(async (valid: boolean) => {
      if (valid) {
        loading.value = true;
        try {
          await authService.login(
            loginData.value.username,
            loginData.value.password
          );
          ElMessage.success('Успешный вход');
          router.push('/');
        } catch (error) {
          ElMessage.error(error);
        } finally {
          loading.value = false;
        }
      }
    });
  };

  const goToRegister = () => {
    router.push('/register');
  };
</script>

<style scoped>
  .auth-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
  }

  .auth-container {
    width: 400px;
    padding: 30px;
    background-color: #fff;
    border-radius: 8px;
  }

  .auth-container h2 {
    text-align: center;
    margin-bottom: 20px;
  }

  .switch-auth {
    text-align: center;
    margin-top: 20px;
  }

  .el-form-item {
    margin-bottom: 20px;
  }

  .el-input {
    width: 100%;
  }
</style>
