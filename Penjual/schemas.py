from ninja import Schema

class RegisterBody(Schema):
    nama_toko: str
    nomor_telepon: str
    email: str
    password: str

class EditPenjualBody(Schema):
    id_toko: int
    alamat_lengkap: str
    jam_operasional_buka: str
    jam_operasional_tutup: str
    metode_pembayaran: str
    rekening: str

class ProductAddBody(Schema):
    id_toko: int
    nama_barang: str
    deskripsi: str
    harga: float

class ProductsResponse(Schema):
    pk: int
    ID_TOKO: int
    nama_barang: str
    deskripsi: str
    harga: float

class EditProductBody(Schema):
    id_product: int
    nama_barang: str
    deskripsi: str
    harga: float

