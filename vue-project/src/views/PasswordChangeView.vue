<template>
    <div class="custom-bg">
        <h1>Change Password</h1>
        <form @submit.prevent="changePassword">
        <div>
            <label for="old_password">Old Password:</label>
            <input type="password" v-model="form.old_password" required />
        </div>
        <div>
            <label for="new_password1">New Password:</label>
            <input type="password" v-model="form.new_password1" required />
        </div>
        <div>
            <label for="new_password2">Confirm New Password:</label>
            <input type="password" v-model="form.new_password2" required />
        </div>
        <button type="submit">Change Password</button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">{{ success }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useProfileStore } from '@/stores/profile'
import router from '@/router';
const store = useProfileStore()
const API_URL = store.API_URL

const form = ref({
    old_password: '',
    new_password1: '',
    new_password2: ''
})
const error = ref(null)
const success = ref(null)

const changePassword = function () {
    error.value = null
    success.value = null

    if (!store.currentUser) {
        error.value = 'User not logged in'
        return 
    } 

    axios({
        method: 'post',
        url: `${API_URL}/accounts/${store.currentUser}/password/change/`,
        headers: {
        'Authorization': `Token ${store.token}`
        },
        data: form.value
    })
    .then((response) => {
        success.value = response.data.message
        console.log('비밀번호 변경 성공!')
        router.push({ name: 'home'})
    })
    .catch((error) => {
        console.log(error)
        error.value = error.response.data
    })
}

</script>

<style scoped>

</style>