from datetime import datetime


#  Перевірка на минулий час очевидно ж


def check_if_past_time(date):
    now = str(datetime.now())
    res = False
    year = int(date[0] + date[1] + date[2] + date[3]) - int(now[0] + now[1] + now[2] + now[3])
    print(year)
    month = int(date[5] + date[6]) - int(now[5] + now[6])
    print(month)
    day = int(date[8] + date[9]) - int(now[8] + now[9])
    print(day)
    if year == 0:
        if month == 0:
            if day > 0:
                res = True
        elif month > 0:
            res = True
    elif 0 < year < 5:
        res = True
    return res
