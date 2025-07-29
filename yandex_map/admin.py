from django.contrib import admin

# Register your models here.
'''
def get_logo (company):

    bitrix_domain = settings.BITRIX_DOMAIN
    root_url = settings.ROOT_URL
    download_url = company.get('LOGO').get('downloadUrl')
    full_url = f'https://{bitrix_domain}{download_url}'
    logo_dir = os.path.join(settings.MEDIA_ROOT, 'company_logos')
    os.makedirs(logo_dir, exist_ok=True)
    file_path = os.path.join(logo_dir, f'logo_{company["ID"]}.png')

    if os.path.exists(file_path):
        relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
        return root_url+f'{settings.MEDIA_URL}{relative_path}'.replace( '\\', '/')
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f'Download error, id: {company["ID"]}: {e}')
    relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
    return root_url + f'{settings.MEDIA_URL}{relative_path}'.replace('\\','/')

'''