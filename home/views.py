from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from .models import Profile, Crop, Farmers
from .forms import YourSignupForm, YourLoginForm

import matplotlib.pyplot as plt
import os


def index(request):
    context = {}

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
                firstname = signup_form.cleaned_data.get('firstname')
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


def details(request):

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    context = {
        'username': username
    }
    return render(request, 'home/detail.html', context)


def crops(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''
    context = {
        'username': username
    }
    return render(request, 'home/crops.html', context)

def single_crop(request, pk):
    if request.method == 'POST':
        print('POST ajax')
        user = get_object_or_404(User, Q(username=request.user.username))
        crop = get_object_or_404(Crop, Q(crop_id=pk))
        
        profile = get_object_or_404(Profile, Q(user=user))
        fullname = profile.firstname+' '+profile.lastname
        print(fullname)

        farmer = Farmers.objects.create(user=user)
        farmer.crop_id = pk
        price = request.POST.get('price')
        print(request.POST.get('quantity'))
        print(int(price))
        print(type(int(price)))
        farmer.price = int(price)
        farmer.quantity = request.POST.get('quantity')
        farmer.location = request.POST.get('location')
        farmer.crop_mobile_no = request.POST.get('phone')
        farmer.description = request.POST.get('description')
        farmer.save()

        crop.farmers.add(farmer)
        crop.save()

        context = {
            'price': request.POST.get('price'),
            'quantity': request.POST.get('quantity'),
            'location': request.POST.get('location'),
            'crop_mobile_no': request.POST.get('phone'),
            'description': request.POST.get('description'),
            'fullname': fullname
        }

        return HttpResponse(JsonResponse(context), content_type='application/json')

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''
        return redirect('home:home')
    farmers = Farmers.objects.filter(crop_id=pk)
    user = get_object_or_404(User, Q(username=request.user.username))
        
    profile = get_object_or_404(Profile, Q(user=user))
    fullname = profile.firstname+' '+profile.lastname
    print(fullname)

    if len(farmers)>0:
        empty_list = 0
    else:
        empty_list = 1

    context = {
        'pk': pk,
        'farmers': farmers,
        'username': username,
        'empty_list': empty_list,
        'fullname': fullname
    }

    return render(request, 'home/buyorsell.html', context)


def logout_url(request):
    logout(request)

    return redirect('home:home')


def profile(request):
    username = ''
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # heights of bars
    sales = [1000, 2400, 3600, 4000, 5000, 1000, 2400, 3600, 4000]

    left = []
    # x-coordinates of left sides of bars
    for i in range(len(sales)):
        left.append(i + 1)
    # left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    tick_label = []
    # labels for bars
    start_month = 4
    start_year = 18
    for i in range(len(sales)):
        tick_label.append(str(start_month) + '/' + str(start_year))
        start_month = start_month + 1
        if start_month == 13:
            start_month = 1
            start_year = start_year + 1
    # tick_label = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    fig = plt.figure()
    # plotting a bar chart
    plt.bar(left, sales, tick_label=tick_label,
            width=0.5, color=['green'])
    # x-axis label
    plt.xlabel('Month')
    # frequency label
    plt.ylabel('Sales')
    # plot title
    plt.title('Sales')

    # function to show the plot
    # plt.show()

    file_url = os.path.join(BASE_DIR, "static", "images", "sales.png")
    fig.savefig(file_url)

    user = get_object_or_404(User, Q(username=request.user.username))
    profile = get_object_or_404(Profile, Q(user=user))
    if request.user.is_authenticated:
        username = request.user.username
        mob = profile.mobile_no
        city = profile.city
    else:
        username = ''


    context = {
        'username': username,
        'mob': mob,
        'city': city
    }

    return render(request, 'home/profile.html', context)
