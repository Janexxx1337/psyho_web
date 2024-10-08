<template>
	<el-config-provider :locale="ruLocale">
		<el-container>
			<!-- Сайдбар отображается, если пользователь авторизован и не на мобильном устройстве -->
			<Sidebar v-if="isAuthenticated && !isMobile" />
			<el-main
				:style="{ marginLeft: isAuthenticated && !isMobile ? '200px' : '0' }"
			>
				<RouterView />
			</el-main>
		</el-container>
	</el-config-provider>
</template>

<script setup lang="ts">
	import { computed } from 'vue';
	import { RouterView } from 'vue-router';
	import Sidebar from './components/common/Sidebar.vue';
	import { authService } from './services/authService';
	import { ElConfigProvider } from 'element-plus';
	import ruLocale from 'element-plus/es/locale/lang/ru';

	const isAuthenticated = computed(() => !!authService.currentUser.value);
	const isMobile = computed(() => window.innerWidth <= 768);
</script>

<style scoped>
	* {
    font-family: "PT Serif", serif;
	}

	.el-main {
		padding: 20px;
		overflow: hidden;
	}

	.el-button {
		width: fit-content;
	}

	.main-container,
	.el-main {
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
			margin-left: 0 !important;
		}
	}
</style>
