from django.shortcuts import render

def List(request):
    context = {}
    return render(request, 'Item/List.html', context)

def Entry(request):
    context = {}
    return render(request, 'Item/Entry.html', context)