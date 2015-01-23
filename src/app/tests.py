from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from datetime import date

from app.models import TimeEntry
from app.model_helpers import add_department, add_project, add_time_entry, add_user

class ReportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'test@mail.com', 'password')
        self.client.login(username='test_user', password='password')
    
    def assert_projects(self, responseProjects, projects):
        for i, project in enumerate(projects):
            self.assertEqual(responseProjects[i].name, project.name)
        return
    
    
    def test_no_data_displays_helpful_message(self):
        """
        If no data exists display a helpful no data message.
        """
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No data available")
        self.assertEqual(len(response.context['data']), 0)
        
    def test_with_gap(self):
        """
        Three projects (A, B, C) and one user with time on A and C.
        """
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile = add_user('username', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile, date(2015, 1, 12), 8)
        add_time_entry(project_c, user_profile, date(2015, 1, 13), 8)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [{'username': u'username', 'submitted_until': date(2015, 1, 18), 'project_hours': [8, '', 8]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
        
    def first_user_has_no_time(self):
        return
        
    def no_time_on_first_project(self):
        return
    
    def don_not_count_time_after_submitted_until(self):
        return
    