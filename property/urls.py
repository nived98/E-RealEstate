from django.urls import path
from property.views import(
    create_property_view,
    detail_property_view,
    edit_property_view,
    check_price,
    bank_api
)

app_name = 'property'

urlpatterns = [
    path('create/', create_property_view, name="create"),
    path('<slug>/', detail_property_view, name="detail"),
    path('<slug>/price', check_price, name="price"),
    path('<slug>/edit', edit_property_view, name="edit"),
    path('<slug>/bank', bank_api, name="bank"),

]
