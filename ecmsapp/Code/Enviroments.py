import platform,socket
from user_agents import parse
from django.shortcuts import render,redirect,HttpResponse
from ecmsapp.models import Enviroment,House,Renter,userLoggers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
import json

# Create your views here.
p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)

@login_required(login_url='user_login')
def enviroment(request):
    houses = House.objects.filter(status=0)
    renters = Renter.objects.filter(status=0)
    enivroments = Enviroment.objects.filter(status=0)
    context = {
        'houseData': houses,
        'renterData': renters,
        'enviromentData':enivroments
    }
    return render(request,'Enviroment/enviroment.html',context)

@login_required(login_url='user_login')
def createEnviroment(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        new_house = request.POST['houseno']
        new_renter = request.POST['renter']
        new_date = request.POST['regoster_date']
        new_status = request.POST['status']

        house = House.objects.get(id=new_house)
        renter = Renter.objects.get(id=new_renter)

        if new_house != "" and new_renter != "" and new_date != "" and new_status != "":
            # print(f"{new_date} {new_status} {new_house} {new_renter}")
            add_environment = Enviroment(register_date=new_date,status=new_status,house_id=house.id,renter_id=renter.id)
            
            add_environment.save()
            if add_environment.pk:
                msg = f"{house.houseno} Was Been Successfuly Rented by {renter.name} and Added to the System"
                userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            else:
                msg = f"{house.houseno} Was Not Successfuly Rented by {renter.name} and Not Added to the System"
                userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()

            isError = True
            return HttpResponse(isError)
        else:
            isError = False
            return HttpResponse(isError)
        
@login_required(login_url='user_login')
def get_environment(request):
    if request.method == "GET":
        env_id = request.GET.get('id')
        env = Enviroment.objects.get(id=env_id)
        data = {
            'env_id': env.id,
            'renter_name': env.renter.name,
            'renter_id': env.renter.id,
            'house_id': env.house.id,
            'house_no': env.house.houseno
        }
        return JsonResponse(data)

        # singleEnviroment = Enviroment.objects.filter(id=env_id).all()
        # for env in singleEnviroment:
        #     print(env.id, env.renter.name, env.house.houseno)
        # data = {'env':singleEnviroment}
        # data = json.dumps(singleEnviroment)
        # print(singleEnviroment)
        # return JsonResponse(data, safe=False)
        # return HttpResponse("succes")