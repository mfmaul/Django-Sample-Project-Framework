from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def List(request):
    context = {}
    return render(request, 'Item/List.html', context)

@login_required
def Entry(request):
    context = {}
    return render(request, 'Item/Entry.html', context)