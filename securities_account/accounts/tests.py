from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import AccountApplication


class AccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        #建立使用者
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')

    def test_register_view(self):
        #測試註冊頁面 GET 請求
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, '註冊')
        #測試註冊 POST 請求
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertRedirects(response, reverse('login'))
        # 確認新使用者已建立
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_superuser_register_view(self):
        #測試管理員註冊頁面 GET 請求
        response = self.client.get(reverse('superuser_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, '建立管理員帳號')

        # 測試管理員註冊 POST 請求
        response = self.client.post(reverse('superuser_register'), {
            'username': 'superuser2',
            'password1': 'superpassword123',
            'password2': 'superpassword123',
        })
        self.assertRedirects(response, reverse('login'))
        #確認新管理員帳號已建立且為 superuser
        self.assertTrue(User.objects.filter(username='superuser2', is_superuser=True).exists())

    def test_apply_account_view(self):
        self.client.login(username='testuser', password='testpass')
        #測試申請帳號頁面 GET 請求
        response = self.client.get(reverse('apply_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/apply.html')

        #測試申請帳號 POST 請求
        response = self.client.post(reverse('apply_account'), {
            'account_name': 'Test Account',
            'phone': '0912345678',
            'address': 'Tauyuan',
        })
        self.assertRedirects(response, reverse('view_my_applications'))
        self.assertTrue(AccountApplication.objects.filter(user=self.user, account_name='Test Account').exists())

    def test_view_my_applications_redirect_to_approved(self):
        self.client.login(username='testuser', password='testpass')
        #建立一筆已通過的申請
        AccountApplication.objects.create(user=self.user, account_name='A', phone='1', address='2', status='APPROVED')
        #自動跳轉到approved_page
        response = self.client.get(reverse('view_my_applications'))
        self.assertRedirects(response, reverse('approved_page'))

    def test_supplement_info_post(self):
        self.client.login(username='testuser', password='testpass')
        #建立一筆需補件的申請
        app = AccountApplication.objects.create(user=self.user, account_name='B', phone='1', address='2', status='ADDITIONAL')
        #測試補件頁面 GET 請求
        response = self.client.get(reverse('supplement_info', args=[app.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/apply.html')

        #測試補件 POST 請求
        response = self.client.post(reverse('supplement_info', args=[app.id]), {
            'account_name': 'B',
            'phone': '0911222333',
            'address': '新北市',
        })
        app.refresh_from_db()
        self.assertRedirects(response, reverse('view_my_applications'))
        self.assertEqual(app.status, 'PENDING')

    def test_approved_page_without_approved_application(self):
        #若沒有通過的申請自動導向view_my_applications
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('approved_page'))
        self.assertRedirects(response, reverse('view_my_applications'))

    def test_admin_actions(self):
        # 測試 Django admin actions
        app1 = AccountApplication.objects.create(user=self.user, account_name='C', phone='1', address='2', status='PENDING')
        app2 = AccountApplication.objects.create(user=self.user, account_name='D', phone='1', address='2', status='PENDING')
        # 登入管理員
        self.client.login(username='admin', password='adminpass')
        # 模擬 admin action: mark_approved
        AccountApplication.objects.filter(pk=app1.pk).update(status='APPROVED')
        app1.refresh_from_db()
        self.assertEqual(app1.status, 'APPROVED')
        # 模擬 admin action: mark_rejected
        app2.status = 'REJECTED'
        app2.rejection_reason = '帳號重複'
        app2.save()
        app2.refresh_from_db()
        self.assertEqual(app2.status, 'REJECTED')
        self.assertEqual(app2.rejection_reason, '帳號重複')
        # 模擬 admin action: mark_additional
        app2.status = 'ADDITIONAL'
        app2.additional_requirements = '請補充電話或地址'
        app2.save()
        app2.refresh_from_db()
        self.assertEqual(app2.status, 'ADDITIONAL')
        self.assertEqual(app2.additional_requirements, '請補充電話或地址')


