<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/"><img @click="closeSearchList" src="@/assets/image.png" alt="" height="50"></router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'review-ranking' }">Review Ranking</router-link>
            </li>
          </ul>
          <ul class="navbar-nav mt-2">
            <li class="nav-item mx-2">
              <SearchComponent @search-results="getSearchResults"/>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link class="nav-link" :to="{ name: 'login' }">LogIn</router-link>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link class="nav-link" :to="{ name: 'signup' }">SignUp</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <a class="nav-link" href="#" @click.prevent="logOut">LogOut</a>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" :to="{ name: 'profile', params: { userId: currentUserId } }">My
                Page</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div style="padding-top: 70px;"></div>
      <SearchList 
      v-if="searchResults"
      :searchResults="searchResults"
      @close="closeSearchList"
      />
  </header>

  <router-view />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useProfileStore } from './stores/profile'
import { ref, computed } from 'vue'
import SearchComponent from './components/HomeViewComponents/SearchComponent.vue';
import SearchList from './components/HomeViewComponents/SearchList.vue';

const store = useProfileStore()
const isAuthenticated = computed(() => store.isAuthenticated)
const logOut = store.logOut
const currentUserId = computed(() => store.currentUser)

const searchResults = ref(null)

const getSearchResults = function(movies){
  searchResults.value = movies
}

const closeSearchList = () => {
  searchResults.value = null;
};

</script>

<style scoped>
.container-fluid {
  display: flex;
  align-items: center;
  /* 요소들을 수직 중앙 정렬 */
}
.custom-btn {
    background-color: #f1824e;
    color: white;
    margin: 5px;
    margin-right: 5px;
}

/* Mouseover 시 텍스트 색상 변경 */
:deep(.navbar-nav .nav-link:hover) {
  color: #f1824e !important;
}
.custom-bg {
  background-color: #333538;
  /* 짙은 회색 */
  color: white;
  /* 텍스트 흰색 */
}
</style>
