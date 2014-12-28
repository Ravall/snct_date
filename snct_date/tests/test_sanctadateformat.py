# -*- coding: utf-8 -*-
from unittest import TestCase
from datetime import date
from testutil import data_provider
from snct_date.date import sancta_datefrormat


class SanctaDatefrormatTest(TestCase):
    # pylint: disable=E0211
    def provider_formats():
        today_year = date.today().year
        return (
            (date(1983, 11, 3), '[d].[m].[y]', '3.11.83'),
            (date(1983, 11, 3), '[dd].[m].[iY]', '03.11.1983'),
            (date(1983, 9, 3), '[dd].[m].[iY]', '03.9.1983'),
            (date(1983, 9, 3), '[dd].[mm].[iY]', '03.09.1983'),
            (date(1983, 11, 3), '[d].[m].[Y]', '3.11.1983'),
            (date(1983, 11, 3), '[d].[m].[iY]', '3.11.1983'),
            (date(1983, 11, 3), '[d] [M]. [Y]', '3 ноя. 1983'),
            (date(1983, 11, 3), '[M1] [Y]', 'ноябрь 1983'),
            (date(1983, 11, 3), '[d] [M2] [Y]', '3 ноября 1983'),
            (date(today_year, 11, 3), '[M1][iY]', 'ноябрь'),

        )

    @data_provider(provider_formats)
    def test_dateformat(self, my_date, date_format, result):
        self.assertEqual(
            sancta_datefrormat(my_date, date_format), result
        )
