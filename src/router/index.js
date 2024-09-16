// router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import FormPage from '../views/forms/FormPage.vue';
import RecommendationsPage from '../views/recommendations/RecommendationsPage.vue';
import History from '@/views/history/History.vue';
import SessionDetails from '../views/history/SessionDetails.vue';
import Login from '@/views/user/Login.vue';
import Register from '@/views/user/Register.vue';
import UserProfile from '../views/user/UserProfile.vue';
import MoodDiary from "@/views/mood/MoodDiary.vue";
import LogicPage from '@/views/tests/LogicPage.vue';
import { authService } from '@/services/authService';

const routes = [
    {
        path: '/',
        name: 'FormPage',
        component: FormPage,
        meta: { requiresAuth: true },
    },
    {
        path: '/Logic',
        name: 'LogicPage',
        component: LogicPage,
        meta: { requiresAuth: true },
    },
    {
        path: '/recommendations',
        name: 'RecommendationsPage',
        component: RecommendationsPage,
        props: route => ({ recommendations: route.params.recommendations }),
        meta: { requiresAuth: true },
    },
    {
        path: '/history',
        name: 'History',
        component: History,
        meta: { requiresAuth: true },
    },
    {
        path: '/session/:session_id',
        name: 'SessionDetails',
        component: SessionDetails,
        props: true,
        meta: { requiresAuth: true },
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
        path: '/mood-diary',
        name: 'MoodDiary',
        component: MoodDiary,
        meta: { requiresAuth: true },
    },
    {
        path: '/profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Навигационный охранник
router.beforeEach((to, from, next) => {
    const currentUser = authService.getCurrentUser(); // Проверяем текущего пользователя через authService

    if (to.meta.requiresAuth && !currentUser) {
        next({ path: '/login', query: { redirect: to.fullPath } }); // Перенаправляем на страницу входа с сохранением целевого пути
    } else {
        next(); // Продолжаем навигацию
    }
});

export default router;
