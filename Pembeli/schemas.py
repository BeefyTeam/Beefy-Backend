from ninja import Schema
from datetime import datetime

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

class ScanHistoryResponse(Schema):
    gambar_url: str
    tanggal: datetime
    segar: bool
    level_kesegaran: int
    jenis: str