<!-- components/Register.vue -->
<template>
	<div class="auth-page">
		<el-card class="auth-container">
			<h2>Регистрация</h2>
			<el-form
				ref="registerForm"
				:model="registerData"
				:rules="rules"
				@submit.prevent="handleRegister"
				label-position="top"
			>
				<el-form-item prop="username">
					<el-input
						v-model="registerData.username"
						placeholder="Имя пользователя"
						clearable
						prefix-icon="user"
					/>
				</el-form-item>
				<el-form-item prop="password">
					<el-input
						v-model="registerData.password"
						type="password"
						placeholder="Пароль"
						clearable
						prefix-icon="lock"
					/>
				</el-form-item>
				<el-form-item prop="confirmPassword">
					<el-input
						v-model="registerData.confirmPassword"
						type="password"
						placeholder="Подтвердите пароль"
						clearable
						prefix-icon="lock"
					/>
				</el-form-item>
				<el-form-item>
					<el-button
						type="primary"
						:loading="loading"
						native-type="submit"
						round
						block
					>
						Зарегистрироваться
					</el-button>
				</el-form-item>
			</el-form>
			<p class="switch-auth">
				Уже есть аккаунт?
				<el-link type="primary" @click="goToLogin">Вход</el-link>
			</p>
		</el-card>
	</div>
</template>

<script setup lang="ts">
	import { ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { authService } from '@/services/authService';
	import { ElMessage } from 'element-plus';

	const router = useRouter();
	const registerData = ref({
		username: '',
		password: '',
		confirmPassword: '',
	});
	const loading = ref(false);

	const rules = {
		username: [
			{
				required: true,
				message: 'Пожалуйста, введите имя пользователя',
				trigger: 'blur',
			},
		],
		password: [
			{
				required: true,
				message: 'Пожалуйста, введите пароль',
				trigger: 'blur',
			},
		],
		confirmPassword: [
			{
				required: true,
				message: 'Пожалуйста, подтвердите пароль',
				trigger: 'blur',
			},
			{ validator: validateConfirmPassword, trigger: 'blur' },
		],
	};

	const registerForm = ref(null);

	function validateConfirmPassword(
		rule: any,
		value: string,
		callback: Function
	) {
		if (value !== registerData.value.password) {
			callback(new Error('Пароли не совпадают'));
		} else {
			callback();
		}
	}

	const handleRegister = async () => {
		await registerForm.value.validate(async (valid: boolean) => {
			if (valid) {
				loading.value = true;
				try {
					await authService.register(
						registerData.value.username,
						registerData.value.password
					);
					ElMessage.success('Успешная регистрация');
					await router.push('/login');
				} catch (error) {
					ElMessage.error(error);
				} finally {
					loading.value = false;
				}
			}
		});
	};

	const goToLogin = () => {
		router.push('/login');
	};
</script>

<style scoped>
	.auth-page {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
	}

	.auth-container {
		width: 400px;
		padding: 30px;
		background-color: #fff;
		border-radius: 8px;
	}

	.auth-container h2 {
		text-align: center;
		margin-bottom: 20px;
	}

	.switch-auth {
		text-align: center;
		margin-top: 20px;
	}

	.el-form-item {
		margin-bottom: 20px;
	}

	.el-input {
		width: 100%;
	}
</style>
