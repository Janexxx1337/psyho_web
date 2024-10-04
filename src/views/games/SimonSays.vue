<!-- views/games/SimonSays.vue -->
<template>
  <div class="simon-says">
    <h1>Игра "Симон говорит"</h1>
    <p v-if="!gameStarted" class="instructions">
      Нажмите "Начать игру", чтобы начать.
    </p>
    <p v-else>Уровень: {{ level }}</p>
    <div class="game-board">
      <div
        v-for="color in colors"
        :key="color"
        :class="['color-button', color]"
        @click="handleUserInput(color)"
      ></div>
    </div>
    <div class="controls">
      <el-button
        type="primary"
        @click="startGame"
        :disabled="acceptingInput || (!gameOver && gameStarted)"
      >
        {{
          gameStarted
            ? gameOver
              ? 'Начать заново'
              : 'Идет игра...'
            : 'Начать игру'
        }}
      </el-button>
    </div>
    <el-dialog
      title="Игра окончена"
      :visible.sync="showGameOverDialog"
      width="30%"
      :before-close="() => (showGameOverDialog = false)"
    >
      <div>
        <p>Ваш достигнутый уровень: {{ level }}</p>
        <h3>Разблокированные достижения:</h3>
        <ul>
          <li
            v-for="achievement in unlockedAchievements"
            :key="achievement.key"
          >
            🏆 {{ achievement.title }} - {{ achievement.description }}
          </li>
        </ul>
      </div>
      <template #footer>
        <el-button type="primary" @click="startGame">Начать заново</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
  import { ref, watch, computed } from 'vue';
  import { ElMessage } from 'element-plus';
  import { useAchievementStore } from '@/stores/achievementStore';

  const colors = ['red', 'green', 'blue', 'yellow'];

  const sequence = ref<string[]>([]);
  const userSequence = ref<string[]>([]);
  const level = ref(0);
  const gameOver = ref(false);
  const gameStarted = ref(false);
  const acceptingInput = ref(false);
  const showGameOverDialog = ref(false);

  const achievementStore = useAchievementStore();

  const unlockedAchievements = computed(() => {
    return achievementStore.allAchievements.filter((achievement) =>
      achievementStore.isAchievementUnlocked(achievement.key)
    );
  });

  watch(level, (newLevel) => {
    if (newLevel === 1) {
      achievementStore.unlockAchievement('first_step');
      ElMessage.success('Достижение разблокировано: Первый шаг!');
    } else if (newLevel === 5) {
      achievementStore.unlockAchievement('novice');
      ElMessage.success('Достижение разблокировано: Новичок!');
    } else if (newLevel === 10) {
      achievementStore.unlockAchievement('expert');
      ElMessage.success('Достижение разблокировано: Эксперт!');
    } else if (newLevel === 15) {
      achievementStore.unlockAchievement('master');
      ElMessage.success('Достижение разблокировано: Мастер!');
    } else if (newLevel === 20) {
      achievementStore.unlockAchievement('legend');
      ElMessage.success('Достижение разблокировано: Легенда!');
    }
  });

  const playSequence = async () => {
    acceptingInput.value = false;
    for (const color of sequence.value) {
      await highlightButton(color);
      await delay(600);
    }
    acceptingInput.value = true;
  };

  const highlightButton = async (color: string) => {
    const button = document.querySelector(`.${color}`) as HTMLElement;
    if (button) {
      button.classList.add('active');
      playSound(color);
      await delay(500);
      button.classList.remove('active');
    }
  };

  const delay = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  const playSound = (color: string) => {
    const context = new (window.AudioContext ||
      (window as any).webkitAudioContext)();
    const o = context.createOscillator();
    const g = context.createGain();
    o.type = 'sine';
    o.frequency.value = getFrequency(color);
    o.connect(g);
    g.connect(context.destination);
    o.start(0);
    g.gain.exponentialRampToValueAtTime(0.00001, context.currentTime + 0.5);
  };

  const getFrequency = (color: string): number => {
    switch (color) {
      case 'red':
        return 261.6; // C4
      case 'green':
        return 329.6; // E4
      case 'blue':
        return 392.0; // G4
      case 'yellow':
        return 523.3; // C5
      default:
        return 440;
    }
  };

  const addColorToSequence = () => {
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    sequence.value.push(randomColor);
  };

  const handleUserInput = async (color: string) => {
    if (!acceptingInput.value || gameOver.value) return;
    userSequence.value.push(color);
    playSound(color);
    const currentStep = userSequence.value.length - 1;
    const button = document.querySelector(`.${color}`) as HTMLElement;
    button.classList.add('active');
    await delay(200);
    button.classList.remove('active');
    if (userSequence.value[currentStep] !== sequence.value[currentStep]) {
      gameOver.value = true;
      acceptingInput.value = false;
      showGameOverDialog.value = true;
    } else if (userSequence.value.length === sequence.value.length) {
      level.value++;
      userSequence.value = [];
      addColorToSequence();
      await delay(1000);
      playSequence();
    }
  };

  const startGame = async () => {
    sequence.value = [];
    userSequence.value = [];
    level.value = 1;
    gameOver.value = false;
    gameStarted.value = true;
    showGameOverDialog.value = false;
    addColorToSequence();
    await delay(500);
    playSequence();
  };
</script>

<style scoped>
  /* Ваши существующие стили */
</style>

<style scoped>
  .simon-says {
    text-align: center;
    padding: 20px;
  }

  .instructions {
    font-size: 18px;
    margin-bottom: 20px;
  }

  .game-board {
    display: grid;
    grid-template-columns: repeat(2, minmax(100px, 140px));
    grid-gap: 10px;
    justify-content: center;
    margin-top: 20px;
  }

  .color-button {
    width: 100%;
    padding-bottom: 100%;
    position: relative;
    border-radius: 10px;
    cursor: pointer;
    opacity: 0.9;
    transition: transform 0.1s;
  }

  .color-button.active {
    opacity: 1;
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  }

  .color-button::after {
    content: '';
    display: block;
    padding-bottom: 100%;
  }

  .color-button.red {
    background-color: #f44336;
  }

  .color-button.green {
    background-color: #4caf50;
  }

  .color-button.blue {
    background-color: #2196f3;
  }

  .color-button.yellow {
    background-color: #ffeb3b;
  }

  .controls {
    margin-top: 20px;
  }

  .el-dialog__body {
    text-align: center;
  }

  @media (max-width: 600px) {
    .game-board {
      grid-template-columns: repeat(2, 1fr);
      grid-gap: 10px;
    }
  }
</style>
