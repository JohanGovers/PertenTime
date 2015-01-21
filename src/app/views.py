import datetime, json
from django.shortcuts import render
from django.db.models import Prefetch, Sum, F
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import Project, TimeEntry, UserProfile
from app.forms import UserForm, UserProfileForm

#TODO: Split into multiple files. Multiple apps even?

@login_required
def index(request):
    return render(request, 'app/index.html')

@login_required
def report(request):
    projects = Project.objects.order_by('name')
    
    user_data = TimeEntry.objects.filter(user_profile__submitted_until__gte=F('date'))
    user_data = user_data.values('project__name', 'user_profile__user__username', 'user_profile__submitted_until')
    user_data = user_data.annotate(total_hours=Sum('hours')).order_by('user_profile__user__username', 'project__name')
    
    context_dict = {'data': [], 'projects': projects}
    
    # TODO: Tests for this method! E.g. it does not pad at the end and the first row is potentially duplicated!!
    current_user = ''
    for data_entry in user_data:
        if data_entry['user_profile__user__username'] != current_user:
            user_project_hours = []
            current_user = data_entry['user_profile__user__username']
            context_dict['data'].append({'username': data_entry['user_profile__user__username'], 
                                         'submitted_until': data_entry['user_profile__submitted_until'], 
                                         'project_hours': user_project_hours})
        for project in projects:
            if data_entry['project__name'] == project.name:
                user_project_hours.append(data_entry['total_hours'])
                break
            else:
                user_project_hours.append('')
    
    return render(request, 'app/report.html', context_dict)

@login_required
def get_time_entries(request):
    user_profile = UserProfile.objects.get(user=request.user)
    # TODO: Prefetch does not work here. It spams the db with queries. 
    projects = Project.objects.order_by('name').prefetch_related(Prefetch('timeentry_set', queryset=TimeEntry.objects.order_by('date').filter(user_profile=user_profile)))

    date_parse_string = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(request.GET['startDate'], date_parse_string).date()
    end_date = datetime.datetime.strptime(request.GET['endDate'], date_parse_string).date()
    
    response_data = {'projects': [], 'submittedUntil': user_profile.submitted_until.strftime('%Y-%m-%d')}
    
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