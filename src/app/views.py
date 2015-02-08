import datetime, json
from datetime import timedelta
from django.shortcuts import render
from django.db.models import Prefetch, Sum, F, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.models import Project, TimeEntry, UserProfile
from app.forms import UserForm, UserProfileForm


#TODO: Split into multiple files. Multiple apps even?

@login_required
def index(request):
    return render(request, 'app/index.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def report(request):
    projects = Project.objects.order_by('name')
    
    user_data = TimeEntry.objects.filter(user_profile__submitted_until__gte=F('date'))
    user_data = user_data.values('project__name', 'user_profile__user__username', 'user_profile__submitted_until')
    user_data = user_data.annotate(total_hours=Sum('hours')).order_by('user_profile__user__username', 'project__name')

    users_with_no_data = list(UserProfile.objects.annotate(num_timeentries=Count('timeentry')).filter(num_timeentries=0).order_by('user__username').values('user__username', 'submitted_until'))
    
    context_dict = {'data': [], 'projects': projects}
    
    current_user = ''
    user_project_hours = []
    latest_project_added = ''
    for data_entry in user_data:
        if data_entry['user_profile__user__username'] != current_user:
            if current_user != data_entry['user_profile__user__username'] and current_user != '':
                while len(user_project_hours) < len(projects):
                    user_project_hours.append('')
                    
            user_project_hours = []
            latest_project_added = ''
            current_user = data_entry['user_profile__user__username']
            
            if len(users_with_no_data) > 0:
                while users_with_no_data[0]['user__username'] < current_user:
                    context_dict['data'].append({'username': users_with_no_data[0]['user__username'], 
                                         'submitted_until': users_with_no_data[0]['submitted_until'], 
                                         'project_hours': ['' for i in range(len(projects))]})
                    users_with_no_data.pop(0)
                    if(len(users_with_no_data) == 0):
                        break
            
            context_dict['data'].append({'username': data_entry['user_profile__user__username'], 
                                         'submitted_until': data_entry['user_profile__submitted_until'], 
                                         'project_hours': user_project_hours})
            
        for project in projects:
            if data_entry['project__name'] == project.name:
                user_project_hours.append(data_entry['total_hours'])
                latest_project_added = project.name
                break
            elif latest_project_added < project.name < data_entry['project__name']: 
                user_project_hours.append('')
                
    while len(user_project_hours) < len(projects):
                    user_project_hours.append('')        
    
    while len(users_with_no_data) > 0:
        context_dict['data'].append({'username': users_with_no_data[0]['user__username'], 
                             'submitted_until': users_with_no_data[0]['submitted_until'], 
                             'project_hours': ['' for i in range(len(projects))]})
        users_with_no_data.pop(0)
    
    return render(request, 'app/report.html', context_dict)

@login_required
def get_time_entries(request):
    user_profile = UserProfile.objects.get(user=request.user)
    # TODO: Prefetch does not work here. It spams the db with queries. 
    projects = Project.objects.order_by('name').prefetch_related(Prefetch('timeentry_set', queryset=TimeEntry.objects.order_by('date').filter(user_profile=user_profile)))

    date_parse_string = "%Y-%m-%d"
    if 'startDate' in request.GET:        
        start_date = datetime.datetime.strptime(request.GET['startDate'], date_parse_string).date()
    else:
        # sunday +1, monday +0, tuesday -1, wednesday -2, thursday -3, friday -4, saturday -5
        weekday_nr = user_profile.submitted_until.isoweekday()
        if weekday_nr == 7:
            start_date = user_profile.submitted_until + timedelta(days=1)
        else:
            start_date = user_profile.submitted_until - timedelta(days=weekday_nr - 1)
            
    end_date = start_date + timedelta(days=6)
    
    response_data = {
        'projects': [],
        'submittedUntil': user_profile.submitted_until.strftime(date_parse_string),
        'startDate': start_date.strftime(date_parse_string),
        'endDate': end_date.strftime(date_parse_string)}
    
    for project in projects:
        current_date = start_date
        p = {'id': project.id,
             'name': project.name,
             'timeentries': []}
    
        while current_date <= end_date:
            # TODO: This is where the excess queries happen
            entry = project.timeentry_set.filter(date=current_date, user_profile=user_profile).first()
            p['timeentries'].append({'date': current_date.strftime('%Y-%m-%d'),
                                      'hours': entry.hours if entry else None,
                                      'submitted': current_date <= user_profile.submitted_until})
            
            current_date += datetime.timedelta(days=1)
            
        response_data['projects'].append(p)

    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json")

@login_required
def save_time_entry(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        project_id = request.POST.get('projectId')
        project = Project.objects.get(id=project_id)
        date = request.POST.get('date')
        hours = request.POST.get('hours')
        
        entry, created = TimeEntry.objects.get_or_create(project=project, date=date, user_profile=user_profile)
        entry.hours = hours
        entry.save()
        
        response_data = {}
        response_data['msg'] = 'Added new entry' if created else 'Updated existing entry'
        
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

@login_required        
def set_last_submitted(request):
    if request.method == 'POST':
        new_date = request.POST.get('date')
        
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.submitted_until = new_date
        user_profile.save()
        
        return HttpResponse('Last submetted set to ' + new_date)
        
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
            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

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
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'app/login.html', {})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')