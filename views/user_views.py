# MANAGEMENT_OF_TRANSACTIONS/views/user_views.py
from django.conf import settings
from django.urls import reverse
from integration_utils.bitrix24.functions.api_call import api_call
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from settings import APP_PUBLIC_URL

def oauth_start(request):
    from urllib.parse import urlencode
    print("Incoming GET params:", request.GET)
    client_id = settings.APP_SETTINGS.application_bitrix_client_id
    redirect_uri = f"{settings.APP_PUBLIC_URL}/bitrix/callback/"

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
    }
    url = f"https://oauth.bitrix.info/oauth/authorize?{urlencode(params)}"
    return redirect(url)


@csrf_exempt
def oauth_callback(request):
    code = request.GET.get("code")
    domain = request.GET.get("domain")
    print("===> Исходный DOMAIN из Bitrix:", request.GET.get('DOMAIN') or request.POST.get('DOMAIN'))
    if not code or not domain:
        return HttpResponse("Ошибка: code или domain не передан.", status=400)


    token_response = api_call(
        domain=domain,
        api_method="oauth.token",
        params={
            "grant_type": "authorization_code",
            "client_id": settings.APP_SETTINGS.application_bitrix_client_id,
            "client_secret": settings.APP_SETTINGS.application_bitrix_client_secret,
            "code": code,
        },
        access_token=None
    )
    print("Token response:", token_response)

    access_token = token_response.get("access_token")
    if not access_token:
        return HttpResponse("Ошибка получения токена.", status=400)


    request.session["access_token"] = access_token
    request.session["domain"] = domain
    print("Сохранили в сессию: ", access_token, domain)
    print("===> Исходный DOMAIN из Bitrix:", request.GET.get('DOMAIN') or request.POST.get('DOMAIN'))
    return redirect("home")

@csrf_exempt
def home(request):
    access_token = request.session.get('access_token')
    domain = request.session.get('domain')
    print("Session access_token:", access_token)
    print("Session domain:", domain)

    if not access_token or not domain:
        print("Токен не найден. Перенаправляем на OAuth start...")
        return redirect("bitrix_oauth_start")

    response = api_call(
        domain=domain,
        api_method="user.current",
        auth_token=access_token
    )
    response_data = response.json()
    print("Bitrix API response:", response_data)

    user = response_data.get("result", {})
    return render(request, "start_page.html", {"user": user})