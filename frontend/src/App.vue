<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <Header />
    <main class="flex-grow">
      <RouterView />
    </main>
    <footer class="bg-white border-t-2 border-black mt-16">
      <div class="max-w-7xl mx-auto px-4 py-8 text-center">
        <p>© 2026 FastAPI Shop.</p>
      </div>
    </footer>

    <!-- Добавляем модальное окно авторизации сюда -->
    <AuthModal />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import AuthModal from '@/components/AuthModal.vue' // <-- Импортируем модалку
import { onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

onMounted(() => {
  cartStore.fetchCartDetails()
})
</script>