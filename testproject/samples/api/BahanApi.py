from django.http import HttpResponse, JsonResponse
import json
import samples.controller.BahanController as BahanController
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def ListData(request):
    try:
        data = json.loads(request.body)
        items = BahanController.ListData(data['PageIndex'], data['PageSize'], data['SearchBy'], data['Keywords'])
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
def GetData(request):
    try:
        data = json.loads(request.body)
        items = BahanController.GetData(data['uid'])
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
def SaveUpdate(request):
    try:
        data = json.loads(request.body)
        data['header']['modified_by'] = str(request.user)
        items = BahanController.SaveUpdate(data['header'])
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