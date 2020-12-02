from django.http import HttpResponse, JsonResponse
import json
import samples.controller.ItemController as ItemController

# Create your views here.
def ItemListData(request):
    try:
        data = json.loads(request.body)
        items = ItemController.ItemListData(data['PageIndex'], data['PageSize'], data['SearchBy'], data['Keywords'])
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

def ItemGetData(request):
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

def ItemSaveUpdate(request):
    try:
        data = json.loads(request.body)
        data['header']['modified_by'] = 'del'
        print(data)
        items = ItemController.ItemSaveUpdate(data['header'])
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