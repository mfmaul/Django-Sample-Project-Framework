from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def Dashboard(request):
    return render(request, 'Dashboard/Dashboard.html')