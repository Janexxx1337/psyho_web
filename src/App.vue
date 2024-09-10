<script setup lang="ts">
import { RouterView } from 'vue-router';
import Sidebar from './components/Sidebar.vue'; // Импортируем компонент сайдбара
</script>

<template>
  <el-container>
    <!-- Сайдбар -->
    <Sidebar />

    <!-- Основное содержимое -->
    <el-main>
      <RouterView />
    </el-main>
  </el-container>
</template>

<style scoped>
.el-main {
  padding: 20px;
}
:deep(svg.input-icon) {
 width:20px;
 height: 20px;
}
</style>
