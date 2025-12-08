import type { Notification } from '../model/notification'
import { apiClient } from '../../../shared/config/api'

// Используем общий apiClient вместо создания нового экземпляра
export const notificationService = {
  // Получить все уведомления текущего пользователя
  async getAll(): Promise<Notification[]> {
    const response = await apiClient.get<Notification[]>('/notifications')
    return response.data
  }
}

