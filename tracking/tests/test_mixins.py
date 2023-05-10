from rest_framework.test import APITestCase, APIRequestFactory
from django.test import override_settings

from tracking.models import APIRequestLog
from .views import MockLoggingView


@override_settings(ROOT_URLCONF='tracking.tests.urls')
class TestLoggingMixin(APITestCase):
    def test_no_logging_no_log_created(self):
        self.client.get('/no-logging/')
        self.assertEqual(APIRequestLog.objects.count(), 0)

    def test_logging_creates_log(self):
        self.client.get('/logging/')
        self.assertEqual(APIRequestLog.objects.count(), 1)

    def test_log_path(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.path, '/logging/')

    def test_log_remote_ip(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.2'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.2')

    def test_log_remote_ipv6(self):
        request = APIRequestFactory().get('/logging/')
        ip = '2001:0db8:3444:2222::ae24:0245:'
        request.META['REMOTE_ADDR'] = ip
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, ip)

    def test_log_remote_ipv6_loopback(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '::1'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '::1')

    def test_log_remote_ip_list(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.1.2, 127.0.0.3, 121.1.1.1'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.1.2')
