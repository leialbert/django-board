from django.test import TestCase
from boards.models import Board
from django.urls import reverse,resolve
from ..views import home

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django',description='Django Board.')
        url = reverse('home')
        self.response = self.client.get(url)


    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func,home)

    def test_home_view_contains_link_to_topic_page(self):
        board_topics_url = reverse('board_topics',kwargs={
            'pk':self.board.pk
        })
        self.assertContains(self.response,'href="{0}"'.format(board_topics_url))
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics',kwargs={'pk':1})
        response = self.client.get(board_topics_url)
        home_page_url = reverse('home')
        self.assertContains(response,'href="{0}"'.format(home_page_url))