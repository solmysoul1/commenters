<template>
    <div>
        <h2 class="section-title">{{ mainListText }}</h2>
        <SubCurationItem :movie="recommendList" />
        <h2 v-if="watchList.length > 0" class="section-title">{{ watchlistText }}</h2>
        <SubCurationItem :movie="watchList" />
        <h2 class="section-title">오늘의 퍼스널 컬러 ! <span :style="{ color: movieColor }">{{ textColor }}</span> 색감의
            영화 추천</h2>
        <SubCurationItem :movie="colorMovies" />
    </div>
</template>

<script setup>
import { ref, computed, watch, watchEffect } from 'vue';
import axios from 'axios';
import SubCurationItem from './SubCurationItem.vue';
import { useMovieStore } from '@/stores/movie';
import { useProfileStore } from '@/stores/profile';

const movieStore = useMovieStore();
const profileStore = useProfileStore();
const randomDate = movieStore.getRandomDate();
const hexColor = ref('');
const movieColor = ref('');
const textColor = ref('');
const API_URL = movieStore.API_URL;
const colorMovies = ref([]);
const watchList = ref([]);
const recommendList = ref([]);
const is_nickname = ref(false);

const mainListText = profileStore.currentUser ? '고객님의 팔로워 기반 추천 영화' : '인기 추천 영화'
const watchlistText = profileStore.currentUser ? '당신의 워치리스트' : '가장 많이 워치리스트에 추가된 영화들'

const mainCurationHeaders = profileStore.token
    ? { 'Authorization': `Token ${profileStore.token}` }
    : {};

axios({
    method: 'get',
    url: `${API_URL}/movies/main_recommendation/`,
    headers: mainCurationHeaders,
})
    .then((response) => {
        recommendList.value = response.data;
    })
    .catch((error) => {
        console.log(error);
    });

const getColor = function () {
    axios({
        method: 'get',
        url: `https://colors.zoodinkers.com/api?date=${randomDate}/`,
    })
        .then((response) => {
            hexColor.value = response.data.hex;
        })
        .catch((error) => {
            console.log(error);
        });
};

getColor();

const color = function (hexCode) {
    const red = parseInt(hexCode.slice(1, 3), 16);
    const green = parseInt(hexCode.slice(3, 5), 16);
    const blue = parseInt(hexCode.slice(5, 7), 16);

    if (red > 200 && green < 100 && blue < 100) {
        return "red";
    } else if (red > 200 && green > 150 && green < 200 && blue > 200) {
        return "pink";
    } else if (red > 200 && green > 200 && blue < 100) {
        return "yellow";
    } else if (red < 100 && green > 200 && blue < 100) {
        return "green";
    } else if (red > 120 && red < 240 && green < 100 && blue > 120 && blue < 240) {
        return "purple";
    } else if (red < 100 && green < 100 && blue > 200) {
        return "blue";
    } else {
        const colorDistances = {
            "red": Math.sqrt(Math.pow(red - 255, 2) + Math.pow(green - 0, 2) + Math.pow(blue - 0, 2)),
            "pink": Math.sqrt(Math.pow(red - 255, 2) + Math.pow(green - 182, 2) + Math.pow(blue - 193, 2)),
            "yellow": Math.sqrt(Math.pow(red - 255, 2) + Math.pow(green - 255, 2) + Math.pow(blue - 0, 2)),
            "green": Math.sqrt(Math.pow(red - 0, 2) + Math.pow(green - 255, 2) + Math.pow(blue - 0, 2)),
            "purple": Math.sqrt(Math.pow(red - 160, 2) + Math.pow(green - 32, 2) + Math.pow(blue - 240, 2)),
            "blue": Math.sqrt(Math.pow(red - 0, 2) + Math.pow(green - 0, 2) + Math.pow(blue - 255, 2))
        };

        let minDistance = Infinity;
        let closestColor = "";
        for (const color in colorDistances) {
            if (colorDistances[color] < minDistance) {
                minDistance = colorDistances[color];
                closestColor = color;
            }
        }
        return closestColor;
    }
};

watch(hexColor, (newValue) => {
    if (newValue) {
        movieColor.value = color(newValue);
    }
});

watch(movieColor, (newValue) => {
    if (newValue) {
        axios({
            method: 'get',
            url: `${API_URL}/movies/sub_color/${movieColor.value}/`
        })
            .then((response) => {
                colorMovies.value = response.data;
                if (movieColor.value === 'red') {
                    textColor.value = '빨간';
                } else if (movieColor.value == 'blue') {
                    textColor.value = '파란';
                } else if (movieColor.value == 'purple') {
                    textColor.value = '보라';
                } else if (movieColor.value == 'yellow') {
                    textColor.value = '노란';
                } else if (movieColor.value == 'green') {
                    textColor.value = '초록';
                } else if (movieColor.value == 'pink') {
                    textColor.value = '핑크';
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }
});



watchEffect(() => {
    if (profileStore.nickname) {
        is_nickname.value = true;
    } else {
        is_nickname.value = false;
    }
});

axios({
    method: 'get',
    url: `${API_URL}/movies/watchlist_or_recommendation/`,
    headers: mainCurationHeaders,
})
    .then((response) => {
        watchList.value = response.data;
    })
    .catch((error) => {
        console.log(error);
    });

</script>

<style scoped>
.section-title {
    background-color: #333538; 
    margin-bottom: 30px;
    /* h2 태그와 SubCurationItem 사이 간격 조절 */
    margin-top: 30px;
}
</style>
