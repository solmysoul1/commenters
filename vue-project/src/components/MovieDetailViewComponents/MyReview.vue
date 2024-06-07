<template>
    <div v-if="!isDeleted">
      <DetailReviewUpdate
        v-if="isEditing"
        :rating="myReview.rating"
        :content="myReview.content"
        :reviewPk="myReview.id"
        @update-success="handleUpdateSuccess"
      />
      <div v-if="myReview && !isEditing" class="card w-80 mx-auto">
        <div class="card-body">
          <h3 class="card-title">내가 작성한 리뷰</h3>
          <hr>
          <p class="card-text mt-5">⭐️ {{ myReview.rating }}</p>
          <h4 class="card-text">{{ myReview.content }}</h4>
          <p class="card-text mt-3">{{ myReview.created_at.slice(0, 10) }}</p>
          <p class="card-text">💗 {{ myReview.like_users_count }}</p>
          <div class="d-flex justify-content-end">
            <button class="btn custom-btn mx-1" @click="isEditing = !isEditing">리뷰 수정</button>
            <button class="btn custom-btn mx-1" @click="showPopup = true">리뷰 삭제</button>
          </div>
        </div>
      </div>
      <ReviewDeleteConfirmModal v-if="showPopup" @confirm="handleConfirmDelete" @cancel="handleCancelDelete" />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  const props = defineProps({
    myReview: Object,
  })
  
  import DetailReviewUpdate from './DetailReviewUpdate.vue'
  import ReviewDeleteConfirmModal from './ReviewDeleteConfirmModal.vue'
  import { useProfileStore } from '@/stores/profile'
  const profileStore = useProfileStore()
  import axios from 'axios'
  
  const emit = defineEmits(['delete-success'])
  
  const isEditing = ref(false)
  const isDeleted = ref(false)
  const showPopup = ref(false)
  
  const reviewDelete = async function () {
    try {
      await axios({
        method: 'DELETE',
        url: `${profileStore.API_URL}/movies/detail/${props.myReview.id}/delete_review/`,
        headers: {
          'Authorization': `Token ${profileStore.token}`
        },
      })
      isDeleted.value = true
      emit('delete-success')
    } catch (error) {
      console.log(error)
    }
  }
  
  const handleConfirmDelete = function () {
    showPopup.value = false
    reviewDelete()
  }
  
  const handleCancelDelete = function () {
    showPopup.value = false
  }
  
  const handleUpdateSuccess = function (updatedReview) {
    Object.assign(props.myReview, updatedReview)
    isEditing.value = false
  }
  </script>
  
  <style scoped>
  .custom-btn {
    background-color: #f1824e;
    color: white;
  }
  </style>
  