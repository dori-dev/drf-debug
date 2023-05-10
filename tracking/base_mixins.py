from traceback import format_exc
import logging

from django.utils.timezone import now


logger = logging.getLogger(__name__)


class BaseLoggingMixin:
    logging_methods = '__all__'
    sensitive_fields = []

    def initial(self, request, *args, **kwargs):
        user, username = self._get_user(request)
        self.log = {
            'requested_at': now(),
            'method': request.method,
            'host': request.get_host(),
            'path': request.path,
            'remote_addr': self._get_ip_address(request),
            'view': self._get_view_name(request),
            'view_method': self._get_view_method(request),
            'query_params': self._cleaned_data(request),
            'user': user,
            'username_persistent': username,
            'data': request.data,
        }
        super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        self.log.update({
            'response_ms': self._get_response_ms(),
            'status_code': response.status_code,
            'response': response.data,
        })
        try:
            self.handle_log(request, response)
        except Exception:
            logger.exception('Logging API call raise exception!')
        return response

    def handle_log(self, request, response):
        raise NotImplementedError

    def should_log(self, request, response):
        return bool(
            self.logging_methods == '__all__' or
            request.method in self.logging_methods
        )

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log['errors'] = format_exc()
        return response

    def _get_ip_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '').split(',')[0]

    def _get_view_name(self, request):
        class_ = self.__class__
        return f"{class_.__module__}.{class_.__name__}"

    def _get_view_method(self, request):
        if hasattr(self, 'action'):
            return self.action or None
        return request.method.lower()

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None, 'Anonymous'
        return user, user.get_username()

    def _get_response_ms(self):
        timedelta = now() - self.log['requested_at']
        response_ms = round(timedelta.total_seconds() * 1000)
        return max(response_ms, 0)

    def _cleaned_data(self, request):
        data: dict = request.query_params.dict()
        return dict(filter(
            lambda item: item[0] not in self.sensitive_fields,
            data.items(),
        ))
