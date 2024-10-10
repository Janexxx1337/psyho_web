<template>
	<el-container class="app-container">
		<el-main class="main">
			<el-card class="form-card" shadow="hover">
				<h2>
					<span class="material-symbols-outlined">psychology</span>
					Психологическая поддержка
				</h2>
				<p class="form-description">
					Пожалуйста, заполните эту форму, чтобы мы могли предоставить вам
					персональные рекомендации и поддержку.
				</p>

				<!-- Шаги формы -->
				<el-steps
					:active="formStore.activeStep"
					finish-status="success"
					align-center
				>
					<el-step title="Информация"></el-step>
					<el-step title="Состояние"></el-step>
					<el-step title="Описание"></el-step>
				</el-steps>

				<!-- Форма -->
				<el-form
					:model="formStore.form"
					:rules="formStore.rules"
					ref="formRef"
					label-position="top"
					label-width="120px"
					class="step-form"
				>
					<!-- Шаг 1: Персональная информация -->
					<div v-if="formStore.activeStep === 0">
						<el-form-item label="Ваше имя" prop="name">
							<div class="input-with-icon">
								<span class="material-symbols-outlined input-icon">person</span>
								<el-input
									v-model="formStore.form.name"
									placeholder="Введите ваше имя"
								></el-input>
							</div>
						</el-form-item>

						<el-form-item label="Ваш возраст" prop="age">
							<div class="input-with-icon">
								<span class="material-symbols-outlined input-icon"
									>calendar_today</span
								>
								<el-input-number
									v-model="formStore.form.age"
									placeholder="Введите ваш возраст"
									:min="0"
									:max="120"
									controls-position="right"
									:step="1"
									class="age-input-number"
								></el-input-number>
							</div>
						</el-form-item>
					</div>

					<!-- Шаг 2: Состояние -->
					<div v-if="formStore.activeStep === 1">
						<el-form-item
							label="Оцените своё состояние по шкале от 1 до 10"
							prop="conditionRating"
						>
							<div class="rating-with-icon">
								<span class="material-symbols-outlined rating-icon">mood</span>
								<el-rate
									v-model="formStore.form.conditionRating"
									:max="10"
									show-score
								></el-rate>
							</div>
						</el-form-item>

						<el-form-item
							label="Выберите симптомы, которые вы испытываете"
							prop="symptoms"
						>
							<div class="checkbox-group-with-icon">
								<span class="material-symbols-outlined checkbox-icon"
									>health_and_safety</span
								>
								<el-checkbox-group v-model="formStore.form.symptoms">
									<el-checkbox label="Бессонница"></el-checkbox>
									<el-checkbox label="Потеря аппетита"></el-checkbox>
									<el-checkbox label="Раздражительность"></el-checkbox>
									<el-checkbox label="Тревожность"></el-checkbox>
									<el-checkbox label="Панические атаки"></el-checkbox>
									<!-- Добавьте другие варианты -->
								</el-checkbox-group>
							</div>
						</el-form-item>
					</div>

					<!-- Шаг 3: Описание -->
					<div v-if="formStore.activeStep === 2">
						<el-form-item
							label="Опишите подробнее ваше состояние"
							prop="description"
						>
							<div class="textarea-with-icon">
								<span class="material-symbols-outlined textarea-icon"
									>description</span
								>
								<el-input
									v-model="formStore.form.description"
									type="textarea"
									:rows="4"
									placeholder="Опишите ваше состояние подробнее..."
								></el-input>
							</div>
						</el-form-item>
					</div>

					<!-- Кнопки управления -->
					<div class="form-actions">
						<el-button v-if="formStore.activeStep > 0" @click="prevStep">
							<span class="material-symbols-outlined">arrow_back</span> Назад
						</el-button>
						<el-button
							v-if="formStore.activeStep < 2"
							type="primary"
							@click="handleNextStep"
						>
							Далее <span class="material-symbols-outlined">arrow_forward</span>
						</el-button>
						<el-button
							v-if="formStore.activeStep === 2"
							type="success"
							@click="handleFormSubmit"
							:loading="formStore.isLoading"
						>
							<span class="material-symbols-outlined">send</span> Отправить
						</el-button>
					</div>
				</el-form>
			</el-card>
		</el-main>
	</el-container>
</template>

<script setup lang="ts">
	import { ref } from 'vue';
	import { useFormStore } from '@/stores/formStore';
	import { useUserActivitiesStore } from '@/stores/userActivities';
	import { useRouter } from 'vue-router';
	// Инициализация хранилища формы
	const router = useRouter();
	const formStore = useFormStore();
	const userActivitiesStore = useUserActivitiesStore();
	const formRef = ref<InstanceType<typeof import('element-plus').Form>>();

	// Обработчики шагов
	const handleNextStep = () => {
		formRef.value.validate((valid: boolean) => {
			if (valid) {
				formStore.nextStep();
			} else {
				console.log('Форма содержит ошибки.');
			}
		});
	};

	const prevStep = () => {
		formStore.prevStep();
	};

	const handleFormSubmit = () => {
		formRef.value.validate(async (valid: boolean) => {
			if (valid) {
				await formStore.handleSubmit();
				router.push({ name: 'RecommendationsPage' });
			} else {
				console.log('Форма содержит ошибки.');
			}
		});
	};
</script>

<style scoped>
	@import 'formpage.css';
</style>
