from ninja import Schema

class RegisterBody(Schema):
    nama: str = 'Your Name'
    email: str = 'your@email.com'
    password: str = '12345678'


class EditAlamatBody(Schema):
    id_pembeli: str
    nama: str = 'Your name'
    alamat_lengkap: str = 'Your Address'
    nama_penerima: str = 'Your Name Receiver'
    nomor_telp: str = 'Your Phone Number'
    label_alamat: str = 'Your Label Address'

class EditPhotoProfile(Schema):
    id_pembeli: int

class NewHistory(Schema):
    id_pembeli: int