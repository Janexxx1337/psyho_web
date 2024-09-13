<script setup lang="ts">
import { computed } from 'vue';
import { RouterView } from 'vue-router';
import Sidebar from './components/common/Sidebar.vue';
import { authService } from './services/authService';

const isAuthenticated = computed(() => !!authService.currentUser.value);
</script>

<template>
  <el-container>
    <!-- Сайдбар отображается, если пользователь авторизован -->
    <Sidebar v-if="isAuthenticated" />
    <!-- Основное содержимое -->
    <el-main :style="{ marginLeft: isAuthenticated ? '200px' : '0' }">
      <RouterView />
    </el-main>
  </el-container>
</template>

<style scoped>
.el-main {
  padding: 20px;
  overflow: hidden;
}

.main-container {
  margin-left: 200px;
  transition: margin-left 0.3s;
}

:deep(svg.input-icon) {
  width:20px;
  height: 20px;
}

@media (max-width: 768px) {
  .main-container {
    margin-left: 64px;
  }
}
</style>
