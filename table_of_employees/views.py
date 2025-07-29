from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from datetime import timedelta
from django.utils.timezone import now
import logging


@main_auth(on_cookies=True)
def employee_table(request):
    logger = logging.getLogger(__name__)
    bitrix_token = request.bitrix_user_token

    # Получаем всех активных пользователей
    response = bitrix_token.call_api_method('user.get', {
        'FILTER': {'ACTIVE': 'Y'},
        'SELECT': ['ID', 'NAME', 'LAST_NAME', 'UF_HEAD']
    })
    users = response.get('result', [])
    user_dict = {user['ID']: user for user in users}

    date_from = (now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S%z')

    employees = []
    for user in users:
        chain = []
        current = user.get('UF_HEAD')
        visited = set()
        while current and current not in visited:
            visited.add(current)
            supervisor = user_dict.get(current)
            if supervisor:
                name = f"{supervisor['NAME']} {supervisor['LAST_NAME']}"
                chain.append(name)
                current = supervisor.get('UF_HEAD')
            else:
                break

        try:
            date_from = (now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S%z').replace(':', '')
            call_data = bitrix_token.call_api_method('voximplant.statistic.get', {
                'FILTER': {
                    'USER_ID': int(user['ID']),
                    'CALL_TYPE': 1,
                    'CALL_DURATION_from': 60,
                    'CALL_START_from': date_from
                }
            })
            raw_calls = call_data.get('result', [])
            filtered_calls = [c for c in raw_calls if str(c['PORTAL_USER_ID']) == str(user['ID'])]

            logger.warning(f"Filtered {len(filtered_calls)} calls for user {user['ID']}")
            call_count = len(filtered_calls)
        except Exception as e:
            logger.error(f"Error getting call data for {user['ID']}: {e}")
            call_count = 0

        employees.append({
            'id': user['ID'],
            'name': f"{user['NAME']} {user['LAST_NAME']}",
            'supervisors': chain,
            'calls': call_count
        })

    return render(request, 'table_of_employees/employee_table.html', {
        'employees': employees
    })