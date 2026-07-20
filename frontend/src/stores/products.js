import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsAPI, categoriesAPI } from '@/services/api'

export const useProductsStore = defineStore('products', () => {
  const products = ref([])
  const categories = ref([])
  const selectedCategory = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const currentPage = ref(1)
  const itemsPerPage = ref(10)
  const totalProducts = ref(0)

  const productsCount = computed(() => products.value.length)

  async function fetchProducts() {
    loading.value = true
    error.value = null
    try {
      let response
      if (selectedCategory.value) {
        response = await productsAPI.getByCategory(selectedCategory.value, currentPage.value, itemsPerPage.value)
      } else {
        response = await productsAPI.getAll(currentPage.value, itemsPerPage.value)
      }
      
      if (response.data && Array.isArray(response.data.items)) {
        products.value = response.data.items
        totalProducts.value = response.data.total
      } else if (Array.isArray(response.data)) {
        products.value = response.data
        totalProducts.value = response.data.length
      } else {
        products.value = []
        totalProducts.value = 0
      }
    } catch (err) {
      error.value = 'Failed to load products'
      console.error('Error fetching products:', err)
      products.value = []
      totalProducts.value = 0
    } finally {
      loading.value = false
    }
  }

  async function fetchProductById(id) {
    loading.value = true
    error.value = null
    try {
      const response = await productsAPI.getById(id)
      return response.data
    } catch (err) {
      error.value = 'Failed to load product'
      console.error('Error fetching product:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await categoriesAPI.getAll()
      categories.value = response.data
    } catch (err) {
      console.error('Error fetching categories:', err)
    }
  }

  function setCategory(categoryId) {
    selectedCategory.value = categoryId
    currentPage.value = 1 
    fetchProducts()
  }

  function clearCategoryFilter() {
    selectedCategory.value = null
    currentPage.value = 1
    fetchProducts()
  }

  function setPage(page) {
    currentPage.value = page
    fetchProducts()
  }

  return {
    products,
    categories,
    selectedCategory,
    loading,
    error,
    currentPage,
    itemsPerPage,
    totalProducts,
    productsCount,
    fetchProducts,
    fetchProductById,
    fetchCategories,
    setCategory,
    clearCategoryFilter,
    setPage,
  }
})