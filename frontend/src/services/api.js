import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true 
})

export const productsAPI = {
  getAll(page = 1, limit = 10) {
    return apiClient.get('/products', {
      params: { page, limit }
    })
  },

  getById(id) {
    return apiClient.get(`/products/${id}`)
  },

  getByCategory(categoryId, page = 1, limit = 10) {
    return apiClient.get('/products', {
      params: { 
        category_id: categoryId, 
        page, 
        limit 
      }
    })
  },
}

export const categoriesAPI = {
  getAll() {
    return apiClient.get('/categories')
  },

  getById(id) {
    return apiClient.get(`/categories/${id}`)
  },
}

export const cartAPI = {
  getCart() {
    return apiClient.get('/cart')
  },

  addItem(productId, quantity = 1) {
    return apiClient.post('/cart', {
      product_id: productId,
      quantity: quantity
    })
  },

  updateItem(productId, quantity) {
    return apiClient.patch(`/cart/${productId}`, {
      quantity: quantity
    })
  },

  removeItem(productId) {
    return apiClient.delete(`/cart/${productId}`)
  },

  clearCart() {
    return apiClient.delete('/cart')
  }
}

export const authAPI = {
  register(userData) {
    return apiClient.post('/auth/register', userData)
  },

  login(username, password) {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
    
    return apiClient.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  }
}

export const ordersAPI = {
  createOrder(orderData) {
    return apiClient.post('/orders', orderData)
  },

  getUserOrders() {
    return apiClient.get('/orders')
  },

  getOrderById(id) {
    return apiClient.get(`/orders/${id}`)
  }
}

export default apiClient