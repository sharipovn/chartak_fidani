from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required  
from django.views.decorators.http import require_http_methods
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator
from django.db.models import Q


@require_http_methods(["GET", "POST"])
def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next") or "home"
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        messages.error(request, "Login yoki parol noto‘g‘ri.")
    return render(request, "login.html", {"next": next_url})

def logout_view(request):
    next_url = request.GET.get("next") or "home"
    logout(request)
    return redirect(next_url)




@login_required
def products_list(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.select_related("create_user").order_by("-created_at")
    if q:
        qs = qs.filter(Q(meat_name__icontains=q) | Q(meat_code__icontains=q))

    paginator = Paginator(qs, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    form = ProductForm()

    return render(request, "products_list.html", {
        "form": form,
        "page_obj": page_obj,
        "total_count": paginator.count,
        "q": q,
    })

@login_required
def product_create(request):
    if request.method != "POST":
        return redirect("products_list")
    form = ProductForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.create_user = request.user
        obj.save()
        messages.success(request, "Mahsulot qo'shildi.")
    else:
        messages.error(request, "Formada xatolik bor. Qayta tekshiring.")
    return redirect("products_list")

@login_required
def product_update(request, pk):
    if request.method != "POST":
        return redirect("products_list")
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        form.save()  # updated_at avtomatik yangilanadi; SimpleHistory ham yozadi
        messages.success(request, f"Mahsulot yangilandi: {product.meat_name}")
    else:
        messages.error(request, "Tahrirlashda xatolik. Maydonlarni tekshiring.")
    return redirect("products_list")


@login_required
def history(request):
    pass
    return render(request, "history.html")








def home(request):
    return render(request, "home.html")
