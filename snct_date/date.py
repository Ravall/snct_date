# -*- coding: utf-8 -*-
# исторический код уберем проверку C0103 на короткие имена
# pylint: disable=C0103
# pylint: disable=R0913
# pylint: disable=R0911

import datetime
from pytils import dt


def date_diff(date1, date2):
    '''
    возвращает разницу между датами в днях
    '''
    return count_days(date1) - count_days(date2)


def count_days(date):
    '''
    возвращает количество дней от 0000-00-00
    '''
    _y = int(date[2]) - 1
    leap_years = _y/4 - _y/100 + _y/400
    count_days = 365 * _y + leap_years
    count_days = reduce(
        lambda res, x: res + num_days_in_month(x, date[2]),
        xrange(1, int(date[1])),
        count_days
    )
    return count_days + int(date[0])



def yyyy_mm_dd(date):
    '''
    возвращает кортеж дат в строку формате YYYY-mm-dd
    '''
    return '{2:02d}-{1:02d}-{0:02d}'.format(*date)


def date_to_dict(date):
    '''
    переводим дату в кортеж для работы
    '''
    if type(date) == datetime.datetime or type(date) == datetime.date:
        date_arr = [date.day, date.month, date.year]
    else:
        date_arr = date.split('-')[::-1]
        date_arr = map(int, date_arr)
    return date_arr


def is_leap_year(year):
    '''
    Проверяем год на високосность
    '''
    return bool(not int(year) % 4 and int(year) % 100) or not int(year) % 400


def date_compare(d1, m1, y1, d2, m2, y2):
    '''
    Сравниваются даты
        1 - вторая дата позже
        -1 - первая дата позже
        0 - даты совпадают

    '''
    if int(y2) > int(y1):
        return 1
    if int(y2) < int(y1):
        return -1
    if int(m2) > int(m1):
        return 1
    if int(m2) < int(m1):
        return -1
    if int(d2) > int(d1):
        return 1
    if int(d2) < int(d1):
        return -1
    return 0


def num_days_in_year(year):
    '''
    возвращем количество дней  в году
    '''
    return 366 if is_leap_year(year) else 365


def num_days_in_month(month, year):
    '''
    возвращем количество дней в месяце
    '''
    if int(month) in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if int(month) in (4, 6, 9, 11):
        return 30
    if int(month) == 2:
        return 28 + is_leap_year(year)
    raise Exception("Неверный месяц в num_days_in_month!")


def date_shift(day, month, year, shift):
    '''
    Сдвигает дату на $shift дней
    '''
    day, month, year, shift = map(int, [day, month, year, shift])
    if not shift:
        return (day, month, year)
    day += shift
    while day < 1:
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        day += num_days_in_month(month, year)
    while day > num_days_in_month(month, year):
        day -= num_days_in_month(month, year)
        month += 1
        if month > 12:
            month = 1
            year += 1
    return (day, month, year)


def today():
    '''
    текущая дата
    '''
    dt = datetime.datetime.now()
    return [dt.day, dt.month, dt.year]


def get_current_year():
    '''
    получаем текущий год
    '''
    return today()[2]


def is_date_correct(d, m, y=0):
    '''
    Проверяем дату на корректность
    '''
    d, m, y = map(int, [d, m, y])
    if not y:
        y = get_current_year()
    if d is None or m is None or not str(y).isdigit():
        return 0
    if not str(d).isdigit() or d < 1 or d > 31:
        return 0
    if not str(m).isdigit() or m < 1 or m > 12:
        return 0
    if m == 2 and d > 28 + is_leap_year(y):
        return 0
    if (m == 4 or m == 6 or m == 9 or m == 11) and d == 31:
        return 0
    return 1


def get_day_of_week(d, m, y):
    """
    Находим день недели. Работает и после 2036 года.

    Для нашего современного календаря:

    W = d + [ (13m - 1) / 5 ] + y + [ y / 4 ] + [ c / 4 ] - 2c

    где d - число месяца;
    m - номер месяца, начиная с марта (март=1, апрель=2, ... февраль=12);
    y - номер года в столетии (например, для 1965 года y=65.
        Для января и февраля 1965 года, т.е.
    для m=11 или m=12 номер года надо брать предыдущий, т.е. y=64);
    c - количество столетий (например, для 2000 года c=20.
        И здесь для января и февраля 2000 года
    надо брать предыдущее столетие с=19);
    квадратные скобки означают целую часть полученного числа
    (отбрасываем дробную).
    Результат W делите на 7 и модуль остатка от деления даст
    день недели (воскресенье=0, понедельник=1, ... суббота=6)
    Пример: для 31 декабря 2008 года определяем:
    d=31, m=10, y=8, c=20
    По формуле находим:
    W = 31 + [ ( 13 * 10 - 1 ) / 5 ] + 8 + [ 8 / 4 ] + [ 20 / 4 ] - 2 * 20 =
      = 31 + 25 + 8 + 2 + 5 - 40 = 31
    Теперь делим W на 7 и находим остаток от деления: 31 / 7 = 4 и 3 в остатке.
    Тройка соответствует дню недели СРЕДА.
    """
    d, m, y = map(int, [d, m, y])
    if not is_date_correct(d, m, y):
        return -1

    if m < 3:
        y -= 1
    c = int(y / 100)
    y %= 100
    m -= 2
    if m < 1:
        m += 12
    W = (d + int((13 * m - 1) / 5) + y + int(y / 4) + int(c / 4) - 2 * c) % 7
    if W <= 0:
        W += 7
    return W


def Pascha(year):
    '''
    Вычисляем дату православной Пасхи
    '''
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = 3 + int((d + e + 21) / 31)
    day = (d + e + 21) % 31 + 1
    #Переход на григорианский календаь в России состаялся 26.01.1918г.
    #Ввод григорианского календаря в католических странах 5.10.1582г.
    #Вот тут надо подумать, какую дату ставить в сравнение?
    #Дата более ранняя - выдаём дату по юлианскому календарю
    if not is_gregorian(day, month, year):
        return [day, month, year]
    #Если дата более поздняя - пересчитываем на григорианский календарь
    delta = int(year / 100) - int(c / 4) - 2
    day, month, year = date_shift(day, month, year, delta)
    #Ближайшее раннее воскресенье
    a = get_day_of_week(day, month, year)
    if a < 7:
        day, month, year = date_shift(day, month, year, -a)
    return (day, month, year)


def is_gregorian(d, m, y, russia=True):
    '''
    сравниваем с датой введения григорианского  календаря
    Переход на григорианский календаь в России состаялся 26.01.1918г.
    Ввод григорианского календаря в католических странах 5.10.1582г.
    '''
    d, m, y = map(int, [d, m, y])
    dt = date_compare(d, m, y, 26, 1, 1918) if russia \
        else date_compare(d, m, y, 5, 10, 1582)
    return False if dt >= 0 else True


def get_old_style_date(d, m, y):
    '''
    возвращаем дату в старом стиле
    '''
    d, m, y = map(int, [d, m, y])
    # если до перехода на григорианский календарь - вернем туже дату
    if not is_gregorian(d, m, y):
        return [d, m, y]
    diff = 0
    if y % 100 == 0 and y % 400 != 0:
        diff = -1 if m < 3 else 0
    dt = len([
        x * 100
        for x in range(15, ((y + diff) / 100) + 1)
        if x * 100 % 400 != 0
    ]) - 1 + 10
    return date_shift(d, m, y, -1 * dt)




def month_range(date):
    return (
        datetime.date(
            date.year, date.month, 1
        ),
        datetime.date(
            date.year, date.month,
            num_days_in_month(date.month, date.year)
        )
    )



# pylint: disable=W0622, C0103
def sancta_datefrormat(date, format):
    """
    формат даты
    [iToday] - выведет вчера, сегодня или завтра,
        по отношению заданной даты к сегодняшнему числу

    [d]  - 2
    [dd] - 02

    [M]  - янв
    [M1] - январт
    [M2] - января
    [mm] - 01
    [m]  - 1

    [Y]  - 1983
    [y]  - 83
    [iY] - если текущий год отличается от года даты,
         то выведет год, иначе не выведет
    """

    date_arr = date_to_dict(date)

    if date_arr == today():
        iToday = u'Сегодня'
    elif date_shift(*(today()+[1])) == date_arr:
        iToday = u'Завтра'
    elif date_shift(*(today()+[-1])) == date_arr:
        iToday = u'Вчера'
    else:
        iToday = ''
    format = format.replace(u'[iToday]', iToday)

    format = format.replace(u'[d]', str(date_arr[0]))
    format = format.replace(u'[dd]', "{0:02d}".format(int(date_arr[0])))

    format = format.replace(u'[mm]', "{0:02d}".format(date_arr[1]))
    format = format.replace(u'[m]', str(date_arr[1]))

    format = format.replace('[M]', dt.MONTH_NAMES[date_arr[1] - 1][0])
    format = format.replace('[M1]', dt.MONTH_NAMES[date_arr[1] - 1][1])
    format = format.replace('[M2]', dt.MONTH_NAMES[date_arr[1] - 1][2])

    format = format.replace(u'[y]', str(date_arr[2])[2:4])
    format = format.replace(u'[Y]', str(date_arr[2]))

    format = format.replace(u'[iY]', '') \
        if today()[2] == date_arr[2] \
        else format.replace(u'[iY]', str(date_arr[2]))
    return format.encode('utf-8')
