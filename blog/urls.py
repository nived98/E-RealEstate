from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.home, name='home'),
    path('mapssas/',views.buymaps,name='buymaps'),
    path('account/', views.account_view, name='account'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    # path('edit/', views.edit_profile_view, name='edit'),
    path('search/', views.search_view, name='search'),
    path('rent/', views.rent_view, name='rent'),
    path('sell/', views.sell_view, name='sell'),
    path('type1/', views.type1_view, name='type1'),
    path('type2/', views.type2_view, name='type2'),
    path('search_s/', views.sell_search_view, name='search_s'),
    path('search_r/', views.rent_search_view, name='search_r'),
    path('search_t1/', views.t1_search_view, name='search_t1'),
    path('search_t2/', views.t2_search_view, name='search_t2'),
    path('<city>/', views.city_view, name='city'),
    path('<city>/list', views.city_props, name='props'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    path('profile/', views.profile_view, name='profile')      
]