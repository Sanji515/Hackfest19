from django.contrib import admin
from .models import Profile, Farmers, Crop

# Register your models here.
admin.site.register(Profile)
admin.site.register(Farmers)
admin.site.register(Crop)
