from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from app.models import Department, UserProfile
from app.model_helpers import add_department

class RegistrationViewTests(TestCase):
    def setUp(self):
        self.test_department = add_department('42', 'Unit testers')
    
    def test_can_load_form(self):
        """
        Load the registration view form
        """
        
        response = self.client.get(reverse('app.views.register'))
        self.assertEqual(response.status_code, 200)
        
    def test_can_create_user(self):
        """
        Create a user using the form
        """
              
        username = "username"
        email = "username@pertenTime.com"
        first_name = "Bob"
        last_name = "Tester"
        password = "secret"
        department_id = self.test_department.id
        
        post_data = {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'password': password, 'department': department_id}
        
        response = self.client.post(reverse('app.views.register'), post_data)
        self.assertEqual(response.status_code, 200)