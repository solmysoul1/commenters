<template>
  <div class='custom-bg'>
    <MainCuration />
    <GenreButton 
    :genres="genres"
    />
    <SubCurationList/>
  </div>
</template>

<script setup>
import MainCuration from '../components/HomeViewComponents/MainCuration.vue'
import GenreButton from '../components/HomeViewComponents/GenreButton.vue'
import SubCurationList from '../components/HomeViewComponents/SubCurationList.vue'
import axios from 'axios'
import { ref } from 'vue'

import { useProfileStore } from '@/stores/profile'

const profileStore = useProfileStore()
const movies = ref([])
const genres = ref([])
const searchResults = ref([])

axios({
  url: 'http://127.0.0.1:8000/api/v1/movies/movie_list/',
  method: 'get',
})
.then((response)=>{
  movies.value = response.data
})
.catch((error) => {
  console.log(error)
})

axios({
  method: 'get',
  url: 'http://127.0.0.1:8000/api/v1/movies/genre_list/'
})
.then((response) => {
  genres.value = response.data
})
.catch((error) => {
  console.log(error)
})

</script>

<style scoped>
.container {
    display: flex;
    flex-direction: row;
    gap: 10px; /* 버튼 사이 간격 */
    justify-content: center;
    flex-wrap: wrap;
    overflow-x: auto; /* 공간이 부족할 때 가로 스크롤 */
}
.custom-bg {
  background-color: #333538;
  /* 짙은 회색 */
  color: white;
  /* 텍스트 흰색 */
  min-height: 100vh;
  /* 최소 높이 설정 */
  padding: 20px;
  /* 여백 설정 */
}

.custom-btn {
    background-color: #f1824e;
    color: white;
    margin: 5px;
    margin-right: 5px;
}

</style>