<template>
    <div class="content custom-bg">
        <div class="title-container mt-5">
            <h2>좋아요한 영화</h2>
            <hr>
        </div>
        <div class="movies-container">
            <div class="movies-wrapper" :style="{ justifyContent: moviesJustifyContent }">
            <div v-for="(movie, index) in like_list" :key="movie.id" class="movie">
                <div class="movie-image-container" @click="goMovieDetail(movie.id)" @mouseover="showMovieDetail(index)" @mouseleave="hideMovieDetail(index)">
                <div class="blur-image"></div>
                <img :src="`https://image.tmdb.org/t/p/w780/${movie.poster_path}`" alt="#" height="400">
                <div v-if="showDetails[index]" class="movie-details">
                    <div class="movie-info">
                    <p class="movie-title">{{ movie.title }}</p>
                    <p class="movie-info-item">
                        <span class="movie-info-value"><span style="color:red;">⭐️</span>{{ movie.vote_average }}</span>
                    </p>
                    <p class="movie-info-item">
                        <span class="movie-info-value">{{ movie.runtime }}분</span>
                    </p>
                    <p class="movie-info-item">
                        <span class="movie-info-value">{{ movie.release_date }}</span>
                    </p>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useProfileStore } from "@/stores/profile";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { ref, computed } from "vue";

const store = useProfileStore();
const route = useRoute();
const router = useRouter();
const API_URL = store.API_URL;
const userId = route.params.userId;
const like_list = ref([]);
const showDetails = ref(Array(like_list.value.length).fill(false));

axios({
  method: "get",
  url: `${API_URL}/accounts/profile/${userId}/likelist/`,
  headers: {
    Authorization: `Token ${store.token}`,
  },
})
  .then((response) => {
    like_list.value = response.data;
    console.log("좋아요한 영화 받아오기 성공!");
  })
  .catch((error) => {
    console.log(error);
  });

const goMovieDetail = (movieId) => {
  router.push({ name: "movie-detail", params: { movieId: movieId } });
};

const showMovieDetail = (index) => {
    showDetails.value[index] = true;
};

const hideMovieDetail = (index) => {
    showDetails.value[index] = false;
};
const moviesJustifyContent = computed(() => {
  return like_list.value.length <= 4 ? 'flex-start' : 'center'; // 영화 개수에 따라 중앙 정렬이나 왼쪽 정렬 결정
});
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10%;
}
.custom-bg {
  background-color: #333538;  
  color: white; 
  min-height: 100vh; 
  padding: 20px; 
}
.title-container {
  text-align: center;
  margin-bottom: 20px; /* 제목과 영화 목록 사이의 간격 */
}
.movies-container {
  position: relative;
  overflow: hidden;
  margin: 5%
}
.movies-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; /* 영화 간의 간격을 설정 */
  transition: transform 0.5s ease;
}

.movie {
  flex: 0 0 auto;
  margin-right: 10px; /* 수정된 부분: 영화 사이의 우측 간격 조절 */
}
.movie-image-container {
  position: relative;
  cursor: pointer;
}
.blur-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  filter: blur(5px);
  z-index: -1;
}
.movie-details {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 10px;
  box-sizing: border-box;
  color: white;
  opacity: 0;
  transition: opacity 0.3s;
}

.movie-image-container:hover .movie-details {
  opacity: 1;
  cursor: pointer;
}

.movie-info {
  text-align: left;
}

.movie-info-item {
  margin-bottom: 5px;
}

.movie-info-label {
  font-weight: bold;
}
</style>
