from integration_utils.bitrix24.functions.api_call import api_call
from integration_utils.bitrix24.functions.batch_api_call import _batch_api_call
import csv


def create_contacts_from_data(bitrix_token, data):
    """Создаёт или обновляет контакты в Bitrix24 из списка словарей, исключая пустые и дубли."""

    # Загружаем список компаний
    companies_resp = api_call(
        domain=bitrix_token.domain,
        api_method='crm.company.list',
        auth_token=bitrix_token.auth_token,
        params={'select': ['ID', 'TITLE']}
    ).json()

    companies = {c['TITLE']: c['ID'] for c in companies_resp.get('result', [])}

    methods = []

    for idx, row in enumerate(data):
        name = (row.get('имя') or '').strip()
        last_name = (row.get('фамилия') or '').strip()
        phone = (row.get('номер телефона') or '').strip()
        email = (row.get('почта') or '').strip()
        company = (row.get('компания') or '').strip()

        # Пропускаем полностью пустые строки
        if not (name or phone or email):
            continue

        # Проверка наличия контакта с таким телефоном или email
        search_filter = {}
        if phone:
            search_filter['PHONE'] = phone
        elif email:
            search_filter['EMAIL'] = email

        existing_contact = []
        if search_filter:
            existing_resp = api_call(
                domain=bitrix_token.domain,
                api_method='crm.contact.list',
                auth_token=bitrix_token.auth_token,
                params={
                    'filter': search_filter,
                    'select': ['ID']
                }
            ).json()
            existing_contact = existing_resp.get('result', [])

        fields = {
            'NAME': name,
            'LAST_NAME': last_name,
        }
        if phone:
            fields['PHONE'] = [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}]
        if email:
            fields['EMAIL'] = [{'VALUE': email, 'VALUE_TYPE': 'WORK'}]
        if company and company in companies:
            fields['COMPANY_ID'] = companies[company]

        if existing_contact:
            # Обновляем найденный контакт
            contact_id = existing_contact[0]['ID']
            methods.append((f"update_{idx}", 'crm.contact.update', {
                'id': contact_id,
                'fields': fields
            }))
        else:
            # Создаём новый
            methods.append((f"add_{idx}", 'crm.contact.add', {'fields': fields}))

    # Пакетная отправка
    if methods:
        _batch_api_call(methods, bitrix_token, function_calling_from_bitrix_user_token_think_before_use=True)


def export_contacts_to_csv(bitrix_token, response):
    """Экспорт контактов в CSV без дублирующихся и пустых записей."""

    # Загружаем контакты
    contacts_resp = api_call(
        domain=bitrix_token.domain,
        api_method='crm.contact.list',
        auth_token=bitrix_token.auth_token,
        params={
            'select': ['ID', 'NAME', 'LAST_NAME', 'PHONE', 'EMAIL', 'COMPANY_ID'],
            'filter': {}  # все контакты
        }
    ).json()

    contacts = contacts_resp.get('result', [])

    # Загружаем компании для маппинга
    companies_resp = api_call(
        domain=bitrix_token.domain,
        api_method='crm.company.list',
        auth_token=bitrix_token.auth_token,
        params={'select': ['ID', 'TITLE']}
    ).json()

    companies = {c['ID']: c['TITLE'] for c in companies_resp.get('result', [])}

    # Создаём CSV
    writer = csv.writer(response)
    writer.writerow(['имя', 'фамилия', 'номер телефона', 'почта', 'компания'])

    seen = set()  # для проверки уникальности записей

    for c in contacts:
        phone = ''
        if c.get('PHONE'):
            phone = c['PHONE'][0].get('VALUE', '').strip()

        email = ''
        if c.get('EMAIL'):
            email = c['EMAIL'][0].get('VALUE', '').strip()

        company_name = companies.get(c.get('COMPANY_ID'), '')

        # Пропускаем записи, если нет ни телефона, ни email
        if not phone and not email:
            continue

        # Убираем дубликаты
        record_key = (c.get('NAME', '').strip(),
                      c.get('LAST_NAME', '').strip(),
                      phone,
                      email)

        if record_key in seen:
            continue

        seen.add(record_key)

        writer.writerow([
            c.get('NAME', '').strip(),
            c.get('LAST_NAME', '').strip(),
            phone,
            email,
            company_name
        ])

