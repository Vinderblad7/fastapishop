<template>
  <div class="min-h-screen bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="mb-10">
        <h1 class="text-3xl sm:text-4xl font-extrabold text-black mb-3">Оформление заказа</h1>
        <p class="text-lg text-gray-500">Заполните данные для доставки товара</p>
      </div>

      <!-- Успешное оформление -->
      <div v-if="orderSuccess" class="border-2 border-black p-8 text-center my-12">
        <div class="w-16 h-16 bg-black text-white flex items-center justify-center mx-auto mb-6 text-2xl font-bold">
          ✓
        </div>
        <h2 class="text-3xl font-bold text-black mb-4">Заказ успешно оформлен!</h2>
        <p class="text-gray-600 text-lg mb-8">Номер вашего заказа: <span class="font-bold text-black">#{{ createdOrderId }}</span></p>
        <router-link to="/" class="inline-block bg-black text-white py-4 px-8 text-lg font-semibold rounded-none hover:bg-gray-900 transition-colors">
          Вернуться на главную
        </router-link>
      </div>

      <!-- Форма оформления -->
      <form v-else @submit.prevent="submitOrder" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-8">
          
          <div v-if="errorMessage" class="p-4 border-2 border-red-600 bg-red-50 text-red-700 font-medium">
            {{ errorMessage }}
          </div>

          <!-- Контактная информация -->
          <div class="border-2 border-gray-100 p-8 rounded-none">
            <h2 class="text-xl font-bold text-black mb-6 uppercase tracking-wider">1. Контактная информация</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-black mb-2 uppercase">Email *</label>
                <input 
                  v-model="form.email" 
                  type="email" 
                  required 
                  placeholder="user@example.com"
                  class="w-full border-2 border-gray-200 p-3 rounded-none focus:border-black focus:outline-none transition-colors"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-black mb-2 uppercase">Телефон *</label>
                <input 
                  v-model="form.phone_number" 
                  type="tel" 
                  required 
                  placeholder="+7 (999) 000-00-00"
                  class="w-full border-2 border-gray-200 p-3 rounded-none focus:border-black focus:outline-none transition-colors"
                />
              </div>
            </div>
          </div>

          <!-- Адрес доставки -->
          <div class="border-2 border-gray-100 p-8 rounded-none">
            <h2 class="text-xl font-bold text-black mb-6 uppercase tracking-wider">2. Адрес доставки</h2>
            <div>
              <label class="block text-sm font-semibold text-black mb-2 uppercase">Адрес *</label>
              <input 
                v-model="form.address" 
                type="text" 
                required 
                placeholder="г. Москва, ул. Пушкина, д. 10, кв. 4"
                class="w-full border-2 border-gray-200 p-3 rounded-none focus:border-black focus:outline-none transition-colors"
              />
            </div>
          </div>

        </div>

        <!-- Состав заказа -->
        <div class="lg:col-span-1">
          <div class="bg-white border-2 border-gray-100 rounded-none p-8 sticky top-24">
            <h2 class="text-2xl font-bold text-black mb-6">Ваш заказ</h2>
            
            <div class="divide-y-2 divide-gray-100 mb-6 max-h-60 overflow-y-auto pr-2">
              <div v-for="item in cartStore.items" :key="item.product_id" class="py-3 flex justify-between items-center text-sm">
                <div>
                  <p class="font-bold text-black">{{ getProductName(item) }}</p>
                  <p class="text-gray-500">{{ item.quantity }} шт.</p>
                </div>
                <span class="font-semibold text-black">{{ (getProductPrice(item) * item.quantity).toFixed(2) }} руб.</span>
              </div>
            </div>

            <div class="border-t-2 border-black pt-6 space-y-4 mb-8">
              <div class="flex justify-between text-gray-600">
                <span>Товары ({{ cartStore.itemsCount }})</span>
                <span>{{ cartStore.totalPrice.toFixed(2) }} руб.</span>
              </div>
              <div class="flex justify-between text-gray-600">
                <span>Доставка</span>
                <span class="text-green-600 font-medium">Бесплатно</span>
              </div>
              <div class="flex justify-between text-xl font-bold text-black pt-2 border-t border-gray-100">
                <span>К оплате</span>
                <span>{{ cartStore.totalPrice.toFixed(2) }} руб.</span>
              </div>
            </div>

            <button 
              type="submit" 
              :disabled="loading || !cartStore.hasItems"
              class="w-full bg-black text-white py-4 px-6 text-lg font-semibold rounded-none hover:bg-gray-900 transition-colors disabled:opacity-50"
            >
              {{ loading ? 'Оформление...' : 'Подтвердить заказ' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ordersAPI } from '@/services/api'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const orderSuccess = ref(false)
const createdOrderId = ref(null)
const errorMessage = ref('')

// Данные строго соответствуют структуре OrderModel на бэкенде
const form = reactive({
  email: '',
  phone_number: '',
  address: ''
})

function getProductName(item) {
  const p = item.products || item.product || {}
  return p.name || 'Товар'
}

function getProductPrice(item) {
  const p = item.products || item.product || {}
  return Number(p.price || 0)
}

async function submitOrder() {
  if (!cartStore.hasItems) return
  
  loading.value = true
  errorMessage.value = ''

  try {
    // Формируем payload точно под схему FastAPI (Pydantic)
    const payload = {
      email: form.email,
      phone_number: form.phone_number,
      address: form.address
    }

    const res = await ordersAPI.createOrder(payload)
    createdOrderId.value = res.data.id
    orderSuccess.value = true
    await cartStore.fetchCartDetails()
  } catch (err) {
    console.error(err)
    errorMessage.value = err.response?.data?.detail || 'Ошибка при оформлении заказа'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await cartStore.fetchCartDetails()
  if (!cartStore.hasItems) {
    router.push('/cart')
  }
})
</script>