from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from datetime import date

from app.models import TimeEntry
from app.model_helpers import add_department, add_project, add_time_entry, add_user

class ReportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('test_user', 'test@mail.com', 'password')
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
        
    def test_only_middle_user_has_time(self):
        """
        Three projects, three users only middle user has time. All users should be in the list.
        """
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile_1 = add_user('username1', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile_2, date(2015, 1, 12), 7)
        add_time_entry(project_c, user_profile_2, date(2015, 1, 13), 8)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'username': u'username1', 'submitted_until': date(2015, 1, 18), 'project_hours': ['', '', '']},
                            {'username': u'username2', 'submitted_until': date(2015, 1, 18), 'project_hours': [7, '', 8]},
                            {'username': u'username3', 'submitted_until': date(2015, 1, 18), 'project_hours': ['', '', '']}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_three_users_has_time(self):
        """
        Three projects, three users all users has time on all projects. All users should be in the list.
        """
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile_1 = add_user('username1', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile_1, date(2015, 1, 12), 1)
        add_time_entry(project_b, user_profile_1, date(2015, 1, 13), 2)
        add_time_entry(project_c, user_profile_1, date(2015, 1, 14), 3)
        
        add_time_entry(project_a, user_profile_2, date(2015, 1, 12), 4)
        add_time_entry(project_b, user_profile_2, date(2015, 1, 13), 5)
        add_time_entry(project_c, user_profile_2, date(2015, 1, 14), 6)
        
        add_time_entry(project_a, user_profile_3, date(2015, 1, 12), 7)
        add_time_entry(project_b, user_profile_3, date(2015, 1, 13), 8)
        add_time_entry(project_c, user_profile_3, date(2015, 1, 14), 9)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'username': u'username1', 'submitted_until': date(2015, 1, 18), 'project_hours': [1, 2, 3]},
                            {'username': u'username2', 'submitted_until': date(2015, 1, 18), 'project_hours': [4, 5, 6]},
                            {'username': u'username3', 'submitted_until': date(2015, 1, 18), 'project_hours': [7, 8, 9]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_no_time_on_middle_project(self):
        """
        Three projects (A, B, C) and one user with time on A and C.
        """
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile = add_user('username', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile, date(2015, 1, 12), 7)
        add_time_entry(project_c, user_profile, date(2015, 1, 13), 8)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [{'username': u'username', 'submitted_until': date(2015, 1, 18), 'project_hours': [7, '', 8]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
        
    def test_no_time_on_first_project(self):
        """
        Three users, three projects. No time reported on the first project.
        """
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile_1 = add_user('username1', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_b, user_profile_1, date(2015, 1, 12), 1)
        add_time_entry(project_c, user_profile_1, date(2015, 1, 14), 3)
        
        add_time_entry(project_b, user_profile_2, date(2015, 1, 12), 4)
        add_time_entry(project_c, user_profile_2, date(2015, 1, 14), 6)
        
        add_time_entry(project_b, user_profile_3, date(2015, 1, 12), 7)
        add_time_entry(project_c, user_profile_3, date(2015, 1, 14), 9)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'username': u'username1', 'submitted_until': date(2015, 1, 18), 'project_hours': ['', 1, 3]},
                            {'username': u'username2', 'submitted_until': date(2015, 1, 18), 'project_hours': ['', 4, 6]},
                            {'username': u'username3', 'submitted_until': date(2015, 1, 18), 'project_hours': ['', 7, 9]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_no_time_on_last_project(self):
        """
        Three users, three projects. No time reported on the third project.
        """
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile_1 = add_user('username1', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile_1, date(2015, 1, 12), 1)
        add_time_entry(project_b, user_profile_1, date(2015, 1, 13), 2)
        
        add_time_entry(project_a, user_profile_2, date(2015, 1, 12), 4)
        add_time_entry(project_b, user_profile_2, date(2015, 1, 13), 5)
        
        add_time_entry(project_a, user_profile_3, date(2015, 1, 12), 7)
        add_time_entry(project_b, user_profile_3, date(2015, 1, 13), 8)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'username': u'username1', 'submitted_until': date(2015, 1, 18), 'project_hours': [1, 2, '']},
                            {'username': u'username2', 'submitted_until': date(2015, 1, 18), 'project_hours': [4, 5, '']},
                            {'username': u'username3', 'submitted_until': date(2015, 1, 18), 'project_hours': [7, 8, '']}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_don_not_count_time_after_submitted_until(self):
        project_a = add_project('project a')
        project_b = add_project('project b')
        project_c = add_project('project c')
        
        department = add_department('code', 'name')
        user_profile = add_user('username', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile, date(2015, 1, 12), 7)
        add_time_entry(project_b, user_profile, date(2015, 1, 12), 1)
        add_time_entry(project_c, user_profile, date(2015, 1, 13), 8)
        
        add_time_entry(project_a, user_profile, date(2015, 1, 19), 7)
        add_time_entry(project_b, user_profile, date(2015, 1, 19), 1)
        add_time_entry(project_c, user_profile, date(2015, 1, 20), 8)
        
        response = self.client.get(reverse('app.views.report'))
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [{'username': u'username', 'submitted_until': date(2015, 1, 18), 'project_hours': [7, 1, 8]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    