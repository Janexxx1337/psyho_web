<template>
  <el-card class="entry-card">
    <div class="form-header">
      <h3>Как вы себя чувствуете сегодня?</h3>
      <MoodIcon :rating="rating" class="mood-icon-large" />
    </div>
    <el-form @submit.prevent="handleSubmit" class="mood-form">
      <el-form-item class="slider-form" label="Оцените ваше настроение">
        <el-slider
            v-model="rating"
            :min="1"
            :max="10"
            show-tooltip
            :marks="marks"
        ></el-slider>
      </el-form-item>
      <el-form-item label="Комментарий">
        <el-input
            class="comment-text"
            type="textarea"
            v-model="comment"
            placeholder="Опишите ваше настроение"
            :rows="3"
        ></el-input>
      </el-form-item>
      <el-button type="primary" native-type="submit" class="submit-button">
        <span class="material-symbols-outlined">edit</span>
        Добавить запись
      </el-button>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { defineEmits, ref } from 'vue';
import MoodIcon from '@/views/mood/icons/MoodIcon.vue';

const emit = defineEmits(['submit']);

const rating = ref(5);
const comment = ref('');

const marks = {
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

const handleSubmit = () => {
  emit('submit', { rating: rating.value, comment: comment.value });
  rating.value = 5;
  comment.value = '';
};
</script>

<style scoped>
.mood-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

</style>
