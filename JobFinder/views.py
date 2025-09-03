from django.shortcuts import render,redirect
from django.template.context_processors import request

from .models import user, category,job,applications


# Create your views here.

def home(request):
    return render(request,'home.html')


def register(request):
    if request.method == 'POST':
        users_obj = user()
        users_obj.username = request.POST.get('username')
        users_obj.password = request.POST.get('password')
        users_obj.name = request.POST.get('name')
        users_obj.phone = request.POST.get('contact')
        users_obj.user_type = request.POST.get('job-type')
        users_obj.save()
        return redirect('/')
    return render(request,'user_register.html')


def delete(request,id):
    job_details = job.objects.get(id = id)
    job_details.delete()
    return redirect('/recruit',{'job_data':job_details})


def login(request):
    if request.method == 'POST':
        usernm = request.POST.get('username')
        psw = request.POST.get('password')
        user_data = user.objects.filter(username = usernm,password = psw)
        if user_data :
            request.session['user'] = usernm
            print(user_data.values())
            return redirect('/')
    return render(request,'login.html')


def logout_user(request):
    del request.session['user']
    return redirect('/')


def recruit(request):
    if 'user' in request.session:
        x=request.session['user']
        user_obj = user.objects.get(username = x)
        job_data = job.objects.filter(user_recruiter = user_obj.id)
        return render(request,'recruit.html',{'data':user_obj,'job_data':job_data})
    else:
        return redirect('/login')

def manage_job(request,id):
    job_data = job.objects.get(id=id)
    category_data = category.objects.all()
    if request.method == 'POST':
        job_data.title = request.POST.get('title')
        job_data.date = request.POST.get('date')
        job_data.time = request.POST.get('time')
        job_data.location = request.POST.get('location')
        job_data.wage = request.POST.get('wage')
        job_data.vacancy = request.POST.get('members_required')
        job_data.description = request.POST.get('description')
        job_data.category = category.objects.get(id = request.POST.get('category'))
        job_data.save()
        return redirect('/recruit')
    return render(request,'manage.html',{'x':job_data, "data":category_data })


def post_job(request,user_id):
    category_data = category.objects.all()
    user_data = user.objects.get(id = user_id)
    if request.method == 'POST':
        job_obj = job()
        job_obj.title = request.POST.get('title')
        job_obj.date = request.POST.get('date')
        job_obj.time = request.POST.get('time')
        job_obj.location = request.POST.get('location')
        job_obj.wage = request.POST.get('payment')
        job_obj.vacancy = request.POST.get('members_required')
        job_obj.description = request.POST.get('description')
        job_obj.category = category.objects.get(id = request.POST.get('category'))
        job_obj.user_recruiter =user.objects.get(id = user_id)
        job_obj.save()
        return redirect('/recruit')
    job_data = job.objects.filter(id = user_id)
    return render(request,'post_job.html', {'data': category_data,'user_data':user_data})


def applicants(request,id):
    applicants_data = applications.objects.filter(job_id = id)
    return render(request,'applicants.html',{'applicant':applicants_data})

def job_fun(request):
    jobs = job.objects.all()
    return render(request,'jobs.html',{'job':jobs})

def apply(request,id):
    job_data = job.objpects.get(id=id)
    if 'user' in request.session:
        username = request.session['user']
        user_data = user.objects.get(username=username)
        if request.method == 'POST':
            application_obj = applications()
            application_obj.job = job.objects.get(id=id)
            application_obj.applicant = user.objects.get(username=username)
            application_obj.email = request.POST.get('email')
            application_obj.save()
            return render(request,'success.html')
        return render(request, 'apply.html', {'job': job_data, 'user': user_data})
    else:
        print('NOT LOGGED in')
        return redirect('/login')

def success(request):
    return render(request,'success.html')