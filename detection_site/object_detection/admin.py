from django.contrib import admin
from .models import *

# Ренистрация нужных моделей
admin.site.register(Doctors)
# Register your models here.
admin.site.register(Users)
admin.site.register(Writing)

