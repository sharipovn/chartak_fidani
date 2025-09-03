from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    
    path("products/", views.products_list, name="products_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/update/", views.product_update, name="product_update"),  # ⬅️ YANGI
    path("products/history/", views.products_list, name="history"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]