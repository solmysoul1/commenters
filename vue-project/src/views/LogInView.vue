<template>
    <div class="custom-bg">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="text-center mb-4">로그인</h1>
                    <form @submit.prevent="logIn">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" v-model.trim="username" id="username" class="form-control">
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" v-model.trim="password" id="password" class="form-control">
                        </div>
                        <div class="d-flex justify-content-center">
                            <button type="submit" class="btn custom-btn">로그인</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProfileStore } from '@/stores/profile'
const store = useProfileStore()

const username = ref('')
const password = ref('')

const logIn = function () {
    const payload = {
        username: username.value,
        password: password.value
    }
    store.logIn(payload)
}

</script>

<style scoped>
.custom-bg {
    background-color: #333538;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.custom-btn {
    background-color: #f1824e;
    color: white;
    margin: 5px;
    margin-right: 5px;
}
</style>