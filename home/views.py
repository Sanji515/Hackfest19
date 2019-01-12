#!/usr/bin/env python
from django.shortcuts import render

import matplotlib.pyplot as plt
import os


# Create your views here.


def index(request):
    context = {}

    return render(request, 'home/index.html', context)


def profile(request):
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

    context = {}

    return render(request, 'home/profile.html', context)
