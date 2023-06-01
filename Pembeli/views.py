from django.contrib.auth.models import User
from Pembeli import schemas as SchemasBody
from Pembeli.models import PembeliDB, ScanHistroyDB
from ninja import Router
from ninja import Form, NinjaAPI
from ninja import File
from ninja.files import UploadedFile
from typing import List
import requests
from datetime import datetime

from Penjual.models import PenjualDB, ProdukDB

app = NinjaAPI()

# Create your views here.

router = Router(
    tags=['Pembeli endpoints']
)


@router.post("register-pembeli/")
def register(request, payload: SchemasBody.RegisterBody = Form(...)):
    try:
        userNew = User.objects.create_user(
            username=payload.email,
            email='account@email.com',
            password=payload.password,
        )
        userNew.is_staff = False
        userNew.save()
    except:
        return app.create_response(
            request,
            {'message': f'account with email {payload.email} already exists'},
            status=409
        )
    pembeliNew = PembeliDB.objects.create(
        nama=payload.nama,
        nama_penerima=payload.nama,
        alamat_lengkap='None',
        nomor_telp='None',
        label_alamat='None',
        photo_profile='None',
        ID_USER=userNew
    )
    return {
        'message': 'register success',
        'id_user': userNew.pk,
        'id_pembeli': pembeliNew.pk
    }

@router.post('edit-pembeli/')
def editPembelit(request, payload: SchemasBody.EditPembeliBody = Form(...)):
    print(payload.id_pembeli)
    pembeliObj = PembeliDB.objects.filter(pk=int(payload.id_pembeli)).exists()
    if (pembeliObj):
        pembeliObj = PembeliDB.objects.get(pk=int(payload.id_pembeli))
        pembeliObj.nama = payload.nama
        pembeliObj.alamat_lengkap = payload.alamat_lengkap
        pembeliObj.nama_penerima = payload.nama_penerima
        pembeliObj.nomor_telp = payload.nomor_telp
        pembeliObj.label_alamat = payload.label_alamat
        pembeliObj.save()
    else:
        return app.create_response(
            request,
            {'message': f'Pembeli with id {payload.id_pembeli} Not Found'},
            status=404
        )
    return {'message': f'Success edit pembeli for pembeli id {payload.id_pembeli}'}

@router.post('edit-pp-pembeli/')
def editPhotoPembeli(request, id_pembeli: int = Form(...), file_image: UploadedFile = File(...)):
    userPembeliObj = PembeliDB.objects.filter(pk=id_pembeli).exists()
    if (userPembeliObj):
        responeImgBB = requests.post('https://api.imgbb.com/1/upload', params={
            'key': '1a30bea6baf246a32e390350c7efa81c'
        }, files={
            'image': file_image.read()
        }).json()
        urlGambar = responeImgBB['data']['display_url']

        userPembeliObj = PembeliDB.objects.get(pk=id_pembeli)
        userPembeliObj.photo_profile = urlGambar
        userPembeliObj.save()
    else:
        return app.create_response(
            request,
            {'message': f'Pembeli with id {id_pembeli} not found'},
            status=404
        )
    return {'message': 'Success Edit photo profile'}

@router.get('user/detail/{id_pembeli}')
def getPembeliDetail(request, id_pembeli: int):
    userObj = PembeliDB.objects.filter(pk=id_pembeli).exists()
    if (not userObj):
        return app.create_response(
            request,
            {'message': f'Pembeli with id {id_pembeli} not found'},
            status=404
        )
    userObj = PembeliDB.objects.get(pk=id_pembeli)
    responseBody = {
        'nama': userObj.nama,
        'alamat_lengkap': userObj.alamat_lengkap,
        'nama_penerima': userObj.nama_penerima,
        'nomor_telp': userObj.nomor_telp,
        'label_alamat': userObj.label_alamat,
        'photo_profile': userObj.photo_profile,
        'user_account': {
            'id_account': userObj.ID_USER.pk,
            'email': userObj.ID_USER.username,
        }
    }
    return responseBody

@router.post('scan-meat/')
def scanDaging(request, id_pembeli: int = Form(...), file_image: UploadedFile = File(...)):
    try:
        gambar = file_image.read()
        responeImgBB = requests.post('https://api.imgbb.com/1/upload', params={
            'key': '1a30bea6baf246a32e390350c7efa81c'
        }, files={
            'image': gambar
        }).json()
        urlGambar = responeImgBB['data']['display_url']

        responeModelApi = requests.post('https://model-beefy-33n3233q4q-uc.a.run.app/predict/', params={
        }, files={
            'fileUpload': gambar
        }).json()
    except:
        return app.create_response(
            request,
            {'message': 'Error communication with model API'},
            status=500
        )

    print(responeModelApi)

    ScanHistroyDB.objects.create(
        ID_Pembeli=id_pembeli,
        gambar_url=urlGambar,
        tanggal=datetime.now(),
        segar=True if responeModelApi['label'] == 'fresh' else False,
        level_kesegaran=int(float(str(responeModelApi['kesegaran']).replace('%', ''))),
        jenis='sapi'
    )
    return {
        'message': 'Meat Scan Success',
        'data': {
            'url_gambar': urlGambar,
            'hasil': responeModelApi['label'],
            'level_kesegaran': responeModelApi['kesegaran'],
            'jenis': 'sapi'
        }
    }

@router.get('scan-history/{id_pembeli}', response=List[SchemasBody.ScanHistoryResponse])
def scanHistory(request, id_pembeli: int):
    histroyObjs = ScanHistroyDB.objects.filter(ID_Pembeli=id_pembeli)
    return histroyObjs

@router.get('store/profile/{id_toko}')
def getProfileStore(request, id_toko: int):
    userObj = PenjualDB.objects.filter(pk=id_toko).exists()
    if (not userObj):
        return app.create_response(
            request,
            {'message': f'Toko penjual with id {id_toko} not found'},
            status=404
        )
    userObj = PenjualDB.objects.get(pk=id_toko)
    responseBody = {
        'logo_toko': userObj.logo_toko,
        'nama_toko': userObj.nama_toko,
        'rekening': userObj.rekening,
        'metode_pembayaran': userObj.metode_pembayaran,
        'alamat_lengkap': userObj.alamat_lengkap,
        'nomor_telp': userObj.nomor_telp,
        'jam_operasional_buka': userObj.jam_operasional_buka,
        'jam_operasional_tutup': userObj.jam_operasional_tutup,
        'user_account': {
            'email': userObj.ID_USER.username,
        }
    }
    return responseBody

@router.get('get-stores/', response=List[SchemasBody.StoresResponse])
def getStores(request):
    stores = PenjualDB.objects.all()
    return stores

@router.get('search-toko/', response=List[SchemasBody.StoresResponse])
def searcToko(request, toko_name: str):
    getStores = PenjualDB.objects.filter(nama_toko__contains=toko_name)
    if (len(getStores) == 0):
        return app.create_response(
            request,
            {'message': f'Toko with name {toko_name} not found'},
            status=404
        )
    return getStores

@router.get('search-product/', response=List[SchemasBody.ProductsResponse])
def searchProduct(request, product_name: str):
    getProducts =ProdukDB.objects.filter(nama_barang__contains=product_name)
    if (len(getProducts) == 0):
        return app.create_response(
            request,
            {'message': f'Toko with name {product_name} not found'},
            status=404
        )
    return getProducts