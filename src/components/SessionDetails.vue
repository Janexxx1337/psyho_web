<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const sessionDetails = ref(null);

// Функция для загрузки деталей сессии
const fetchSessionDetails = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/get_session_details?session_id=${route.params.session_id}`);
    sessionDetails.value = response.data.session;
  } catch (error) {
    console.error('Ошибка при получении деталей сессии:', error);
  }
};

// При монтировании компонента загружаем детали сессии
onMounted(() => {
  fetchSessionDetails();
});

// Функция для фильтрации истории общения, чтобы исключить начальный промпт и ответ на него
const filteredHistory = computed(() => {
  if (!sessionDetails.value || !sessionDetails.value.history) return [];

  // Начальный промпт всегда будет первым, а его ответ вторым, поэтому начинаем с третьего сообщения
  return sessionDetails.value.history.slice(2);
});
</script>

<template>
  <div class="session-details-container">
    <h2>Детали сессии</h2>
    <el-card v-if="sessionDetails">
      <h3>Информация о пациенте</h3>
      <p><strong>Имя:</strong> {{ sessionDetails.name }}</p>
      <p><strong>Возраст:</strong> {{ sessionDetails.age }} лет</p>
      <p><strong>Дата:</strong> {{ sessionDetails.date }}</p>

      <h3>История общения</h3>
      <div v-if="filteredHistory && filteredHistory.length > 0">
        <div v-for="(message, index) in filteredHistory" :key="index" class="message">
          <p>
            <strong>{{ message.role === 'user' ? 'Вопрос' : 'Ответ' }}:</strong>
            <span v-html="message.content.replace(/(?:\r\n|\r|\n)/g, '<br>')"></span>
          </p>
        </div>
      </div>
      <div v-else>
        <p>Нет данных для отображения.</p>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.session-details-container {
  padding: 2rem;
}

h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #333;
}

.message {
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  word-wrap: break-word;
  white-space: pre-wrap;
}
</style>
