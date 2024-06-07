<template>
    <div class="custom-bg">
        <h1 class="text-center pt-3 mb-3">{{ genreName }}</h1>
        <div class="d-flex justify-content-end container">
            <button class="btn custom-btn mx-2" @click="sortByLikes">인기순</button>
            <button class="btn custom-btn mx-2" @click="sortByDate">최신순</button>
        </div>
        <div class="content">
            <div v-for="(movie, index) in sortedMovies" :key="movie.id" class="movie">
              <div class="movie-image-container" @click="goMovieDetail(movie.id)" @mouseover="showMovieDetail(index)" @mouseleave="hideMovieDetail(index)">
                <div class="blur-image"></div>
                <img class="img-fluid custom-img-fluid" :src="`https://image.tmdb.org/t/p/w780/${movie.poster_path}`" alt="#" >
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
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted, computed } from 'vue'
import axios from 'axios';
import { useMovieStore } from '@/stores/movie';


const store = useMovieStore()
const route = useRoute()
const router = useRouter()
const movies = ref([])
const genreName = ref()

const sortedMovies = computed(() => movies.value)

const fetchMovies = async () => {
    try {
        const response = await axios.get(`${store.API_URL}/movies/genre/${route.params.genreId}/`)
        genreName.value = response.data.genre
        movies.value = response.data.movies
        sortByLikes()
    } catch (error) {
        console.log(error)
    }
}

onMounted(fetchMovies)

const showDetails = ref(Array(sortedMovies.value.length).fill(false));

const showMovieDetail = (index) => {
    showDetails.value[index] = true;
};

const hideMovieDetail = (index) => {
    showDetails.value[index] = false;
};

const goMovieDetail = (movieId) => {
    router.push({ name: 'movie-detail', params: { movieId: movieId }})
}

const sortByLikes = () => {
    movies.value = [...movies.value].sort((a, b) => b.like_users.length - a.like_users.length)
}

const sortByDate = () => {
    movies.value = [...movies.value].sort((a, b) => new Date(b.release_date) - new Date(a.release_date))
}



</script>

<style scoped>
.content {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 5%;
}
.movie {
  flex: 0 0 auto;
  margin-right: 10px; /* 수정된 부분: 영화 사이의 우측 간격 조절 */
}

.movies-container {
  position: relative;
  overflow: hidden;
}
.movie-image-container {
  position: relative;
  cursor: pointer;
}

.custom-img-fluid {
  max-width: 300px; /* 최대 너비 설정 */
  height: auto; /* 높이 자동 조정 */
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
.custom-btn {
    background-color: #f1824e;
    color: rgb(255, 255, 255);
}
.custom-btn:hover {
    font-weight: bold;
}
.button-container {
    margin-right: 20%;
}
</style>