<template>
    <div class="custom-bg">
        <div class="d-flex justify-content-end mx-3">
            <button class="btn custom-btn" @click="sortByLikes">인기순</button>
            <button class="btn custom-btn" @click="sortByDate">최신순</button>
        </div>
        <div v-if="sortedReviews.length > 0">
            <div v-for="review in sortedReviews" :key="review.id">
                <hr>
                <div class="d-flex flex-wrap align-items-start review-item">
                    <img @click="goMovieDetail(review.movie.id)" :src="`https://image.tmdb.org/t/p/w780/${review.movie.poster_path}`" alt="#" height="300" class="poster m-3">
                    <div class="review-content">
                        <h3><strong>{{ review.movie.title }}</strong></h3>
                        <p>⭐️ {{ review.rating }}</p>
                        <p>{{ review.content }}</p>
                        <p>{{ review.created_at.slice(0,10) }}</p>
                        <p>💗 {{ review.like_users.length }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted } from 'vue'
import { useProfileStore } from '@/stores/profile';
import { useRouter } from 'vue-router';

const router = useRouter()

const goMovieDetail = (movieId) => {
    router.push({ name: 'movie-detail', params: { movieId: movieId }})
}

const store = useProfileStore()
const API_URL = store.API_URL
const reviews = ref([])

const fetchReviews = async () => {
    try {
        const response = await axios.get(`${API_URL}/movies/review_list/`)
        reviews.value = response.data
        sortByLikes()
    } catch (error) {
        console.log(error)
    }
}

onMounted(fetchReviews)

const sortByDate = () => {
    reviews.value = [...reviews.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0,30)
}

const sortByLikes = () => {
    reviews.value = [...reviews.value].sort((a, b) => b.like_users.length - a.like_users.length).slice(0,30)
}

const sortedReviews = computed(() => reviews.value)
</script>

<style scoped>
.custom-btn {
    background-color: #f1824e;
    color: white;
    margin: 5px;
    margin-right: 5px;
}
.custom-btn:hover {
    font-weight: bold;
}
.review-item {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    margin-bottom: 15px; /* 리뷰들 사이의 간격 추가 */
}
.poster {
    margin-right: 15px;
}
.review-content {
    display: flex;
    flex-direction: column;
    flex: 1; /* 리뷰 내용이 이미지와 나란히 정렬되도록 합니다 */
    justify-content: center;
    margin: 50px;
}
.custom-bg {
  background-color: #333538; /* 짙은 회색 */
  color: white; /* 텍스트 흰색 */
  min-height: 100vh; /* 최소 높이 설정 */
  padding: 20px; /* 여백 설정 */
}
</style>