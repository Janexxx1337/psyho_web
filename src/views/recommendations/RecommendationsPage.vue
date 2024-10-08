<template>
	<el-container class="recommendations-container">
		<el-main class="main">
			<el-card class="recommendations-card" shadow="always">
				<!-- Информация о пациенте -->
				<div v-if="recommendationsData" class="patient-info">
					<h2>Информация о пациенте</h2>
					<div class="patient-details">
						<p>
							<User class="input-icon" aria-label="Имя" />
							<strong>Имя:</strong> {{ patientName }}
						</p>
						<p>
							<Calendar class="input-icon" aria-label="Возраст" />
							<strong>Возраст:</strong> {{ patientAge }} лет
						</p>
						<p>
							<Calendar class="input-icon" aria-label="Дата" />
							<strong>Дата:</strong> {{ currentDate }}
						</p>
					</div>
				</div>
				<div v-else>
					<el-alert
						title="Нет данных для отображения"
						type="warning"
						show-icon
					></el-alert>
				</div>

				<!-- История общения -->
				<div v-if="recommendationsData" class="conversation-section">
					<h3>История общения</h3>
					<div class="conversation-history" ref="chatContainer">
						<transition-group name="message-fade" tag="div">
							<div
								v-for="(message, index) in conversationHistory"
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
									<div class="message-meta">
										<el-icon
											@click="voiceMessage(message)"
											class="voice-icon"
											:aria-label="'Озвучить сообщение'"
										>
											<Microphone />
										</el-icon>
										<span class="timestamp">{{ message.timestamp }}</span>
									</div>
								</div>
							</div>
						</transition-group>
					</div>
				</div>

				<!-- Поле ввода вопроса -->
				<div v-if="recommendationsData" class="input-section">
					<el-input
						v-model="additionalQuestion"
						:placeholder="
							loading ? 'Пожалуйста, подождите...' : 'Введите ваш вопрос...'
						"
						class="question-input"
						@keyup.enter="sendAdditionalQuestion"
						clearable
						:disabled="loading"
					>
						<template #append>
							<el-button
								class="send-button"
								type="primary"
								icon="Position"
								@click="sendAdditionalQuestion"
								:loading="loading"
								:disabled="loading || !additionalQuestion.trim()"
								aria-label="Отправить"
							></el-button>
						</template>
					</el-input>
				</div>

				<!-- Действия -->
				<div v-if="recommendationsData" class="actions">
					<el-button @click="toggleMute">
						<span class="material-symbols-outlined">
							{{ isMuted ? 'volume_mute' : 'brand_awareness' }}
						</span>
						{{ isMuted ? 'Включить звук' : 'Отключить звук' }}
					</el-button>
					<el-button @click="printRecommendation">
						<span class="material-symbols-outlined">print</span> Печать
					</el-button>
					<el-button @click="saveRecommendation">
						<span class="material-symbols-outlined">download</span> Сохранить
					</el-button>
					<el-button @click="goToHomePage">
						<span class="material-symbols-outlined">arrow_back</span> Вернуться
						на главную
					</el-button>
				</div>
			</el-card>
		</el-main>
	</el-container>
</template>

<script setup lang="ts">
	import { ref, computed, onMounted, nextTick, onBeforeUnmount } from 'vue';
	import { useRouter } from 'vue-router';
	import axios from 'axios';
	import { ElMessage, ElAlert } from 'element-plus';
	import { useFormStore } from '@/stores/formStore';
	const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
	// Импорт иконок из Element Plus
	import {
		User,
		Calendar,
		ChatLineRound,
		Microphone,
	} from '@element-plus/icons-vue';

	interface Message {
		role: 'user' | 'assistant';
		content: string;
		timestamp: string;
	}

	const router = useRouter();
	const formStore = useFormStore();
	const recommendationsData = computed(() =>
		formStore.getRecommendationsData()
	);
	const patientName = computed(
		() => recommendationsData.value?.name || 'Имя не указано'
	);
	const patientAge = computed(
		() => recommendationsData.value?.age || 'Возраст не указан'
	);
	const currentDate = computed(() => new Date().toLocaleDateString());
	const additionalQuestion = ref('');
	const loading = ref(false);
	const conversationHistory = ref<Message[]>([]);
	const chatContainer = ref<HTMLElement | null>(null);
	const isMuted = ref(false);

	const formatTimestamp = (date: Date) =>
		date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

	onMounted(() => {
		if (recommendationsData.value) {
			conversationHistory.value.push({
				role: 'assistant',
				content: formattedRecommendations.value,
				timestamp: formatTimestamp(new Date()),
			});
			scrollToBottom();
		} else {
			ElMessage.warning(
				'Нет данных для отображения. Пожалуйста, заполните форму.'
			);
			router.push({ name: 'FormPage' });
		}
	});

	onBeforeUnmount(() => {
		if (speechSynthesis.speaking) {
			speechSynthesis.cancel();
		}
	});

	const formattedRecommendations = computed(() => {
		if (!recommendationsData.value?.recommendations) return 'Нет рекомендаций';
		const lines = recommendationsData.value.recommendations
			.split(/\n/)
			.filter((line) => line.trim() !== '');
		return `<ul>${lines.map((line) => `<li>${line.trim()}</li>`).join('')}</ul>`;
	});

	const scrollToBottom = () => {
		nextTick(() => {
			if (chatContainer.value) {
				chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
			}
		});
	};

	const printRecommendation = () => window.print();
	const goToHomePage = () => router.push({ name: 'FormPage' });

	const sendAdditionalQuestion = async () => {
		if (!additionalQuestion.value.trim()) return;
		loading.value = true;
		try {
			conversationHistory.value.push({
				role: 'user',
				content: additionalQuestion.value,
				timestamp: formatTimestamp(new Date()),
			});
			const formData = new FormData();
			formData.append('question', additionalQuestion.value);
			formData.append(
				'session_id',
				recommendationsData.value?.session_id || ''
			);
			formData.append('name', recommendationsData.value?.name || '');
			formData.append('age', String(recommendationsData.value?.age || ''));
			formData.append(
				'condition',
				String(recommendationsData.value?.condition || '')
			);
			formData.append(
				'description',
				recommendationsData.value?.description || ''
			);

			const { data } = await axios.post(
				`${API_BASE_URL}/get_recommendations`,
				formData,
				{
					headers: { 'Content-Type': 'multipart/form-data' },
				}
			);

			conversationHistory.value.push({
				role: 'assistant',
				content: data.recommendations,
				timestamp: formatTimestamp(new Date()),
			});

			additionalQuestion.value = '';
			scrollToBottom();
		} catch (error) {
			ElMessage.error(
				'Не удалось отправить ваш вопрос. Пожалуйста, попробуйте позже.'
			);
		} finally {
			loading.value = false;
		}
	};

	const saveRecommendation = async () => {
		try {
			if (!recommendationsData.value)
				throw new Error('Нет данных для сохранения.');

			const data = {
				session_id: recommendationsData.value.session_id,
				name: recommendationsData.value.name,
				age: recommendationsData.value.age,
				condition: recommendationsData.value.condition,
				description: recommendationsData.value.description,
				date: currentDate.value,
			};

			console.log('Отправляем данные для сохранения сессии:', data);

			const response = await axios.post(`${API_BASE_URL}/save_session`, data, {
				headers: {
					'Content-Type': 'application/json',
				},
			});

			console.log('Ответ от сервера:', response);

			if (response.status === 200) {
				ElMessage.success('Сессия успешно сохранена.');
			} else {
				throw new Error(
					'Не удалось сохранить сессию. Неправильный ответ от сервера.'
				);
			}
		} catch (error) {
			console.error('Ошибка при сохранении сессии:', error);
			ElMessage.error(`Не удалось сохранить сессию. Ошибка: ${error.message}`);
		}
	};

	const voiceMessage = (message: Message) => {
		if (isMuted.value) return;
		if (speechSynthesis.speaking) speechSynthesis.cancel();
		const utterance = new SpeechSynthesisUtterance(message.content);
		utterance.lang = 'ru-RU';
		const voices = speechSynthesis.getVoices();
		const selectedVoice = voices.find(
			(voice) => voice.lang === 'ru-RU' && voice.name.includes('Premium')
		);
		if (selectedVoice) utterance.voice = selectedVoice;
		speechSynthesis.speak(utterance);
	};

	const toggleMute = () => {
		isMuted.value = !isMuted.value;
		if (isMuted.value && speechSynthesis.speaking) speechSynthesis.cancel();
	};
</script>

<style scoped>
	@import 'recomendations.css';
</style>
