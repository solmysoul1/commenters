<template>
    <div class="popup-overlay">
        <div class="popup-content">
            <p>로그인 해주세요!</p>
            <button class="btn custom-btn" @click="goToLogin">확인</button>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
    router.push({ name: 'login' })
}

</script>

<style scoped>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup-content {
    background: #000000;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
    color: #f1824e;
    font-weight: bolder;
    font-size: 1.2rem ;
}
.custom-btn {
    color: rgb(209, 201, 201);
}
.custom-btn:hover {
    color: #f1824e;
}
</style>
