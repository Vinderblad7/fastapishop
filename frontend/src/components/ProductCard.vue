<template>
  <router-link
    :to="{ name: 'product-detail', params: { id: Number(product.id) } }"
    class="block bg-white border-2 border-gray-100 rounded-none overflow-hidden hover:border-black transition-all duration-300 cursor-pointer"
  >
    <div class="aspect-square overflow-hidden bg-gray-50">
      <img
        :src="productImage"
        :alt="product.name"
        class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        @error="handleImageError"
      />
    </div>

    <div class="p-4">
      <h3 class="text-lg font-bold text-black mb-2 hover:text-gray-700 transition-colors line-clamp-2 min-h-[3.5rem]">
        {{ product.name }}
      </h3>

      <p class="text-2xl font-black text-black mb-4">{{ product.price.toFixed(2) }} руб.</p>

      <button
        @click.prevent.stop="handleAddToCart"
        :disabled="adding"
        class="w-full bg-black text-white py-3 px-4 rounded-none hover:bg-gray-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold cursor-pointer"
      >
        {{ adding ? 'Добавление...' : 'В корзину' }}
      </button>

      <transition name="fade">
        <div v-if="showNotification" class="mt-2 text-sm text-green-600 text-center font-medium">
          ✓ Товар добавлен в корзину!
        </div>
      </transition>
    </div>
  </router-link>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '@/stores/cart'

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
})

const cartStore = useCartStore()
const adding = ref(false)
const showNotification = ref(false)

const productImage = computed(() => {
  if (!props.product.image_url) return 'https://placehold.co/400x400?text=No+Image'
  return props.product.image_url
    .replace('http://localhost:8000', '')
    .replace('http://127.0.0.1:8000', '')
})

async function handleAddToCart() {
  adding.value = true
  const success = await cartStore.addToCart(props.product.id, 1)

  if (success) {
    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 2000)
  }

  adding.value = false
}

function handleImageError(event) {
  event.target.src = 'https://placehold.co/400x400?text=No+Image'
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>