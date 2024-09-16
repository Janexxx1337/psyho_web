<!-- VesselAnimation.vue -->
<template>
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
      <text x="100" y="200" text-anchor="middle" font-size="40" fill="#000" stroke="#000" stroke-width="1" paint-order="stroke">
        {{ percentage }}%
      </text>
    </svg>
  </div>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue';
import anime from 'animejs';

// Правильно получаем доступ к пропсам
const { percentage } = defineProps({
  percentage: {
    type: Number,
    required: true,
  },
});

const vesselSvg = ref(null);

// Уровень воды в зависимости от процента
const waterLevel = computed(() => {
  const maxY = 340; // Минимальный уровень воды (пустой сосуд)
  const minY = 40;  // Максимальный уровень воды (полный сосуд)
  return maxY - ((maxY - minY) * (percentage / 100));
});

// Путь для воды с волной
const waterPath = computed(() => {
  const amplitude = 20; // Амплитуда волны
  const wavelength = 600; // Длина волны
  const offset = -300; // Смещение волны по оси X

  return `
    M${offset},${waterLevel.value}
    C${offset + wavelength / 4},${waterLevel.value - amplitude} ${offset + wavelength / 4},${waterLevel.value + amplitude} ${offset + wavelength / 2},${waterLevel.value}
    S${offset + (3 * wavelength) / 4},${waterLevel.value - amplitude} ${offset + wavelength},${waterLevel.value}
    L${offset + wavelength},400 L${offset},400 Z
  `;
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

// Анимация волны
const animateWave = () => {
  const water = vesselSvg.value.querySelector('.water');
  anime.remove(water); // Удаляем предыдущие анимации
  anime({
    targets: water,
    translateX: ['-100', '100'], // Смещение волны
    duration: 4000,
    easing: 'linear',
    direction: 'alternate',
    loop: true,
  });
};

onMounted(() => {
  animateWave();
  createBubbles();
});

// Обновляем пузырьки при изменении уровня воды
watch(waterLevel, () => {
  createBubbles();
});
</script>

<style scoped>
.progress-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.vessel-svg {
  width: 120px;
  height: 240px;
}
</style>
