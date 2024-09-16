<template>
  <div class="logic-page">
    <h1>{{ test.title }}</h1>
    <p>{{ test.description }}</p>

    <div v-if="!isTestCompleted">
      <div class="progress-container">
        <svg ref="vesselSvg" viewBox="0 0 200 400" class="vessel-svg">
          <!-- Фон сосуда -->
          <path
              d="M50,20 L150,20 C160,20 160,30 160,40 L160,340 C160,360 140,380 100,380 C60,380 40,360 40,340 L40,40 C40,30 40,20 50,20 Z"
              fill="#fff"
              stroke="#409EFF"
              stroke-width="4"
          />
          <!-- Вода -->
          <g clip-path="url(#vesselClip)">
            <path
                class="water"
                :d="waterPath"
                fill="#409EFF"
            ></path>
            <!-- Пузырьки -->
            <g class="bubbles"></g>
          </g>
          <!-- Клиппинг для воды -->
          <defs>
            <clipPath id="vesselClip">
              <path
                  d="M50,20 L150,20 C160,20 160,30 160,40 L160,340 C160,360 140,380 100,380 C60,380 40,360 40,340 L40,40 C40,30 40,20 50,20 Z"
              />
            </clipPath>
          </defs>
          <!-- Контур сосуда поверх воды -->
          <path
              d="M50,20 L150,20 C160,20 160,30 160,40 L160,340 C160,360 140,380 100,380 C60,380 40,360 40,340 L40,40 C40,30 40,20 50,20 Z"
              fill="none"
              stroke="#409EFF"
              stroke-width="4"
          />
          <!-- Процент внутри сосуда -->
          <text x="100" y="200" text-anchor="middle" font-size="40" fill="#fff" stroke="#000" stroke-width="1" paint-order="stroke">
            {{ progressPercentage }}%
          </text>
        </svg>
      </div>
      <p class="question-number">Вопрос {{ currentQuestionIndex + 1 }} из {{ totalQuestions }}</p>

      <transition name="fade" mode="out-in">
        <el-card :key="currentQuestionIndex" class="question-card">
          <p class="question">{{ currentQuestion.question }}</p>
          <el-radio-group v-model="userAnswer" class="options">
            <el-radio
                v-for="option in currentQuestion.options"
                :key="option"
                :label="option"
                class="option-radio"
            >
              {{ option }}
            </el-radio>
          </el-radio-group>
        </el-card>
      </transition>

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

      <!-- Добавлен аккордеон с неправильными ответами -->
      <el-collapse v-if="incorrectAnswers.length" class="incorrect-answers">
        <el-collapse-item
            v-for="(answer, index) in incorrectAnswers"
            :key="index"
            :title="`Вопрос ${index + 1}`"
        >
          <p class="incorrect-question"><strong>Вопрос:</strong> {{ answer.question }}</p>
          <p><strong>Ваш ответ:</strong> {{ answer.selected }}</p>
          <p><strong>Правильный ответ:</strong> {{ answer.correct }}</p>
        </el-collapse-item>
      </el-collapse>

      <el-button type="success" @click="retakeTest">Пройти снова</el-button>
      <el-button @click="goBack">Вернуться к тестам</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { logicTest } from '@/state/tests/logicTest';
import anime from 'animejs';

const router = useRouter();

const test = ref(logicTest);
const currentQuestionIndex = ref(0);
const userAnswer = ref(null);
const answers = ref([]);
const isSubmitting = ref(false);

const vesselSvg = ref(null);

const currentQuestion = computed(() => {
  return test.value.questions[currentQuestionIndex.value];
});

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === test.value.questions.length - 1;
});

const isTestCompleted = computed(() => {
  return currentQuestionIndex.value >= test.value.questions.length;
});

const totalQuestions = computed(() => {
  return test.value.questions.length;
});

const correctAnswers = computed(() => {
  return answers.value.filter(
      (a) => a.selected === a.correct
  ).length;
});

const incorrectAnswers = computed(() => {
  return answers.value.filter(
      (a) => a.selected !== a.correct
  );
});

const progressPercentage = computed(() => {
  return Math.round(((currentQuestionIndex.value) / totalQuestions.value) * 100);
});

// Уровень воды в зависимости от прогресса
const waterLevel = computed(() => {
  const maxY = 340; // Минимальный уровень воды (пустой сосуд)
  const minY = 40;  // Максимальный уровень воды (полный сосуд)
  const level = maxY - ((maxY - minY) * (progressPercentage.value / 100));
  return level;
});

// Путь для воды с волной
const waterPath = computed(() => {
  const amplitude = 20; // Амплитуда волны
  const wavelength = 600; // Увеличили длину волны
  const offset = -300; // Увеличили смещение волны по оси X

  return `
    M${offset},${waterLevel.value}
    C${offset + wavelength / 4},${waterLevel.value - amplitude} ${offset + wavelength / 4},${waterLevel.value + amplitude} ${offset + wavelength / 2},${waterLevel.value}
    S${offset + (3 * wavelength) / 4},${waterLevel.value - amplitude} ${offset + wavelength},${waterLevel.value}
    L${offset + wavelength},400 L${offset},400 Z
  `;
});

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

// Функция для создания пузырьков
const createBubbles = () => {
  const bubblesGroup = vesselSvg.value.querySelector('.bubbles');
  bubblesGroup.innerHTML = ''; // Очистка предыдущих пузырьков

  for (let i = 0; i < 10; i++) {
    const bubble = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    const size = Math.random() * 5 + 2;
    bubble.setAttribute('cx', Math.random() * 200);
    bubble.setAttribute('cy', waterLevel.value + Math.random() * (400 - waterLevel.value));
    bubble.setAttribute('r', size);
    bubble.setAttribute('fill', '#fff');
    bubblesGroup.appendChild(bubble);

    anime({
      targets: bubble,
      cy: waterLevel.value - 20,
      opacity: [1, 0],
      duration: Math.random() * 2000 + 2000,
      easing: 'linear',
      delay: Math.random() * 2000,
      complete: () => {
        bubble.remove();
      }
    });
  }
};

onMounted(() => {
  animateWave();
  createBubbles();
});

watch(waterLevel, () => {
  animateWave();
  createBubbles();
});

// Анимация волны с помощью anime.js
const animateWave = () => {
  const water = vesselSvg.value.querySelector('.water');
  anime.remove(water); // Удаляем предыдущие анимации
  anime({
    targets: water,
    translateX: ['-100', '100'], // Увеличили смещение
    duration: 4000,
    easing: 'linear',
    direction: 'alternate',
    loop: true,
  });
};

const nextQuestion = async () => {
  if (!userAnswer.value) return;

  isSubmitting.value = true;

  await new Promise((resolve) => setTimeout(resolve, 300));

  answers.value.push({
    question: currentQuestion.value.question,
    selected: userAnswer.value,
    correct: currentQuestion.value.answer,
  });

  userAnswer.value = null;
  currentQuestionIndex.value++;

  isSubmitting.value = false;
};

const retakeTest = () => {
  currentQuestionIndex.value = 0;
  userAnswer.value = null;
  answers.value = [];
};

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

.progress-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.vessel-svg {
  width: 120px; /* Увеличили ширину */
  height: 240px; /* Пропорционально увеличили высоту */
}

.question-number {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
}

.question-card {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.question {
  font-size: 1.3em;
  margin-bottom: 20px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-radio {
  width: 100%;
  margin: 0;
}

.option-radio .el-radio__label {
  width: 100%;
}

.option-radio .el-radio__input {
  margin-right: 10px;
}

.option-radio .el-radio__content {
  width: 100%;
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

.nickname-section {
  margin-bottom: 30px;
}

.nickname-image {
  width: 100px;
  margin-bottom: 10px;
}

.nickname-title {
  font-size: 1.5em;
  font-weight: bold;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.incorrect-answers {
  text-align: left;
  margin: 20px auto;
  max-width: 600px;
}

@media (max-width: 600px) {
  .question {
    font-size: 1.1em;
  }

  .option-radio {
    font-size: 0.9em;
  }

  .vessel-svg {
    width: 100px;
    height: 200px;
  }
}
</style>
