import random
import rest_framework_simplejwt.exceptions
from django.contrib.auth.models import User

from ninja import Router
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenRefreshSerializer
from BeefyREST import Schemas as SchemasBody
from django.shortcuts import render
from ninja import NinjaAPI, Form

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.username
        token['tipe'] = 'penjual' if user.is_staff else 'pembeli'

        return token


# Create your views here.
def index(request):
    quotes = [
        "Beef. Yes. Roast beef. It's the Swedish term for beef that is roasted",
        "Not eating meat is a decision. Eating meat is an instinct.",
        "Live life. Eat meat.",
        "No Vegans, just eat meat",
        "Meat is my therapy.",
        "You can't buy happiness, but you can buy meat and that's basically the same thing.",
        "Heaven sends us good meat, but the Devil sends us cooks.",
        "First we eat meat, then we do everything else.",
        "Becoming a vegetarian is just a big mis-steak.",
        "You had me at meat tornado."
    ]
    contexs = {
        'quote': random.choice(quotes)
    }
    userAdmin = User.objects.get(username='admin')
    print(userAdmin)
    userAdmin.set_password('mimin123')
    userAdmin.save()
    print('Success Ganti Password')
    return render(request=request, template_name='index.html', context=contexs)


# Authentication Router
router = Router(
    tags=['Authentication']
)
app = NinjaAPI()


def validTokenCheck(token: str) -> bool:
    validasi = TokenVerifySerializer()
    try:
        validasi.validate({
            "token": token
        })
        return True
    except:
        return False


@router.post("/login")
def login(request, payload: SchemasBody.LoginBody = Form(...)):
    try:
        obtainObj = MyTokenObtainPairSerializer()
        token = obtainObj.validate(attrs={'username': payload.email, 'password': payload.password})
    except:
        return app.create_response(
            request,
            {'message': 'Wrong email or password'},
            status=401
        )
    return token


@router.post('/refresh-token')
def refresh_token(request, payload: SchemasBody.RefreshBody = Form(...)):
    token = TokenRefreshSerializer()
    try:
        new_token = token.validate({
            'refresh': payload.token
        })
    except rest_framework_simplejwt.exceptions.TokenError:
        return app.create_response(
            request,
            {
                'message': 'Token has wrong type or expired or invalid, please login again to get refresh and access token'},
            status=400
        )

    return {'token_access': str(new_token.get('access'))}


@router.post("/check-valid-token")
def valid(request, payload: SchemasBody.Validbody = Form(...)):
    if (validTokenCheck(token=payload.token)):
        return {'message': 'yes token is valid'}
    else:
        return app.create_response(
            request,
            {'message': 'token invalid'},
            status=401
        )


@router.post("/register")
def register(request, payload: SchemasBody.RegisterBody = Form(...)):
    if (payload.tipe not in ['pembeli', 'penjual']):
        return app.create_response(
            request,
            {'message': "tipe harus 'pembeli' atau 'penjual' "},
            status=400
        )
    try:
        userNew = User.objects.create_user(
            username=payload.email,
            email='account@email.com',
            password=payload.password,
        )
    except:
        return app.create_response(
            request,
            {'message': 'account already exists'},
            status=409
        )

    if (payload.tipe == 'penjual'):
        userNew.is_staff = True
        userNew.save()

    print(userNew)
    return {'message': 'register success'}

@router.post('forgot-password/')
def forgot_password(request, payload: SchemasBody.ForgotPassword = Form(...)):
    if (not User.objects.filter(pk=payload.id).exists()):
        return app.create_response(
            request,
            {'message': 'account not found'},
            status=404
        )
    user = User.objects.get(pk=payload.id)
    user.set_password(payload.new_password)
    user.save()
    return {'message': 'change password success'}
