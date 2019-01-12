from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
	path('', views.index, name='home'),
	path('profile/', views.profile, name='profile'),
	path('logout/', views.logout_url, name='logout'),
	path('services/', views.details, name='services'),
	path('services/crops/', views.crops, name='crops'),
	path('services/crops/<int:pk>', views.single_crop, name='single_crop')
]
