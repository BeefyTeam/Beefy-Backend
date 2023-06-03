from django.contrib import admin
from django.urls import path
from BeefyREST.views import index

from BeefyREST.urls import api
from BeefyREST.views import createDummy

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', api.urls, name='Endpoints'),
    path('dummy/', createDummy, name='Create Dummy Data')
]