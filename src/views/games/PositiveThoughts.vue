<!-- views/games/PositiveThoughts.vue -->
<template>
  <div class="positive-thoughts">
    <h1>Позитивные мысли</h1>
    <div v-if="!gameOver">
      <p class="situation">{{ currentSituation.text }}</p>
      <el-row :gutter="20">
        <el-col :span="12" v-for="(option, index) in currentSituation.options" :key="index">
          <el-card class="option-card" @click="selectOption(option)">
            <p>{{ option }}</p>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div v-else>
      <h2>Отличная работа!</h2>
      <p>Вы успешно нашли позитивные мысли.</p>
      <el-button type="primary" @click="restartGame">Начать заново</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { situations } from '@/state/games/situations.js';

interface Situation {
  text: string;
  options: string[];
  correctOption: string;
}

const currentSituationIndex = ref(0);
const currentSituation = computed(() => situations[currentSituationIndex.value]);
const gameOver = ref(false);

// Звуковые эффекты с использованием Audio API
const correctSound = new Audio('/sounds/correct.mp3');
const incorrectSound = new Audio('/sounds/incorrect.mp3');

const selectOption = (option: string) => {
  if (option === currentSituation.value.correctOption) {
    correctSound.play();
    ElMessage.success('Правильно! Это позитивная мысль.');
    if (currentSituationIndex.value < situations.length - 1) {
      currentSituationIndex.value++;
    } else {
      gameOver.value = true;
    }
  } else {
    incorrectSound.play();
    ElMessage.error('Попробуйте снова.');
  }
};

const restartGame = () => {
  currentSituationIndex.value = 0;
  gameOver.value = false;
};
</script>


<style scoped>
.positive-thoughts {
  padding: 20px;
  text-align: center;
}

.situation {
  font-size: 24px;
  margin-bottom: 30px;
}

.option-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.option-card:hover {
  transform: scale(1.05);
}

.el-card {
  text-align: center;
}

h2 {
  margin-top: 20px;
}

.el-button {
  margin-top: 20px;
}
</style>
