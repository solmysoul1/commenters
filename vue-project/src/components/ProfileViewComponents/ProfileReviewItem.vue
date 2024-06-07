<template>
    <div v-if="review">
        <div class="d-flex flex-wrap align-items-start review-item">
            <img class="poster" @click="goMovieDetail(review.movie.id)" :src="`https://image.tmdb.org/t/p/w500/${ review.movie.poster_path }`" alt="#" height="300">
            <div class="review-content">
                <h3 class="mb-3"><strong>{{ review.movie.title }}</strong></h3>
                <p>⭐️ {{ review.rating }}</p>
                <p>{{ review.content }}</p>
                <p>{{ review.created_at.slice(0,10) }}</p>
                <p>💗 {{ review.like_users_count }}</p>
                <div v-if="!isEditing">
            </div>
        </div>
    </div>
        <ProfileReviewUpdate 
            v-if="isEditing" 
            :rating="review.rating"
            :content="review.content"
            :reviewPk="review.id"
            @update-success="handleUpdateSuccess"
        />
        <div style="display: flex; gap: 10px;" class="mt-1">
            <button class="btn custom-btn" v-if="isSelf" @click="isEditing = !isEditing"> 리뷰 수정 </button>
            <button class="btn custom-btn" v-if="isSelf" @click="showPopup = true"> 리뷰 삭제 </button>
        </div>
        <hr>
        <ReviewDeleteConfirmModal v-if="showPopup" @confirm="handleConfirmDelete" @cancel="handleCancelDelete" />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import ProfileReviewUpdate from './ProfileReviewUpdate.vue'
import ReviewDeleteConfirmModal from './ReviewDeleteConfirmModal.vue';

const router = useRouter()
const props = defineProps({
    review: Object,
})

const goMovieDetail = (movieId) => {
    router.push({ name: 'movie-detail', params: { movieId: movieId }})
}

console.log(props.review.movie)
import { useMovieStore } from '@/stores/movie'
import { useProfileStore } from '@/stores/profile'

const movieStore = useMovieStore()
const profileStore = useProfileStore()
const route = useRoute()
const review = ref(props.review)

const isSelf = computed(() => {
    return profileStore.currentUser == route.params.userId ? true : false
})

const isEditing = ref(false)
const showPopup = ref(false)

console.log(props.review)

const reviewDelete = function () {
    axios({
        method: 'DELETE',
        url: `${profileStore.API_URL}/movies/detail/${props.review.id}/delete_review/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`
        },
    }).then((response) => {
        review.value = false
    }).catch((error) => {
        console.log(error)
    })
}

const handleUpdateSuccess = function (updatedReview) {
    review.value = {
        ...review.value,
        rating: updatedReview.rating,
        content: updatedReview.content,
    }
    isEditing.value = false
}

const handleConfirmDelete = function () {
    showPopup.value = false
    reviewDelete()
}

const handleCancelDelete = function () {
    showPopup.value = false
}

</script>


<style scoped>
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
.custom-btn {
    background-color: #f1824e;
    color: white;
    margin: 5px;
    margin-right: 5px;
}
</style>