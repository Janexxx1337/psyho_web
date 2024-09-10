<template>
  <el-container class="app-container">
    <el-main class="main">
      <el-card class="form-card" shadow="hover">
        <h2>Заполните форму</h2>
        <!-- Форма с элементами и иконками Element Plus -->
        <el-form :model="form" @submit.prevent="handleSubmit" label-position="top" label-width="120px">
          <el-form-item label="Ваше имя" required>
            <div class="input-with-icon">
              <User class="input-icon" />
              <el-input v-model="form.name" placeholder="Введите ваше имя"></el-input>
            </div>
          </el-form-item>
          <el-form-item label="Ваш возраст" required>
            <div class="input-with-icon">
              <Calendar class="input-icon" />
              <el-input type="number" v-model="form.age" placeholder="Введите ваш возраст"></el-input>
            </div>
          </el-form-item>
          <el-form-item label="Оцените свое состояние" required>
            <div class="input-with-icon">
              <Document class="input-icon" />
              <el-select v-model="form.condition" placeholder="Выберите состояние">
                <el-option label="Спокойный и уверенный" value="Спокойный и уверенный"></el-option>
                <el-option label="Немного напряженный, но справляюсь" value="Немного напряженный, но справляюсь"></el-option>
                <el-option label="Чувствую беспокойство и стресс" value="Чувствую беспокойство и стресс"></el-option>
                <el-option label="Усталость и эмоциональное выгорание" value="Усталость и эмоциональное выгорание"></el-option>
                <el-option label="Чувствую себя подавленным и одиноким" value="Чувствую себя подавленным и одиноким"></el-option>
                <el-option label="Испытываю панику или страх" value="Испытываю панику или страх"></el-option>
              </el-select>
            </div>
          </el-form-item>
          <el-form-item label="Опишите подробнее ваше состояние">
            <div class="input-with-icon">
              <Document class="input-icon" />
              <el-input type="textarea" v-model="form.description" placeholder="Введите подробное описание"></el-input>
            </div>
            <!-- Множественный выбор тегов -->
            <el-select v-model="selectedDescriptions" multiple placeholder="Выберите заготовки состояния" @change="handleDescriptionChange">
              <el-option
                  v-for="(description, index) in stateDescriptions"
                  :key="index"
                  :label="description"
                  :value="description"
              ></el-option>
            </el-select>
            <!-- Отображение выбранных тегов -->
            <div class="selected-tags">
              <el-tag v-for="(tag, index) in selectedDescriptions" :key="index" type="info" closable @close="removeTag(tag)">
                {{ tag }}
              </el-tag>
            </div>
          </el-form-item>
          <el-button
              type="primary"
              @click="handleSubmit"
              class="submit-button"
              :disabled="isSubmitDisabled || isLoading"
              :loading="isLoading"
          >
            <Download /> Отправить
          </el-button>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

import axios from 'axios';
import { stateDescriptions } from '@/state/descriptions';

// Импортируем иконки из Element Plus
import { User, Calendar, Document, Download } from '@element-plus/icons-vue';

const router = useRouter();

const form = ref({
  name: '',
  age: null,
  condition: '',
  description: ''
});

const selectedDescriptions = ref<string[]>([]);

const handleDescriptionChange = (value: string[]) => {
  form.value.description = value.join(', '); // Обновляем описание на основе выбранных заготовок
};

// Удаление тега
const removeTag = (tag: string) => {
  const index = selectedDescriptions.value.indexOf(tag);
  if (index !== -1) {
    selectedDescriptions.value.splice(index, 1);
    handleDescriptionChange(selectedDescriptions.value);
  }
};

// Состояние загрузки
const isLoading = ref(false);

// Проверка, что все поля заполнены
const isSubmitDisabled = computed(() => {
  return (
      !form.value.name ||
      !form.value.age ||
      !form.value.condition ||
      !form.value.description
  );
});

const handleSubmit = async () => {
  if (isSubmitDisabled.value) return; // Проверяем, что все поля заполнены

  isLoading.value = true; // Устанавливаем состояние загрузки в true

  try {
    const formData = new FormData();
    formData.append('name', form.value.name);
    formData.append('age', String(form.value.age)); // Преобразуем число в строку
    formData.append('condition', form.value.condition);
    formData.append('description', form.value.description);
    formData.append('session_id', Date.now().toString()); // Генерируем уникальный session_id

    const { data } = await axios.post('http://localhost:8000/get_recommendations', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // Передача данных в параметры маршрута
    await router.push({
      name: 'RecommendationsPage',
      params: {
        recommendations: data.recommendations,
        name: form.value.name,
        age: form.value.age,
        session_id: Date.now().toString() // Передаем session_id для продолжения диалога
      }
    });
  } catch (error) {
    console.error('Ошибка при отправке формы:', error);
  } finally {
    isLoading.value = false; // После получения ответа или ошибки сбрасываем состояние загрузки
  }
};
</script>


<style scoped>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.main {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  min-height: calc(100vh - 80px);
  background-color: #f0f2f5;
}

.form-card {
  width: 100%;
  max-width: 500px;
  padding: 2rem;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
  font-size: 1.6rem;
}

.input-with-icon {
  display: flex;
  align-items: center;
  width: 100%;
}

.input-with-icon .el-input,
.input-with-icon .el-select {
  flex: 1;
}

.input-icon {
  margin-right: 10px;
  font-size: 1.2rem;
  color: #3e8e41;
}

.submit-button {
  width: 100%;
  margin-top: 1rem;
  font-size: 1rem;
  padding: 0.75rem;
  border-radius: 5px;
}

.selected-tags {
  margin-top: 0.5rem;
}
</style>
