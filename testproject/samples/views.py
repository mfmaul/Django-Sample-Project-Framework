from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Create your views here.
@login_required
def Dashboard(request):
    return render(request, 'Dashboard/Dashboard.html')

@login_required
def test(request):
    return render(request, 'test.html')


# error handler
def handler401(request, *args, **argv):
    response = render(None, '401.html', {})
    response.status_code = 401
    return response

def handler404(request, *args, **argv):
    response = render(None, '404.html', {})
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    response = render(None, '500.html', {})
    response.status_code = 500
    return response

# def handler404(request, exception, template_name="404.html"):
#     response = render_to_response(template_name)
#     response.status_code = 404
#     return response