<template>
    <div class="custom-container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-12">
                <h3 class="text-center mb-4">리뷰 작성</h3>
                <form @submit.prevent="submitReview" class="custom-form-group">
                    <div class="mb-4 d-flex align-items-center justify-content-center">
                        <label for="rating" class="form-label me-3 fs-5">⭐️</label>
                        <input type="number" v-model.number="rating" id="rating" min="1" max="10" class="form-control form-control-lg w-100">
                    </div>
                    <div class="mb-4" style="width: 70%;">
                        <textarea v-model.trim="content" id="content" class="form-control review-content w-100"></textarea>
                    </div>
                    <div class="d-flex justify-content-center">
                        <button class="btn custom-btn btn-lg w-100" type="submit">리뷰 등록</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
const props = defineProps({
    moviePk: Number,
});
import { useMovieStore } from '@/stores/movie';
import { useProfileStore } from '@/stores/profile';
const movieStore = useMovieStore();
const profileStore = useProfileStore();

const rating = ref(1);  // 초기값을 1로 설정
const content = ref('');
const emit = defineEmits(['create-success']);

const submitReview = () => {
    axios({
        method: 'post',
        url: `${movieStore.API_URL}/movies/detail/${props.moviePk}/create_review/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`,
        },
        data: {
            rating: rating.value,
            content: content.value,
        },
    }).then((response) => {
        console.log(response.data);
        const createdReview = response.data;
        emit('create-success', createdReview);
    }).catch((error) => {
        console.log(error);
    });
};
</script>

<style scoped>
.custom-container {
    padding: 0%;
}
.custom-form-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}
.review-content {
    height: 150px;
    font-size: 1.2rem;
}
.custom-btn {
    background-color: #ffffff;
    color: #f1824e;
}
.custom-btn:hover {
    background-color: #f1824e;
    color: #ffffff;
}
</style>
