import datetime, calendar
from datetime import timedelta

from django.shortcuts import render
from django.db.models import Prefetch, Sum, F, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.models import Project, TimeEntry, UserProfile
from app.forms import ReportFilterForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def report(request):
    if (request.method == 'GET'):
        now = datetime.datetime.now().date()
        this_month_day_count = calendar.monthrange(now.year, now.month)[1]
        base_date = now - timedelta(days=this_month_day_count)
        base_date = base_date.replace(day=1) #there is always a first in every month
                
        start_date = base_date.replace(day=1)
        end_day = calendar.monthrange(base_date.year, base_date.month)[1]
        end_date = base_date.replace(day=end_day)
        
        filter_form = ReportFilterForm(initial={'from_date': start_date, 'to_date': end_date})
    else:
        filter_form = ReportFilterForm(request.POST)
        if(filter_form.is_valid()):
            data = filter_form.cleaned_data
            start_date = data['from_date']
            end_date= data['to_date']
        else:
            return render(request, 'app/report.html', {'data': [], 'filter_form': filter_form})
        
    return report_response(request, filter_form, start_date, end_date)
    
def report_response(request, filter_form, start_date, end_date):
    projects = Project.objects.order_by('code')
    
    user_data = TimeEntry.objects.filter(userprofile__submitted_until__gte=F('date'), date__gte=start_date, date__lte=end_date)
    user_data = user_data.values('project__name', 'project__code', 'userprofile__user__username', 'userprofile__department__code', 'userprofile__submitted_until')
    user_data = user_data.annotate(total_hours=Sum('hours')).order_by('userprofile__department__code', 'userprofile__user__username', 'project__code')

    users_with_no_data = list(User.objects.exclude(username__in=user_data.values('userprofile__user__username'))
                            .values('username', 'userprofile__submitted_until', 'userprofile__department__code')
                            .order_by('userprofile__department__code', 'username'))
    
    context_dict = {'data': [], 'projects': projects,
        'filter_form': filter_form}
    
    current_user = ''
    user_project_hours = []
    latest_project_added = ''
    for data_entry in user_data:
        if data_entry['userprofile__user__username'] != current_user:
            if current_user != data_entry['userprofile__user__username'] and current_user != '':
                while len(user_project_hours) < len(projects):
                    user_project_hours.append('')
                    
            user_project_hours = []
            latest_project_added = ''
            current_user = data_entry['userprofile__user__username']
            
            if len(users_with_no_data) > 0:
                while users_with_no_data[0]['userprofile__department__code'] < data_entry['userprofile__department__code'] or users_with_no_data[0]['userprofile__department__code'] == data_entry['userprofile__department__code'] and users_with_no_data[0]['username'] < current_user:
                    context_dict['data'].append({
                                         'username': users_with_no_data[0]['username'],
                                         'department': users_with_no_data[0]['userprofile__department__code'],
                                         'submitted_until': users_with_no_data[0]['userprofile__submitted_until'], 
                                         'late_submission': users_with_no_data[0]['userprofile__submitted_until'] < end_date,
                                         'project_hours': ['' for i in range(len(projects))]})
                    users_with_no_data.pop(0)
                    if(len(users_with_no_data) == 0):
                        break
            
            context_dict['data'].append({'username': data_entry['userprofile__user__username'], 
                                         'department': data_entry['userprofile__department__code'],
                                         'submitted_until': data_entry['userprofile__submitted_until'], 
                                         'late_submission': data_entry['userprofile__submitted_until'] < end_date,
                                         'project_hours': user_project_hours})
            
        for project in projects:
            if data_entry['project__code'] == project.code:
                user_project_hours.append(data_entry['total_hours'])
                latest_project_added = project.code
                break
            elif latest_project_added < project.code < data_entry['project__code']: 
                user_project_hours.append('')
                
    while len(user_project_hours) < len(projects):
                    user_project_hours.append('')        
    
    while len(users_with_no_data) > 0:
        context_dict['data'].append({'username': users_with_no_data[0]['username'],
                             'department': users_with_no_data[0]['userprofile__department__code'],
                             'submitted_until': users_with_no_data[0]['userprofile__submitted_until'], 
                             'late_submission': users_with_no_data[0]['userprofile__submitted_until'] < end_date,
                             'project_hours': ['' for i in range(len(projects))]})
        users_with_no_data.pop(0)
    
    return render(request, 'app/report.html', context_dict)