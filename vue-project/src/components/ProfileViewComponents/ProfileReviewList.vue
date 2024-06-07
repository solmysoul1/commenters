<template>
    <div class="mt-3">
        <h2>{{ userNickname }}님이 작성한 리뷰</h2>
        <hr>
        <ProfileReviewItem 
        v-for="review in userReviews"
        :key="review.id"
        :review="review"
        />
    </div>
</template>

<script setup>
import ProfileReviewItem from './ProfileReviewItem.vue';
const props = defineProps({
    userReviews: Object,
    userNickname: String,
})
</script>

<style scoped>

</style>