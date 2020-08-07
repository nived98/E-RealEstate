from django.urls import path
from property.api.views import (
    api_detail_view,
    api_update_property_view,
    api_delete_property_view,
    api_create_property_view,
    ApiPropertyListView,
    ApiPropertyListView1,
    ApiBankListView,
    ApiAreaPriceView,
    followview

)

app_name = 'property'

urlpatterns = [

    path('create', api_create_property_view, name='create'),
    path('list', ApiPropertyListView.as_view(), name='list'),
    path('list_get', ApiPropertyListView1.as_view(), name='list_get'),
    path('list1/', followview.as_view(), name='list1'),
    path('area', ApiAreaPriceView.as_view(), name='area'),
    path('bank', ApiBankListView.as_view(), name='bank'),
    path('<slug>/', api_detail_view, name='detail'),
    path('<slug>/update', api_update_property_view, name='update'),
    path('<slug>/delete', api_delete_property_view, name='delete'),


]
