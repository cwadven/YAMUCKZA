"""muckza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import food.views
import login.views
import ownerpage.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', food.views.main, name="main"),
    path('Fmenu/', food.views.Fmenu, name="Fmenu"),
    path('Dmenu/', food.views.Dmenu, name="Dmenu"),
    path('DSelectFood/', food.views.Dselect, name="Dselect"),
    path('SelectFood/', food.views.Fselect, name="Fselect"),
    path('Signup/', login.views.signup, name="Signup"),
    path('Findpassword/', login.views.findpassword, name="Findpassword"),
    path('Ownerdelete/', ownerpage.views.ownerdelete, name="Ownerdelete"),
    path('Ownerpassword/', ownerpage.views.ownerpassword, name="Ownerpassword"),
    path('Ownerpage/', ownerpage.views.ownerpage, name="Ownerpage"),
    path('Ownerupdate/', ownerpage.views.ownerupdate, name="Ownerupdate"),
    path('Login/', login.views.login, name="Login"),
    path('Logout/', login.views.logout, name="Logout"),
    path('Confirming/', login.views.confirming, name="Confirming"),
    path('Update/', ownerpage.views.updateMenu, name="Update"),
    path('Delete/', ownerpage.views.deleteMenu, name="Delete"),
]
