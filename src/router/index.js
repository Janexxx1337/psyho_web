// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import FormPage from '../views/forms/FormPage.vue';
import RecommendationsPage from '../views/recommendations/RecommendationsPage.vue';
import History from '@/views/history/History.vue';
import SessionDetails from '../views/history/SessionDetails.vue';
import Login from '@/views/user/Login.vue';
import Register from '@/views/user/Register.vue';
import UserProfile from '../views/user/UserProfile.vue';

const routes = [
    {
        path: '/',
        name: 'FormPage',
        component: FormPage,
    },
    {
        path: '/recommendations',
        name: 'RecommendationsPage',
        component: RecommendationsPage,
        props: route => ({ recommendations: route.params.recommendations }),
        meta: { requiresAuth: true }, // Требуется авторизация
    },
    {
        path: '/history',
        name: 'History',
        component: History,
        meta: { requiresAuth: true }, // Требуется авторизация
    },
    {
        path: '/session/:session_id',
        name: 'SessionDetails',
        component: SessionDetails,
        props: true,
        meta: { requiresAuth: true }, // Требуется авторизация
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
    },
    {
        path: '/profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { requiresAuth: true }, // Требуется авторизация
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Навигационный охранник
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('user'); // Проверяем наличие пользователя
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login'); // Перенаправляем на страницу входа
    } else {
        next(); // Продолжаем навигацию
    }
});

export default router;
