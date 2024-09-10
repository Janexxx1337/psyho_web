import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

// Импортируем все иконки Element Plus
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

const app = createApp(App);

app.use(router);
app.use(ElementPlus);

// Регистрируем все иконки как глобальные компоненты
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}

app.mount('#app');
