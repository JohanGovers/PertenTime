from django.test import TestCase
from datetime import date
from app.date_helpers import *

class DateHelperTests(TestCase):
    def test_get_last_of_january_2015(self):
        """
        Test that a date in february 2015 returns last of january
        """
        self.assertEquals(
            get_last_date_of_previous_month(date(2015,2,25)), 
                                            date(2015,1,31))
        
    def test_get_last_of_leap_year(self):
            """
            Test that a date with after a leap year returns a leap year
            """
            self.assertEquals(
                get_last_date_of_previous_month(date(2015,3,25)), 
                                                date(2015,2,28))
            
    def test_get_last_of_year_shift(self):
            """
            Test that a date in january returns the last of december
            the previous year.
            """
            self.assertEquals(
                get_last_date_of_previous_month(date(2012,1,11)), 
                                                date(2011,12,31))
            
    def test_current_date_has_later_day_than_last_day_of_previous_month(self):
                """
                Test 2015-03-30 since it failed.
                """
                self.assertEquals(
                    get_last_date_of_previous_month(date(2015,3,30)), 
                                                    date(2015,2,28))        
    
    def test_string_2015_05_03_to_date(self):
        """
        Parse date string happy case 2015-05-03.
        """
        self.assertEquals(string_to_date("2015-05-03"), date(2015,5,3))
        
    def test_string_to_date_without_leading_zeroes(self):
        """
        Parse date string 2015-5-3 without leading zeroes.
        """
        self.assertEquals(string_to_date("2015-5-3"), date(2015,5,3))