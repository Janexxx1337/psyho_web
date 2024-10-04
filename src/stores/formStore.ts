// src/stores/formStore.ts
import { defineStore } from 'pinia';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useUserActivitiesStore } from '@/stores/userActivities';

interface FormModel {
  name: string;
  age: number | null;
  conditionRating: number;
  symptoms: string[];
  description: string;
}

export const useFormStore = defineStore('formStore', () => {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const router = useRouter();
  const userActivitiesStore = useUserActivitiesStore();

  // Form state
  const form = reactive<FormModel>({
    name: '',
    age: null,
    conditionRating: 0,
    symptoms: [],
    description: '',
  });

  // Step state
  const activeStep = ref(0);

  // Loading state
  const isLoading = ref(false);

  // Validation rules
  const rules = {
    name: [
      {
        required: true,
        message: 'Пожалуйста, введите ваше имя',
        trigger: 'blur',
      },
    ],
    age: [
      {
        required: true,
        message: 'Пожалуйста, введите ваш возраст',
        trigger: 'blur',
      },
      {
        type: 'number',
        min: 0,
        message: 'Возраст должен быть положительным числом',
        trigger: 'blur',
      },
    ],
    conditionRating: [
      {
        required: true,
        message: 'Пожалуйста, оцените ваше состояние',
        trigger: 'change',
      },
    ],
    symptoms: [
      {
        required: true,
        message: 'Пожалуйста, выберите симптомы',
        trigger: 'change',
      },
    ],
    description: [
      {
        required: true,
        message: 'Пожалуйста, опишите ваше состояние',
        trigger: 'blur',
      },
    ],
  };

  // Action to go to the next step
  const nextStep = () => {
    if (activeStep.value < 2) {
      activeStep.value++;
    }
  };

  // Action to go to the previous step
  const prevStep = () => {
    if (activeStep.value > 0) {
      activeStep.value--;
    }
  };

  // Action to handle form submission
  const handleSubmit = async () => {
    isLoading.value = true;
    try {
      const sessionId = Date.now().toString();

      const formData = new FormData();
      formData.append('name', form.name);
      formData.append('age', String(form.age));
      formData.append('condition', String(form.conditionRating));
      formData.append('symptoms', form.symptoms.join(', '));
      formData.append('description', form.description);
      formData.append('session_id', sessionId);

      const { data } = await axios.post(
        `${API_BASE_URL}/get_recommendations`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      await router.push({
        name: 'RecommendationsPage',
        params: {
          recommendations: data.recommendations,
          name: form.name,
          age: form.age,
          condition: form.conditionRating,
          symptoms: form.symptoms,
          description: form.description,
          session_id: sessionId,
        },
      });

      const activity = 'Был посещен сеанс с доктором ИИ';
      const date = new Date();

      console.log('Добавление активности в store:', { date, activity });
      userActivitiesStore.addActivity(date, activity);
    } catch (error) {
      console.error('Ошибка при отправке формы:', error);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    form,
    activeStep,
    isLoading,
    rules,
    nextStep,
    prevStep,
    handleSubmit,
  };
});
