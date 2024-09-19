<template>
  <div class="mood-diary">
    <h2>Мой Дневник Настроения 📖</h2>
    <!-- Карточка для формы ввода -->
    <el-card class="entry-card">
      <div class="form-header">
        <h3>Как вы себя чувствуете сегодня?</h3>
        <MoodIcon :rating="moodRating" class="mood-icon-large" />
      </div>
      <el-form @submit.prevent="saveMoodEntry" class="mood-form">
        <el-form-item class="slider-form" label="Оцените ваше настроение">
          <el-slider
              v-model="moodRating"
              :min="1"
              :max="10"
              show-tooltip
              :marks="sliderMarks"
          ></el-slider>
        </el-form-item>
        <el-form-item label="Комментарий">
          <el-input
              class="comment-text"
              type="textarea"
              v-model="moodComment"
              placeholder="Опишите ваше настроение"
              :rows="3"
          ></el-input>
        </el-form-item>
        <el-button
            type="primary"
            native-type="submit"
            icon="el-icon-edit"
            class="submit-button"
        >
          Добавить запись
        </el-button>
      </el-form>
    </el-card>

    <!-- Вкладки для разделения контента -->
    <el-tabs v-model="activeTab" class="mood-tabs" type="card">
      <!-- Вкладка Динамика настроения -->
      <el-tab-pane label="Динамика настроения" name="dynamics">
        <div v-if="moodEntries.length" class="chart-section">
          <h3>Динамика настроения</h3>
          <!-- Фильтры для графика -->
          <div class="chart-filters">
            <el-button-group>
              <el-button @click="filterChart('week')">Неделя</el-button>
              <el-button @click="filterChart('month')">Месяц</el-button>
              <el-button @click="filterChart('all')">Все</el-button>
            </el-button-group>
          </div>
          <!-- Используем VueECharts с правильным именем и пропом -->
          <VueECharts
              ref="moodChart"
              :option="chartOption"
              autoresize
              class="mood-chart"
          />
        </div>
      </el-tab-pane>

      <!-- Вкладка История настроений -->
      <el-tab-pane label="История настроений" name="history">
        <div v-if="moodEntries.length" class="history-section">
          <h3>История настроений</h3>
          <div class="history-container">
            <el-collapse v-model="activeEntries">
              <el-collapse-item
                  v-for="(entry, index) in paginatedEntries"
                  :key="entry.id"
                  :title="entry.date"
                  :name="entry.id"
              >
                <div class="entry-content">
                  <div class="entry-header">
                    <MoodIcon :rating="entry.rating" class="mood-icon" />
                    <span class="entry-rating">{{ entry.rating }}/10</span>
                  </div>
                  <p class="entry-comment">{{ entry.comment }}</p>
                </div>
              </el-collapse-item>
            </el-collapse>
            <!-- Пагинация -->
            <el-pagination
                layout="prev, pager, next"
                :total="moodEntries.length"
                :page-size="entriesPerPage"
                @current-change="handlePageChange"
                class="pagination"
            ></el-pagination>
          </div>
        </div>
      </el-tab-pane>

      <!-- Вкладка Анализ настроений -->
      <el-tab-pane label="Анализ настроений" name="analysis">
        <div v-if="moodAnalysis" class="analysis-section">
          <h3>Анализ настроений</h3>
          <el-card shadow="hover" class="analysis-card">
            <p>{{ moodAnalysis }}</p>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { authService } from '@/services/authService';
import { useRouter } from 'vue-router';

// Импортируем компонент MoodIcon
import MoodIcon from '@/views/mood/MoodIcon.vue';

// Импортируем VueECharts и необходимые компоненты echarts
import VueECharts from 'vue-echarts';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import {
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
} from 'echarts/components';

// Регистрируем необходимые компоненты echarts
use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
]);

// **Импортируем userActivitiesStore**
import { useUserActivitiesStore } from '@/stores/userActivities';

const router = useRouter();
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;




// Проверка авторизации пользователя
const currentUser = authService.getCurrentUser();
if (!currentUser) {
  router.push('/login');
}

const moodRating = ref(5);
const moodComment = ref('');
const moodEntries = ref([]);
const moodAnalysis = ref('');

const activeEntries = ref([]);
const currentPage = ref(1);
const entriesPerPage = 5;

const paginatedEntries = computed(() => {
  const start = (currentPage.value - 1) * entriesPerPage;
  const end = start + entriesPerPage;
  return reversedMoodEntries.value.slice(start, end);
});

const reversedMoodEntries = computed(() => [...moodEntries.value].reverse());

// **Инициализируем userActivitiesStore**
const userActivitiesStore = useUserActivitiesStore();

const saveMoodEntry = async () => {
  if (!currentUser) return;
  if (moodRating.value === 0) {
    ElMessage.warning('Пожалуйста, оцените ваше настроение.');
    return;
  }
  try {
    const entry = {
      id: Date.now(),
      user_id: currentUser.username,
      date: new Date().toLocaleDateString(),
      rating: moodRating.value,
      comment: moodComment.value || 'Без комментария',
    };
    await axios.post(`${API_BASE_URL}/save_mood_entry`, entry);
    moodEntries.value.push(entry);
    moodRating.value = 5;
    moodComment.value = '';
    ElMessage.success('Запись настроения сохранена.');

    // **Добавляем запись активности в календарь**
    const date = new Date();
    const activityComment = entry.comment ? entry.comment : 'Без комментария';
    const activity = `Запись в дневник настроений: "${activityComment}"`;
    userActivitiesStore.addActivity(date, activity);

    await loadMoodAnalysis();
    updateChart();
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
    updateChart();
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

// Для графика настроения
const chartOption = ref({});

const updateChart = (filter = 'all') => {
  let filteredEntries = [...moodEntries.value];

  // Фильтрация данных для графика
  if (filter === 'week') {
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    filteredEntries = filteredEntries.filter(
        (entry) => new Date(entry.date) >= weekAgo
    );
  } else if (filter === 'month') {
    const monthAgo = new Date();
    monthAgo.setMonth(monthAgo.getMonth() - 1);
    filteredEntries = filteredEntries.filter(
        (entry) => new Date(entry.date) >= monthAgo
    );
  }

  const dates = filteredEntries.map((entry) => entry.date);
  const ratings = filteredEntries.map((entry) => entry.rating);

  chartOption.value = {
    xAxis: {
      type: 'category',
      data: dates,
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 10,
    },
    series: [
      {
        data: ratings,
        type: 'line',
        smooth: true,
        areaStyle: {
          color: 'rgba(115, 183, 245, 0.2)',
        },
        lineStyle: {
          width: 3,
          color: '#73b7f5',
        },
        itemStyle: {
          borderWidth: 2,
          color: '#409EFF',
        },
      },
    ],
    tooltip: {
      trigger: 'axis',
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
  };
};

// Функция для фильтрации графика по времени
const filterChart = (period) => {
  updateChart(period);
};

// Обработчик изменения страницы
const handlePageChange = (page) => {
  currentPage.value = page;
};

// Метки для слайдера
const sliderMarks = {
  1: '1',
  2: '',
  3: '3',
  4: '',
  5: '5',
  6: '',
  7: '7',
  8: '',
  9: '9',
  10: '10',
};
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

.mood-chart {
  width: 100%;
  height: 200px;
}


h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
  font-size: 2.5rem;
}

.entry-card {
  margin-bottom: 2rem;
  border-radius: 10px;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.9);
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.mood-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.el-form-item {
  margin-bottom: 0;
}

.el-slider__marks {
  font-size: 12px;
}

.el-input {
  width: 100%;
}

.submit-button {
  align-self: flex-end;
}

.history-section {
  margin-bottom: 2rem;
}

.entry-item {
  margin-bottom: 1rem;
}

.entry-card {
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.9);
}

.entry-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.entry-date {
  font-weight: bold;
  color: #333;
}

.entry-comment {
  margin-top: 0.5rem;
  font-style: italic;
  color: #555;
}

.analysis-section {
  margin-bottom: 2rem;
}

.analysis-card {
  padding: 1rem;
  text-align: center;
  background-color: rgba(255, 255, 255, 0.9);
}

.chart-section {
  margin-bottom: 2rem;
}

.chart-section h3 {
  margin-bottom: 1rem;
}

.el-form-item {
  display: flex;
  margin-top: 10px;
  flex-wrap: wrap;
}

:deep(.slider-form .el-slider) {
  min-width: 200px;
}

v-chart {
  width: 100%;
  height: 400px;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.5s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Фоновые стили */
body {
  background-color: #f0eae1;
}

.comment-text {
  min-width: 200px;
}
:deep(.el-form-item__content) {
  min-width: auto;
}

@media (max-width: 768px) {
  .form-header h3 {
    font-size: 1.2rem;
  }
}
</style>
