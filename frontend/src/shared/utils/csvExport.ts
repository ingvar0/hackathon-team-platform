/**
 * Утилита для экспорта данных команд в CSV формат
 */

type TeamMember = {
  telegram_id: string
  fullname: string
  role?: string | null
  description?: string | null
  tags?: string[] | null
  pic?: string | null
}

type TeamData = {
  team_id: number
  hackathon_id: number
  title: string
  description: string
  captain: TeamMember
  participants: TeamMember[]
  password?: string | null
}

/**
 * Экранирует значение для CSV (обрабатывает кавычки и запятые)
 */
function escapeCSVValue(value: string | null | undefined): string {
  if (value === null || value === undefined) {
    return ''
  }
  
  const stringValue = String(value)
  
  // Если значение содержит запятую, кавычку или перенос строки, оборачиваем в кавычки
  if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
    // Экранируем кавычки удвоением
    return `"${stringValue.replace(/"/g, '""')}"`
  }
  
  return stringValue
}

/**
 * Преобразует массив навыков в строку
 */
function formatSkills(skills: string[] | null | undefined): string {
  if (!skills || skills.length === 0) {
    return ''
  }
  return skills.join('; ')
}

/**
 * Преобразует данные команд в CSV формат
 */
export function exportTeamsToCSV(teams: TeamData[], hackathonTitle: string = 'Хакатон'): string {
  // Заголовки CSV
  const headers = [
    'ID команды',
    'Название команды',
    'Описание команды',
    'Роль участника',
    'ФИО',
    'Telegram ID',
    'Роль в команде',
    'Описание',
    'Навыки'
  ]
  
  // Создаем строки CSV
  const rows: string[] = []
  
  // Добавляем название хакатона как первую строку (комментарий)
  rows.push(`# Хакатон: ${escapeCSVValue(hackathonTitle)}`)
  
  // Добавляем заголовки
  rows.push(headers.map(escapeCSVValue).join(','))
  
  // Обрабатываем каждую команду
  for (const team of teams) {
    // Добавляем капитана
    const captainRow = [
      team.team_id.toString(),
      escapeCSVValue(team.title),
      escapeCSVValue(team.description),
      'Капитан',
      escapeCSVValue(team.captain.fullname),
      escapeCSVValue(team.captain.telegram_id),
      escapeCSVValue(team.captain.role),
      escapeCSVValue(team.captain.description),
      escapeCSVValue(formatSkills(team.captain.tags))
    ]
    rows.push(captainRow.join(','))
    
    // Добавляем участников
    for (const participant of team.participants) {
      const participantRow = [
        team.team_id.toString(),
        escapeCSVValue(team.title),
        escapeCSVValue(team.description),
        'Участник',
        escapeCSVValue(participant.fullname),
        escapeCSVValue(participant.telegram_id),
        escapeCSVValue(participant.role),
        escapeCSVValue(participant.description),
        escapeCSVValue(formatSkills(participant.tags))
      ]
      rows.push(participantRow.join(','))
    }
  }
  
  return rows.join('\n')
}

/**
 * Скачивает CSV файл
 */
export function downloadCSV(csvContent: string, filename: string): void {
  // Добавляем BOM для корректного отображения кириллицы в Excel
  const BOM = '\uFEFF'
  const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })
  
  // Создаем ссылку для скачивания
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  // Освобождаем память
  URL.revokeObjectURL(url)
}
