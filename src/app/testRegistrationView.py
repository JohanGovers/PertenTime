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
        
        user_profiles = UserProfile.objects.all()
        
        self.assertEqual(len(user_profiles), 1)
        self.assertEqual(user_profiles[0].department_id, department_id)
        self.assertIsNotNone(user_profiles[0].submitted_until)
        self.assertEqual(user_profiles[0].user.username, username)
        self.assertEqual(user_profiles[0].user.email, email)
        self.assertEqual(user_profiles[0].user.first_name, first_name)
        self.assertEqual(user_profiles[0].user.last_name, last_name)
        self.assertIsNotNone(user_profiles[0].user.password)
        