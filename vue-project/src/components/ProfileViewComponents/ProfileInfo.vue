<template>
    <div class="profile-container mb-2 mt-2">
        <h2>{{ userProfile.nickname }}</h2>
        <span>팔로워 : {{ userProfile.followers_count }}</span>
        <span v-if="!userProfile.is_self">
            <button class="btn custom-btn" @click="followBtn(userProfile.id)">
                {{ followText }}
            </button>
        </span>
        <p>팔로잉 : {{ userProfile.followings_count }}</p>
        <div class="links-container">
            <RouterLink class="btn custom-btn" :to="{ name: 'like_list', params : { 'userId': props.userProfile.id }}">좋아요한 영화</RouterLink>
            <RouterLink class="btn custom-btn" :to="{ name: 'dislike_list', params : { 'userId': props.userProfile.id }}">싫어요한 영화</RouterLink>
            <RouterLink class="btn custom-btn" :to="{ name: 'watch_list', params : { 'userId': props.userProfile.id } }">워치리스트</RouterLink>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios'
import { ref, watch, computed } from 'vue'
import { useProfileStore } from '@/stores/profile';
import { RouterLink } from 'vue-router';

const store = useProfileStore()
const API_URL = store.API_URL

const props = defineProps({
    userProfile: Object,
})

// userProfile을 반응형으로 만듦
const userProfile = ref({ ...props.userProfile })

const followText = computed(() => {
    return userProfile.value.is_following ? '팔로우 취소' : '팔로우';
})

const followBtn = function(userId){
    axios({
        method: 'post',
        url: `${API_URL}/accounts/${userId}/follow/`,
        headers: {
            'Authorization': `Token ${store.token}`
        }
    })
    .then((response) => {
        console.log(response.data)
        userProfile.value.followers_count = response.data.followers_count
        userProfile.value.is_following = response.data.is_following // 서버에서 is_following 정보를 받아와서 업데이트
        console.log('팔로우 기능 실행 성공!')
    })
    .catch((error) => {
        console.log(error)
        console.log(store.token)
    })
}


// userProfile이 변경될 때마다 업데이트
watch(() => props.userProfile, (newVal) => {
    userProfile.value = { ...newVal }
}, { immediate: true })

</script>

<style scoped>
.profile-container {
    display: flex;
    flex-direction: column;
    gap: 10px; /* 요소들 사이에 10px 간격을 추가 */
}
.links-container {
    display: flex;
    gap: 10px; /* 링크들 사이에 10px 간격을 추가 */
}

.custom-btn {
    background-color: #f1824e;
    color: white;
}
.custom-btn:hover {
    font-weight: bold;
}
</style>