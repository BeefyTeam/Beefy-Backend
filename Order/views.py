import requests
from ninja import NinjaAPI, Router, Form, File
from ninja.files import UploadedFile
from Order import schemas as SchemasBody
from Order.models import Orders, Pembayaran
from Pembeli.models import PembeliDB
from Penjual.models import PenjualDB, ProdukDB
from typing import List

# Create your views here.
app = NinjaAPI()
router = Router(
    tags=['Orders']
)

@router.post('new-order/')
def newOrder(request, payload: SchemasBody.NewOrderBody = Form(...)):
    if (not PembeliDB.objects.filter(pk=payload.ID_PEMBELI).exists()):
        return app.create_response(
            request,
            {'message': f'Pembeli with id {payload.ID_PEMBELI} not found when create new order'},
            status=404
        )
    if (not PenjualDB.objects.filter(pk=payload.ID_TOKO).exists()):
        return app.create_response(
            request,
            {'message': f'Toko with id {payload.ID_TOKO} not found when create new order'},
            status=404
        )
    if (not ProdukDB.objects.filter(pk=payload.ID_BARANG).exists()):
        return app.create_response(
            request,
            {'message': f'Product with id {payload.ID_BARANG} not found when create new order'},
            status=404
        )

    try:
        pembayaranObj = Pembayaran.objects.create(
            bukti_bayar='None',
            rekening=payload.rekening,
            total_harga=float(payload.total_harga),
            biaya_pengiriman=float(payload.biaya_pengiriman),
            kode_unik=int(payload.kode_unik),
            status='M'
        )
        newOrderObj = Orders.objects.create(
            ID_PEMBAYARAN=pembayaranObj.pk,
            ID_PEMBELI=int(payload.ID_PEMBELI),
            ID_TOKO=int(payload.ID_TOKO),
            ID_BARANG=int(payload.ID_BARANG),
            catatan=payload.catatan,
            alamat_pengiriman=payload.alamat_pengiriman,
            metode_pembayaran=payload.metode_pembayaran,
        )

    except:
        return app.create_response(
            request,
            {'message': f'Error with database when create new order'},
            status=500
        )

    return {
        'message': 'success add order',
        'id_order': newOrderObj.pk,
        'data_pembayaran': {
            'bank': newOrderObj.metode_pembayaran,
            'nomor_rekening': pembayaranObj.rekening,
            'atas_nama': PenjualDB.objects.get(pk=newOrderObj.ID_TOKO).nama_toko,
            'total_pembayaran': pembayaranObj.total_harga
        }
    }

@router.post('upload-bukti/')
def uploadBuktiBayar(request, id_order: int = Form(...), file_image: UploadedFile = File(...)):
    if (not Orders.objects.filter(pk=id_order).exists()):
        return app.create_response(
            request,
            {'message': f'Order with id {id_order} not found'},
            status=404
        )
    orderObj = Orders.objects.get(pk=id_order)
    if (not Pembayaran.objects.filter(pk=orderObj.ID_PEMBAYARAN).exists()):
        return app.create_response(
            request,
            {'message': f'Pembayaran with id {orderObj.ID_PEMBAYARAN} not found'},
            status=404
        )
    responeImgBB = requests.post('https://api.imgbb.com/1/upload', params={
        'key': '1a30bea6baf246a32e390350c7efa81c'
    }, files={
        'image': file_image.read()
    }).json()
    urlGambar = responeImgBB['data']['display_url']

    try:
        pembayaranObj = Pembayaran.objects.get(pk=orderObj.ID_PEMBAYARAN)
        pembayaranObj.bukti_bayar = urlGambar
        pembayaranObj.status = 'T'
        pembayaranObj.save()
    except:
        return app.create_response(
            request,
            {'message': f'Error with database when upload bukti bayar'},
            status=500
        )

    return {'message': 'success upload bukti bayar'}

@router.get('order-in-process/', response=List[SchemasBody.OrderProceessResponse])
def orderProcess(request, id_pembeli: int = None, id_toko:int = None):
    if (id_toko is None):
        orderProcessObj = Orders.objects.filter(ID_PEMBELI=id_pembeli, status='Diproses')
        return orderProcessObj
    elif (id_pembeli is None):
        orderProcessObj = Orders.objects.filter(ID_TOKO=id_toko, status='Diproses')
        return orderProcessObj

@router.get('order-in-waiting/', response=List[SchemasBody.OrderProceessResponse])
def orderWaiting(request, id_pembeli: int = None, id_toko:int = None):
    if (id_toko is None):
        orderProcessObj = Orders.objects.filter(ID_PEMBELI=id_pembeli, status='Menunggu')
        return orderProcessObj
    elif (id_pembeli is None):
        orderProcessObj = Orders.objects.filter(ID_TOKO=id_toko, status='Menunggu')
        return orderProcessObj

@router.get('order-in-complete/', response=List[SchemasBody.OrderProceessResponse])
def orderComplete(request, id_pembeli: int = None, id_toko:int = None):
    if (id_toko is None):
        orderProcessObj = Orders.objects.filter(ID_PEMBELI=id_pembeli, status='Selesai')
        return orderProcessObj
    elif (id_pembeli is None):
        orderProcessObj = Orders.objects.filter(ID_TOKO=id_toko, status='Selesai')
        return orderProcessObj

@router.get('orders/', response=List[SchemasBody.OrderProceessResponse])
def orders(request, id_pembeli: int = None, id_toko:int = None):
    ordersObj = Orders.objects.filter(ID_PEMBELI=id_pembeli)
    return ordersObj


