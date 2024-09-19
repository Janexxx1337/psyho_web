<template>
  <div class="history-container">
    <h2>История обращений</h2>
    <el-input
        v-model="searchQuery"
        placeholder="Поиск по имени или описанию"
        clearable
        class="search-input"
    ></el-input>
    <el-table
        :data="filteredSessions"
        border
        stripe
        style="width: 100%;"
        @sort-change="handleSortChange"
    >
      <el-table-column
          prop="date"
          label="Дата"
          width="150"
          sortable="custom"
      ></el-table-column>
      <el-table-column prop="description" label="Описание"></el-table-column>
      <el-table-column label="Действия" width="150">
        <template #default="scope">
          <el-button
              type="primary"
              @click="viewSessionDetails(scope.row.id)"
              size="small"
          >
            Посмотреть
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

interface Session {
  id: string;
  date: string;
  description: string;
  fullDescription: any[];
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


const userRequests = ref<Session[]>([]);
const router = useRouter();
const searchQuery = ref('');
const sortKey = ref('');
const sortOrder = ref('');

const stripHtmlTags = (html: string) => {
    return html.replace(/<\/?[^>]+(>|$)/g, '');
  };

const fetchSessions = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get_sessions`);
    userRequests.value = response.data.sessions.map((session: any) => {
      const assistantMessage = session.history.find(
          (message: any) => message.role === 'assistant'
      );
      const plainText = assistantMessage
          ? stripHtmlTags(assistantMessage.content).slice(0, 50)
          : 'Нет данных';
      return {
        id: session.session_id,
        date: session.date,
        description: `${session.name} (${session.age} лет) - ${plainText}...`,
        fullDescription: session.history, // Полная история общения
      };
    });
  } catch (error) {
    console.error('Ошибка при получении истории обращений:', error);
  }
};

const getSessionPreview = (history: any[]) => {
  const assistantMessage = history.find(message => message.role === 'assistant');
  if (assistantMessage) {
    return assistantMessage.content.slice(0, 30);
  }
  return 'Нет данных';
};

const viewSessionDetails = (sessionId: string) => {
  router.push({ name: 'SessionDetails', params: { session_id: sessionId } });
};

const handleSortChange = ({ prop, order }: { prop: string; order: string }) => {
  sortKey.value = prop;
  sortOrder.value = order;
};

const filteredSessions = computed(() => {
  let data = userRequests.value;
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    data = data.filter(session =>
        session.description.toLowerCase().includes(query)
    );
  }
  if (sortKey.value && sortOrder.value) {
    data = data.slice().sort((a, b) => {
      const result = a[sortKey.value].localeCompare(b[sortKey.value]);
      return sortOrder.value === 'ascending' ? result : -result;
    });
  }
  return data;
});

onMounted(() => {
  fetchSessions();
});
</script>

<style scoped>
.history-container {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  background-color: #f9fafc;
}

h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #333;
}

.search-input {
  margin-bottom: 1rem;
  width: 300px;
}

@media (max-width: 600px) {
  .search-input {
    width: 100%;
  }
}
</style>
