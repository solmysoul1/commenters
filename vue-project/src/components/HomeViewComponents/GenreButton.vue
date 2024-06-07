<template >
    <div class="custom-container">
        <div v-for="genre in props.genres">
            <RouterLink :class="'custom-link'" :to="{ name: 'genre', params: { 'genreId': genre.id } }">
                {{ genre.name }}
            </RouterLink>
        </div>
    </div>  
</template>

<script setup>
import { RouterLink } from 'vue-router';

const props = defineProps({
    genres:Object
})

</script>

<style scoped>
.custom-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: auto;
    margin-bottom: 30px;
    margin-right: auto; /* 좌측 정렬 */
    margin-left: auto; /* 우측 정렬 */
}
.custom-link {
    display: inline-block;
    color: #f1824e;
    text-decoration: none;
    padding: 10px;
    border: 1px solid #f1824e;
    border-radius: 5px;
    transition: background-color 0.3s;
    margin: 5px;
}

.custom-link:hover {
    background-color: rgb(233, 195, 137);
    color: black;
}

</style>