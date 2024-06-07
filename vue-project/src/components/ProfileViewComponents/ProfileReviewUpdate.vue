<template>
    <div class="custom-container mt-2 mb-4">
        <div class="row">
            <div class="col-md-6">
                <form @submit.prevent="reviewUpdate" class="form-group">
                    <div class="mb-3 d-flex align-items-center">
                        <label for="rating" class="form-label me-2">⭐️</label>
                        <input type="number" v-model.number="ratingValue" id="rating" min="1" max="10" class="form-control form-control-sm w-auto">
                    </div>
                    <div class="mb-3">
                        <textarea v-model.trim="contentValue" id="content" class="form-control review-content"></textarea>
                    </div>
                    <button class="btn custom-btn" type="submit">수정 완료</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProfileStore } from '@/stores/profile'
import axios from 'axios'

const props = defineProps({
    rating: Number,
    content: String,
    reviewPk: Number,
})

const profileStore = useProfileStore()

// ref를 사용해 rating과 content를 관리합니다.
const ratingValue = ref(props.rating)
const contentValue = ref(props.content)

// 부모 컴포넌트로 이벤트를 전달하기 위해 defineEmits를 사용합니다.
// 여기서는 'update-success' 이벤트를 정의하고 있습니다.
const emit = defineEmits(['update-success'])

const reviewUpdate = async function () {
    axios({
        method: 'post',
        url: `${profileStore.API_URL}/movies/detail/${props.reviewPk}/update_review/`,
        headers: {
            Authorization: `Token ${profileStore.token}`,
        },
        data: {
            rating: ratingValue.value,
            content: contentValue.value,
        },

    }).then((response)=>{
        const updatedReview = response.data
        // 응답 데이터를 부모 컴포넌트로 전송하기 위해 'update-success' 이벤트를 트리거합니다.
        emit('update-success', updatedReview)
    }).catch((error)=>{
        console.log(error)
    })
}
</script>


<style scoped>
.custom-container {
    padding-left: 5px; /* 왼쪽 여백 제거 */
}
.review-content {
    height: 100px;
}
.custom-btn {
    background-color: #ffffff;
    color: #f1824e;
}
.custom-btn:hover {
    background-color: #f1824e;
    color: #ffffff;
}
</style>
