<template>
  <el-tabs v-model="activeTab" class="mood-tabs" type="card">
    <el-tab-pane label="Динамика настроения" name="dynamics">
      <MoodChart :entries="entries" />
    </el-tab-pane>

    <el-tab-pane label="История настроений" name="history">
      <MoodHistory :entries="entries" :pageSize="entriesPerPage" />
    </el-tab-pane>

    <el-tab-pane label="Анализ настроений" name="analysis">
      <MoodAnalysis :analysis="analysis" />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import MoodChart from '../chart/MoodChart.vue';
  import MoodHistory from '../history/MoodHistory.vue';
  import MoodAnalysis from '../analysis/MoodAnalysis.vue';

  const props = defineProps({
    entries: {
      type: Array,
      required: true,
    },
    analysis: {
      type: String,
      required: true,
    },
    entriesPerPage: {
      type: Number,
      default: 5,
    },
  });
  const activeTab = ref('dynamics');
</script>

<style scoped>
  .mood-tabs {
    margin-top: 10px;
  }
</style>
