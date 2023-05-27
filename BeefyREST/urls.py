from ninja import NinjaAPI
from ninja import Router
from BeefyREST.views import router

api = NinjaAPI(
    title='🥩 Beefy Endpoints',
    version='v1.0',
    description='### Hello fellows what do you want? I serve anything for you in this documentation Beefy Restful Api',
    default_router=Router(tags=['Root'])
)

api.add_router('auth/', router)

@api.get("/")
def hello(request):
    return {'message': "Hello I'm Beefy Backend"}