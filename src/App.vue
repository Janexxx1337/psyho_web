<script setup lang="ts">
import { computed } from 'vue';
import { RouterView } from 'vue-router';
import Sidebar from './components/common/Sidebar.vue';
import { authService } from './services/authService';

const isAuthenticated = computed(() => !!authService.currentUser.value);
const isMobile = computed(() => window.innerWidth <= 768); // Определяем мобильное устройство
</script>

<template>
  <el-container>
    <!-- Сайдбар отображается, если пользователь авторизован и не на мобильном устройстве -->
    <Sidebar v-if="isAuthenticated && !isMobile" />
    <!-- Основное содержимое -->
    <el-main :style="{ marginLeft: isAuthenticated && !isMobile ? '200px' : '0' }">
      <RouterView />
    </el-main>
  </el-container>
</template>

<style scoped>
* {
  font-family: "Lato", sans-serif;
}

.el-main {
  padding: 20px;
  overflow: hidden;
}

.main-container, .el-main {
  margin-left: 200px;
  transition: margin-left 0.3s;
}

:deep(svg.input-icon) {
  width: 20px;
  height: 20px;
}

@media (max-width: 768px) {
  .main-container,
  .el-main {
    margin-left: 0!important;
  }
}
</style>
