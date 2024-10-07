<template>
	<div class="logic-page">
		<h1>{{ test.title }}</h1>
		<p>{{ test.description }}</p>

		<div v-if="!isTestCompleted">
			<!-- Используем компонент VesselAnimation -->
			<ProgressVessel :percentage="progressPercentage" />

			<p class="question-number">
				Вопрос {{ currentQuestionIndex + 1 }} из {{ totalQuestions }}
			</p>

			<transition name="fade" mode="out-in">
				<el-card :key="currentQuestionIndex" class="question-card">
					<p class="question">{{ currentQuestion.question }}</p>
					<el-radio-group v-model="userAnswer" class="options">
						<el-radio
							v-for="option in currentQuestion.options"
							:key="option"
							:label="option"
							class="option-radio"
						>
							{{ option }}
						</el-radio>
					</el-radio-group>
				</el-card>
			</transition>

			<div class="navigation-buttons">
				<el-button
					type="primary"
					@click="nextQuestion"
					:disabled="!userAnswer"
					:loading="isSubmitting"
				>
					{{ isLastQuestion ? 'Завершить тест' : 'Следующий вопрос' }}
				</el-button>
			</div>
		</div>

		<div v-else class="results">
			<h2>Результаты Теста</h2>
			<p>
				Вы ответили правильно на
				<strong>{{ correctAnswers }}</strong>
				из
				<strong>{{ totalQuestions }}</strong>
				вопросов.
			</p>
			<div class="nickname-section">
				<img
					:src="nickname.image"
					:alt="nickname.title"
					class="nickname-image"
				/>
				<p class="nickname-title">{{ nickname.title }}</p>
			</div>

			<!-- Аккордеон с неправильными ответами -->
			<el-collapse v-if="incorrectAnswers.length" class="incorrect-answers">
				<el-collapse-item
					v-for="(answer, index) in incorrectAnswers"
					:key="index"
					:title="`Вопрос ${index + 1}`"
				>
					<p class="incorrect-question">
						<strong>Вопрос:</strong> {{ answer.question }}
					</p>
					<p><strong>Ваш ответ:</strong> {{ answer.selected }}</p>
					<p><strong>Правильный ответ:</strong> {{ answer.correct }}</p>
				</el-collapse-item>
			</el-collapse>

			<el-button type="success" @click="retakeTest">Пройти снова</el-button>
			<el-button @click="goBack">Вернуться к тестам</el-button>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref, computed } from 'vue';
	import { useRouter } from 'vue-router';
	import { logicTest } from '@/state/tests/logicTest';

	// Импортируем компонент прогресса
	import ProgressVessel from '@/components/common/ProgressVessel.vue';

	// Импортируем стор пользовательских активностей
	import { useUserActivitiesStore } from '@/stores/userActivities';

	const router = useRouter();

	const test = ref(logicTest);
	const currentQuestionIndex = ref(0);
	const userAnswer = ref(null);
	const answers = ref([]);
	const isSubmitting = ref(false);

	// Инициализируем стор активностей
	const userActivitiesStore = useUserActivitiesStore();

	const currentQuestion = computed(() => {
		return test.value.questions[currentQuestionIndex.value];
	});

	const isLastQuestion = computed(() => {
		return currentQuestionIndex.value === test.value.questions.length - 1;
	});

	const isTestCompleted = computed(() => {
		return currentQuestionIndex.value >= test.value.questions.length;
	});

	const totalQuestions = computed(() => {
		return test.value.questions.length;
	});

	const correctAnswers = computed(() => {
		return answers.value.filter((a) => a.selected === a.correct).length;
	});

	const incorrectAnswers = computed(() => {
		return answers.value.filter((a) => a.selected !== a.correct);
	});

	const progressPercentage = computed(() => {
		return Math.round(
			(currentQuestionIndex.value / totalQuestions.value) * 100
		);
	});

	const nickname = computed(() => {
		const score = correctAnswers.value;
		if (score >= 14) {
			return {
				title: 'Эксперт Логики',
				image: new URL('@/assets/icons/expert.svg', import.meta.url).href,
			};
		} else if (score >= 10) {
			return {
				title: 'Профи Логики',
				image: new URL('@/assets/icons/profi.svg', import.meta.url).href,
			};
		} else if (score >= 6) {
			return {
				title: 'Ученик Логики',
				image: new URL('@/assets/icons/scholar.svg', import.meta.url).href,
			};
		} else {
			return {
				title: 'Начинающий Логик',
				image: new URL('@/assets/icons/junior.svg', import.meta.url).href,
			};
		}
	});

	const nextQuestion = async () => {
		if (!userAnswer.value) return;

		isSubmitting.value = true;

		await new Promise((resolve) => setTimeout(resolve, 300));

		answers.value.push({
			question: currentQuestion.value.question,
			selected: userAnswer.value,
			correct: currentQuestion.value.answer,
		});

		userAnswer.value = null;
		currentQuestionIndex.value++;

		isSubmitting.value = false;

		// Проверяем, завершен ли тест
		if (isTestCompleted.value) {
			// Добавляем активность в календарь
			const date = new Date();
			const activity = `"${test.value.title}" пройден. Правильных ответов: ${correctAnswers.value} из ${totalQuestions.value}`;
			userActivitiesStore.addActivity(date, activity);
		}
	};

	const retakeTest = () => {
		currentQuestionIndex.value = 0;
		userAnswer.value = null;
		answers.value = [];
	};

	const goBack = () => {
		router.push('/Logic');
	};
</script>

<style scoped>
	@import 'logic.css';
</style>
