from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PembeliDB(models.Model):
    nama = models.CharField(max_length=100)
    alamat_lengkap = models.CharField(max_length=255)
    nama_penerima = models.CharField(max_length=100)
    nomor_telp = models.CharField(max_length=15)
    label_alamat = models.CharField(max_length=100)
    photo_profile = models.CharField(max_length=255)

    ID_USER = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.pk} | {self.nama}'

class ScanHistroyDB(models.Model):
    ID_Pembeli = models.IntegerField()
    gambar_url = models.CharField(max_length=255)
    tanggal = models.DateTimeField()
    hasil = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.pk} | {self.gambar_url}'