<template>
  <div>
    <el-calendar
        v-model="currentDate"
        :locale="ruLocale"
    >
      <template #date-cell="{ data }">
        <div class="activity-cell">
          <div class="date-number">{{ data.day.split('-')[2] }}</div>
          <!-- Индикатор активности с тултипом -->
          <el-tooltip
              v-if="hasActivity(data)"
              :content="getActivitiesDescription(data)"
              placement="top"
              effect="dark"
          >
            <div
                :class="['activity-dot', getActivityClass(data)]"
                @click="openActivityDialog(data.day)"
            ></div>
          </el-tooltip>
          <!-- Кнопка добавления события с тултипом -->
          <el-tooltip content="Добавить событие" placement="top">
            <el-button
                icon="Plus"
                @click="handleAddActivityClick(data.day)"
                class="add-activity-button"
                circle
                size="small"
                type="primary"
            ></el-button>
          </el-tooltip>
        </div>
      </template>
    </el-calendar>

    <!-- Диалоговое окно с деталями активности -->
    <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
        :lock-scroll="false"
    >
      <div>
        <el-form @submit.prevent="addActivity" class="add-activity-form">
          <el-form-item>
            <el-input
                v-model="newActivity"
                placeholder="Введите описание события"
                clearable
                prefix-icon="Edit"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit">Добавить событие</el-button>
          </el-form-item>
        </el-form>
        <el-divider />
        <ul class="activity-list">
          <li v-for="(activity, index) in selectedActivities" :key="index">
            <el-icon><Document /></el-icon>
            {{ activity }}
          </li>
        </ul>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">Закрыть</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import dayjs from 'dayjs';
import 'dayjs/locale/ru';
import ruLocale from 'element-plus/es/locale/lang/ru';
import { ElMessage } from 'element-plus';
import { Edit, Document, Plus } from '@element-plus/icons-vue';
import { useUserActivitiesStore } from '@/stores/userActivities';

dayjs.locale('ru');

const currentDate = ref(new Date());
const dialogVisible = ref(false);
const selectedActivities = ref<string[]>([]);
const selectedDate = ref('');
const newActivity = ref('');

const userActivitiesStore = useUserActivitiesStore();

// Проверка наличия активности на дату
const hasActivity = (data: any) => {
  const activityDate = data.day;
  return !!userActivitiesStore.activities[activityDate];
};

// Получение количества активностей на дату
const getActivityCount = (data: any) => {
  const activityDate = data.day;
  const activities = userActivitiesStore.activities[activityDate];
  return activities ? activities.length : 0;
};

// Получение класса для индикатора активности в зависимости от количества событий
const getActivityClass = (data: any) => {
  const count = getActivityCount(data);
  if (count >= 3) return 'activity-dot-red';
  if (count === 2) return 'activity-dot-yellow';
  if (count === 1) return 'activity-dot-blue';
  return '';
};

// Получение описания активностей для тултипа
const getActivitiesDescription = (data: any) => {
  const activityDate = data.day;
  const activities = userActivitiesStore.activities[activityDate];
  if (activities && activities.length > 0) {
    return activities.join('\n');
  }
  return '';
};

// Открытие диалога для просмотра активностей
const openActivityDialog = (date: string) => {
  selectedDate.value = date;
  selectedActivities.value = userActivitiesStore.activities[date] || [];
  dialogVisible.value = true;
};

// Обработчик клика по кнопке добавления события
const handleAddActivityClick = (date: string) => {
  selectedDate.value = date;
  selectedActivities.value = userActivitiesStore.activities[date] || [];
  dialogVisible.value = true;
};

// Добавление новой активности
const addActivity = () => {
  if (newActivity.value.trim() === '') {
    ElMessage.warning('Пожалуйста, введите описание события.');
    return;
  }
  userActivitiesStore.addActivity(dayjs(selectedDate.value).toDate(), newActivity.value);
  selectedActivities.value = [...userActivitiesStore.activities[selectedDate.value]];
  newActivity.value = '';
  ElMessage.success('Событие добавлено.');
};

// Форматирование заголовка диалога
const formatDate = (date: string) => {
  return dayjs(date).format('D MMMM YYYY');
};

const dialogTitle = computed(() => `Активность за ${formatDate(selectedDate.value)}`);
</script>

<style scoped>
.activity-cell {
  position: relative;
  padding: 4px;
  text-align: center;
}

.date-number {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 4px;
}

.activity-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin: 0 auto;
  cursor: pointer;
}

.activity-dot-blue {
  background-color: blue;
}

.activity-dot-yellow {
  background-color: yellow;
}

.activity-dot-red {
  background-color: red;
}

.add-activity-button {
  position: absolute;
  top: 2px;
  right: 2px;
  font-size: 12px;
  padding: 0;
}

.add-activity-button .el-icon {
  font-size: 12px;
}

/* Дополнительно: Предотвращение скачка интерфейса */
.el-dialog {
  max-height: 80vh;
}
</style>
