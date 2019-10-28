import json

from django.http import JsonResponse
from main.models import *

# def get_airlines(request):
#     id = request.GET.get("id")
#     if id is not None:
#         response = {
#             "airline": Airline.objects.get(pk=id).as_dict()
#         }
#     else:
#         response = {
#             "airlines": [airline.as_dict() for airline in Airline.objects.all()]
#         }
#     return JsonResponse(response)

# def delete_airline(request):
#     id = request.GET.get("id")
#     if id is not None:
#         try:
#             airline = Airline.objects.get(pk=int(id))
#         except:
#             return JsonResponse({"result": "error", "error": "airline not found"})
# 
#         airline.delete()
#         return JsonResponse({"result": "success"})
#     else:
#         return JsonResponse({"result": "error", "error": "no id provided"})
