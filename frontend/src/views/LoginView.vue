<template>
  <div class="max-w-md mx-auto mt-16 p-8 border-2 border-black">
    <h2 class="text-3xl font-black mb-6">Вход</h2>
    
    <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
      <input 
        v-model="username" 
        type="text" 
        placeholder="Имя пользователя или email" 
        class="border-2 border-black p-3 w-full outline-none focus:bg-gray-50"
        required
      />
      <input 
        v-model="password" 
        type="password" 
        placeholder="Пароль" 
        class="border-2 border-black p-3 w-full outline-none focus:bg-gray-50"
        required
      />
      
      <button 
        type="submit" 
        :disabled="loading"
        class="bg-black text-white py-4 font-black hover:bg-gray-800 transition-colors disabled:opacity-50"
      >
        {{ loading ? 'Вход...' : 'Войти' }}
      </button>
    </form>
    
    <p v-if="error" class="text-red-600 mt-4 font-bold">{{ errorMessage }}</p>

    <div class="mt-6 pt-4 border-t border-gray-200 text-center">
      <p class="text-sm font-bold text-gray-600">
        Нет аккаунта? 
        <router-link to="/register" class="text-black underline font-black hover:text-gray-700">
          Зарегистрироваться
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  loading.value = true
  error.value = false
  errorMessage.value = ''

  const res = await authStore.login(username.value, password.value)
  
  if (res.success) {
    router.push('/')
  } else {
    error.value = true
    errorMessage.value = res.error || 'Ошибка: неверные данные'
  }
  loading.value = false
}
</script>