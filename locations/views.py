from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from locations.models import User


def index(request):
    users = User.objects.all()
    return render(request,'locations/index.html',{'users':users})

def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'locations/user.html',{'user': user})

def all_users(request):
    users = User.objects.all()
    user_array = []
    for u in users:
        user_array.append({'id':u.id,'username':u.username})
    return JsonResponse(user_array, safe=False)

def last_location(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    last_loc = user.get_last_location()
    return HttpResponse("{'lat':"+str(last_loc.latitude)+",'long':"+str(last_loc.longitude)+",'time':"+str(last_loc.timestamp)+"}")

@csrf_exempt
def update_location(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        lat = request.POST['latitude']
        long = request.POST['longitude']
        user.location_set.create(latitude=lat, longitude=long)
    except:
        return HttpResponse("not OK")
    user.save()
    return HttpResponse("Ok")


@csrf_exempt
def register_user(request):
    username = request.POST['username']
    u = User.objects.create(username=username)
    u.save()
    return u.id
