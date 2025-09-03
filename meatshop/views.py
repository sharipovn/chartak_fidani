from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required  
from django.views.decorators.http import require_http_methods
from .models import Product,IncomeSale
from .forms import ProductForm,IncomeSaleForm
from django.core.paginator import Paginator
from django.db.models import Sum, Q, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now, timedelta


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


@login_required
def home(request):
    q = request.GET.get("q", "").strip()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # faqat perexod qilinmagan yozuvlar
    qs = IncomeSale.objects.filter(is_perexod=False).select_related("meat", "create_user").order_by("-operation_date")

    # sana filtri faqat foydalanuvchi tanlasa ishlaydi
    if start_date and end_date:
        qs = qs.filter(operation_date__date__gte=start_date, operation_date__date__lte=end_date)
    elif start_date:
        qs = qs.filter(operation_date__date__gte=start_date)
    elif end_date:
        qs = qs.filter(operation_date__date__lte=end_date)

    # qidiruv
    if q:
        qs = qs.filter(Q(meat__meat_code__icontains=q) | Q(meat__meat_name__icontains=q))

    # sahifalash
    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # umumiy hisob (filtrlarsiz, faqat is_perexod=False)
    base_qs = IncomeSale.objects.filter(is_perexod=False)
    total_kirim = base_qs.filter(action_type="KIRIM").aggregate(Sum("quantity"))["quantity__sum"] or 0
    total_sotuv = base_qs.filter(action_type="SOTUV").aggregate(Sum("quantity"))["quantity__sum"] or 0
    total_left_kg = total_kirim - total_sotuv

    print('page_obj:',page_obj)
    context = {
        "page_obj": page_obj,
        "q": q,
        "start_date": start_date,
        "end_date": end_date,
        "total_left_kg": total_left_kg,
        "total_left_ton": total_left_kg / 1000,
        "form": IncomeSaleForm(),
    }
    return render(request, "home.html", context)


@login_required
def income_sale_create(request):
    if request.method == "POST":
        form = IncomeSaleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.create_user = request.user

            # quantity ni kg ga o‘tkazish
            qty = obj.quantity * (1000 if obj.quantity_unit == "TONNA" else 1)

            # narxlarni product dan olish
            obj.in_price = obj.meat.meat_in_price
            obj.sell_price = obj.meat.meat_sell_price

            # umumiy hisob
            obj.total_in_price = qty * obj.in_price
            obj.total_sell_price = qty * obj.sell_price

            obj.save()
            messages.success(request, "IncomeSale qo‘shildi.")
        else:
            messages.error(request, "Formada xatolik bor.")
    return redirect("home")


@login_required
def income_sale_update(request, pk):
    income_sale = get_object_or_404(IncomeSale, pk=pk)
    if income_sale.create_user != request.user and not request.user.is_superuser:
        messages.error(request, "Faqat o‘zingiz yaratgan yozuvni tahrirlay olasiz.")
        return redirect("home")

    if request.method == "POST":
        form = IncomeSaleForm(request.POST, instance=income_sale)
        if form.is_valid():
            obj = form.save(commit=False)

            qty = obj.quantity * (1000 if obj.quantity_unit == "TONNA" else 1)
            obj.in_price = obj.meat.meat_in_price
            obj.sell_price = obj.meat.meat_sell_price
            obj.total_in_price = qty * obj.in_price
            obj.total_sell_price = qty * obj.sell_price

            obj.save()
            messages.success(request, "IncomeSale yangilandi.")
        else:
            messages.error(request, "Tahrirlashda xatolik bor.")
    return redirect("home")
