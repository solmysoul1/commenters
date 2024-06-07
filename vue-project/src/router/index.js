import { createRouter, createWebHistory } from 'vue-router'
import PasswordChangeView from '@/views/PasswordChangeView.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/:movieId',
      name: 'movie-detail',
      component: () => import('../views/MovieDetailView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUpView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LogInView.vue')
    },
    {
      path: '/profile/:userId',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      children: [
        {
          path: 'update',
          name: 'update',
          component: () => import('../views/ProfileUpdateView.vue')
        },
        {
          path: 'password_change',
          name: 'password_change',
          component: () => import('../views/PasswordChangeView.vue')
        },
      ]
    },
    {
      path: '/genre/:genreId/',
      name: 'genre',
      component: () => import('../views/GenreListView.vue')
    },
    {
      path: '/profile/:userId/likelist/',
      name: 'like_list',
      component: () => import('../views/LikeMovieListView.vue'),
    },
    {
      path: '/profile/:userId/dislikelist/',
      name: 'dislike_list',
      component: () => import('../views/DislikeMovieListView.vue')
    },
    {
      path: '/profile/:userId/watchlist/',
      name: 'watch_list',
      component: () => import('../views/WatchListView.vue')
    },
    {
      path: '/reviews/ranking/',
      name: 'review-ranking',
      component: () => import('../views/ReviewListView.vue')
    }
  ]

})

export default router
