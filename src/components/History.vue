<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const userRequests = ref([]);
const router = useRouter();

const fetchSessions = async () => {
  try {
    const response = await axios.get('http://localhost:8000/get_sessions');
    userRequests.value = response.data.sessions.map((session: any) => ({
      id: session.session_id,
      date: session.date,
      description: `${session.name} (${session.age} лет) - ${session.recommendations.slice(0, 30)}...`,
      fullDescription: session.recommendations // Полное описание
    }));
  } catch (error) {
    console.error('Ошибка при получении истории обращений:', error);
  }
};

const viewSessionDetails = (sessionId: string) => {
  router.push({ name: 'SessionDetails', params: { session_id: sessionId } });
};

onMounted(() => {
  fetchSessions();
});
</script>

<template>
  <div class="history-container">
    <h2>История обращений</h2>
    <el-table :data="userRequests" border stripe>
      <el-table-column prop="date" label="Дата" width="150"></el-table-column>
      <el-table-column prop="description" label="Описание"></el-table-column>
      <el-table-column label="Действия" width="150">
        <template #default="scope">
          <el-button type="primary" @click="viewSessionDetails(scope.row.id)">Посмотреть</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
.history-container {
  padding: 2rem;
}

h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #333;
}
</style>
