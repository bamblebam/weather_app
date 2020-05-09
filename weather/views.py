from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CreateUserForm,CityForm
from django.contrib.auth import logout
import requests
from .models import City
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def home(request):
    url ='http://api.openweathermap.org/data/2.5/weather?q={}&appid=844a4bcec8a21d7d3031ec573968da7a'
    err_msg=''
     
    if request.method == 'POST':
        form=CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            r=requests.get(url.format(new_city)).json()
            if r['cod']==200:
                city1=form.save(commit=False)
                city1.author=request.user
                city1.save()
            else:
                err_msg='city does not exist'
    
    form=CityForm()
    cities=City.objects.filter(author=request.user)
    city_list=[]
    
    for city in cities:
        r=requests.get(url.format(city)).json()
        city_weather={
            'id':city.id,
            'city':city.name,
            'temperature':r['main']['temp'],
            'weather':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon']
        }
        city_list.append(city_weather)
    
    context={
        'city_list':city_list,
        'form':form,
        'err_msg':err_msg
    }
    return render(request,'weather/weather.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,"account has been created " + username)
            return redirect('home')
    context={'form':form}
    return render(request,'weather/register.html',context=context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def deleteCity(request,pk):
    city=City.objects.get(id=pk)
    city.delete()
    return redirect('home')