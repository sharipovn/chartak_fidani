from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User  # <-- qo'shildi
from simple_history.models import HistoricalRecords   # 👈 qo'shildi
from django.utils.timezone import now

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    meat_code = models.CharField(max_length=64, unique=True, db_index=True, help_text="Mahsulot kodi yagona bo‘lishi kerak.")
    meat_name = models.CharField(max_length=160, db_index=True)
    meat_in_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    meat_sell_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_products")  # <-- ForeignKey
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # 🔥 SimpleHistory
    history = HistoricalRecords()
    
    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.meat_name} ({self.meat_code})"


class IncomeSale(models.Model):
    class ActionType(models.TextChoices):
        KIRIM = "KIRIM", "Kirim"
        SOTUV = "SOTUV", "Sotuv"

    class QuantityUnit(models.TextChoices):
        KG = "KG", "Kilogram"
        TONNA = "TONNA", "Tonna"

    id = models.BigAutoField(primary_key=True)
    meat = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="income_sales", db_index=True)
    in_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=Decimal("0.00"))
    sell_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=Decimal("0.00"))
    action_type = models.CharField(max_length=6, choices=ActionType.choices, db_index=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal('0.001'))])
    quantity_unit = models.CharField(max_length=8, choices=QuantityUnit.choices, default=QuantityUnit.KG)
    total_in_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)], default=Decimal("0.00"))
    total_sell_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)], default=Decimal("0.00"))
    operation_date = models.DateTimeField(db_index=True, default=now)  # ✅ default bugungi sana
    from_where = models.CharField(max_length=500)
    to_where = models.CharField(max_length=500)
    create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_income_sales")  # <-- ForeignKey
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_perexod = models.BooleanField(default=False, db_index=True)
    perexod_time = models.DateTimeField(null=True, blank=True)
    
    # 🔥 SimpleHistory
    history = HistoricalRecords()
    
    class Meta:
        db_table = "income_sale"
        ordering = ["-operation_date", "-id"]
        indexes = [
            models.Index(fields=["meat", "operation_date"]),
            models.Index(fields=["action_type", "operation_date"]),
        ]

    def __str__(self):
        return f"{self.action_type} | {self.meat} | {self.quantity} {self.quantity_unit}"
