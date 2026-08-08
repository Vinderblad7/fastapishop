<template>
  <div class="min-h-screen bg-white py-12 px-4 max-w-7xl mx-auto">
    <router-link
      to="/"
      class="inline-block mb-6 font-bold border-2 border-black px-4 py-2 hover:bg-black hover:text-white transition-colors cursor-pointer"
    >
      ← Назад к каталогу
    </router-link>

    <div v-if="loading" class="text-center py-24">
      <div class="inline-block animate-spin h-12 w-12 border-b-2 border-black"></div>
      <p class="mt-4 text-gray-500 font-medium">Загрузка товара...</p>
    </div>

    <div v-else-if="error" class="text-center py-24 text-red-600 font-bold">
      {{ error }}
    </div>

    <div v-else-if="product" class="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
      <div class="border-2 border-black p-2 bg-gray-50 aspect-square overflow-hidden">
        <img
          :src="productImage"
          :alt="product.name"
          class="w-full h-full object-cover"
          @error="handleImageError"
        />
      </div>

      <div>
        <h1 class="text-4xl font-black text-black mb-4">{{ product.name }}</h1>
        <p class="text-3xl font-extrabold text-black mb-6">{{ product.price?.toFixed(2) }} руб.</p>
        
        <div class="mb-8 text-gray-700">
          <h3 class="font-bold text-black mb-2">Описание:</h3>
          <p class="leading-relaxed">{{ product.description || 'Описание отсутствует' }}</p>
        </div>

        <button
          @click="addToCart"
          :disabled="adding"
          class="w-full bg-black text-white py-4 font-bold hover:bg-gray-900 transition-colors disabled:opacity-50 cursor-pointer shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
        >
          {{ adding ? 'Добавление...' : 'Добавить в корзину' }}
        </button>

        <div v-if="showNotification" class="mt-4 text-center font-bold text-green-600">
          ✓ Товар успешно добавлен в корзину!
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import axios from 'axios'

const route = useRoute()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)
const error = ref(null)
const adding = ref(false)
const showNotification = ref(false)

const productImage = computed(() => {
  const rawUrl = product.value?.image_url || product.value?.image || ''
  if (!rawUrl) return 'https://placehold.co/600x600?text=No+Image'
  return rawUrl.replace('http://localhost:8000', '').replace('http://127.0.0.1:8000', '')
})

function handleImageError(event) {
  event.target.src = 'https://placehold.co/600x600?text=No+Image'
}

onMounted(async () => {
  try {
    const productId = route.params.id
    const response = await axios.get(`/api/products/${productId}`)
    product.value = response.data
  } catch (err) {
    error.value = 'Не удалось загрузить товар. Возможно, он был удален.'
  } finally {
    loading.value = false
  }
})

async function addToCart() {
  if (!product.value) return
  adding.value = true
  const success = await cartStore.addToCart(product.value.id, 1)

  if (success !== false) {
    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 2000)
  }
  adding.value = false
}
</script>