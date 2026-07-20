<template>
  <div class="min-h-screen bg-white">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="mb-8">
        <h1 class="text-4xl font-extrabold text-black mb-2">Каталог товаров</h1>
        <p class="text-gray-500">Откройте для себя наши лучшие предложения</p>
      </div>

      <main class="w-full">
        <div class="mb-6 flex items-center justify-between">
          <p class="text-gray-700">
            Найдено товаров: <span class="font-bold">{{ productsStore.totalProducts }}</span>
          </p>
        </div>

        <!-- Состояние загрузки -->
        <div v-if="productsStore.loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-none h-12 w-12 border-b-2 border-black"></div>
          <p class="mt-4 text-gray-500">Загрузка товаров...</p>
        </div>

        <!-- Ошибка -->
        <div v-else-if="productsStore.error" class="text-center py-12">
          <p class="text-red-600 font-medium">{{ productsStore.error }}</p>
        </div>

        <!-- Отображение товаров -->
        <div v-else-if="productsStore.products && productsStore.products.length > 0">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
            <ProductCard
              v-for="product in productsStore.products"
              :key="product.id"
              :product="product"
            />
          </div>

          <!-- Блок Пагинации -->
          <div 
            v-if="totalPages > 1"
            class="flex justify-center items-center gap-2 border-t border-gray-100 pt-8 mt-12"
          >
            <!-- Кнопка Назад -->
            <button
              :disabled="productsStore.currentPage === 1"
              @click="productsStore.setPage(productsStore.currentPage - 1)"
              class="px-4 py-2 border-2 border-black font-bold disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors"
            >
              ←
            </button>

            <!-- Кнопки с номерами страниц -->
            <button
              v-for="page in totalPages"
              :key="page"
              @click="productsStore.setPage(page)"
              :class="[
                'px-4 py-2 border-2 border-black font-bold transition-all',
                productsStore.currentPage === page
                  ? 'bg-black text-white'
                  : 'bg-white text-black hover:bg-gray-100'
              ]"
            >
              {{ page }}
            </button>

            <!-- Кнопка Вперед -->
            <button
              :disabled="productsStore.currentPage === totalPages"
              @click="productsStore.setPage(productsStore.currentPage + 1)"
              class="px-4 py-2 border-2 border-black font-bold disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors"
            >
              →
            </button>
          </div>
        </div>

        <!-- Пустой список -->
        <div v-else class="text-center py-12">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-16 w-16 mx-auto text-gray-400 mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
            />
          </svg>
          <p class="text-gray-500 text-lg font-medium">Товары не найдены</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'

const productsStore = useProductsStore()

// Вычисляем общее количество страниц
const totalPages = computed(() => {
  return Math.ceil(productsStore.totalProducts / productsStore.itemsPerPage) || 1
})

onMounted(async () => {
  await productsStore.fetchProducts()
})
</script>