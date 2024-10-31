from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    
    def setUp(self) -> None:
        self.data = {
            'ferst_name': 'admin', 'last_name': 'Ustinov',
            'username': 'admin', 'email': '5690@mail.ru',
            'password1': 'qazxsw21', 'password2': 'qazxsw21'
        }
        self.path = reverse('users:registration')
    
    def test_user_registration_get(self):
        response = self.client.get(self.path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')
    
    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users:login')
        self.assertTrue(User.objects.filter(username=username).exists())
        
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
