from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsViewTestCase(TestCase):
    fixtures = ['categories.json',
                'goods.json']  # Будет заполняться тестовая БД
    
    def setUp(self) -> None:
        self.products = Product.objects.all()
    
    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertEqual(list(response.context_data['object_list']),
                         list(self.products[:3]))
    
    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': 1})
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )
