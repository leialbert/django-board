from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = 'albert',
            email = 'albert@hotmail.com',
            password='123cdeff'
        )
        url = reverse('password_reset')
        data = {
            'email': 'albert@hotmail.com'
        }
        self.response = self.client.post(url,data)
        self.email = mail.outbox[0]


    def test_email_subject(self):
        self.assertEqual('[Django Board] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm',kwargs={
            'uidb64':uid,
            'token':token
        })

        self.assertIn(password_reset_token_url,self.email.body)
        self.assertIn('albert',self.email.body)
        self.assertIn('albert@hotmail.com',self.email.body)

    def test_mail_to(self):
        self.assertEqual(['albert@hotmail.com'],self.email.to)