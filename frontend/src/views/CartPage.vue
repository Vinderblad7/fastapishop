<template>
  <div class="min-h-screen bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="mb-10">
        <h1 class="text-3xl sm:text-4xl font-extrabold text-black mb-3">Корзина покупок</h1>
        <p class="text-lg text-gray-500">Проверьте выбранные товары перед оформлением заказа</p>
      </div>

      <!-- Загрузка -->
      <div v-if="cartStore.loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-14 w-14 border-b-4 border-black"></div>
        <p class="mt-4 text-lg text-gray-500">Загрузка корзины...</p>
      </div>

      <!-- Если пользователь не авторизован -->
      <div v-else-if="!authStore.isAuthenticated" class="text-center py-16 max-w-md mx-auto border-2 border-black p-8">
        <h2 class="text-2xl font-black text-black mb-3">Вы не вошли в аккаунт</h2>
        <p class="text-gray-600 mb-6 font-medium">Чтобы просмотреть и сохранить товары в корзине, авторизуйтесь в системе.</p>
        
        <div class="flex flex-col gap-3">
          <router-link to="/login" class="w-full bg-black text-white py-3.5 px-6 font-black text-center hover:bg-gray-800 transition-colors">
            Войти
          </router-link>
          <router-link to="/register" class="w-full border-2 border-black text-black py-3 px-6 font-black text-center hover:bg-gray-100 transition-colors">
            Зарегистрироваться
          </router-link>
        </div>
      </div>

      <!-- Если корзина пуста (для авторизованных) -->
      <div v-else-if="!cartStore.hasItems" class="text-center py-16">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-28 w-28 mx-auto text-gray-300 mb-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h2 class="text-2xl font-bold text-black mb-3">Ваша корзина пуста</h2>
        <p class="text-lg text-gray-500 mb-8">Добавьте товары из каталога, чтобы начать покупки.</p>
        <router-link to="/" class="inline-block bg-black text-white py-3 px-8 text-lg font-semibold rounded-none hover:bg-gray-900 transition-colors">
          Перейти в каталог
        </router-link>
      </div>

      <!-- Таблица корзины -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-6">
          <CartItem v-for="item in cartStore.items" :key="item.product_id" :item="item" />
        </div>

        <div class="lg:col-span-1">
          <div class="bg-white border-2 border-gray-100 rounded-none p-8 shadow-sm sticky top-24">
            <h2 class="text-2xl font-bold text-black mb-8">Итого</h2>
            <div class="space-y-6 mb-8">
              <div class="flex justify-between text-lg text-gray-600">
                <span>Товары ({{ cartStore.itemsCount }})</span>
                <span>{{ cartStore.totalPrice.toFixed(2) }} руб.</span>
              </div>
              <div class="flex justify-between text-lg text-gray-600">
                <span>Доставка</span>
                <span class="text-green-600 font-medium">Бесплатно</span>
              </div>
              <div class="border-t-2 border-gray-100 pt-6">
                <div class="flex justify-between text-xl font-bold text-black">
                  <span>Общая стоимость</span>
                  <span>{{ cartStore.totalPrice.toFixed(2) }} руб.</span>
                </div>
              </div>
            </div>
            <button class="w-full bg-black text-white py-4 px-6 text-lg font-semibold rounded-none hover:bg-gray-900 transition-colors mb-4" @click="handleCheckout">
              Оформить заказ
            </button>
            <router-link to="/" class="block w-full bg-gray-100 text-black py-4 px-6 text-lg font-semibold rounded-none hover:bg-gray-200 transition-colors text-center">
              Продолжить покупки
            </router-link>
            <button @click="handleClearCart" class="w-full mt-6 text-base text-red-600 hover:text-red-700 transition-colors font-medium">
              Очистить корзину
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import CartItem from '@/components/CartItem.vue'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

function handleCheckout() {
  router.push('/checkout')
}

function handleClearCart() {
  if (confirm('Вы уверены, что хотите очистить корзину?')) {
    cartStore.clearCart()
  }
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await cartStore.fetchCartDetails()
  }
})
</script>