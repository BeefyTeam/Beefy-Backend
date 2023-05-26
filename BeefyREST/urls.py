from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(
    title='🥩 Beefy Endpoints',
    version='v1.0',
    description='### Hello fellows what do you want? I serve anything for you in this documentation Beefy Restful Api'
)

@api.get("/")
def hello(request):
    return {'message': "Hello I'm Beefy Backend"}