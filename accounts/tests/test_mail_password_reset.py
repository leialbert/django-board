from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordResetMailTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username = 'Albert',
            email = 'albert@hotmail.com',
            password='123cdf'
        )
        self.response = self.client.post(reverse('password_reset'),{'email':'albert@hotmail.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Django Boards] Please reset your password', self.email.subject)

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
        self.assertEqual(['john@doe.com'],self.email.to)