import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useProfileStore = defineStore('profile', () => {
    
    const API_URL = 'http://127.0.0.1:8000/api/v1'
    const token = ref(null)
    const currentUser = ref(null)
    const router = useRouter()
    const isAuthenticated = ref(false)
    const nickname = ref(null)

    const signUp = function (payload) {
        const username = payload.username
        const nickname = payload.nickname
        const email = payload.email
        const password1 = payload.password1
        const password2 = payload.password2
        axios({
          method: 'post',
          url: `${API_URL}/accounts/signup/`,
          data: {
            username: username,
            nickname: nickname,
            email: email,
            password1: password1,
            password2: password2
          }
        })
        .then((response) => {
            console.log(response)
            console.log('회원가입 성공!')
            const password = password1
            logIn({ username, password })
        })
        .catch((error) => {
          console.log(error)
        })
    }
    
    const logIn = function (payload) {
        const { username, password } = payload
        axios({
            method: 'post',
            url: `${API_URL}/accounts/login/`,
            data: {
            username, password
            }
        })
        .then((response) => {
            console.log(response.data)
            token.value = response.data.key
            axios({
                method:'get',
                url: `${API_URL}/accounts/user/`,
                headers: {
                    'Authorization': `Token ${response.data.key}`
                }
            })
            .then((userResponse) => {
                nickname.value = userResponse.data.nickname
                currentUser.value = userResponse.data.id
                isAuthenticated.value = true
                console.log(currentUser.value)
                router.push({ name: 'home' })
            })
        })
        .catch((error) => {
            console.log(error)
        })
        .catch((error) => {
            console.log(error)
        })

    }

    const logOut = () => {
        token.value = null
        currentUser.value = null
        isAuthenticated.value = false
        router.push({ name: 'login' })
    }

    const deleteAccount = function() {
        axios({
            method: 'post',
            url: `${API_URL}/accounts/delete/`,
            headers: {
            'Authorization': `Token ${token.value}`
            }
        })
        .then((response) => {
            console.log(response)
            console.log('회원 탈퇴 성공!')
            token.value = null
            isAuthenticated.value = false
            currentUser.value = null
            router.push({ name: 'signup' })
        })
        .catch((error) => {
            console.log(error)
        })
    }

    return { signUp, API_URL, logIn, logOut, deleteAccount, token, isAuthenticated, currentUser }
}, { persist: true })