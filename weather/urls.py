from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='weather/login.html',redirect_authenticated_user=True),name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('delete/<pk>',views.deleteCity,name='delete_city')
]