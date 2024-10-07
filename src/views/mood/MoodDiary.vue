<template>
	<div class="mood-diary">
		<h2>Мой Дневник Настроения 📖</h2>
		<MoodForm @submit="saveMoodEntry" />
		<MoodTabs
			:entries="moodEntries"
			:analysis="moodAnalysis"
			:entriesPerPage="5"
		/>
	</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue';
	import axios from 'axios';
	import { ElMessage } from 'element-plus';
	import { useRouter } from 'vue-router';
	import MoodForm from './form/MoodForm.vue';
	import MoodTabs from './tabs/MoodTabs.vue';
	import { authService } from '@/services/authService';
	import { useUserActivitiesStore } from '@/stores/userActivities';

	const router = useRouter();
	const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

	// Проверка авторизации пользователя
	const currentUser = authService.getCurrentUser();
	if (!currentUser) {
		router.push('/login');
	}

	const moodEntries = ref([]);
	const moodAnalysis = ref('');

	const userActivitiesStore = useUserActivitiesStore();

	const saveMoodEntry = async ({ rating, comment }) => {
		if (!currentUser) return;
		if (rating === 0) {
			ElMessage.warning('Пожалуйста, оцените ваше настроение.');
			return;
		}
		try {
			const entry = {
				id: Date.now(),
				user_id: currentUser.username,
				date: new Date().toLocaleDateString(),
				rating: rating,
				comment: comment || 'Без комментария',
			};
			await axios.post(`${API_BASE_URL}/save_mood_entry`, entry);
			moodEntries.value.push(entry);
			ElMessage.success('Запись настроения сохранена.');

			// Добавляем запись активности в календарь
			const date = new Date();
			const activityComment = entry.comment ? entry.comment : 'Без комментария';
			const activity = `Запись в дневник настроений: "${activityComment}"`;
			userActivitiesStore.addActivity(date, activity);

			await loadMoodAnalysis();
			// Обновление графика происходит автоматически через реактивность
		} catch (error) {
			console.error('Ошибка при сохранении записи настроения:', error);
			ElMessage.error('Не удалось сохранить запись настроения.');
		}
	};

	const loadMoodEntries = async () => {
		if (!currentUser) return;
		try {
			const { data } = await axios.get(`${API_BASE_URL}/get_mood_entries`, {
				params: { user_id: currentUser.username },
			});
			moodEntries.value = data.entries;
		} catch (error) {
			console.error('Ошибка при загрузке записей настроения:', error);
		}
	};

	const loadMoodAnalysis = async () => {
		if (!currentUser) return;
		try {
			const { data } = await axios.get(`${API_BASE_URL}/get_mood_analysis`, {
				params: { user_id: currentUser.username },
			});
			moodAnalysis.value = data.analysis;
		} catch (error) {
			console.error('Ошибка при получении анализа настроений:', error);
		}
	};

	onMounted(() => {
		loadMoodEntries();
		loadMoodAnalysis();
	});
</script>

<style scoped>
	.mood-diary {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem 1rem;
		background-size: cover;
		background-position: center;
		background-attachment: fixed;
		background-color: #f9fafc;
	}

	h2 {
		text-align: center;
		margin-bottom: 2rem;
		color: #333;
		font-size: 2.5rem;
	}
</style>
