<template>
    <div class="custom-bg">
        <div v-if="userProfile.is_self">
            <a class="btn custom-btn" href="#" @click.prevent="deleteAccount">탈퇴</a>
            <RouterLink class="btn custom-btn" :to="`/profile/${route.params.userId}/update`">개인정보수정</RouterLink>
            <RouterLink class="btn custom-btn" :to="`/profile/${route.params.userId}/password_change`">비밀번호 변경</RouterLink>
        </div>
        <div>
            <RouterView />
        </div>
        <div v-if="!isEditing">
            <ProfileInfo v-if="userProfile" :userProfile="userProfile" />
            <ProfileReviewList v-if="userProfile" :userReviews="userProfile.review_set" :userNickname="userProfile.nickname" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useProfileStore } from '@/stores/profile'
import ProfileInfo from './../components/ProfileViewComponents/ProfileInfo.vue'
import ProfileReviewList from './../components/ProfileViewComponents/ProfileReviewList.vue'

const route = useRoute()
const profileStore = useProfileStore()

const userProfile = ref({})
const isAuthenticated = computed(() => profileStore.isAuthenticated)
const deleteAccount = profileStore.deleteAccount

const fetchUserProfile = () => {
    const headers = profileStore.token
        ? { 'Authorization': `Token ${profileStore.token}` }
        : {};
    
    axios({
        method: 'get',
        url: `${profileStore.API_URL}/accounts/profile/${Number(route.params.userId)}/`,
        headers: headers,
    })
        .then((response) => {
            console.log(response.data)
            userProfile.value = response.data
        })
        .catch((error) => {
            console.log(error)
        })
}

onMounted(fetchUserProfile)

// route.params.userId의 변화를 감지합니다.
watch(() => route.params.userId, (newVal, oldVal) => {
    if (newVal !== oldVal) {
        fetchUserProfile()
    }
})

// 현재 라우트가 프로필 수정 또는 비밀번호 변경 페이지인지 확인
const isEditing = computed(() => {
    return ['update', 'password_change'].includes(route.name)
})

</script>

<style scoped>
.custom-bg {
  background-color: #333538; /* 짙은 회색 */
  color: white; /* 텍스트 흰색 */
  min-height: 100vh; /* 최소 높이 설정 */
  padding: 20px; /* 여백 설정 */
}
.custom-btn {
    color: rgb(131, 127, 127);
}
.custom-btn:hover {
    color: #f1824e;
}
</style>
