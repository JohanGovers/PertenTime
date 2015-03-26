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
    