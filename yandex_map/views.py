import requests
import os
from django.conf import settings
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import json


def get_geocode(address):
    address_str = ', '.join(filter(None, [
        address.get('ADDRESS_1'),
        address.get('ADDRESS_2'),
        address.get('CITY'),
        address.get('PROVINCE'),
        address.get('REGION'),
        address.get('COUNTRY')
    ]))

    if not address_str.strip():
        raise ValueError("Адрес пуст — пропуск геокодирования.")

    api_key = settings.YANDEX_API_KEY
    if not api_key:
        raise ValueError("YANDEX_API_KEY не задан в настройках.")

    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address_str}&format=json'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Ошибка запроса к Yandex Geocoder: {response.status_code}, {response.text}")

    try:
        data = response.json()
        feature_member = data['response']['GeoObjectCollection']['featureMember']
        if not feature_member:
            raise ValueError(f"Геоданные не найдены по адресу: {address_str}")
        position = feature_member[0]['GeoObject']['Point']['pos']
        return [float(coord) for coord in position.split(' ')[::-1]]
    except Exception as e:
        print("Ошибка геокодирования:", e)
        return None


@main_auth (on_cookies=True)
def company_map (request):
    but = request.bitrix_user_token
    companies = but.call_list_method('crm.company.list')


    companies = but.call_list_method('crm.company.list', fields={"select": ["*"]})
    # debug
    print(json.dumps(companies[0], indent=4, ensure_ascii=False))
    #


    addresses = but.call_list_method('crm.address.list')
    # debug
    print(json.dumps(addresses, indent=4, ensure_ascii=False))
    #
    companies = {str(company['ID']): company for company in companies}
    addresses = {str(address['ENTITY_ID']): address for address in addresses}

    points = []
    for company_id, address in addresses.items():
        company = companies.get(company_id)
        if not company:
            print(f"Компания с ID {company_id} не найдена.")
            continue

        try:
            geocode = get_geocode(address)
            if not geocode:
                continue
        except Exception as e:
            print(f"Пропуск компании {company.get('TITLE')} из-за ошибки геокодирования: {e}")
            continue

        point = {
            'TITLE': company['TITLE'],
            'GEOCODE': geocode,
        }
        points.append(point)
    print("POINTS DATA >>>", json.dumps(points, ensure_ascii=False, indent=4))
    return render(request, 'yandex_map/yandex_map.html', {'points': points})

