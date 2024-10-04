import { ref } from 'vue';

const currentUser = ref(null);

export const authService = {
  login,
  logout,
  register,
  getCurrentUser,
  currentUser, // Экспортируем реактивное свойство
};

function login(username, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username && password) {
        const user = { username };
        localStorage.setItem('user', JSON.stringify(user));
        currentUser.value = user; // Обновляем реактивное свойство
        resolve(user);
      } else {
        reject('Неверные учетные данные');
      }
    }, 1000);
  });
}

function logout() {
  localStorage.removeItem('user');
  currentUser.value = null; // Обновляем реактивное свойство
}

function register(username, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username && password) {
        resolve();
      } else {
        reject('Ошибка при регистрации');
      }
    }, 1000);
  });
}

function getCurrentUser() {
  if (!currentUser.value) {
    const userData = localStorage.getItem('user');
    if (userData) {
      currentUser.value = JSON.parse(userData);
    }
  }
  return currentUser.value;
}
