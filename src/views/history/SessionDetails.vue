<script setup lang="ts">
	import { computed, onMounted, ref } from 'vue';
	import { useRoute } from 'vue-router';
	import axios from 'axios';
	import { ChatLineRound, User } from '@element-plus/icons-vue';

	const route = useRoute();
	const sessionDetails = ref(null);

	const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

	const fetchSessionDetails = async () => {
		try {
			const response = await axios.get(
				`${API_BASE_URL}/get_session_details?session_id=${route.params.session_id}`
			);
			sessionDetails.value = response.data.session;
		} catch (error) {
			console.error('Ошибка при получении деталей сессии:', error);
		}
	};

	onMounted(() => {
		fetchSessionDetails();
	});

	const filteredHistory = computed(() => {
		if (!sessionDetails.value || !sessionDetails.value.history) return [];

		// Фильтруем историю, исключая только начальный промпт (первое сообщение от пользователя с заготовкой)
		return sessionDetails.value.history.filter((message, index) => {
			// Ищем первое сообщение от пользователя (начальный промпт)
			return !(index === 0 && message.role === 'user');
		});
	});
</script>

<template>
	<div class="session-details-container">
		<el-card v-if="sessionDetails">
			<h3>Информация о пациенте</h3>
			<p><strong>Имя:</strong> {{ sessionDetails.name }}</p>
			<p><strong>Возраст:</strong> {{ sessionDetails.age }} лет</p>
			<p><strong>Дата:</strong> {{ sessionDetails.date }}</p>

			<h3>История общения</h3>
			<div
				v-if="filteredHistory && filteredHistory.length > 0"
				class="conversation-history"
			>
				<div
					v-for="(message, index) in filteredHistory"
					:key="index"
					:class="['message', message.role]"
				>
					<div class="avatar">
						<el-avatar
							:icon="message.role === 'user' ? User : ChatLineRound"
							:size="40"
						></el-avatar>
					</div>
					<div class="content">
						<p v-html="message.content"></p>
						<span class="timestamp">{{ message.timestamp }}</span>
					</div>
				</div>
			</div>
			<div v-else>
				<p>Нет данных для отображения.</p>
			</div>
		</el-card>
	</div>
</template>

<style scoped>
	@import 'details.css';
</style>
