from ninja import Schema

class RegisterBody(Schema):
    nama_toko: str
    nomor_telepon: str
    email: str
    password: str

class EditPenjualBody(Schema):
    id_penjual: int
    alamat_lengkap: str
    jam_operasional_buka: str
    jam_operasional_tutup: str
    metode_pembayaran: str
    rekening: str

class ProductAddBody(Schema):
    id_penjual: int
    nama_barang: str
    deskripsi: str
    harga: float

class ProductsResponse(Schema):
    pk: int
    ID_PENJUAL: int
    nama_barang: str
    deskripsi: str
    harga: float

class EditProductBody(Schema):
    id_product: int
    nama_barang: str
    deskripsi: str
    harga: float

