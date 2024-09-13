<!-- components/Sidebar.vue -->
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  Menu as MenuIcon,
  Document as DocumentIcon,
  Fold,
  Expand,
  User as UserIcon, SwitchButton,

} from '@element-plus/icons-vue';
import { authService } from '@/services/authService';


const router = useRouter();
const route = useRoute();

const isCollapsed = ref(false);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

const currentUser = computed(() => authService.currentUser.value);

const handleLogout = () => {
  authService.logout();
  router.push('/login');
};
</script>

<template>
  <el-aside :width="isCollapsed ? '64px' : '200px'" class="sidebar">
    <div class="toggle-button" @click="toggleCollapse">
      <el-icon>
        <component :is="isCollapsed ? Expand : Fold" />
      </el-icon>
    </div>
    <el-menu
        :default-active="route.path"
        :collapse="isCollapsed"
        router
        background-color="#2d3a4b"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
    >
      <el-menu-item index="/">
        <template #title>
          <MenuIcon class="input-icon" />
          <span>Главная</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/history">
        <template #title>
          <DocumentIcon class="input-icon" />
          <span>История</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/profile">
        <template #title>
          <UserIcon class="input-icon" />
          <span>Профиль</span>
        </template>
      </el-menu-item>
    </el-menu>
    <div v-if="currentUser" class="logout-section">
      <el-button type="text" @click="handleLogout">
        <SwitchButton class="input-icon" /> <span>Выйти</span>
      </el-button>
    </div>
  </el-aside>
</template>

<style scoped>
.sidebar {
  background-color: #2d3a4b;
  color: #fff;
  min-height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  transition: width 0.3s;
}

.toggle-button {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  cursor: pointer;
  color: #fff;
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
  font-size: 20px;
}

.logout-section {
  padding: 10px;
  margin-left: 8px;
}

span {
  margin-left: 10px;
}

.logout-section .el-button {
  color: #fff;
}
</style>
