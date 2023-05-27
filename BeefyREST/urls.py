from ninja import NinjaAPI
from ninja import Router
from ninja.security import HttpBearer
from BeefyREST.views import router, validTokenCheck


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if (validTokenCheck(token=token)):
            return token
        else:
            pass


api = NinjaAPI(
    title='🥩 Beefy Endpoints',
    version='v1.0',
    description='### Hello fellows what do you want? Give me some meat, i will cook for you',
    default_router=Router(tags=['Hello World'])
)

api.add_router('auth/', router)


@api.get("/", auth=AuthBearer())
def hello(request):
    return {'message': "Hello I'm Beefy Backend"}
