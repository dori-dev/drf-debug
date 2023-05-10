from rest_framework.views import APIView
from rest_framework.response import Response

from tracking.mixins import LoggingMixin


class Home(LoggingMixin, APIView):
    # logging_methods = [
    #     'GET',
    # ]
    
    sensitive_fields = [
        'secret',
        'password'
    ]

    # def should_log(self, request, response):
    #     return response.status_code >= 400

    def get(self, request):
        return Response({}, status=404)

    def post(self, request):
        return Response({})
