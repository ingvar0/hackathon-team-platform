// Конфигурация API
import axios from 'axios'

// Определяем базовый URL для API
// ВСЕГДА используем относительный путь /api, который проксируется через nginx (production) или Vite (development)
const getApiBaseUrl = () => {
  // Если есть переменная окружения - используем её (можно задать через .env)
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // ВСЕГДА используем относительный путь
  // В development - проксируется через Vite на backend:8000
  // В production - проксируется через nginx на http://89.169.160.161/api
  return '/api'
}

export const API_BASE_URL = getApiBaseUrl()

// Создаем общий экземпляр axios с базовыми настройками
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Важно для работы с cookies
  timeout: 30000, // Увеличиваем таймаут до 30 секунд для медленных соединений
})

// Interceptor для обработки ошибок
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.method?.toUpperCase(), response.config.url, response.status)
    return response
  },
  (error) => {
    // Детальное логирование для отладки
    const errorInfo = {
      message: error.message,
      code: error.code,
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      baseURL: error.config?.baseURL,
      fullURL: error.config?.baseURL ? `${error.config.baseURL}${error.config.url}` : error.config?.url,
      data: error.response?.data,
    }
    console.error('API Error:', errorInfo)
    
    // Если это network error, даем более понятное сообщение
    if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
      console.error('Network Error - проверьте:')
      console.error('1. Доступность сервера:', error.config?.baseURL)
      console.error('2. CORS настройки на сервере')
      console.error('3. Настройки прокси в nginx/vite')
    }
    
    return Promise.reject(error)
  }
)

// Interceptor для логирования запросов
apiClient.interceptors.request.use(
  (config) => {
    const fullURL = config.baseURL ? `${config.baseURL}${config.url}` : config.url
    console.log('API Request:', {
      method: config.method?.toUpperCase(),
      url: fullURL,
      baseURL: config.baseURL,
      path: config.url,
      data: config.data,
    })
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

