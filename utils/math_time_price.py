HOURS_IN_ONE_WEAK = '40'
HOURS_IN_ONE_DAY = '8'


def convert_time(time : str) -> int:
    time = time.replace('PT', '')

    if 'W' in time:
        time = time.replace('W', f' * {HOURS_IN_ONE_WEAK} + ')
        time = time.replace('T', '')
        time = time.replace('P', '')
    if "DT" in time:
        time = time.replace('DT', f' * {HOURS_IN_ONE_DAY} + ')
        time = time.replace('T', '')
        time = time.replace('P', '')

    if 'H' in time:
        time = time.replace('H', ' * 60 + ')
        time = time.replace('T', '')
        time = time.replace('P', '')

    if 'M' in time:
        time = time.replace('M', '')
        time = time.replace('T', '')
        time = time.replace('P', '')

    if time.endswith(' + '):
        time = time[:-3]

    return eval(time)


def math_price(price_per_hour, issue_spent_time):
    return int(price_per_hour * (issue_spent_time // 60)) # Заменить на // если нужно делить без остатка
