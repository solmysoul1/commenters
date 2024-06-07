<template>
    <div v-if="movieDetail" class="container">
        <h1>{{ movieDetail.title }}</h1>
        <div>
            <img :src="backdropUrl" alt="#" width="1000">
        </div>
        <p>성인여부 : {{ movieDetail.adult }}</p>
        <p>평점 : {{ movieDetail.vote_average }}</p>
        <p>개봉일 : {{ movieDetail.release_date }}</p>
        <div>
            <span>장르 : </span>
            <span v-for="genre in movieDetail.genres">| {{ genre.name }}  |</span>
        </div>
        <p>{{ movieDetail.overview }}</p>
        <div style="display: flex gap: 10px;" class="group">
            <span>💗 {{ movieDetail.like_users_count }}</span>
            <span>❌ {{ movieDetail.dislike_users_count }}</span>
            <span>✔️ {{ movieDetail.watch_users_count }}</span>
        </div>
        <div style="display: flex; gap: 10px;" class="button-group">
          <span><button v-if="!movieDetail.is_dislike && !user_has_disliked" class="custom-btn btn mt-3" @click="handleClick(movie_like)">{{ likeText }}</button></span>
          <span><button v-if="!movieDetail.is_like && !user_has_liked" class="custom-btn btn mt-3" @click="handleClick(movie_dislike)">{{ dislikeText }}</button></span>
          <span><button class="custom-btn btn mt-3" v-if="!movieDetail.is_my_review" @click="handleClick(movie_watch)">{{ watchText }}</button></span>
          <span><button class="custom-btn btn mt-3" @click="handleClick(() => is_creating = !is_creating)" v-if="!movieDetail.is_my_review">
            {{ createText }}</button></span>
        </div>
        <div v-if="is_creating">
            <DetailReviewCreate 
            :moviePk="movieDetail.id"
            @create-success="onCreateSuccess"
            /> 
        </div>
        <MyReview 
        v-if="movieDetail.is_my_review"
        :myReview="movieDetail.my_review"
        @delete-success="onDeleteSuccess"
        />
        <LoginRequiredModal v-if="showPopup" @confirm="redirectToLogin" />
    </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie';
import { useProfileStore } from '@/stores/profile';
import MyReview from './MyReview.vue'
import DetailReviewCreate from './DetailReviewCreate.vue';
import LoginRequiredModal from './LoginRequiredModal.vue'

const profileStore = useProfileStore()
const movieStore = useMovieStore()
const user_has_liked = ref()
const user_has_disliked = ref()
const user_has_watch = ref()
const is_creating = ref(false)
const showPopup = ref(false)

const props = defineProps({
    movieDetail: Object,
})

console.log(props.movieDetail)
const handleClick = (action) => {
    if (!isAuthenticated.value) {
        showPopup.value = true
    } else {
        action()
    }
}

const redirectToLogin = () => {
    showPopup.value = false
    router.push({ name: 'login' })
}

const likeText = computed(() => {
    return user_has_liked.value ? '좋아요 취소' : '좋아요'
})

const dislikeText = computed(() => {
    return user_has_disliked.value ? '싫어요 취소' : '싫어요'
})

const watchText = computed(() => {
    return user_has_watch.value ? '워치리스트 삭제' : '워치리스트 추가'
})
const createText = computed(() => {
    return is_creating.value ? '작성 취소' : '리뷰 작성'
})

const isAuthenticated = computed(() => {
    return profileStore.isAuthenticated
})

const movie_like = function () {
    axios({
        method: 'post',
        url: `${movieStore.API_URL}/movies/detail/${props.movieDetail.id}/likelist/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`
        }
    })
    .then((response) => {
        user_has_liked.value = response.data.is_like
        if (user_has_liked.value) {
            props.movieDetail.like_users_count++
            console.log('영화 좋아요 성공!')
        } else {
            props.movieDetail.like_users_count--
            console.log('영화 좋아요 취소 성공!')
        }
    })
    .catch((error) => {
        console.log(error)
    })
}

const movie_dislike = function () {
    axios({
        method: 'post',
        url: `${movieStore.API_URL}/movies/detail/${props.movieDetail.id}/dislikelist/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`
        }
    })
    .then((response) => {
        user_has_disliked.value = response.data.is_dislike
        if (user_has_disliked.value) {
            props.movieDetail.dislike_users_count++
            console.log('영화 싫어요 성공!')
        } else {
            props.movieDetail.dislike_users_count--
            console.log('영화 싫어요 취소 성공!')
            if (user_has_watch.value) {
            props.movieDetail.is_my_review = true
            props.movieDetail.watch_users_count--
        }
        }
    })
    .catch((error) => {
        console.log(error)
})
}

const movie_watch = function () {
    axios({
        method: 'post',
        url: `${movieStore.API_URL}/movies/detail/${props.movieDetail.id}/watchlist/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`
        }
    })
    .then((response) => {
        user_has_watch.value = response.data.is_watch
        if (user_has_watch.value) {
            props.movieDetail.watch_users_count++
            console.log('영화 와치리스트 추가 성공!')
        } else {
            props.movieDetail.watch_users_count--
            console.log('영화 와치리스트 취소 성공!')
        }
    })
    .catch((error) => {
        console.log(error)
})
}

// 기존의 onMounted 로직을 watchEffect로 변경
watchEffect(() => {
    if (props.movieDetail.is_like) {
        user_has_liked.value = true
    } else {
        user_has_liked.value = false
    }

    if (props.movieDetail.is_dislike) {
        user_has_disliked.value = true
    } else {
        user_has_disliked.value = false
    }

    if (props.movieDetail.is_watch) {
        user_has_watch.value = true
    } else {
        user_has_watch.value = false
    }

})

const baseImageUrl = 'https://image.tmdb.org/t/p/w1280'
const backdropUrl = computed (() => {
    return baseImageUrl + props.movieDetail.backdrop_path
})

const tmdbId = computed(()=>{
    return props.movieDetail.tmdb_id
})

const onCreateSuccess = function (createdReview) {
    console.log(createdReview)
    props.movieDetail.my_review = createdReview
    props.movieDetail.is_my_review = true
    is_creating.value = false

    if (props.movieDetail.is_watch) {
        props.movieDetail.watch_users_count--
        user_has_watch.value = false
    }
}

const onDeleteSuccess = () => {
    props.movieDetail.is_my_review = false
    
}

</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    gap: 20px; /* 아이템 사이의 간격을 20px로 설정 */
    margin-top: 10px;
    margin-bottom: 15px;
}
.button-group {
    display: flex;
    justify-content: center;
    gap: 10px; /* 버튼 사이의 간격을 10px로 설정 */
    margin-bottom: 15px;
}
.group {
    display: flex;
    justify-content: center;
    gap: 10px;
}
.custom-btn {
    color: rgb(177, 172, 172);
}
.custom-btn:hover {
    color: #f1824e;
}
</style>