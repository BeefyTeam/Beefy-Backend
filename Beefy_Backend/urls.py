from django.contrib import admin
from django.urls import path
from BeefyREST.views import index

from BeefyREST.urls import api

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', api.urls, name='Endpoints'),
]