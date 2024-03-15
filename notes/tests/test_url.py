from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings

from notes.views import ( HeartBeatAPIVIEW, download_file_on_the_go, webhook, bulk_create_test,
                    for_loop_create_test, SendMailApiView, Home, index,
                    AnnotateCategory )

class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_download_file_on_the_go(self):
        url = reverse('download_file_on_the_go', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_webhook(self):
        url = reverse('webhook')
        response = self.client.post(url)
        self.assertIsInstance(response, HttpResponse)

    def test_bulk_create_test(self):
        url = reverse('bulk_create_test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_for_loop_create_test(self):
        url = reverse('for_loop_create_test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sendmail_view(self):
        url = reverse('sendmail_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        
    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
