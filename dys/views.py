from django.shortcuts import render, HttpResponse

# Create your views here.
def all_ok(request):
    return HttpResponse("All OK")