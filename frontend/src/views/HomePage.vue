<template>
  <div class="min-h-screen bg-white">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="mb-8">
        <h1 class="text-4xl font-extrabold text-black mb-2">Каталог товаров</h1>
        <p class="text-gray-500">Откройте для себя наши лучшие предложения</p>
      </div>

      <div class="mb-8 flex flex-col gap-4">
        <div class="flex flex-col md:flex-row gap-4 justify-between items-center">
          <div class="w-full md:w-96">
            <input
              v-model="searchInput"
              @input="onSearchInput"
              type="text"
              placeholder="Поиск по названию..."
              class="w-full px-4 py-2 border-2 border-black font-medium focus:outline-none shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
            />
          </div>

          <div v-if="productsStore.categories.length > 0" class="flex flex-wrap gap-2 items-center w-full md:w-auto">
            <button
              @click="productsStore.clearCategoryFilter()"
              :class="[
                'px-4 py-2 text-sm font-bold border-2 border-black transition-all cursor-pointer',
                !productsStore.selectedCategory
                  ? 'bg-black text-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white text-black hover:bg-gray-100'
              ]"
            >
              Все
            </button>

            <button
              v-for="category in productsStore.categories"
              :key="category.id"
              @click="productsStore.setCategory(category.id)"
              :class="[
                'px-4 py-2 text-sm font-bold border-2 border-black transition-all cursor-pointer',
                productsStore.selectedCategory === category.id
                  ? 'bg-black text-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white text-black hover:bg-gray-100'
              ]"
            >
              {{ category.name }}
            </button>
          </div>
        </div>

        <div class="flex flex-wrap gap-2 items-center">
          <span class="text-sm font-bold">Цена:</span>
          <input
            v-model="minPriceInput"
            @input="onPriceInput"
            type="number"
            placeholder="От"
            class="w-24 px-3 py-1 text-sm border-2 border-black font-medium focus:outline-none shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
          />
          <span class="text-sm font-bold">—</span>
          <input
            v-model="maxPriceInput"
            @input="onPriceInput"
            type="number"
            placeholder="До"
            class="w-24 px-3 py-1 text-sm border-2 border-black font-medium focus:outline-none shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
          />
        </div>
      </div>

      <main class="w-full">
        <div class="mb-6 flex items-center justify-between">
          <p class="text-gray-700">
            Найдено товаров: <span class="font-bold">{{ productsStore.totalProducts }}</span>
          </p>
        </div>

        <div v-if="productsStore.loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-none h-12 w-12 border-b-2 border-black"></div>
          <p class="mt-4 text-gray-500">Загрузка товаров...</p>
        </div>

        <div v-else-if="productsStore.error" class="text-center py-12">
          <p class="text-red-600 font-medium">{{ productsStore.error }}</p>
        </div>

        <div v-else-if="productsStore.products && productsStore.products.length > 0">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
            <ProductCard
              v-for="product in productsStore.products"
              :key="product.id"
              :product="product"
            />
          </div>

          <div 
            v-if="totalPages > 1"
            class="flex justify-center items-center gap-2 border-t border-gray-100 pt-8 mt-12"
          >
            <button
              :disabled="productsStore.currentPage === 1"
              @click="productsStore.setPage(productsStore.currentPage - 1)"
              class="px-4 py-2 border-2 border-black font-bold disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors cursor-pointer"
            >
              ←
            </button>

            <button
              v-for="page in totalPages"
              :key="page"
              @click="productsStore.setPage(page)"
              :class="[
                'px-4 py-2 border-2 border-black font-bold transition-all cursor-pointer',
                productsStore.currentPage === page
                  ? 'bg-black text-white'
                  : 'bg-white text-black hover:bg-gray-100'
              ]"
            >
              {{ page }}
            </button>

            <button
              :disabled="productsStore.currentPage === totalPages"
              @click="productsStore.setPage(productsStore.currentPage + 1)"
              class="px-4 py-2 border-2 border-black font-bold disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors cursor-pointer"
            >
              →
            </button>
          </div>
        </div>

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
import { ref, computed, onMounted } from 'vue'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'

const productsStore = useProductsStore()
const searchInput = ref(productsStore.searchQuery)
const minPriceInput = ref(productsStore.minPrice)
const maxPriceInput = ref(productsStore.maxPrice)

let searchTimeout = null
const onSearchInput = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    productsStore.setSearchQuery(searchInput.value)
  }, 350)
}

let priceTimeout = null
const onPriceInput = () => {
  clearTimeout(priceTimeout)
  priceTimeout = setTimeout(() => {
    productsStore.setPriceRange(minPriceInput.value, maxPriceInput.value)
  }, 400)
}

const totalPages = computed(() => {
  const itemsPerPage = Number(productsStore.itemsPerPage) || 10
  const total = Number(productsStore.totalProducts) || 0
  return Math.ceil(total / itemsPerPage) || 1
})

onMounted(async () => {
  await Promise.all([
    productsStore.fetchCategories(),
    productsStore.fetchProducts()
  ])
})
</script>