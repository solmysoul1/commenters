<template>
  <div class='custom-bg'>
    <div class="centered">
      <DetailInfo 
        v-if="movieDetail"
        :movieDetail="movieDetail"
      />
      <DetailReviewList 
        v-if="movieDetail"
        :reviews="movieDetail.review_set"
        :title="movieDetail.title"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/movie';
import { useProfileStore } from '@/stores/profile';
import DetailInfo from '@/components/MovieDetailViewComponents/DetailInfo.vue';
import DetailReviewList from '@/components/MovieDetailViewComponents/DetailReviewList.vue';

const movieDetail = ref({});
const route = useRoute();
const movieStore = useMovieStore();
const profileStore = useProfileStore();

onMounted(() => {
  const headers = profileStore.token ? { 'Authorization': `Token ${profileStore.token}` } : {};

  axios.get(`${movieStore.API_URL}/movies/movie/${route.params.movieId}/`, { headers })
    .then((response) => {
      console.log(response.data);
      movieDetail.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>

<style scoped>
.custom-bg {
  background-color: #333538; /* 짙은 회색 */
  color: white; /* 텍스트 흰색 */
  min-height: 100vh; /* 최소 높이 설정 */
  padding: 20px; /* 여백 설정 */
}

.custom-bg h1 {
  margin-bottom: 20px; /* 제목 아래 여백 추가 */
}

.centered {
  text-align: center;
}
</style>
