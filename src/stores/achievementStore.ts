// stores/achievementStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAchievementStore = defineStore('achievements', () => {
  const achievements = ref<Record<string, boolean>>({});

  const unlockAchievement = (key: string) => {
    achievements.value[key] = true;
  };

  const isAchievementUnlocked = (key: string) => {
    return !!achievements.value[key];
  };

  const allAchievements = [
    {
      key: 'first_step',
      title: 'Первый шаг',
      description: 'Пройден 1 уровень',
    },
    { key: 'novice', title: 'Новичок', description: 'Достигнут 5 уровень' },
    { key: 'expert', title: 'Эксперт', description: 'Достигнут 10 уровень' },
    { key: 'master', title: 'Мастер', description: 'Достигнут 15 уровень' },
    { key: 'legend', title: 'Легенда', description: 'Достигнут 20 уровень' },
    // Добавьте больше достижений по необходимости
  ];

  return {
    achievements,
    unlockAchievement,
    isAchievementUnlocked,
    allAchievements,
  };
});
