from rest_framework.views import APIView
from rest_framework.response import Response

from tracking.mixins import LoggingMixin


class MockNoLoggingView(APIView):
    def get(self, request):
        return Response('no logging')


class MockLoggingView(LoggingMixin, APIView):
    logging_methods = [
        'GET',
        'POST',
    ]
    sensitive_fields = [
        'secret',
        'password'
    ]

    # def should_log(self, request, response):
    #     return response.status_code >= 400

    def get(self, request):
        return Response({'secret': 'hello'}, status=404)

    def post(self, request):
        return Response({})
