// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import FormPage from '../components/FormPage.vue';
import RecommendationsPage from '../components/RecommendationsPage.vue';
import History from '../components/History.vue';
import SessionDetails from '../components/SessionDetails.vue';

const routes = [
    {
        path: '/',
        name: 'FormPage',
        component: FormPage
    },
    {
        path: '/recommendations',
        name: 'RecommendationsPage',
        component: RecommendationsPage,
        props: route => ({ recommendations: route.params.recommendations })
    },
    {
        path: '/history',
        name: 'History',
        component: History
    },
    {
        path: '/session/:session_id',
        name: 'SessionDetails', // Имя маршрута должно совпадать
        component: SessionDetails,
        props: true // Пропсы передаются из URL параметров
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
