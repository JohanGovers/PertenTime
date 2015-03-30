from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import date
from app import urls
from app.models import UserProfile
from app.model_helpers import add_department#, add_project, add_time_entry, add_user

class BrowseUrlTests(TestCase):
    def setUp(self):
            self.client = Client()
            self.user = User.objects.create_superuser('__test_user', 'test@mail.com', 'password')
            department = add_department('_T', 'Test')
            up = UserProfile(user=self.user)
            up.department = department
            up.submitted_until = date(2012,1,11)
            up.save()
            
            self.client.login(username='__test_user', password='password')
    
    def test_get_all_urls(self):
        """
        Loop through all urls and make sure they return status code 200.
        """

        accepted_codes = [200, 302]
        
        # print(urls.urlpatterns)
        for url in urls.urlpatterns:
            response = self.client.get(reverse(url.name))
            self.assertTrue(response.status_code in accepted_codes)
                
        