"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from samples import views as sample_views
from samples.api import ItemApi as item_api
from samples.app_views import ItemViews as item_views

urlpatterns = [
    path('6eb292a79addf36f91b3660166cf8aa823625525/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # django-allauth

    path('Item/ItemListData', item_api.ItemListData, name='item_list_data'),
    path('Item/ItemSaveUpdate', item_api.ItemSaveUpdate, name='item_save_update'),
    path('Item/ItemGetData', item_api.ItemGetData, name='item_save_update'),
    path('Item/Entry', item_views.Entry, name='item_entry'),
    path('Item/List', item_views.List, name='item_list'),

    path('', sample_views.Dashboard, name='dashboard'),
]
