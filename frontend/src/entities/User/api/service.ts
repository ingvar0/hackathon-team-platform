import type { User } from '../model/user'
import { apiClient } from '../../../shared/config/api'

// Используем общий apiClient вместо создания нового экземпляра
export const userService = {
  // Получить текущего пользователя
  async getCurrent(): Promise<User> {
    const response = await apiClient.get<User>('/users/me')
    return response.data
  },

  // Получить пользователя по ID
  async getById(id: number): Promise<User> {
    const response = await apiClient.get<User>(`/users/${id}`)
    return response.data
  },
}

