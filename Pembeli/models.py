from django.db import models

# Create your models here.
class PembeliDB(models.Model):
    alamat_lengkap = models.CharField(max_length=255)
    nama_penerima = models.CharField(max_length=100)
    nomor_telp = models.CharField(max_length=15)
    label_alamat = models.CharField(max_length=100)

class ScanHistroyDB(models.Model):
    ID_Pembeli = models.IntegerField()
    gambar_url = models.CharField(max_length=255)
    tanggal = models.DateTimeField()
    hasil = models.CharField(max_length=10)