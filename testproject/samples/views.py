from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def Dashboard(request):
    return render(request, 'Dashboard/Dashboard.html')

@login_required
def test(request):
    return render(request, 'test.html')