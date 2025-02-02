import stripe
from django.db import models
from django.conf import settings

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True,
                                   blank=True)
    
    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', null=True,
                              blank=True)
    category = models.ForeignKey(to=ProductCategory,
                                 on_delete=models.CASCADE)
    stripe_product_price_id = models.CharField(max_length=128, null=True,
                                               blank=True)
    
    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False,
                                  using=None, update_fields=None)
    
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),  # Цена в копейках
            currency='rub'
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)
    
    # Для Stripe (получаем id объекта цены из Stripe, чтоб сохранить в БД)
    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    
    # Переопределяем менеджер objects, так как добавили собственные методы
    objects = BasketQuerySet.as_manager()
    
    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'
    
    def sum(self):
        return self.product.price * self.quantity
    
    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)
    
    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)
    
    def de_json(self):
        
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        
        return basket_item
    
    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)
        
        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id,
                                        quantity=1)
            is_created = True
            return obj, is_created
        else:
            baskets = baskets.first()
            baskets.quantity += 1
            baskets.save()
            is_created = False
            return baskets, is_created
