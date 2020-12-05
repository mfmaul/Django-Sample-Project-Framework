from django.http import HttpResponse, JsonResponse
import json
import samples.controller.ItemController as ItemController
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def ItemListData(request):
    """
    sample list request : 
    {"PageIndex":1,"PageSize":5,"item_type":"Minuman","SearchBy":"","Keywords":"Tea"}
    """
    try:
        data = json.loads(request.body)
        items = ItemController.ItemListData(
            PageIndex=data['PageIndex'], 
            PageSize=data['PageSize'], 
            item_type=data['item_type'],
            SearchBy=data['SearchBy'], 
            Keywords=data['Keywords']
        )
        context = {
            'd': items,
            'ProcessSuccess': True
        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            'd': {},
            'ProcessSuccess': False,
            'InfoMessage': str(e)
        }
        return JsonResponse(context)

@login_required
def ItemGetData(request):
    """
    sample get data request :
    {"uid":"5AC03B10-6D92-46C2-8031-80C529FB0B1D"}
    """
    try:
        data = json.loads(request.body)
        items = ItemController.ItemGetData(data['uid'])
        context = {
            'd': items,
            'ProcessSuccess': True
        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            'd': {},
            'ProcessSuccess': False,
            'InfoMessage': str(e)
        }
        return JsonResponse(context)

@login_required
def ItemSaveUpdate(request):
    """
    sample save request :
    {"header":{"uid":"5AC03B10-6D92-46C2-8031-80C529FB0B1D","item_code":"ITM0001","item_name":"Ice Tea","price":"3500.0000","item_type":"Minuman","rowstatus":1},"detail":[{"uid":"D1A3D7FF-E84B-4822-A05B-FCF0D3F46AD1","item_uid":"5AC03B10-6D92-46C2-8031-80C529FB0B1D","item_code":"ITM0001","item_name":"Ice Tea","bahan_uid":"FB925764-A04F-43AA-A6BA-8F660D72279F","bahan_code":"00002","bahan_name":"Air","qty":"200.0000","unit_code":"G","rowstatus":1},{"uid":"36F57DC8-02F2-4C6C-B5C1-E86EA3EB6201","item_uid":"5AC03B10-6D92-46C2-8031-80C529FB0B1D","item_code":"ITM0001","item_name":"Ice Tea","bahan_uid":"369A212F-3EB0-487C-A9E3-A0829B1CF8E6","bahan_code":"00001","bahan_name":"Gula","qty":"20.0000","unit_code":"G","rowstatus":1}]}
    """
    try:
        data = json.loads(request.body)
        data['header']['modified_by'] = str(request.user)
        items = ItemController.ItemSaveUpdate(
            header=data['header'],
            detail=data['detail']
        )
        context = {
            'd': items,
            'ProcessSuccess': True
        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            'd': {},
            'ProcessSuccess': False,
            'InfoMessage': str(e)
        }
        return JsonResponse(context)