<template>
    <div class="custom-bg">
        <h1>회원가입</h1>
        <form @submit.prevent="signUp">
            <div>
                <label for="username">username : </label>
                <input type="text" v-model.trim="username" id="username">
            </div>
            <div>
                <label for="nickname">nickname : </label>
                <input type="text" v-model.trim="nickname" id="nickname">
            </div>
            <div>
                <label for="email">email : </label>
                <input type="email" v-model.trim="email" id="email">
            </div>
            <div>
                <label for="password1">password : </label>
                <input type="password" v-model.trim="password1" id="password1">
            </div>
            <div>
                <label for="password2">password confirmation : </label>
                <input type="password" v-model.trim="password2" id="password2">
            </div>
            <input type="submit">
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProfileStore } from '@/stores/profile'
const store = useProfileStore()

const username = ref('')
const nickname = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')

const signUp = function () {
    console.log(nickname.value)
    const payload = {
        username: username.value,
        nickname: nickname.value,
        email: email.value,
        password1: password1.value,
        password2: password2.value,
    }
    store.signUp(payload)
}

</script>

<style scoped>

</style>