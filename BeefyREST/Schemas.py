from ninja import Schema

class RegisterBody(Schema):
    email: str = 'your@email.com'
    password: str = '12345678'
    tipe: str = 'pembeli/penjual'

class LoginBody(Schema):
    email: str = 'admin'
    password: str = 'mimin123'

class RefreshBody(Schema):
    token: str = 'token'

class Validbody(Schema):
    token: str = 'token'
