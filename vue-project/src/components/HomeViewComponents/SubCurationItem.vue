<template>
  <div class="content">
    <div class="movies-container">
      <div class="movies-wrapper" :style="{ transform: `translateX(${slideIndex * slideWidth}px)`, justifyContent: moviesJustifyContent }">
        <div v-for="(movie, index) in limitedmovies" :key="movie.id" class="movie">
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
      <button class="prev-button" @click="prevSlide">&lt;</button>
      <button class="next-button" @click="nextSlide">&gt;</button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const props = defineProps({
  movie: Array
})

const limitedmovies = computed(() => props.movie.slice(0, 8))
const showDetails = ref(Array(limitedmovies.value.length).fill(false));
const slideIndex = ref(0);
const slideWidth = 350; // 수정된 부분: 각 슬라이드의 너비를 더 크게 조정

const goMovieDetail = (movieId) => {
    router.push({ name: 'movie-detail', params: { movieId: movieId } })
}

const showMovieDetail = (index) => {
  showDetails.value[index] = true;
};

const hideMovieDetail = (index) => {
  showDetails.value[index] = false;
};

const prevSlide = () => {
  if (slideIndex.value === 2) {
    slideIndex.value = -2; // 마지막에 도달했을 때 처음 슬라이드로 이동
  } else {
    slideIndex.value ++; // 이전 슬라이드로 이동
  }
};

const nextSlide = () => {
  if (slideIndex.value === -2) {
    slideIndex.value = 2; // 처음에 도달했을 때 마지막 슬라이드로 이동
  } else {
    slideIndex.value --; // 다음 슬라이드로 이동
  }
};

const moviesJustifyContent = computed(() => {
  return limitedmovies.value.length <= 4 ? 'flex-start' : 'center'; // 영화 개수에 따라 중앙 정렬이나 왼쪽 정렬 결정
});
console.log(slideIndex.value)
</script>

<style scoped>
.content {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.movies-container {
  position: relative;
  overflow: hidden;
}

.movies-wrapper {
  display: flex;
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

.prev-button,
.next-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  z-index: 1;
}

.prev-button {
  left: 10px;
}

.next-button {
  right: 10px;
}
</style>
