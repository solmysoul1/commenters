<template>
  <form @submit.prevent="onSearch" class="input-group mb-3">
    <input ref="searchInput" @input="updateQuery" type="text" class="form-control" placeholder="제목을 입력해주세요." />
    <button class="btn btn-outline-secondary" type="submit">검색</button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useProfileStore } from '@/stores/profile';

const store = useProfileStore();
const API_URL = store.API_URL;
const query = ref('');
const movies = ref([]);
const searchInput = ref(null);

const emit = defineEmits(['search-results', 'reset-query']);

const updateQuery = (event) => {
  query.value = event.target.value;
};

const onSearch = async () => {
  if (query.value.length > 1) {
    try {
      const response = await fetch(`${API_URL}/movies/search/?q=${query.value}`);
      const data = await response.json();
      movies.value = data.results;
      emit('search-results', movies.value);
      if (searchInput.value) {
        searchInput.value.value = ''; // Directly update the input field's value
      }
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  } else {
    movies.value = [];
    emit('search-results', movies.value);
  }
};

watch(query, (newQuery) => {
  if (newQuery !== '') {
    emit('reset-query');
  }
});
</script>

<style scoped></style>
