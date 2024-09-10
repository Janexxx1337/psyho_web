<script setup lang="ts">
import { ElMenu, ElMenuItem } from 'element-plus';
import { useRouter } from 'vue-router';

// Импортируем нужные иконки из Element Plus
import { Menu as MenuIcon, Document as DocumentIcon } from '@element-plus/icons-vue';

const router = useRouter();

// Функция для обработки перехода по маршрутам
const handleMenuSelect = (index: string) => {
  router.push(index);
};
</script>

<template>
  <el-aside width="200px" class="sidebar">
    <el-menu default-active="1" @select="handleMenuSelect">
      <!-- Главная страница -->
      <el-menu-item index="/">
        <!-- Используем иконку как компонент -->
        <MenuIcon class="input-icon"/>
        <span>Главная</span>
      </el-menu-item>
      <!-- История -->
      <el-menu-item index="/history">
        <!-- Используем иконку как компонент -->
        <DocumentIcon class="input-icon"/>
        <span>История</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style scoped>
.sidebar {
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  min-height: 100vh;
  padding-top: 20px;
}

.el-menu {
  height: 100%;
  border-right: none;
}

.el-menu-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.el-menu-item span {
  margin-left: 8px;
}
.sidebar {
  overflow: hidden;
}
</style>
