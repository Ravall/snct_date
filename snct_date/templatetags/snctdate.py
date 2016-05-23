# -*- coding: utf-8 -*-
from django import template
from snct_date.date import (
    sancta_datefrormat, date_to_dict, get_old_style_date,
    yyyy_mm_dd, num_days_in_month, date_shift,orth_month
)


# pylint: disable=C0103
register = template.Library()


@register.filter
def snct_dateformat(date, date_format):
    return sancta_datefrormat(date, date_format)


@register.filter
def snct_dinc(date, diff):
    return yyyy_mm_dd(
        date_shift(
            *(date_to_dict(date) + [int(diff)])
        )
    )


@register.filter
def number_month(date, case):
    number = date_to_dict(date)[1]
    return orth_month[case][number-1]

@register.filter
def snct_minc(date, diff):

    diff = int(diff)
    _date = date_to_dict(date)
    sign = diff/abs(diff)
    sift = 0
    for i in xrange(min(0, diff), max(0, diff)):
        sift += num_days_in_month(_date[1], _date[2])
        _date = date_shift(
            *(_date + [sign*sift])
        )
    return yyyy_mm_dd(_date)


#@register.filter
#def snct_yinc(date, diff):
#    return date_inc(date, 0, 0, diff)


@register.filter
def old_style(date):
    '''
    переводит дату в старый стиль
    '''
    return yyyy_mm_dd(get_old_style_date(*(date.split('-')[::-1])))