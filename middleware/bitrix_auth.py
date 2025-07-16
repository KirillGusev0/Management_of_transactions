from django.utils.deprecation import MiddlewareMixin

class BitrixAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_id = request.GET.get('AUTH_ID') or request.POST.get('AUTH_ID')

        domain = request.GET.get('DOMAIN') or request.POST.get('DOMAIN')
        if domain:
            domain = domain.rstrip("/rest")
            request.session["domain"] = domain
        if auth_id and domain:
            print("===> BitrixAuthMiddleware: сохранили AUTH_ID и DOMAIN в сессию")
            request.session['access_token'] = auth_id
            request.session['domain'] = domain
        else:
            print("===> BitrixAuthMiddleware: AUTH_ID и DOMAIN не найдены в запросе")