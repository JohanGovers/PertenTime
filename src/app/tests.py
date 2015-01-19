from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from app.models import TimeEntry

class ReportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'test@mail.com', 'password')
        
    def test_report_view_with_no_data(self):
        """
        If no data exists display a helpful no data message.
        """
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No data available")
        self.assertEqual(len(response.context['data']), 0)