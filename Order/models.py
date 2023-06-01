from django.db import models
from datetime import datetime
# Create your models here.
class Pembayaran(models.Model):
    bukti_bayar = models.CharField(max_length=255)
    rekening = models.CharField(max_length=15)
    total_harga = models.FloatField()
    biaya_pengiriman = models.FloatField()
    kode_unik = models.IntegerField()

    STATUS_PEMBAYARAN_CHOICES = (
        ('M', 'Menunggu'),
        ('T', 'Dibayar')
    )
    status = models.CharField(max_length=1, choices=STATUS_PEMBAYARAN_CHOICES, default='Menunggu')

    def __str__(self):
        return f'{self.id} | {self.kode_unik}'

class Orders(models.Model):
    ID_PEMBAYARAN = models.IntegerField()
    ID_PEMBELI = models.IntegerField()
    ID_TOKO = models.IntegerField()
    ID_BARANG = models.IntegerField()
    catatan = models.CharField(max_length=255)
    alamat_pengiriman = models.TextField()
    metode_pembayaran = models.CharField(max_length=10)
    tanggal_order = models.DateTimeField(auto_now=True)

    STATUS_ORDER_CHOICES = (
        ('Menunggu', 'Menunggu Diterima Seller'),
        ('Diproses', 'Diproses oleh kurir'),
        ('Selesai', 'Pesanan Selesai')
    )
    status = models.CharField(max_length=80, choices=STATUS_ORDER_CHOICES, default='Menunggu')

    def __str__(self):
        return f'{self.id} | {self.tanggal_order}'
