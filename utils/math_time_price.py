import re
from typing import Union

# Исправленные константы (в минутах)
MINUTES_IN_ONE_WEEK = 10080  # 7 дней * 24 часа * 60 минут
MINUTES_IN_ONE_DAY = 1440    # 24 часа * 60 минут
MINUTES_IN_ONE_HOUR = 60

# Компилированное регулярное выражение для лучшей производительности
TIME_PATTERN = re.compile(r'P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?)?')


def convert_time(time: str) -> int:
    """
    Конвертирует время из ISO 8601 Duration формата в минуты.
    
    Примеры входных данных:
    - PT1H30M -> 90 минут
    - P1W2DT3H4M -> 11584 минуты
    - P1D -> 1440 минут
    
    Args:
        time (str): Время в формате ISO 8601 Duration (например, 'PT1H30M')
    
    Returns:
        int: Общее количество минут
    
    Raises:
        ValueError: Если формат времени некорректный
    """
    if not time or not isinstance(time, str):
        raise ValueError("Время должно быть непустой строкой")
    
    # Очищаем строку от лишних символов
    time = time.strip()
    
    # Ищем совпадения с помощью одного регулярного выражения
    match = TIME_PATTERN.match(time)
    
    if not match:
        raise ValueError(f"Некорректный формат времени: {time}")
    
    weeks, days, hours, minutes = match.groups()
    
    total_minutes = 0
    
    # Обрабатываем каждую единицу времени
    if weeks:
        total_minutes += int(weeks) * MINUTES_IN_ONE_WEEK
    
    if days:
        total_minutes += int(days) * MINUTES_IN_ONE_DAY
    
    if hours:
        total_minutes += int(hours) * MINUTES_IN_ONE_HOUR
    
    if minutes:
        total_minutes += int(minutes)
    
    return total_minutes


def math_price(price_per_hour: Union[int, float], issue_spent_time_minutes: int) -> float:
    """
    Рассчитывает стоимость работы на основе часовой ставки и затраченного времени.
    
    Args:
        price_per_hour (Union[int, float]): Часовая ставка
        issue_spent_time_minutes (int): Затраченное время в минутах
    
    Returns:
        float: Рассчитанная стоимость (округленная до 2 знаков после запятой)
    
    Raises:
        ValueError: Если входные параметры некорректные
    """
    if not isinstance(price_per_hour, (int, float)) or price_per_hour <= 0:
        raise ValueError("Часовая ставка должна быть положительным числом")
    
    if not isinstance(issue_spent_time_minutes, int) or issue_spent_time_minutes < 0:
        raise ValueError("Время должно быть неотрицательным целым числом минут")
    
    # Конвертируем минуты в часы и рассчитываем стоимость
    hours_spent = issue_spent_time_minutes / MINUTES_IN_ONE_HOUR
    result = hours_spent * price_per_hour
    
    # Округляем до 2 знаков после запятой
    return round(result, 2)


# Дополнительные утилиты для удобства
def format_time_human_readable(minutes: int) -> str:
    """
    Форматирует время в человекочитаемый вид.
    
    Args:
        minutes (int): Количество минут
    
    Returns:
        str: Отформатированное время (например, "1 день 2 часа 30 минут")
    """
    if minutes < 0:
        raise ValueError("Время не может быть отрицательным")
    
    weeks = minutes // MINUTES_IN_ONE_WEEK
    remaining_minutes = minutes % MINUTES_IN_ONE_WEEK
    
    days = remaining_minutes // MINUTES_IN_ONE_DAY
    remaining_minutes = remaining_minutes % MINUTES_IN_ONE_DAY
    
    hours = remaining_minutes // MINUTES_IN_ONE_HOUR
    mins = remaining_minutes % MINUTES_IN_ONE_HOUR
    
    parts = []
    if weeks > 0:
        parts.append(f"{weeks} нед.")
    if days > 0:
        parts.append(f"{days} дн.")
    if hours > 0:
        parts.append(f"{hours} ч.")
    if mins > 0:
        parts.append(f"{mins} мин.")
    
    return " ".join(parts) if parts else "0 минут"
