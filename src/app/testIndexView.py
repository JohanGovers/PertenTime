from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from datetime import date

from app.models import UserProfile
from app.model_helpers import add_department

class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('__test_user', 'test@mail.com', 'password')
        test_department = add_department('42', 'Unit testers')
        up = UserProfile(user=self.user)
        up.department = test_department
        up.submitted_until = date(2012,1,11)
        up.save()
        
        self.client.login(username='__test_user', password='password')
        
    def test_can_set_last_submitted(self):
        """
        Set last submitted without providing a value for hideFutureWarnings
        """
        new_date = date(2013,4,5)
        new_date_string = new_date.strftime("%Y-%m-%d")
        post_data = {'date': new_date_string}
        
        response = self.client.post(reverse('app.views.set_last_submitted'), post_data)
        self.assertEqual(response.status_code, 200)
        
        user_profiles = UserProfile.objects.all()
        
        self.assertEqual(len(user_profiles), 1)
        self.assertEqual(user_profiles[0].submitted_until, new_date)
        self.assertEqual(user_profiles[0].skip_confirm_submit_dialog, False)
        
    def test_can_set_last_submitted_without_hiding_future_warnings(self):
        """
        Set last submitted with hideFutureWarnings set to false
        """
        new_date = date(2013,4,5)
        new_date_string = new_date.strftime("%Y-%m-%d")
        post_data = {'date': new_date_string, 'skipFutureWarnings': 'false'}
        
        response = self.client.post(reverse('app.views.set_last_submitted'), post_data)
        self.assertEqual(response.status_code, 200)
        
        user_profiles = UserProfile.objects.all()
        
        self.assertEqual(len(user_profiles), 1)
        self.assertEqual(user_profiles[0].submitted_until, new_date)
        self.assertEqual(user_profiles[0].skip_confirm_submit_dialog, False)
        
    def test_can_set_last_submitted_and_hide_future_warnings(self):
        """
        Set last submitted with hideFutureWarnings set to true
        """
        new_date = date(2013,4,5)
        new_date_string = new_date.strftime("%Y-%m-%d")
        post_data = {'date': new_date_string, 'skipFutureWarnings': 'true'}
        
        response = self.client.post(reverse('app.views.set_last_submitted'), post_data)
        self.assertEqual(response.status_code, 200)
        
        user_profiles = UserProfile.objects.all()
        
        self.assertEqual(len(user_profiles), 1)
        self.assertEqual(user_profiles[0].submitted_until, new_date)
        self.assertEqual(user_profiles[0].skip_confirm_submit_dialog, True)