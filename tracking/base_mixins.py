class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
    def handle_log(self):
        raise NotImplementedError

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
