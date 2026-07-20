<template>
  <transition name="fade">
    <div 
      v-if="cartStore.showAuthModal" 
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      @click.self="cartStore.closeAuthModal()"
    >
      <!-- Карточка модалки с бруталистской прямой тенью и жирной рамкой -->
      <div class="bg-white border-2 border-black p-8 max-w-md w-full shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] relative transition-all">
        <!-- Кнопка закрытия -->
        <button 
          @click="cartStore.closeAuthModal()" 
          class="absolute top-4 right-4 text-xl font-black text-black hover:bg-gray-100 w-8 h-8 flex items-center justify-center border border-black transition-colors"
        >
          ✕
        </button>

        <h3 class="text-2xl font-black text-black mb-3">Нужна авторизация</h3>
        <p class="text-gray-600 mb-6 font-medium leading-relaxed">
          Чтобы добавить товар в корзину, необходимо войти в свой аккаунт или зарегистрироваться.
        </p>

        <div class="flex flex-col gap-3">
          <router-link
            to="/register"
            @click="cartStore.closeAuthModal()"
            class="w-full bg-black text-white py-3.5 px-6 font-black text-center border-2 border-black hover:bg-gray-800 transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,0.2)] active:translate-x-[2px] active:translate-y-[2px]"
          >
            Зарегистрироваться
          </router-link>
          
          <router-link
            to="/login"
            @click="cartStore.closeAuthModal()"
            class="w-full bg-white text-black py-3.5 px-6 font-black text-center border-2 border-black hover:bg-gray-100 transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:translate-x-[2px] active:translate-y-[2px]"
          >
            Войти
          </router-link>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>