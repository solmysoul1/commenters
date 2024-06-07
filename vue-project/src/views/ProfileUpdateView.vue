<template>
    <div class="custom-bg">
        <h1>Profile Update</h1>
        <form v-if="currentUserInfo" @submit.prevent="profileUpdate">
            <div>
                <label for="nickname">Nickname : </label>
                <input type="text" :placeholder="currentUserInfo.nickname" v-model="nickname" />
            </div>
            <div>
                <label for="email">Email : </label>
                <input type="email" :placeholder="currentUserInfo.email" v-model="email" />
            </div>
            <button type="submit">Profile Update</button>
        </form>
        <div v-else>
            <p>Loading...</p>
        </div>
    </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profile'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const profileStore = useProfileStore()
const API_URL = profileStore.API_URL
const nickname = ref('')
const email = ref('')
const currentUserInfo = ref(null)

onMounted(() => {
    axios({
        method: 'get',
        url: `${profileStore.API_URL}/accounts/user/`,
        headers: {
            'Authorization': `Token ${profileStore.token}`
        },
    })
        .then((response) => {
            currentUserInfo.value = response.data
        })
        .catch((error) => {
            console.log(error)
        })
})

const profileUpdate = function () {
    const userId = profileStore.currentUser
    const token = profileStore.token

    axios({
        method: 'put',
        url: `${API_URL}/accounts/${userId}/update/`,
        headers: {
            'Authorization': `Token ${token}`
        },
        data: {
            nickname: nickname.value,
            email: email.value
        }
    })
        .then((response) => {
            currentUserInfo.value = response.data
            console.log('프로필 수정 성공!')
        })
        .catch((error) => {
            console.log(error)
        })
}

// 유저확인용
console.log(profileStore.currentUser)

</script>

<style scoped></style>
