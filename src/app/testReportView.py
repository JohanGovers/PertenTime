from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from datetime import date

from app.models import TimeEntry, UserProfile
from app.model_helpers import add_department, add_project, add_time_entry, add_user

class ReportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('__test_user', 'test@mail.com', 'password')
        department = add_department('_T', 'Test')
        up = UserProfile(user=self.user)
        up.department = department
        up.submitted_until = date(2012,1,11)
        up.save()
        
        self.client.login(username='__test_user', password='password')
    
    def assert_projects(self, responseProjects, projects):
        for i, project in enumerate(projects):
            self.assertEqual(responseProjects[i].name, project.name)
        return

    def test_date_filter(self):
            """
            Test the filter on submitted_until. Make sure time is included as
            it should.
            """
            project_a = add_project('a', 'project a')
            
            department1 = add_department('code1', 'name1')
            user_profile_1 = add_user('username1', 'password', 'first_name', 'last_name', 'email', department1, date(2015, 1, 18))
            
            add_time_entry(project_a, user_profile_1, date(2014, 12, 31), 6)
            add_time_entry(project_a, user_profile_1, date(2015, 1, 1), 7)
            add_time_entry(project_a, user_profile_1, date(2015, 1, 18), 8)
            add_time_entry(project_a, user_profile_1, date(2015, 1, 19), 9)
                        
            response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
            self.assertEqual(response.status_code, 200)
            
            expected_projects = [project_a]
            expected_data = [
                                {'name': u' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['']},
                                {'name': u'first_name last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [15]}]
                                            
            self.assert_projects(response.context['projects'], expected_projects)
            
            self.assertEqual(response.context['data'], expected_data)
    

    def test_only_middle_user_has_time(self):
        """
        Three projects, three users only middle user has time. All users should be in the list.
        """
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
        project_c = add_project('c', 'project c')
        
        department1 = add_department('code1', 'name1')
        department2 = add_department('code2', 'name2')
        user_profile_1 = add_user('username1', 'password', 'first_name1', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name2', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name3', 'last_name', 'email', department2, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile_2, date(2015, 1, 12), 7)
        add_time_entry(project_c, user_profile_2, date(2015, 1, 13), 8)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'name': u' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': u'first_name1 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': u'first_name2 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [7, '', 8]},
                            {'name': u'first_name3 last_name', 'department': department2.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': ['', '', '']}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_three_users_has_time(self):
        """
        Three projects, three users all users has time on all projects. All users should be in the list.
        """
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
        project_c = add_project('c', 'project c')
        
        department1 = add_department('code1', 'name1')
        department2 = add_department('code2', 'name2')
        user_profile_1 = add_user('username1', 'password', 'first_name1', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name2', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name3', 'last_name', 'email', department2, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile_1, date(2015, 1, 12), 1)
        add_time_entry(project_b, user_profile_1, date(2015, 1, 13), 2)
        add_time_entry(project_c, user_profile_1, date(2015, 1, 14), 3)
        
        add_time_entry(project_a, user_profile_2, date(2015, 1, 12), 4)
        add_time_entry(project_b, user_profile_2, date(2015, 1, 13), 5)
        add_time_entry(project_c, user_profile_2, date(2015, 1, 14), 6)
        
        add_time_entry(project_a, user_profile_3, date(2015, 1, 12), 7)
        add_time_entry(project_b, user_profile_3, date(2015, 1, 13), 8)
        add_time_entry(project_c, user_profile_3, date(2015, 1, 14), 9)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'name': u' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': u'first_name1 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [1, 2, 3]},
                            {'name': u'first_name2 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [4, 5, 6]},
                            {'name': u'first_name3 last_name', 'department': department2.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [7, 8, 9]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_no_time_on_middle_project(self):
        """
        Three projects (A, B, C) and one user with time on A and C.
        """
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
        project_c = add_project('c', 'project c')
        
        department = add_department('code', 'name')
        user_profile = add_user('username', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile, date(2015, 1, 12), 7)
        add_time_entry(project_c, user_profile, date(2015, 1, 13), 8)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': 'first_name last_name', 'department': department.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [7, '', 8]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
        
    def test_no_time_on_first_project(self):
        """
        Three users, three projects. No time reported on the first project.
        """
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
        project_c = add_project('c', 'project c')
        
        department1 = add_department('code1', 'name1')
        department2 = add_department('code2', 'name2')
        user_profile_1 = add_user('username1', 'password', 'first_name1', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name2', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name3', 'last_name', 'email', department2, date(2015, 1, 18))
        
        add_time_entry(project_b, user_profile_1, date(2015, 1, 12), 1)
        add_time_entry(project_c, user_profile_1, date(2015, 1, 14), 3)
        
        add_time_entry(project_b, user_profile_2, date(2015, 1, 12), 4)
        add_time_entry(project_c, user_profile_2, date(2015, 1, 14), 6)
        
        add_time_entry(project_b, user_profile_3, date(2015, 1, 12), 7)
        add_time_entry(project_c, user_profile_3, date(2015, 1, 14), 9)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': 'first_name1 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': ['', 1, 3]},
                            {'name': 'first_name2 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': ['', 4, 6]},
                            {'name': 'first_name3 last_name', 'department': department2.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': ['', 7, 9]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_no_time_on_last_project(self):
        """
        Three users, three projects. No time reported on the third project.
        """
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
        project_c = add_project('c', 'project c')
        
        department1 = add_department('code1', 'name1')
        department2 = add_department('code2', 'name2')
        user_profile_1 = add_user('username1', 'password', 'first_name1', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name2', 'last_name', 'email', department1, date(2015, 1, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name3', 'last_name', 'email', department2, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile_1, date(2015, 1, 12), 1)
        add_time_entry(project_b, user_profile_1, date(2015, 1, 13), 2)
        
        add_time_entry(project_a, user_profile_2, date(2015, 1, 12), 4)
        add_time_entry(project_b, user_profile_2, date(2015, 1, 13), 5)
        
        add_time_entry(project_a, user_profile_3, date(2015, 1, 12), 7)
        add_time_entry(project_b, user_profile_3, date(2015, 1, 13), 8)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': 'first_name1 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [1, 2, '']},
                            {'name': 'first_name2 last_name', 'department': department1.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [4, 5, '']},
                            {'name': 'first_name3 last_name', 'department': department2.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [7, 8, '']}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_don_not_count_time_after_submitted_until(self):
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
        project_c = add_project('c', 'project c')
        
        department = add_department('code', 'name')
        user_profile = add_user('username', 'password', 'first_name', 'last_name', 'email', department, date(2015, 1, 18))
        
        add_time_entry(project_a, user_profile, date(2015, 1, 12), 7)
        add_time_entry(project_b, user_profile, date(2015, 1, 12), 1)
        add_time_entry(project_c, user_profile, date(2015, 1, 13), 8)
        
        add_time_entry(project_a, user_profile, date(2015, 1, 19), 7)
        add_time_entry(project_b, user_profile, date(2015, 1, 19), 1)
        add_time_entry(project_c, user_profile, date(2015, 1, 20), 8)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-01-01', 'to_date': '2015-01-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
                            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
                            {'name': 'first_name last_name', 'department': department.code, 'submitted_until': date(2015, 1, 18), 'late_submission': True, 'project_hours': [7, 1, 8]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
    
    def test_only_count_time_for_specified_month(self):
        project_a = add_project('a', 'project a')
        project_b = add_project('b', 'project b')
     
        department = add_department('code', 'name')
        user_profile_1 = add_user('username1', 'password', 'first_name1', 'last_name', 'email', department, date(2015, 5, 18))
        user_profile_2 = add_user('user with entries in other month', 'password', 'first_name2', 'last_name', 'email', department, date(2015, 5, 18))
        user_profile_3 = add_user('user with no entries', 'password', 'first_name3', 'last_name', 'email', department, date(2015, 5, 18))
        
        add_time_entry(project_a, user_profile_1, date(2015, 2, 12), 6)
        add_time_entry(project_a, user_profile_1, date(2015, 3, 2), 7)
        add_time_entry(project_a, user_profile_1, date(2015, 4, 2), 8)
        
        add_time_entry(project_b, user_profile_2, date(2015, 4, 4), 5)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-03-01', 'to_date': '2015-03-31'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b]
        expected_data = [
            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '']},
            {'name': 'first_name1 last_name', 'department': department.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': [7, '']},
            {'name': 'first_name2 last_name', 'department': department.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': ['', '']},
            {'name': 'first_name3 last_name', 'department': department.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': ['', '']},
        ]
        
        self.assert_projects(response.context['projects'], expected_projects)
        
        self.assertEqual(response.context['data'], expected_data)
        
    def test_order(self):
        project_b = add_project('b', 'project 1b')
        project_a = add_project('a', 'project 2a')
        project_c = add_project('c', 'project 1c')
     
        department1 = add_department('1', 'name')
        department2 = add_department('2', 'name')
        department3 = add_department('3', 'name')
        
        user_profile_1 = add_user('username1', 'password', 'first_name1', 'last_name', 'email', department2, date(2015, 5, 18))
        user_profile_2 = add_user('username2', 'password', 'first_name2', 'last_name', 'email', department3, date(2015, 5, 18))
        user_profile_3 = add_user('username3', 'password', 'first_name3', 'last_name', 'email', department1, date(2015, 5, 18))
        user_profile_4 = add_user('username4', 'password', 'a first_name4', 'last_name', 'email', department1, date(2015, 5, 18))
        user_profile_5 = add_user('user5', 'password', 'first_name5', 'last_name', 'email', department2, date(2015, 5, 18))
        
        add_time_entry(project_a, user_profile_1, date(2015, 2, 12), 6)
        add_time_entry(project_b, user_profile_2, date(2015, 2, 2), 7)
        add_time_entry(project_c, user_profile_3, date(2015, 2, 2), 8)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-02-01', 'to_date': '2015-02-28'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a, project_b, project_c]
        expected_data = [
            {'name': 'a first_name4 last_name', 'department': department1.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': ['', '', '']},
            {'name': 'first_name3 last_name', 'department': department1.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': ['', '', 8]},
            {'name': 'first_name1 last_name', 'department': department2.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': [6, '', '']},
            {'name': 'first_name5 last_name', 'department': department2.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': ['', '', '']},
            {'name': 'first_name2 last_name', 'department': department3.code, 'submitted_until': date(2015, 5, 18), 'late_submission': False, 'project_hours': ['', 7, '']},
            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['', '', '']},
            ]
        
        self.assert_projects(response.context['projects'], expected_projects)
        self.assertEqual(response.context['data'], expected_data)
        
    def test_filter_boundaries(self):
        project_a = add_project('a', 'project a')
        
        department = add_department('code', 'name')
        user_profile = add_user('username', 'password', 'first_name', 'last_name', 'email', department, date(2015, 5, 31))
        
        add_time_entry(project_a, user_profile, date(2015, 5, 1), 7)
        add_time_entry(project_a, user_profile, date(2015, 5, 3), 8)
        
        response = self.client.post(reverse('report'), {'from_date': '2015-5-1', 'to_date': '2015-5-3'})
        self.assertEqual(response.status_code, 200)
        
        expected_projects = [project_a]
        expected_data = [
                            {'name': ' ', 'department': '_T', 'submitted_until': date(2012, 1, 11), 'late_submission': True, 'project_hours': ['']},
                            {'name': 'first_name last_name', 'department': department.code, 'submitted_until': date(2015, 5, 31), 'late_submission': False, 'project_hours': [15]}]
        
        self.assert_projects(response.context['projects'], expected_projects)
        self.assertEqual(response.context['data'], expected_data)
        
    def test_incorrect_from_date(self):
        response = self.client.post(reverse('report'), {'from_date': '2015-2-29', 'to_date': '2015-5-3'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'filter_form', 'from_date', 'Enter a valid date.')
        
    def test_incorrect_to_date(self):
        response = self.client.post(reverse('report'), {'from_date': '2015-2-28', 'to_date': '2015-5-32'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'filter_form', 'to_date', 'Enter a valid date.')