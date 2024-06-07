import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'


export const useMovieStore = defineStore('movie', () => { 

  const API_URL = 'http://127.0.0.1:8000/api/v1'
  const token = ref(null)
  const user = ref(null)
  const router = useRouter()

  const fetchMovieDetail = function (movieId){
    const movieDetail = ref(null)
    axios({
      method: 'get',
      url: `https://api.themoviedb.org/3/movie/${movieId}?language=ko-KR`,
      headers: {
      'accept': 'application/json',
      'Authorization': import.meta.env.VITE_TMDB_ACCESS_TOKEN,
      },
    })
    .then((response)=>{
      movieDetail.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
    return movieDetail
  }

  // colorAPI 사용을 위해 랜덤 날짜 받아오는 함수
  const getRandomDate = function () {
    const year = Math.floor(Math.random() * (new Date().getFullYear() - 1900 + 1)) + 1900
    const month = Math.floor(Math.random() * 12) + 1
    const maxDayPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    let maxDays = maxDayPerMonth[month - 1]
    if (month === 2 && ((year % 4 === 0 && year & 100 !== 0) || year % 400 === 0)){
      maxDays = 29
    }
    const day = Math.floor(Math.random() * maxDays) + 1
    const formatteDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`

    return formatteDate
  } 
  
  return { API_URL, fetchMovieDetail, getRandomDate }
  
}) 
