import datetime


def gen_datetime(str_start="2016/10/16"):
    datetime_start = datetime.datetime.strptime(str_start, "%Y/%m/%d")
    str_today = datetime.datetime.today().strftime("%Y/%m/%d")
    datetime_list = list()
    i = 1
    while True:
        next_datetime = datetime_start + datetime.timedelta(days=i)
        str_nextday = next_datetime.strftime("%Y/%m/%d")
        datetime_list.append(str_nextday)
        i += 1
        if str_nextday == str_today:
            break
    return datetime_list