<template>
  <el-container style="max-width: 900px; margin: 0 auto;">
    <el-header height="auto">
      <el-row :gutter="20" align="middle">
        <el-col :span="8">
          <el-input-number
              v-model="sessionDuration"
              :min="5"
              :max="60"
              label="Длительность сессии (мин)"
              placeholder="Длительность сессии"
              style="width: 100%;"
          ></el-input-number>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="startSession" :disabled="sessionActive">
            Начать сессию
          </el-button>
        </el-col>
        <el-col :span="8" style="display: flex; align-items: center;">
          <el-button type="danger" @click="endSession" v-if="sessionActive">
            Завершить сессию
          </el-button>
          <el-progress v-if="sessionActive" :percentage="progress" :format="timeFormat" style="margin-left: 10px; width: 100px;"></el-progress>
        </el-col>
      </el-row>
    </el-header>

    <el-main style="padding: 0;" v-loading="loading" element-loading-text="Загрузка...">
      <div id="chat" class="chat-container">
        <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="message.sender"
        >
          <div class="message-content">
            <span class="material-symbols-outlined avatar-icon">
              {{ message.sender === 'assistant' ? 'medical_information' : 'person' }}
            </span>
            <el-card shadow="never">
              <div v-html="message.content"></div>
            </el-card>
          </div>
        </div>
      </div>
    </el-main>

    <el-footer height="auto">
      <el-row :gutter="10" align="middle" v-if="sessionActive">
        <!-- Варианты ответов -->
        <template v-if="options.length > 0">
          <el-col :span="24">
            <el-radio-group
                v-model="selectedOption"
                style="width: 100%;"
            >
              <el-radio
                  v-for="(option, idx) in options"
                  :key="idx"
                  :label="option"
                  style="margin-bottom: 10px;"
              >
                {{ option }}
              </el-radio>
            </el-radio-group>
          </el-col>
          <el-col :span="24">
            <el-button type="primary" @click="sendMessage" :disabled="loading">
              Отправить
            </el-button>
          </el-col>
        </template>
        <!-- Поле ввода и кнопка отправки -->
        <template v-else>
          <el-col :span="18">
            <el-input
                v-model="userInput"
                placeholder="Введите ваш ответ..."
                @keyup.enter="sendMessage"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="sendMessage" :disabled="loading">
              Отправить
            </el-button>
          </el-col>
        </template>
      </el-row>
    </el-footer>

    <!-- Лоадер -->
    <el-loading
        v-if="loading"
        lock
        text="Загрузка..."
        spinner="el-icon-loading"
        background="rgba(0, 0, 0, 0.7)"
    ></el-loading>
  </el-container>
</template>

<script setup>
import {ref, onUnmounted, nextTick} from 'vue';
import {v4 as uuidv4} from 'uuid';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const sessionId = ref(localStorage.getItem('sessionId') || uuidv4());
localStorage.setItem('sessionId', sessionId.value);

const messages = ref([]);
const userInput = ref('');
const sessionActive = ref(false);
const sessionDuration = ref(15);
const options = ref([]);
const selectedOption = ref('');
const loading = ref(false);
const progress = ref(100); // для прогресса таймера
const timeLeft = ref(sessionDuration.value * 60); // оставшееся время в секундах

const addMessage = async (content, sender) => {
  messages.value.push({content, sender});
  await nextTick();
  const chat = document.getElementById('chat');
  if (chat) {
    chat.scrollTop = chat.scrollHeight;
  }
};

const communicateWithAssistant = async (userResponse = '') => {
  const formData = new URLSearchParams();
  formData.append('session_id', sessionId.value);
  formData.append('session_duration', sessionDuration.value);
  if (userResponse) {
    formData.append('user_response', userResponse);
  }

  try {
    loading.value = true;
    const response = await fetch(`${API_BASE_URL}/start_session`, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();

    if (data.assistant_reply) {
      addMessage(data.assistant_reply, 'assistant');
      if (data.options) {
        options.value = data.options;
      } else {
        options.value = [];
      }
    } else if (data.message) {
      addMessage(data.message, 'assistant');
      sessionActive.value = false;
    }
  } catch (error) {
    console.error('Ошибка:', error);
  } finally {
    loading.value = false;
  }
};

const sendMessage = () => {
  let userResponse = '';

  if (options.value.length > 0 && selectedOption.value) {
    userResponse = selectedOption.value;
    selectedOption.value = '';
    options.value = [];
  } else if (userInput.value.trim()) {
    userResponse = userInput.value.trim();
    userInput.value = '';
  }

  if (userResponse && sessionActive.value) {
    addMessage(userResponse, 'user');
    communicateWithAssistant(userResponse);
  }
};

const startSession = () => {
  sessionActive.value = true;
  messages.value = [];
  options.value = [];
  selectedOption.value = '';
  userInput.value = '';
  timeLeft.value = sessionDuration.value * 60; // обновляем таймер
  communicateWithAssistant();
  startTimer();
};

const endSession = () => {
  sessionActive.value = false;
  addMessage('Сессия была завершена пользователем.', 'assistant');
  stopTimer(); // останавливаем таймер
};

let interval;

const updateTimer = () => {
  if (timeLeft.value > 0) {
    timeLeft.value--;
    progress.value = (timeLeft.value / (sessionDuration.value * 60)) * 100;
  } else {
    endSession(); // завершаем сессию по окончании времени
  }
};

const startTimer = () => {
  interval = setInterval(updateTimer, 1000); // обновляем каждую секунду
};

const stopTimer = () => {
  clearInterval(interval);
};

onUnmounted(() => {
  stopTimer(); // останавливаем таймер при завершении компонента
});

const timeFormat = () => {
  const minutes = Math.floor(timeLeft.value / 60);
  const seconds = timeLeft.value % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

.chat-container {
  height: 500px;
  overflow-y: auto;
  background-color: #f5f5f5;
}

.message {
  margin-bottom: 10px;
}

.message.assistant {
  text-align: left;
}

.message.user {
  text-align: right;
}

.message-content {
  display: flex;
  align-items: center;
  padding: 10px 5px;
}

.message.assistant .message-content {
  flex-direction: row;
}

.message.user .message-content {
  flex-direction: row-reverse;
}

.avatar-icon {
  font-size: 36px;
  margin: 0 10px;
}

.el-card {
  border-radius: 10px;
  padding: 10px;
  max-width: 70%;
}

.el-footer {
  padding: 20px;
}

.el-container {
  background-color: #fff;
}

.el-header,
.el-footer {
  background-color: #fff;
}

.el-button {
  width: 100%;
}

.el-main {
  overflow: hidden;
}

.el-input,
.el-input-number,
.el-radio-group {
  width: 100%;
}

.el-header {
  margin-bottom: 20px;
}
</style>
