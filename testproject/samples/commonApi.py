from django.http import HttpResponse, JsonResponse
import json
import samples.common as common
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def GetOptions(request):
    try:
        data = json.loads(request.body)
        items = common.GetOptions(
            table_name = data['table_name'],
            id_field = data['id_field'],
            name_field = data['name_field'],
        )
        context = {
            'List': items,
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