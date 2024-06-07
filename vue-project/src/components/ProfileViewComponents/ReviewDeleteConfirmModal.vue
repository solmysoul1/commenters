<template>
    <div class="popup-overlay">
        <div class="popup-content">
            <p>당신의 소중한 리뷰, 정말 삭제하시겠습니까?</p>
            <button class="btn custom-btn" @click="confirmDelete">확인</button>
            <button class="btn custom-btn" @click="cancelDelete">취소</button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps(['show'])
const emit = defineEmits(['confirm', 'cancel'])

const confirmDelete = () => {
    emit('confirm')
}

const cancelDelete = () => {
    emit('cancel')
}
</script>

<style scoped>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup-content {
    background: black;
    color: #f1824e;
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