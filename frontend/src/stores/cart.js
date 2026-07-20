import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartAPI } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

export const useCartStore = defineStore('cart', () => {
  const cartItems = ref([])
  const loading = ref(false)
  const showAuthModal = ref(false)

  const authStore = useAuthStore()

  const items = computed(() => cartItems.value)

  const itemsCount = computed(() => {
    return cartItems.value.reduce((acc, item) => acc + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return cartItems.value.reduce((acc, item) => {
      const price = item.product?.price || item.products?.price || 0
      return acc + (price * item.quantity)
    }, 0)
  })

  const hasItems = computed(() => cartItems.value.length > 0)

  function closeAuthModal() {
    showAuthModal.value = false
  }

  function normalizeData(data) {
    const arr = Array.isArray(data) ? data : (data ? [data] : [])
    return arr.map(item => {
      const productData = item.product || item.products || {}
      return {
        ...item,
        product: productData,
        products: productData
      }
    })
  }

  async function fetchCartDetails() {
    if (!authStore.isAuthenticated) {
      cartItems.value = []
      return
    }

    loading.value = true
    try {
      const response = await cartAPI.getCart()
      cartItems.value = normalizeData(response.data)
    } catch (err) {
      console.error('Error fetching cart:', err)
      cartItems.value = []
    } finally {
      loading.value = false
    }
  }

  async function addToCart(productId, quantity = 1) {
    if (!authStore.isAuthenticated) {
      showAuthModal.value = true
      return false
    }

    try {
      await cartAPI.addItem(productId, quantity)
      await fetchCartDetails()
      return true
    } catch (err) {
      console.error('Error adding to cart:', err)
      
      if (err.response?.status === 401) {
        authStore.logout()
        showAuthModal.value = true
      }
      return false
    }
  }

  async function updateQuantity(productId, quantity) {
    if (quantity <= 0) return removeFromCart(productId)
    try {
      await cartAPI.updateItem(productId, quantity)
      await fetchCartDetails()
      return true
    } catch (err) {
      console.error('Error updating quantity:', err)
      return false
    }
  }

  async function removeFromCart(productId) {
    try {
      await cartAPI.removeItem(productId)
      await fetchCartDetails()
      return true
    } catch (err) {
      console.error('Error removing from cart:', err)
      return false
    }
  }

  async function clearCart() {
    try {
      for (const item of cartItems.value) {
        await cartAPI.removeItem(item.product_id)
      }
      cartItems.value = []
      return true
    } catch (err) {
      console.error('Error clearing cart:', err)
      return false
    }
  }

  return {
    loading,
    items,
    itemsCount,
    totalPrice,
    hasItems,
    showAuthModal,
    closeAuthModal,
    fetchCartDetails,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
  }
})