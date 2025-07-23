import os
import logging
from typing import Dict, Any, Optional

from yandex_tracker_client import TrackerClient
from utils.math_time_price import convert_time, math_price

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы для полей
TEST_HOURLY_RATE = '*****--testHourlyRate'
PRICE_FOR_ISSUE = '*****--issuePrice'

# Инициализация клиента (раскомментировано и улучшено)
def get_tracker_client() -> TrackerClient:
    """Получить клиент Яндекс.Трекера с обработкой ошибок"""
    try:
        token = os.environ.get('TOKEN')
        org_id = os.environ.get('ORG_ID')
        
        if not token or not org_id:
            raise ValueError("TOKEN и ORG_ID должны быть установлены в переменных окружения")
        
        return TrackerClient(token=token, cloud_org_id=org_id)
    except Exception as e:
        logger.error(f"Ошибка при инициализации клиента: {e}")
        raise


def validate_event(event: Dict[str, Any]) -> str:
    """Валидация входящего события и извлечение ключа задачи"""
    if not event:
        raise ValueError("Событие не может быть пустым")
    
    query_params = event.get('queryStringParameters')
    if not query_params:
        raise ValueError("Отсутствуют параметры запроса")
    
    issue_key = query_params.get('key')
    if not issue_key:
        raise ValueError("Параметр 'key' обязателен")
    
    return issue_key


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Обработчик Cloud Function для расчета стоимости задачи
    """
    try:
        # Валидация входных данных
        issue_key = validate_event(event)
        logger.info(f"Обработка задачи: {issue_key}")
        
        # Получение клиента
        client = get_tracker_client()
        
        # Получение информации о задаче
        try:
            issue = client.issues[issue_key]
        except Exception as e:
            logger.error(f"Ошибка при получении задачи {issue_key}: {e}")
            return {
                'statusCode': 404,
                'body': f'Задача {issue_key} не найдена'
            }
        
        # Извлечение данных о времени и ставке
        issue_spent_time = getattr(issue, 'spent', None)
        if not issue_spent_time:
            logger.warning(f"Задача {issue_key} не содержит информации о затраченном времени")
            return {
                'statusCode': 400,
                'body': 'Задача не содержит информации о затраченном времени'
            }
        
        issue_price_for_hour = getattr(issue, 'testHourlyRate', None)
        if not issue_price_for_hour:
            logger.warning(f"Задача {issue_key} не содержит информации о часовой ставке")
            return {
                'statusCode': 400,
                'body': 'Задача не содержит информации о часовой ставке'
            }
        
        # Расчет стоимости
        issue_spent_time_in_min = convert_time(issue_spent_time)
        issue_price = math_price(issue_price_for_hour, issue_spent_time_in_min)
        
        # Обновление задачи (исправлен синтаксис)
        try:
            # Если поле глобальное, используем issue.update()
            issue.update(**{PRICE_FOR_ISSUE: issue_price})
            
            logger.info(f"Задача {issue_key} обновлена. Стоимость: {issue_price}")
            
            return {
                'statusCode': 200,
                'body': {
                    'message': 'Стоимость задачи успешно рассчитана и обновлена',
                    'issue_key': issue_key,
                    'price': issue_price,
                    'spent_time_minutes': issue_spent_time_in_min
                }
            }
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении задачи {issue_key}: {e}")
            return {
                'statusCode': 500,
                'body': f'Ошибка при обновлении задачи: {str(e)}'
            }
    
    except ValueError as e:
        logger.error(f"Ошибка валидации: {e}")
        return {
            'statusCode': 400,
            'body': str(e)
        }
    
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return {
            'statusCode': 500,
            'body': 'Внутренняя ошибка сервера'
        }


# Для локального тестирования
if __name__ == '__main__':
    # Пример события для тестирования
    test_event = {
        'queryStringParameters': {
            'key': 'TEST-123'  # Замените на реальный ключ задачи
        }
    }
    
    # Установите переменные окружения для тестирования
    # os.environ['TOKEN'] = 'your_token_here'
    # os.environ['ORG_ID'] = 'your_org_id_here'
    
    result = handler(test_event, context=None)
    print(f"Результат: {result}")
