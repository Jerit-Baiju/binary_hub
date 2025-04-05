from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('scrap/<int:pk>/', views.scrap_detail, name='scrap_detail'),
    path('add-scrap/', views.add_scrap, name='add_scrap'),
    path('edit-scrap/<int:pk>/', views.edit_scrap, name='edit_scrap'),
    path('delete-scrap/<int:pk>/', views.delete_scrap, name='delete_scrap'),
    path('order/<int:pk>/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]