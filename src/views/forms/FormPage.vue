<template>
  <el-container class="app-container">
    <el-main class="main">
      <el-card class="form-card" shadow="hover">
        <h2>Психологическая поддержка</h2>
        <p class="form-description">
          Пожалуйста, заполните эту форму, чтобы мы могли предоставить вам персональные рекомендации и поддержку.
        </p>

        <!-- Шаги формы -->
        <el-steps :active="formStore.activeStep" finish-status="success" align-center>
          <el-step title="Персональная информация"></el-step>
          <el-step title="Состояние"></el-step>
          <el-step title="Описание"></el-step>
        </el-steps>

        <!-- Форма -->
        <el-form
            :model="formStore.form"
            :rules="formStore.rules"
            ref="formRef"
            label-position="top"
            label-width="120px"
            class="step-form"
        >
          <!-- Шаг 1 -->
          <div v-if="formStore.activeStep === 0">
            <el-form-item label="Ваше имя" prop="name">
              <div class="input-with-icon">
                <User class="input-icon" />
                <el-input v-model="formStore.form.name" placeholder="Введите ваше имя"></el-input>
              </div>
            </el-form-item>

            <el-form-item label="Ваш возраст" prop="age">
              <div class="input-with-icon">
                <Calendar class="input-icon" />
                <el-input-number
                    v-model="formStore.form.age"
                    placeholder="Введите ваш возраст"
                    :min="0"
                    :max="120"
                    controls-position="right"
                    :step="1"
                    class="age-input-number"
                ></el-input-number>
              </div>
            </el-form-item>
          </div>

          <!-- Шаг 2 -->
          <div v-if="formStore.activeStep === 1">
            <el-form-item label="Оцените своё состояние по шкале от 1 до 10" prop="conditionRating">
              <el-rate v-model="formStore.form.conditionRating" :max="10" show-score></el-rate>
            </el-form-item>

            <el-form-item label="Выберите симптомы, которые вы испытываете" prop="symptoms">
              <el-checkbox-group v-model="formStore.form.symptoms">
                <el-checkbox label="Бессонница"></el-checkbox>
                <el-checkbox label="Потеря аппетита"></el-checkbox>
                <el-checkbox label="Раздражительность"></el-checkbox>
                <el-checkbox label="Тревожность"></el-checkbox>
                <el-checkbox label="Панические атаки"></el-checkbox>
                <!-- Добавьте другие варианты -->
              </el-checkbox-group>
            </el-form-item>
          </div>

          <!-- Шаг 3 -->
          <div v-if="formStore.activeStep === 2">
            <el-form-item label="Опишите подробнее ваше состояние" prop="description">
              <el-input
                  v-model="formStore.form.description"
                  type="textarea"
                  :rows="4"
                  placeholder="Опишите ваше состояние подробнее..."
              ></el-input>
            </el-form-item>
          </div>

          <!-- Кнопки управления -->
          <div class="form-actions">
            <el-button v-if="formStore.activeStep > 0" @click="prevStep">Назад</el-button>
            <el-button
                v-if="formStore.activeStep < 2"
                type="primary"
                @click="handleNextStep"
            >
              Далее
            </el-button>
            <el-button
                v-if="formStore.activeStep === 2"
                type="success"
                @click="handleFormSubmit"
                :loading="formStore.isLoading"
            >
              <Download /> Отправить
            </el-button>
          </div>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { User, Calendar, Download } from '@element-plus/icons-vue';
import { useFormStore } from '@/stores/formStore';
import { useUserActivitiesStore } from '@/stores/userActivities';

// Initialize the form store
const formStore = useFormStore();


const userActivitiesStore = useUserActivitiesStore();


const formRef = ref<InstanceType<typeof import('element-plus').Form>>();

// Method to handle moving to the next step
const handleNextStep = () => {
  formRef.value.validate((valid: boolean) => {
    if (valid) {
      formStore.nextStep();
    } else {
      console.log('Форма содержит ошибки.');
    }
  });
};

// Method to handle moving to the previous step
const prevStep = () => {
  formStore.prevStep();
};

// Method to handle form submission
const handleFormSubmit = () => {
  formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      await formStore.handleSubmit();
    } else {
      console.log('Форма содержит ошибки.');
    }
  });
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
  background-color: #f9fafc;
}

.form-card {
  width: 100%;
  max-width: 600px;
  padding: 2rem;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 0.5rem;
  text-align: center;
  color: #333;
  font-size: 1.8rem;
}

.form-description {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #666;
}

.el-steps {
  margin-bottom: 2rem;
}

.input-with-icon {
  display: flex;
  align-items: center;
  width: 100%;
}

.input-with-icon .el-input,
.input-with-icon .el-input-number {
  flex: 1;
}

.age-input-number {
  width: 100%;
}

.input-icon {
  margin-right: 10px;
  font-size: 1.2rem;
  color: #409EFF;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.el-button {
  width: 100px;
}

.step-form {
  margin-top: 2rem;
}

.el-form-item {
  margin-bottom: 1.5rem;
}

.el-form-item label {
  font-weight: bold;
  color: #333;
}

.el-input,
.el-input-number,
.el-checkbox-group {
  width: 100%;
}
</style>
