<!-- components/Sidebar.vue -->
<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  Menu as MenuIcon,
  Document as DocumentIcon,
  User as UserIcon,
  SwitchButton,
  MagicStick,
  SwitchFilled,
} from '@element-plus/icons-vue';
import { authService } from '@/services/authService';

const router = useRouter();
const route = useRoute();

const currentUser = computed(() => authService.currentUser.value);

const handleLogout = () => {
  authService.logout();
  router.push('/login');
};
</script>

<template>
  <div>
    <!-- Боковое меню для десктопа -->
    <el-aside class="sidebar" width="200px">
      <el-menu
          :default-active="route.path"
          router
          background-color="#2d3a4b"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
      >
        <!-- Пункты меню -->
        <el-menu-item index="/">
          <MenuIcon class="input-icon" />
          <span>Доктор ИИ</span>
        </el-menu-item>
        <el-menu-item index="/Logic">
          <SwitchFilled class="input-icon" />
          <span>Тест: Логика</span>
        </el-menu-item>
        <el-menu-item index="/history">
          <DocumentIcon class="input-icon" />
          <span>История</span>
        </el-menu-item>
        <el-menu-item index="/profile">
          <UserIcon class="input-icon" />
          <span>Профиль</span>
        </el-menu-item>
        <el-menu-item index="/mood-diary">
          <MagicStick class="input-icon" />
          <span>Дневник настроений</span>
        </el-menu-item>

        <!-- Разделитель перед кнопкой "Выйти" -->
        <el-menu-item-group>
          <el-menu-item index="logout" @click="handleLogout">
            <SwitchButton class="input-icon" />
            <span>Выйти</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-menu>
    </el-aside>


    <!-- Нижнее меню для мобильных устройств -->
    <nav class="bottom-nav">
      <el-row type="flex" justify="space-around" align="middle">
        <button @click="router.push('/')" :class="{ active: route.path === '/' }">
          <MenuIcon class="input-icon" />
          <span>Главная</span>
        </button>
        <button @click="router.push('/Logic')" :class="{ active: route.path === '/Logic' }">
          <SwitchFilled class="input-icon" />
          <span>Логика</span>
        </button>
        <button @click="router.push('/history')" :class="{ active: route.path === '/history' }">
          <DocumentIcon class="input-icon" />
          <span>История</span>
        </button>
        <button @click="router.push('/profile')" :class="{ active: route.path === '/profile' }">
          <UserIcon class="input-icon" />
          <span>Профиль</span>
        </button>
        <button @click="router.push('/mood-diary')" :class="{ active: route.path === '/mood-diary' }">
          <MagicStick class="input-icon" />
          <span>Дневник</span>
        </button>
      </el-row>
    </nav>
  </div>
</template>

<style scoped>
/* Стили для бокового меню */
.sidebar {
  background-color: #2d3a4b;
  color: #fff;
  min-height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  width: 200px;
}

svg {
  width: 24px;
  height: 24px;
}

.el-menu {
  border-right: none;
  background-color: transparent;
}

.el-menu-item {
  margin-bottom: 10px;
}

.el-menu-item.is-active {
  background-color: #1d2733 !important;
}

.el-menu-item .el-icon {
  color: #fff;
}

.el-menu-item:hover {
  background-color: #1d2733;
}

.el-menu-item span {
  margin-left: 8px;
}

.input-icon {
  font-size: 24px;
}

.logout-section {
  padding: 10px;
  margin-left: 8px;
}

.logout-section .el-button {
  color: #fff;
}

/* Стили для нижнего меню */
.bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  padding: 10px 0;
  width: 100%;
  background-color: #2d3a4b;
  color: #fff;
  border-top: 1px solid #1d2733;
  z-index: 1000;
}

.bottom-nav .el-row {
  margin: 0;
}

.bottom-nav .el-col {
  text-align: center;
  padding: 10px 0;
  color: #bfcbd9;
  cursor: pointer;
}

.bottom-nav .input-icon {
  font-size: 24px;
}

.bottom-nav .el-col span {
  display: block;
  font-size: 12px;
  margin-top: 4px;
}

.bottom-nav .active {
  color: #409EFF;
}

.bottom-nav .active .input-icon {
  color: #409EFF;
}


button {
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Адаптивные стили */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  .bottom-nav {
    display: block;
  }
}
</style>
