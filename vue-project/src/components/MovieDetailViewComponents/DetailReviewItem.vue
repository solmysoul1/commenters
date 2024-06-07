<template>
    <div class="container d-flex justify-content-center">
        <div class="row">
            <div class="d-flex">
                <div class="card mt-3 custom-card">
                    <div class="card-body text-left">
                        <router-link 
                            :to="{ name:'profile', params: { userId: review.user } }"
                            class="router-link-custom">
                            <p class="card-text" style="margin-bottom: 5px;"><strong>{{ review.user_nickname }}</strong></p>
                        </router-link>
                        <p class="card-text">⭐ {{ review.rating }}</p>
                        <h5 class="card-text">{{ review.content }}</h5>
                        <p class="card-text">{{ review.created_at.slice(0,10) }}</p>
                        <p class="card-text">💗 {{ review.like_users_count }}</p>
                    </div>
                    <div class="card-footer d-flex justify-content-end">
                        <button class="btn custom-btn" v-if="profileStore.isAuthenticated" @click="review_like">
                            {{ likeText }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie';
import { useProfileStore } from '@/stores/profile';

const profileStore = useProfileStore()
const movieStore = useMovieStore()
const user_has_liked = ref()

const props = defineProps({
    review: Object,
})


const likeText = computed(() => {
    return user_has_liked.value ? '좋아요 취소' : '좋아요'
})

const review_like = function () {
    axios({
        method: 'post',
        url: `${movieStore.API_URL}/movies/review/${props.review.id}/like/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`
        }
    })
    .then((response) => {
        if (response.data.success) {
            user_has_liked.value = response.data.is_like
            if (user_has_liked.value) {
                props.review.like_users_count++
                console.log('리뷰 좋아요 성공!')
            } else {
                props.review.like_users_count--
                console.log('리뷰 좋아요 취소 성공!')
            }
        }
    })
    .catch((error) => {
        console.log(error)
    })
}

onMounted(() => {
    if (props.review.is_like) {
        user_has_liked.value = true
    } else {
        user_has_liked.value = false
    }
})

</script>

<style scoped>
.container {
  padding-top: 20px; /* 상단 여백 설정 */
  text-align: left;
}
.custom-card {
  width: 100%; /* 카드의 너비를 조절합니다. 필요에 따라 조절하세요. */
  margin: 0 auto; /* 가운데 정렬을 위해 margin을 auto로 설정합니다. */
}
.router-link-custom {
  text-decoration: none; /* 밑줄 제거 */
  color: inherit; /* 기본 링크 색상 유지 */
}
.custom-btn {
    background-color: #f1824e;
    color: white;
}
</style>