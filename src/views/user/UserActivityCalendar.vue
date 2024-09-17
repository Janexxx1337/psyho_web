<!-- src/components/UserActivityCalendar.vue -->
<template>
  <div>
    <el-calendar
        v-model="currentDate"
        :date-cell-render="dateCellRender"
        :locale="ruLocale"
    />
    <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
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
import { ref, h, computed } from 'vue';
import dayjs from 'dayjs';
import 'dayjs/locale/ru';
import ruLocale from 'element-plus/es/locale/lang/ru';
import { ElMessage } from 'element-plus';
import { Edit, Document } from '@element-plus/icons-vue';
import { useUserActivitiesStore } from '@/stores/userActivities';

dayjs.locale('ru');

const currentDate = ref(new Date());
const dialogVisible = ref(false);
const selectedActivities = ref<string[]>([]);
const selectedDate = ref('');
const newActivity = ref('');

const userActivitiesStore = useUserActivitiesStore();

const dateCellRender = ({ date }) => {
  const activityDate = dayjs(date).format('YYYY-MM-DD');
  const activities = userActivitiesStore.activities[activityDate];
  const hasActivity = !!activities && activities.length > 0;

  return h(
      'div',
      {
        class: 'activity-cell',
        onClick: () => handleDateClick(activityDate),
        style: { cursor: 'pointer' },
      },
      [
        h('div', { class: 'date-number' }, dayjs(date).date()),
        hasActivity && h('div', { class: 'activity-dot' }),
        hasActivity && h('div', { class: 'activity-count' }, activities.length),
      ]
  );
};

const handleDateClick = (date: string) => {
  selectedDate.value = date;
  selectedActivities.value = userActivitiesStore.activities[date] || [];
  dialogVisible.value = true;
};

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

const formatDate = (date: string) => {
  return dayjs(date).format('D MMMM YYYY');
};

const dialogTitle = computed(() => `Активность за ${formatDate(selectedDate.value)}`);
</script>

<style scoped>
.activity-cell {
  position: relative;
}

.date-number {
  text-align: right;
  padding: 4px;
}

.activity-dot {
  width: 6px;
  height: 6px;
  background-color: #409eff;
  border-radius: 50%;
  position: absolute;
  bottom: 4px;
  right: 4px;
}

.activity-count {
  position: absolute;
  bottom: 4px;
  left: 4px;
  font-size: 12px;
  color: #409eff;
}
</style>
