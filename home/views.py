from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .models import Profile
from .forms import YourSignupForm, YourLoginForm

# Create your views here.

def index(request):
    signup_form = YourSignupForm()
    login_form = YourLoginForm()
    signup_error = 0
    login_error = 0

    if 'signup' in request.POST:
        print('POST method')
        if YourSignupForm(request.POST):
            print('signup------------------------')
            signup_form = YourSignupForm(request.POST)
            print(signup_form.errors)
            if signup_form.is_valid():
                print('valid')
                signup_error = 0
                user = signup_form.save(commit=False)
                user.is_active = True
                user.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                user = get_object_or_404(User, Q(username=request.user.username))

                username = signup_form.cleaned_data['username']
                password = signup_form.cleaned_data['password1']
                firstname =  signup_form.cleaned_data.get('firstname')
                lastname = signup_form.cleaned_data.get('lastname')
                mobile_no = signup_form.cleaned_data.get('mobile_no')
                city = signup_form.cleaned_data.get('country')

                # user = get_object_or_404(User, Q(username=request.user.username))
                profile = get_object_or_404(Profile, Q(user=user))
                profile.firstname = firstname
                profile.lastname = lastname
                profile.mobile_no = mobile_no
                profile.city = city
                profile.save()

                print('saving is done')

            else:
                print('invalid')
                signup_error = 1

        else:
            print('signup')
            signup_form = YourSignupForm()
    elif 'signin' in request.POST:
        if YourLoginForm(request.POST):
                print('submit')
                login_form = YourLoginForm(request.POST)
                if login_form.is_valid():
                    print('valid')
                    username = login_form.cleaned_data['username']
                    password = login_form.cleaned_data['password']
                    user = authenticate(username=username, password=password)
                    login(request, user)
                else:
                    print('form not valid')
                    login_error = 1
        else:
            login_form = YourLoginForm()
    else:
        signup_form = YourSignupForm()
        login_form = YourLoginForm()


    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''


    context = {
        'signup_form': signup_form,
        'login_form': login_form,
        'username': username,
        'login_error': login_error,
        'signup_error': signup_error,
    }

    return render(request, 'home/index.html', context)


def logout_url(request):
    logout(request)

    return redirect('home:home')