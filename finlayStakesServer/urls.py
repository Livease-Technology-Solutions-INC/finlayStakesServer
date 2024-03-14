from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls'))
]
