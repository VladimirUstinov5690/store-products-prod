from rest_framework import serializers, fields

from products.models import Product, ProductCategory, Basket


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name',
                                            queryset=ProductCategory.objects.all())
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'quantity', 'image',
            'category')


class BasketSSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()
    
    class Meta:
        model = Basket
        fields = (
            'id', 'product', 'quantity', 'sum', 'total_sum', 'total_quantity',
            'created_timestamp')
        read_only_fields = ('created_timestamp',)
        pagination_class = None
    
    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
    
    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()
