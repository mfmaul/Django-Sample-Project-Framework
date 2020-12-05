from django.http import HttpResponse, JsonResponse
import json
import samples.controller.UnitController as UnitController
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def ListData(request):
    try:
        context = {
            
        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            
        }
        return JsonResponse(context)

@login_required
def GetData(request):
    try:
       
        context = {

        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            
        }
        return JsonResponse(context)

@login_required
def SaveUpdate(request):
    try:
        context = {

        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            
        }
        return JsonResponse(context)
    
@login_required
def CloseOrder(request):
    try:
        context = {

        }
        return JsonResponse(context)
    except Exception as e:
        context = {
            
        }
        return JsonResponse(context)