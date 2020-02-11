from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def hello(request):
    body_string = request.body.decode("utf-8")

    data = json.loads(body_string)

    return HttpResponse('pong')