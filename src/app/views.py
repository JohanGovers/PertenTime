import datetime, json, calendar
from datetime import timedelta
from django.shortcuts import render
from django.db.models import Prefetch, Sum, F, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.models import Project, TimeEntry, UserProfile
from app.forms import UserForm, UserProfileForm

from app.date_helpers import *

#TODO: Split into multiple files. 

@login_required
def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def report(request):
    projects = Project.objects.order_by('code')
    
    now = datetime.datetime.now()
    this_month_day_count = calendar.monthrange(now.year, now.month)[1]
    base_date = datetime.datetime.now() - timedelta(days=this_month_day_count)
    base_date = base_date.replace(day=1) #there is always a first in every month
    if 'month' in request.GET:
        base_date = base_date.replace(month=int(request.GET['month']))
    if 'year' in request.GET:
        base_date = base_date.replace(year=int(request.GET['year']))
    
    if base_date.month == 12:
        next_year = base_date.year + 1
        next_month = 1
        previous_year = base_date.year
        previous_month = base_date.month - 1
    elif base_date.month == 1:
        next_year = base_date.year
        next_month = base_date.month + 1
        previous_year = base_date.year - 1
        previous_month = 12
    else:
        next_year = base_date.year
        next_month = base_date.month + 1
        previous_year = base_date.year
        previous_month = base_date.month - 1
        
    start_date = base_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_day = calendar.monthrange(base_date.year, base_date.month)[1]
    end_date = base_date.replace(day=end_day, hour=23, minute=59, second=59, microsecond=999999)
    
    user_data = TimeEntry.objects.filter(userprofile__submitted_until__gte=F('date'), date__gte=start_date, date__lte=end_date)
    user_data = user_data.values('project__name', 'project__code', 'userprofile__user__username', 'userprofile__department__code', 'userprofile__submitted_until')
    user_data = user_data.annotate(total_hours=Sum('hours')).order_by('userprofile__department__code', 'userprofile__user__username', 'project__code')

    users_with_no_data = list(User.objects.exclude(username__in=user_data.values('userprofile__user__username'))
                            .values('username', 'userprofile__submitted_until', 'userprofile__department__code')
                            .order_by('userprofile__department__code', 'username'))
    
    context_dict = {'data': [], 'projects': projects,
        'year': base_date.year, 'month': base_date.month,
        'query_for_previous': '?year={0}&month={1}'.format(previous_year, previous_month),
        'query_for_next': '?year={0}&month={1}'.format(next_year, next_month)}
    
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
                                         'late_submission': users_with_no_data[0]['userprofile__submitted_until'] < end_date.date(),
                                         'project_hours': ['' for i in range(len(projects))]})
                    users_with_no_data.pop(0)
                    if(len(users_with_no_data) == 0):
                        break
            
            context_dict['data'].append({'username': data_entry['userprofile__user__username'], 
                                         'department': data_entry['userprofile__department__code'],
                                         'submitted_until': data_entry['userprofile__submitted_until'], 
                                         'late_submission': data_entry['userprofile__submitted_until'] < end_date.date(),
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
                             'late_submission': users_with_no_data[0]['userprofile__submitted_until'] < end_date.date(),
                             'project_hours': ['' for i in range(len(projects))]})
        users_with_no_data.pop(0)
    
    return render(request, 'app/report.html', context_dict)

@login_required
def get_time_entries(request):
    userprofile = UserProfile.objects.get(user=request.user)
    # TODO: Prefetch does not work here. It spams the db with queries. 
    projects = Project.objects.order_by('code').prefetch_related(Prefetch('timeentry_set', queryset=TimeEntry.objects.order_by('date').filter(userprofile=userprofile)))

    date_parse_string = "%Y-%m-%d"
    if 'startDate' in request.GET:        
        start_date = datetime.datetime.strptime(request.GET['startDate'], date_parse_string).date()
    else:
        # sunday +1, monday +0, tuesday -1, wednesday -2, thursday -3, friday -4, saturday -5
        weekday_nr = userprofile.submitted_until.isoweekday()
        if weekday_nr == 7:
            start_date = userprofile.submitted_until + timedelta(days=1)
        else:
            start_date = userprofile.submitted_until - timedelta(days=weekday_nr - 1)
            
    end_date = start_date + timedelta(days=6)
    
    response_data = {
        'projects': [],
        'submittedUntil': userprofile.submitted_until.strftime(date_parse_string),
        'startDate': start_date.strftime(date_parse_string),
        'endDate': end_date.strftime(date_parse_string)}
    
    for project in projects:
        current_date = start_date
        p = {'id': project.id,
             'code': project.code,
             'name': project.name,
             'timeentries': []}
    
        while current_date <= end_date:
            # TODO: This is where the excess queries happen
            entry = project.timeentry_set.filter(date=current_date, userprofile=userprofile).first()
            p['timeentries'].append({'date': current_date.strftime('%Y-%m-%d'),
                                      'hours': str(entry.hours) if entry else None,
                                      'submitted': current_date <= userprofile.submitted_until})
            
            current_date += datetime.timedelta(days=1)
            
        response_data['projects'].append(p)

    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json")

@login_required
def save_time_entry(request):
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        project_id = request.POST.get('projectId')
        project = Project.objects.get(id=project_id)
        date = request.POST.get('date')
        hours = request.POST.get('hours')
        
        entry, created = TimeEntry.objects.get_or_create(project=project, date=date, userprofile=userprofile)
        entry.hours = hours if hours != '' else 0
        entry.save()
        
        response_data = {}
        response_data['msg'] = 'Added new entry with hours set to ' + str(hours) if created else 'Updated existing entry to ' + str(hours)
        
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse()

@login_required        
def set_last_submitted(request):
    if request.method == 'POST':
        new_date = request.POST.get('date')
        
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.submitted_until = new_date
        userprofile.save()
        
        return HttpResponse('Last submetted set to ' + new_date)
    else:
        return HttpResponse()
        
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.submitted_until = get_last_date_of_previous_month(datetime.datetime.now())
            profile.save()

            registered = True

        else:
            print (user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'app/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'app/login.html', {})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')