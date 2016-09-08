from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from redis_app.models import UserProfile, VisitInfo

from redis_app.tasks import visit_user_task  

# Create your views here.

error_dict = {

    'register-required': 'you have to register account',

    'match-password': 'please match both password',

    'same-username': 'already have been same username',

    'account-disabled': 'The password is valid, but the account the has been disabled!',

    'input-mustbeset': 'The given username and password must be set',

    'input-incorrect': 'The username and password incorrect',

}

def login_required(error_code=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():
                return func(request, *args, **kwargs)
            else:
                url = reverse('login')
                if error_code is not None:
                    parameters = {
                        'error_code': error_code
                    }
                    url += '?' + urllib.urlencode(parameters)
                return HttpResponseRedirect(url)
        return inner
    return decorator


def login_handler(request, error_code=None):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            error_code = 'account-disabled'
        else:
            error_code = 'input-incorrect'
        context = {'error_message': error_dict[error_code]}
        return render(request, 'redis_app/login.html', context)
    if request.GET.get('error_code', ''):
        error_code = request.GET.get('error_code')
    else:
        return render(request, 'redis_app/login.html')
    context = {'error_message': error_dict[error_code]}
    return render(request, 'redis_app/login.html', context)


def logout_handler(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('login'))



def register(request):
    if request.method == 'GET':
        return render(request, 'redis_app/signup.html')
    elif request.method == 'POST':
        user_object_list = User.objects.all()
        username = request.POST.get('username', '')
        if username == '':
            context = {'error_message': error_dict['input-mustbeset']}
            return render(request, 'redis_app/signup.html', context)
        for user in user_object_list:
            if user.username == username:
                context = {'error_message': error_dict['same-username']}
                return render(request, 'redis_app/signup.html', context)
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm-password', '')
        if password != confirm_password:
            context = {'error_message': error_dict['match-password']}
            return render(request, 'redis_app/signup.html', context)
        else:
            user = User.objects.create_user(username, email, password)
            visit_object = VisitInfo.objects.create(hits=0)
            profile = UserProfile.objects.create(user=user, email=user.email, visitinfo=visit_object)
	    return HttpResponseRedirect(reverse('login'))



def visit(userid):
    print userid
    user = User.objects.get(id=userid)
    user_email = user.email
    userprofile = get_object_or_404(UserProfile, email=user_email)
    userprofile.visit()


def show_visit(request, userid):
    user = User.objects.get(id=userid)
    profile = get_object_or_404(UserProfile, email=user.email)
    print 'profile user name = '
    print user.username

    visit_num = profile.visitinfo.get_hits()
    context = {'visit_num': visit_num,
               'username': user.username}
    return render(request, 'redis_app/visit.html', context)   


def index(request):
    if request.method == 'GET':
        current_user = request.user
        visit_user_task.delay(current_user.id)
        context = {'userid': current_user.id} 
        return render(request, 'redis_app/index.html', context)
