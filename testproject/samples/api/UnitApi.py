from django.http import HttpResponse, JsonResponse
import json
import samples.controller.UnitController as UnitController
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def ListData(request):
    try:
        data = json.loads(request.body)
        items = UnitController.ListData(
            PageIndex=data['PageIndex'], 
            PageSize=data['PageSize'], 
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
def GetData(request):
    try:
        data = json.loads(request.body)
        items = UnitController.GetData(data['uid'])
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
        items = UnitController.SaveUpdate(data['header'])
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