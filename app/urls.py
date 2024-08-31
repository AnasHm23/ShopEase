from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # authentication
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # password reset
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # products
    path('products/', views.product_list, name='products'),
    path('products/<int:id>', views.product_detail, name='product_detail')
]
