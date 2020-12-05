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
from samples import commonApi as common_api

from samples.api import ItemApi as item_api
from samples.api import BahanApi as bahan_api
from samples.api import UnitApi as unit_api
from samples.api import OrderApi as order_api

from samples.app_views import ItemViews as item_views
from samples.app_views import BahanViews as bahan_views
from samples.app_views import UnitViews as unit_views
from samples.app_views import OrderViews as order_views

urlpatterns = [
    path('6eb292a79addf36f91b3660166cf8aa823625525/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # django-allauth

    path('Item/ItemListData', item_api.ItemListData, name='item_list_data'),
    path('Item/ItemSaveUpdate', item_api.ItemSaveUpdate, name='item_save_update'),
    path('Item/ItemGetData', item_api.ItemGetData, name='item_save_update'),
    path('Item/Entry', item_views.Entry, name='item_entry'),
    path('Item/List', item_views.List, name='item_list'),

    path('Bahan/ListData', bahan_api.ListData, name='bahan_list_data'),
    path('Bahan/SaveUpdate', bahan_api.SaveUpdate, name='bahan_save_update'),
    path('Bahan/GetData', bahan_api.GetData, name='bahan_save_update'),
    path('Bahan/Entry', bahan_views.Entry, name='bahan_entry'),
    path('Bahan/List', bahan_views.List, name='bahan_list'),

    path('Unit/ListData', unit_api.ListData, name='unit_list_data'),
    path('Unit/SaveUpdate', unit_api.SaveUpdate, name='unit_save_update'),
    path('Unit/GetData', unit_api.GetData, name='unit_save_update'),
    path('Unit/Entry', unit_views.Entry, name='unit_entry'),
    path('Unit/List', unit_views.List, name='unit_list'),

    path('Order/ListData', order_api.ListData, name='order_list_data'),
    path('Order/SaveUpdate', order_api.SaveUpdate, name='order_save_update'),
    path('Order/GetData', order_api.GetData, name='order_save_update'),
    path('Order/CloseOrder', order_api.CloseOrder, name='order_close_order'),
    path('Order/Entry', order_views.Entry, name='order_entry'),
    path('Order/List', order_views.List, name='order_list'),

    path('', sample_views.Dashboard, name='dashboard'),
    path('Common/GetOptions', common_api.GetOptions, name='common_get_options'),
    path('59a31cc6d6ae431a5a9e4b922c95fad743c75b39', sample_views.test, name='test'),
]

handler401 = 'samples.views.handler401'
handler404 = 'samples.views.handler404'
handler500 = 'samples.views.handler500'