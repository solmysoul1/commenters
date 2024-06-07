<template>
    <div>
        <hr>
        <h3>{{ title }} 리뷰 목록
        </h3>
        <hr>
        <div class="flex-wrap row g-4">
            <DetailReviewItem 
            v-for="review in reviews"
            :key="review.id"
            :review="review"
            class="col-12 col-md-6 col-lg-4 custom"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useProfileStore } from '@/stores/profile';
import DetailReviewItem from './DetailReviewItem.vue';

const props = defineProps({
    reviews: Object,
    title: String
})

const store = useProfileStore()

const reviews = computed(() => {
    if (props.reviews) {
        return props.reviews.filter((review) => review.user !== store.currentUser)
    } else {
        return []
    }
})

</script>

<style scoped>
.custom {
    width: 300px
}
</style>