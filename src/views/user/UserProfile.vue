<!-- components/UserProfile.vue -->
<template>
  <div class="profile-page">
    <el-card class="profile-container">
      <div class="profile-header">
        <el-avatar
            class="profile-avatar"
            size="80"
            src="https://example.com/default-avatar.png"
        ></el-avatar>
        <h2>{{ userData.username }}</h2>
      </div>
      <el-form :model="userData" @submit.prevent="updateProfile" label-position="top">
        <!-- Добавьте другие поля профиля по необходимости -->
        <el-form-item label="Новый пароль">
          <el-input
              v-model="userData.newPassword"
              type="password"
              placeholder="Оставьте пустым, чтобы не изменять"
              clearable
              prefix-icon="lock"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" round>
            Обновить профиль
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
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
.profile-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.profile-container {
  width: 400px;
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 20px;
}

.profile-avatar {
  margin-bottom: 10px;
}

.el-form-item {
  margin-bottom: 20px;
}
</style>
