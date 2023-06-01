from ninja import Schema
from datetime import datetime

class NewOrderBody(Schema):
    ID_PEMBELI: int
    ID_TOKO: int
    ID_BARANG: int
    rekening: str
    catatan: str
    alamat_pengiriman: str
    metode_pembayaran: str
    biaya_pengiriman: float
    total_harga: float
    kode_unik: int

class OrderProceessResponse(Schema):
    pk: int
    ID_PEMBAYARAN: int
    ID_PEMBELI: int
    ID_TOKO: int
    ID_BARANG: int
    catatan: str
    alamat_pengiriman: str
    metode_pembayaran: str
    tanggal_order: datetime
    status: str
