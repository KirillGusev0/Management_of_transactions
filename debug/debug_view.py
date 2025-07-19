from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

@main_auth(on_cookies=True)
def debug_view(request):
    user = getattr(request, 'bitrix_user_token', None)
    if user:
        return HttpResponse(f"Авторизация ОК. Пользователь: {vars(user)}")
    else:
        return HttpResponse("❌ Нет токена. Пользователь не авторизован.")