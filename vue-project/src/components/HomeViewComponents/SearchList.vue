<template>
  <div v-if="searchResults" class="content custom-bg">
    <h2 class="mt-3">검색한 영화</h2>
    <div class="movies-grid">
      <div v-for="(movie, index) in props.searchResults" :key="movie.id" class="movie">
        <div class="movie-image-container" @mouseover="showMovieDetail(index)" @mouseleave="hideMovieDetail(index)">
          <div class="blur-image" v-if="showDetails[index]"></div>
          <img :src="`https://image.tmdb.org/t/p/w780/${movie.poster_path}`" alt="#" height="400" class="mt-3" @click="handleMovieClick(movie.id)">
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
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();
const props = defineProps({
  searchResults: Array
});
console.log(props.searchResults)
const emit = defineEmits(['close']);

const showDetails = ref(Array(props.searchResults.length).fill(false));

const goMovieDetail = (movieId) => {
  router.push({ name: 'movie-detail', params: { movieId: movieId }});
};

const showMovieDetail = (index) => {
  showDetails.value[index] = true;
};

const hideMovieDetail = (index) => {
  showDetails.value[index] = false;
};

const handleMovieClick = (movieId) => {
  goMovieDetail(movieId);
  emit('close');
};
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.custom-bg {
  background-color: #333538;
  color: white;
  padding: 20px;
}
.movies-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.movie {
  position: relative;
  flex: 1 1 calc(25% - 20px); /* Adjust percentage to change number of columns */
  margin-top: 20px;
}
.movie-image-container {
  position: relative;
  width: 100%;
  cursor: pointer;
}
.custom-img-fluid {
  width: 100%;
  height: auto;
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
  z-index: 2;
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

@media (max-width: 1200px) {
  .movie {
    flex: 1 1 calc(33.333% - 20px); /* 3 columns */
  }
}
@media (max-width: 992px) {
  .movie {
    flex: 1 1 calc(50% - 20px); /* 2 columns */
  }
}
@media (max-width: 768px) {
  .movie {
    flex: 1 1 calc(100% - 20px); /* 1 column */
  }
}
</style>
