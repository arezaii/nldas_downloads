# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:33:39 2019

@author: Ahmad Rezaii
"""

import unittest
import download_nldas_forcings as nldas
from datetime import datetime


class TestDownloadNLDASForcingsMonthDiff(unittest.TestCase):

    def test_month_diff_1_month(self):
        self.assertEqual(nldas.month_difference(datetime(2010, 10, 1), datetime(2010, 11, 1)), 1)

    def test_month_diff_gt_1_yr(self):
        self.assertEqual(nldas.month_difference(datetime(2010, 10, 1), datetime(2011, 12, 1)), 14)

    def test_month_diff_eq_1_yr(self):
        self.assertEqual(nldas.month_difference(datetime(2010, 10, 1), datetime(2011, 10, 1)), 12)

    def test_month_diff_lt_1_yr(self):
        self.assertEqual(nldas.month_difference(datetime(2010, 10, 1), datetime(2011, 8, 1)), 10)

    def test_month_diff_neg(self):
        self.assertEqual(nldas.month_difference(datetime(2010, 10, 1), datetime(2010, 8, 1)), -2)

    def test_month_diff_no_diff(self):
        self.assertEqual(nldas.month_difference(datetime(2010, 10, 1), datetime(2010, 10, 15)), 0)


class TestDownloadNLDASForcingsURLList(unittest.TestCase):

    def setUp(self) -> None:
        self.one_day_urls = nldas.get_url_list(datetime(2010, 10, 1), datetime(2010, 10, 1),
                                               nldas.FORCINGS_DATA_SETS['hourly'])
        self.one_year_urls = nldas.get_url_list(datetime(2010, 10, 1), datetime(2011, 10, 1),
                                                nldas.FORCINGS_DATA_SETS['monthly'])
        self.one_month_url = nldas.get_url_list(datetime(2010, 10, 1), datetime(2010, 10, 1),
                                                nldas.FORCINGS_DATA_SETS['monthly'])

    def test_get_urls_24_per_day(self):
        self.assertEqual(len(self.one_day_urls), 24)

    def test_get_urls_hourly_format(self):
        self.assertEqual(self.one_day_urls[0],
                         'https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.002/2010/274/NLDAS_FORA0125_H.A20101001.0000.002.grb')
        self.assertEqual(self.one_day_urls[23],
                         'https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.002/2010/274/NLDAS_FORA0125_H.A20101001.2300.002.grb')

    def test_get_urls_13_per_year(self):
        self.assertEqual(len(self.one_year_urls), 13)

    def test_get_urls_monthly_1_month(self):
        self.assertEqual(len(self.one_month_url), 1)

    def test_get_urls_monthly_format(self):
        self.assertEqual(self.one_year_urls[0],
                         'https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_M.002/2010/NLDAS_FORA0125_M.A201010.002.grb')
        self.assertEqual(self.one_year_urls[12],
                         'https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_M.002/2011/NLDAS_FORA0125_M.A201110.002.grb')


if __name__ == '__main__':
    unittest.main()
