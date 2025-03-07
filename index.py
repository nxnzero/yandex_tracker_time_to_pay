import os

from yandex_tracker_client import TrackerClient
from utils.math_time_price import convert_time
from utils.math_time_price import math_price


ISSUE_KEY = '<ISSUE KEY>'

TEST_HOURLY_RATE = '*****--testHourlyRate' # Не используем, если поле глобальное
PRICE_FOR_ISSUE = '*****--issuePrice' # Не используем, если поле глобальное


# client = TrackerClient(token=os.environ['TOKEN']', cloud_org_id=os.environ['ORG_ID'])


def handler(event, context):
    issue_key = event['queryStringParameters']['key'] # Заменить на ID или иной query-параметр

    issue = client.issues[issue_key]

    issue_spent_time = issue.spent # Затраченное время в формате 'PT1W1DT1H1M'
    issue_spent_time_in_min = convert_time(issue_spent_time)
    issue_price_for_hour = issue.testHourlyRate

    issue_price = math_price(issue_price_for_hour, issue_spent_time_in_min)

    (**{PRICE_FOR_ISSUE:issue_price})

     return {
        'statusCode':200,
        'body':'Have a good day'
    }
  
    '''
    Если поле глобальное, то используем:
    issue.update(
        taskPrice = issue_price
    )
    '''

'''
if __name__ == '__main__':
    event = {
        'queryStringParameters': {
            'key': f'{ISSUE_KEY}'
        }
    }

    handler(event, context=None)
'''
