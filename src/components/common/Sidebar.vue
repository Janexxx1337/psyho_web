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
		Lightning,
		Aim,
	} from '@element-plus/icons-vue';
	import { authService } from '@/services/authService';

	const router = useRouter();
	const route = useRoute();
	computed(() => authService.currentUser.value);
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
        <el-menu-item index="/Doctor">
          <MenuIcon class="input-icon" />
          <span>Доктор Актив</span>
        </el-menu-item>
				<el-menu-item index="/Logic">
					<SwitchFilled class="input-icon" />
					<span>Тест: Логика</span>
				</el-menu-item>

				<!-- Подменю "Игры" -->
				<el-sub-menu index="games">
					<template #title>
						<Lightning class="input-icon" />
						<span>Игры</span>
					</template>
					<el-menu-item index="/simon-says">
						<Aim class="menu-icon" />
						<span>Симон говорит</span>
					</el-menu-item>
					<el-menu-item index="/positive-thoughts">
						<Aim class="menu-icon" />
						<span>Позитивные мысли</span>
					</el-menu-item>
					<el-menu-item index="/idea-generator">
						<Aim class="menu-icon" />
						<span>Генератор идей</span>
					</el-menu-item>
				</el-sub-menu>

				<el-menu-item index="/history">
					<DocumentIcon class="input-icon" />
					<span>Сессии</span>
				</el-menu-item>
				<el-menu-item index="/profile" class="profile">
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
				<button
					@click="router.push('/')"
					:class="{ active: route.path === '/' }"
				>
					<MenuIcon class="input-icon" />
					<span>Главная</span>
				</button>
				<button
					@click="router.push('/Logic')"
					:class="{ active: route.path === '/Logic' }"
				>
					<SwitchFilled class="input-icon" />
					<span>Логика</span>
				</button>
				<!-- Кнопка "Игры" с выпадающим меню -->
				<el-dropdown trigger="click" placement="top-start">
					<button
						class="dropdown-button"
						:class="{
							active:
								route.path.startsWith('/simon-says') ||
								route.path.startsWith('/positive-thoughts'),
						}"
					>
						<Lightning class="input-icon" />
						<span>Игры</span>
					</button>
					<template #dropdown>
						<el-dropdown-menu>
							<el-dropdown-item @click.native="router.push('/simon-says')">
								<Aim class="menu-icon" />
								<span>Симон говорит</span>
							</el-dropdown-item>
							<el-dropdown-item
								@click.native="router.push('/positive-thoughts')"
							>
								<SmileFilled class="menu-icon" />
								<span>Позитивные мысли</span>
							</el-dropdown-item>
						</el-dropdown-menu>
					</template>
				</el-dropdown>
				<button
					@click="router.push('/history')"
					:class="{ active: route.path === '/history' }"
				>
					<DocumentIcon class="input-icon" />
					<span>Сессии</span>
				</button>
				<button
					@click="router.push('/profile')"
					:class="{ active: route.path === '/profile' }"
				>
					<UserIcon class="input-icon" />
					<span>Профиль</span>
				</button>
				<button
					@click="router.push('/mood-diary')"
					:class="{ active: route.path === '/mood-diary' }"
				>
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
		width: 300px;
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

	.el-menu-item span,
	.el-sub-menu span {
		margin-left: 8px;
	}

	.input-icon {
		font-size: 24px;
	}

	.menu-icon {
		font-size: 18px;
		margin-right: 8px;
		vertical-align: middle;
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
		color: #409eff;
	}

	.bottom-nav .active .input-icon {
		color: #409eff;
	}

	button {
		border-radius: 6px;
		background: none;
		border: none;
		color: inherit;
		padding: 0;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.dropdown-button {
		background: none;
		border: none;
		color: inherit;
		padding: 0;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.dropdown-button .input-icon {
		font-size: 24px;
	}

	.el-dropdown-menu {
		background-color: #2d3a4b;
		border-color: #1d2733;
	}

	.el-dropdown-menu__item {
		color: #bfcbd9;
		display: flex;
		align-items: center;
	}

	.el-dropdown-menu__item:hover {
		background-color: #1d2733;
		color: #409eff;
	}

	.el-dropdown-menu__item .menu-icon {
		font-size: 18px;
		margin-right: 8px;
	}

	.el-dropdown-menu__item span {
		display: inline-block;
	}

	.profile {
		position: fixed;
		right: 0;
		top: 0;
		background: #2d3a4b;
		border-bottom-left-radius: 6px;
	}

	:deep(.el-menu-item-group__title) {
		display: none;
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
