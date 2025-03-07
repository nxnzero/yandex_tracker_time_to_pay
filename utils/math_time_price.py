import re

HOURS_IN_ONE_WEAK = '2400'
HOURS_IN_ONE_DAY = '480'


def convert_time(time: str):
    time = time.replace('PT', '')
    time = time.replace('P', '')

    total_minutes = 0

    weeks = re.search(r'(\d+)W', time)
    if weeks:
        total_minutes += int(weeks.group(1)) * int(HOURS_IN_ONE_WEAK)

    days = re.search(r'(\d+)D', time)
    if days:
        total_minutes += int(days.group(1)) * int(HOURS_IN_ONE_DAY)

    hours = re.search(r'(\d+)H', time)
    if hours:
        total_minutes += int(hours.group(1)) * 60

    minutes = re.search(r'(\d+)M', time)
    if minutes:
        total_minutes += int(minutes.group(1))

    return total_minutes


def math_price(price_per_hour, issue_spent_time):
    return int(issue_spent_time * price_per_hour / 60) # Заменить на // если нужно делить без остатка
