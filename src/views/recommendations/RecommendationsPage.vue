<template>
  <el-container class="recommendations-container">
    <el-main class="main">
      <el-card class="recommendations-card" shadow="always">
        <!-- Информация о пациенте -->
        <div class="patient-info">
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

        <!-- История общения -->
        <div class="conversation-section">
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
                    <el-icon @click="voiceMessage(message)" class="voice-icon" :aria-label="'Озвучить сообщение'">
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
        <div class="input-section">
          <el-input
              v-model="additionalQuestion"
              :placeholder="loading ? 'Пожалуйста, подождите...' : 'Введите ваш вопрос...'"
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
        <div class="actions">
          <el-button @click="printRecommendation">
            <Printer class="input-icon" aria-label="Печать" /> Печать
          </el-button>
          <el-button @click="saveRecommendation">
            <Download class="input-icon" aria-label="Сохранить" /> Сохранить
          </el-button>
          <el-button @click="goToHomePage">
            <Back class="input-icon" aria-label="Вернуться на главную" /> Вернуться на главную
          </el-button>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// Импорт иконок из Element Plus
import {
  User,
  Calendar,
  Position,
  Printer,
  Back,
  ChatLineRound,
  Download,
  Microphone,
} from '@element-plus/icons-vue';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const route = useRoute();
const router = useRouter();

const recommendations = ref(route.params.recommendations || '');
const patientName = computed(() => route.params.name || 'Имя не указано');
const patientAge = computed(() => route.params.age || 'Возраст не указан');
const currentDate = computed(() => new Date().toLocaleDateString());
const additionalQuestion = ref('');
const loading = ref(false);
const sessionId = ref(route.params.session_id);

const conversationHistory = ref<Message[]>([]);

// Ссылка на контейнер чата для автопрокрутки
const chatContainer = ref<HTMLElement | null>(null);

// Функция форматирования времени
const formatTimestamp = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

onMounted(() => {
  // Инициализируем историю общения с начальными рекомендациями
  conversationHistory.value.push({
    role: 'assistant',
    content: formattedRecommendations.value,
    timestamp: formatTimestamp(new Date()),
  });
  scrollToBottom();
});

const formattedRecommendations = computed(() => {
  if (!recommendations.value) return 'Нет рекомендаций';

  const lines = recommendations.value
      .split(/\n/)
      .filter((line) => line.trim() !== '');

  return `
    <ul>
      ${lines.map((line) => `<li>${line.trim()}</li>`).join('')}
    </ul>
  `;
});

// Функция автопрокрутки чата вниз
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

const printRecommendation = () => {
  window.print();
};

const goToHomePage = () => {
  router.push({ name: 'FormPage' });
};

const sendAdditionalQuestion = async () => {
  if (!additionalQuestion.value.trim()) return;
  loading.value = true;

  try {
    const userMessage: Message = {
      role: 'user',
      content: additionalQuestion.value,
      timestamp: formatTimestamp(new Date()),
    };
    conversationHistory.value.push(userMessage);

    const formData = new FormData();
    formData.append('question', additionalQuestion.value);
    formData.append('session_id', sessionId.value);
    formData.append('name', route.params.name as string);
    formData.append('age', String(route.params.age));
    formData.append('condition', route.params.condition as string);
    formData.append('description', route.params.description as string);

    const { data } = await axios.post(
        `${API_BASE_URL}/get_recommendations`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
    );

    const assistantMessage: Message = {
      role: 'assistant',
      content: data.recommendations,
      timestamp: formatTimestamp(new Date()),
    };
    conversationHistory.value.push(assistantMessage);

    additionalQuestion.value = '';
    scrollToBottom();
  } catch (error) {
    console.error('Ошибка при отправке вопроса:', error);
    ElMessage.error('Не удалось отправить ваш вопрос. Пожалуйста, попробуйте позже.');
  } finally {
    loading.value = false;
  }
};

const saveRecommendation = async () => {
  try {
    const data = {
      session_id: sessionId.value,
      name: route.params.name,
      age: route.params.age,
      date: currentDate.value,
    };

    await axios.post(`${API_BASE_URL}/save_session`, data);

    ElMessage.success('Сессия успешно сохранена.');
  } catch (error) {
    console.error('Ошибка при сохранении сессии:', error);
    ElMessage.error('Не удалось сохранить сессию.');
  }
};

// Функция озвучивания сообщения
const voiceMessage = (message: Message) => {
  if ('speechSynthesis' in window) {
    if (speechSynthesis.speaking) {
      speechSynthesis.cancel();
    }
    const utterance = new SpeechSynthesisUtterance(message.content);
    utterance.lang = 'ru-RU'; // Устанавливаем язык на русский
    speechSynthesis.speak(utterance);
  } else {
    console.error('Text-to-speech not supported.');
    ElMessage.error('Ваш браузер не поддерживает озвучивание сообщений.');
  }
};
</script>

<style scoped>
/* Общие стили */
.recommendations-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.main {
  width: 100%;
}

.recommendations-card {
  width: 100%;
  padding: 2rem;
  border-radius: 10px;
  overflow-x: hidden;
  box-sizing: border-box;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.patient-info {
  margin-bottom: 1.5rem;
}

.patient-details p {
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #333;
}

.input-icon {
  margin-right: 10px;
  color: #409eff;
}

/* Стили истории общения */
.conversation-section {
  margin-bottom: 1.5rem;
}

.conversation-history {
  max-height: 400px;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow-x: hidden;
}

.message {
  display: flex;
  margin-bottom: 1rem;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message .avatar {
  margin: 0 10px;
}

.message .content {
  max-width: 70%;
  background-color: #ffffff;
  padding: 0.75rem 1rem;
  border-radius: 20px;
  position: relative;
  word-wrap: break-word;
  overflow-wrap: break-word;
  line-height: 1.5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message.user .content {
  background-color: #e0f7fa;
}

.message.assistant .content {
  background-color: #fff3e0;
}

.message .content p {
  margin: 0;
  word-break: break-word;
  color: #333;
}

/* Стили для метаданных сообщения */
.message-meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.message-meta .voice-icon {
  cursor: pointer;
  margin-right: 0.5rem;
  color: #409eff;
  transition: color 0.3s;
}

.message-meta .voice-icon:hover {
  color: #66b1ff;
}

.message-meta .timestamp {
  font-size: 0.75rem;
  color: #999;
}

/* Поле ввода */
.input-section {
  margin-top: 1.5rem;
}

.question-input {
  width: 100%;
}

.el-input .el-input__inner {
  border-radius: 20px;
}

/* Стиль для кнопки отправки (кнопка с иконкой) */
.send-button {
  border-radius: 50%;
  padding: 0;
  width: 40px;
  height: 40px;
}

/* Кнопки действий */
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.actions .el-button {
  flex: 1 1 calc(33.333% - 1rem);
  border-radius: 8px; /* Закругленные углы для кнопок с текстом */
}

@media (max-width: 600px) {
  .actions .el-button {
    flex: 1 1 100%;
  }

  .message .content {
    max-width: 80%;
  }
}
</style>
