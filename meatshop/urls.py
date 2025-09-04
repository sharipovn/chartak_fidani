from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    
    path("products/", views.products_list, name="products_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/update/", views.product_update, name="product_update"),  # ⬅️ YANGI
    path("products/history/", views.products_list, name="history"),
    path("products/stock/", views.stock, name="stock"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
        # IncomeSale CRUD
    path("income-sale/create/", views.income_sale_create, name="income_sale_create"),
    path("income-sale/<int:pk>/update/", views.income_sale_update, name="income_sale_update"),
]