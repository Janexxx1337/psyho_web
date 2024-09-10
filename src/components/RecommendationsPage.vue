<template>
  <el-container class="recommendations-container">
    <!-- Основное содержимое -->
    <el-main class="main">
      <el-card class="recommendations-card" shadow="always">
        <!-- Информация о пациенте -->
        <div class="patient-info">
          <h2>Информация о пациенте</h2>
          <div class="patient-details">
            <p>
              <User class="input-icon" />
              <strong>Имя:</strong> {{ patientName }}
            </p>
            <p>
              <Calendar class="input-icon" />
              <strong>Возраст:</strong> {{ patientAge }} лет
            </p>
            <p>
              <Calendar class="input-icon" />
              <strong>Дата:</strong> {{ currentDate }}
            </p>
          </div>
        </div>

        <!-- Рекомендации -->
        <div class="recommendations-section">
          <h3>Рекомендации врача</h3>
          <div v-if="loading" class="loading-container">
            <el-loading></el-loading>
          </div>
          <div v-else v-html="formattedRecommendations"></div>
        </div>

        <!-- Уточняющий вопрос -->
        <el-input
            v-model="additionalQuestion"
            placeholder="Введите ваш уточняющий вопрос"
            class="question-input"
        />

        <!-- Действия -->
        <div class="actions">
          <el-button type="primary" @click="printRecommendation">
            <Document class="input-icon" /> Печать
          </el-button>
          <el-button type="success" @click="saveRecommendation">
            <Download class="input-icon" /> Сохранить
          </el-button>
          <el-button type="warning" @click="sendAdditionalQuestion" :loading="loading">
            <Download class="input-icon" /> Задать вопрос
          </el-button>
          <el-button type="danger" @click="goToHomePage">
            <Download class="input-icon" /> Вернуться на главную
          </el-button>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

// Импортируем нужные иконки из Element Plus
import { User, Calendar, Document, Download } from '@element-plus/icons-vue';

const route = useRoute();
const router = useRouter();

const recommendations = ref(route.params.recommendations || '');
const patientName = computed(() => route.params.name || 'Имя не указано');
const patientAge = computed(() => route.params.age || 'Возраст не указан');
const currentDate = computed(() => new Date().toLocaleDateString());
const additionalQuestion = ref('');
const loading = ref(false); // Состояние загрузки

// Получаем session_id из параметров маршрута
const sessionId = ref(route.params.session_id);

const formattedRecommendations = computed(() => {
  if (!recommendations.value) return 'Нет рекомендаций';

  const lines = recommendations.value.split(/(?=\d\.)/).map((line) => {
    const [number, ...rest] = line.trim().split(' ');
    const firstThreeWords = rest.splice(0, 3).join(' ');
    const remainingText = rest.join(' ').replace(/\. /g, '.<br>');

    return `<p style="margin-top: 1rem;"><strong>${number} ${firstThreeWords}</strong> ${remainingText}</p>`;
  });

  return lines.join('');
});

const printRecommendation = () => {
  window.print();
};

const goToHomePage = () => {
  router.push({ name: 'FormPage' });
};

// Функция для отправки уточняющего вопроса на сервер
const sendAdditionalQuestion = async () => {
  if (!additionalQuestion.value.trim()) return;
  loading.value = true; // Устанавливаем состояние загрузки в true

  try {
    const formData = new FormData();
    formData.append('name', route.params.name as string);
    formData.append('age', String(route.params.age));
    formData.append('condition', route.params.condition as string);
    formData.append('description', route.params.description as string);
    formData.append('question', additionalQuestion.value);
    formData.append('session_id', sessionId.value);

    const { data } = await axios.post('http://localhost:8000/get_recommendations', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    recommendations.value = data.recommendations; // Обновляем рекомендации
    additionalQuestion.value = ''; // Очищаем поле вопроса
  } catch (error) {
    console.error('Ошибка при отправке уточняющего вопроса:', error);
  } finally {
    loading.value = false; // Сбрасываем состояние загрузки после получения ответа или ошибки
  }
};

// Функция для сохранения рекомендации
const saveRecommendation = async () => {
  try {
    const data = {
      session_id: sessionId.value,
      recommendations: recommendations.value,
      name: route.params.name,
      age: route.params.age,
      date: currentDate.value
    };

    const response = await axios.post('http://localhost:8000/save_session', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Сессия успешно сохранена:', response.data);
  } catch (error) {
    console.error('Ошибка при сохранении сессии:', error);
  }
};
</script>

<style scoped>
.recommendations-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #ffffff;
}

.main {
  display: flex;
  justify-content: center;
  width: 100%;
}

.recommendations-card {
  width: 100%;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.patient-info {
  margin-bottom: 1rem;
}

.patient-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #333;
  display: flex;
  align-items: center;
}

.recommendations-section h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.recommendations-section p {
  line-height: 1.6;
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 1rem;
}

.question-input {
  margin: 1rem 0;
  width: 100%;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.el-button {
  border-radius: 4px;
  padding: 0.5rem 1rem;
}
</style>
