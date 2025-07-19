# Пример local_settings

DEBUG = True
ALLOWED_HOSTS = ['*']

from integration_utils.bitrix24.local_settings_class import LocalSettingsClass

TINKOFF_API_KEY = 'your-api-key'
ENDPOINT_TINKOFF = 'your-secret-key'
API_KEY_TINKOFF = 'your-api-key'
SECRET_KEY_TINKOFF = 'your-secret-key'

OPEN_AI_API_KEY = 'your-api-key'

NGROK_URL = 'http://localhost:8000'

APP_SETTINGS = LocalSettingsClass(
    portal_domain='b24-dev75q.bitrix24.ru',
    app_domain='127.0.0.1:8000',
    app_name='Management_of_transactions',
    salt='wefiewofioiI(IF(Eufrew8fju8ewfjhwkefjlewfjlJFKjewubhybfwybgybHBGYBGF',
    secret_key='wefewfkji4834gudrj.kjh237tgofhfjekewf.kjewkfjeiwfjeiwjfijewf',
    application_bitrix_client_id='local.68767ce6cfbd41.78311284',
    application_bitrix_client_secret='NL006ZoakbQiVZubB1mYf2bxFzBaFIvh8xJY4pPW92OaiiGutK',
    application_index_path='/',
)

DOMAIN = "56218ef983f3-8301993767665431593.ngrok-free.app"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #   django.db.backends.postgresql
        'NAME': 'management_of_transactions',  # Or path to database file if using sqlite3.
        'USER': 'test_user',  # Not used with sqlite3.
        'PASSWORD': 'asd',  # Not used with sqlite3.
        'HOST': 'localhost',
        'PORT': '5432',
    },
}