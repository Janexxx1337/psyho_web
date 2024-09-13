<!-- components/UserProfile.vue -->
<template>
  <div class="profile-container">
    <h2>Профиль пользователя</h2>
    <el-form :model="userData" @submit.prevent="updateProfile">
      <el-form-item label="Имя пользователя">
        <el-input v-model="userData.username" disabled />
      </el-form-item>
      <!-- Добавьте другие поля профиля по необходимости -->
      <el-form-item label="Новый пароль">
        <el-input
            v-model="userData.newPassword"
            type="password"
            placeholder="Оставьте пустым, чтобы не изменять"
            clearable
        />
      </el-form-item>
      <el-button type="primary" native-type="submit">
        Обновить профиль
      </el-button>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { authService } from '@/services/authService';
import { ElMessage } from 'element-plus';

const userData = ref({
  username: '',
  newPassword: '',
});

onMounted(() => {
  const currentUser = authService.getCurrentUser();
  if (currentUser) {
    userData.value.username = currentUser.username;
  }
});

const updateProfile = () => {
  // Здесь можно добавить логику обновления профиля через бэкенд
  if (userData.value.newPassword) {
    ElMessage.success('Пароль обновлен');
    userData.value.newPassword = '';
  } else {
    ElMessage.info('Профиль обновлен');
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
