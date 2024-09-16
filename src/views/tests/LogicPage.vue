<!-- src/views/LogicPage.vue -->
<template>
  <div class="logic-page">
    <h1>{{ test.title }}</h1>
    <p>{{ test.description }}</p>

    <el-progress
        v-if="!isTestCompleted"
        :percentage="progressPercentage"
        status="success"
        class="progress-bar"
    ></el-progress>

    <div v-if="!isTestCompleted">
      <div class="question-card">
        <p class="question">{{ currentQuestion.question }}</p>
        <el-radio-group v-model="userAnswer" size="large">
          <el-radio
              v-for="option in currentQuestion.options"
              :key="option"
              :label="option"
          >
            {{ option }}
          </el-radio>
        </el-radio-group>
      </div>
      <div class="navigation-buttons">
        <el-button
            type="primary"
            @click="nextQuestion"
            :disabled="!userAnswer"
            :loading="isSubmitting"
        >
          {{ isLastQuestion ? 'Завершить тест' : 'Следующий вопрос' }}
        </el-button>
      </div>
    </div>

    <div v-else class="results">
      <h2>Результаты Теста</h2>
      <p>
        Вы ответили правильно на
        <strong>{{ correctAnswers }}</strong>
        из
        <strong>{{ totalQuestions }}</strong>
        вопросов.
      </p>
      <div class="nickname-section">
        <img :src="nickname.image" :alt="nickname.title" class="nickname-image" />
        <p class="nickname-title">{{ nickname.title }}</p>
      </div>
      <el-button type="success" @click="retakeTest">Пройти снова</el-button>
      <el-button @click="goBack">Вернуться к тестам</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { logicTest } from '@/state/tests/logicTest';

// Инициализация роутера
const router = useRouter();

// Состояния теста
const test = ref(logicTest);
const currentQuestionIndex = ref(0);
const userAnswer = ref(null);
const answers = ref([]);
const isSubmitting = ref(false);

// Вычисляемый текущий вопрос
const currentQuestion = computed(() => {
  return test.value.questions[currentQuestionIndex.value];
});

// Проверка, является ли текущий вопрос последним
const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === test.value.questions.length - 1;
});

// Проверка, завершен ли тест
const isTestCompleted = computed(() => {
  return currentQuestionIndex.value >= test.value.questions.length;
});

// Общее количество вопросов
const totalQuestions = computed(() => {
  return test.value.questions.length;
});

// Количество правильных ответов
const correctAnswers = computed(() => {
  return answers.value.filter(
      (a) => a.selected === a.correct
  ).length;
});

// Прогресс теста
const progressPercentage = computed(() => {
  return Math.round((currentQuestionIndex.value / totalQuestions.value) * 100);
});

// Прозвище и значок на основе количества правильных ответов
const nickname = computed(() => {
  const score = correctAnswers.value;
  if (score >= 23) {
    return {
      title: 'Эксперт Логики',
      image: new URL('@/assets/icons/expert.svg', import.meta.url).href,
    };
  } else if (score >= 15) {
    return {
      title: 'Профи Логики',
      image: new URL('@/assets/icons/profi.svg', import.meta.url).href,
    };
  } else if (score >= 8) {
    return {
      title: 'Ученик Логики',
      image: new URL('@/assets/icons/scholar.svg', import.meta.url).href,
    };
  } else {
    return {
      title: 'Начинающий Логик',
      image: new URL('@/assets/icons/junior.svg', import.meta.url).href,
    };
  }
});

// Функция перехода к следующему вопросу или завершения теста
const nextQuestion = async () => {
  if (!userAnswer.value) return;

  isSubmitting.value = true;

  // Симуляция асинхронной операции (например, сохранение ответа)
  await new Promise((resolve) => setTimeout(resolve, 300));

  // Сохраняем ответ
  answers.value.push({
    question: currentQuestion.value.question,
    selected: userAnswer.value,
    correct: currentQuestion.value.answer,
  });

  // Сбрасываем выбранный ответ
  userAnswer.value = null;

  if (isLastQuestion.value) {
    // Завершаем тест
    currentQuestionIndex.value++;
  } else {
    // Переходим к следующему вопросу
    currentQuestionIndex.value++;
  }

  isSubmitting.value = false;
};

// Функция повторного прохождения теста
const retakeTest = () => {
  currentQuestionIndex.value = 0;
  userAnswer.value = null;
  answers.value = [];
};

// Функция возврата к списку тестов
const goBack = () => {
  router.push('/tests');
};
</script>

<style scoped>
.logic-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 10px;
}

p {
  text-align: center;
  margin-bottom: 30px;
}

.progress-bar {
  margin-bottom: 20px;
}

.question-card {
  background-color: #f9f9f9;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question {
  font-size: 1.3em;
  margin-bottom: 20px;
}

.el-radio-group {
  display: flex;
  justify-content: space-around;
}

.el-radio {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 4px;
  transition: background-color 0.3s, border-color 0.3s;
}

.el-radio:hover {
  background-color: #f0f0f0;
  border-color: #409EFF;
}

.navigation-buttons {
  text-align: center;
  margin-top: 20px;
}

.navigation-buttons .el-button {
  margin: 0 10px;
}

.results {
  text-align: center;
}

.results h2 {
  margin-bottom: 20px;
  color: #67C23A;
}

.results p {
  font-size: 1.2em;
  margin-bottom: 30px;
}

.results .el-button {
  margin: 0 10px;
}

img {
  width: 55px;
}
</style>
