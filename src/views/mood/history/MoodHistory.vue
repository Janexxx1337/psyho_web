<template>
  <div v-if="entries.length" class="history-section">
    <h3>История настроений</h3>
    <div class="history-container">
      <el-collapse v-model="activeEntries">
        <el-collapse-item
          v-for="entry in paginatedEntries"
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
      <el-pagination
        layout="prev, pager, next"
        :total="entries.length"
        :page-size="pageSize"
        @current-change="handlePageChange"
        class="pagination"
      ></el-pagination>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, computed } from 'vue';
  import MoodIcon from '@/views/mood/icons/MoodIcon.vue';

  const props = defineProps({
    entries: {
      type: Array,
      required: true,
    },
    pageSize: {
      type: Number,
      default: 5,
    },
  });

  const activeEntries = ref([]);

  const currentPage = ref(1);

  const reversedEntries = computed(() => [...props.entries].reverse());

  const paginatedEntries = computed(() => {
    const start = (currentPage.value - 1) * props.pageSize;
    const end = start + props.pageSize;
    return reversedEntries.value.slice(start, end);
  });

  const handlePageChange = (page) => {
    currentPage.value = page;
  };
</script>

<style scoped>
  /* Добавьте стили для MoodHistory */
</style>
