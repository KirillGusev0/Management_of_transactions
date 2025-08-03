import os
import tempfile
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .utils.csv_parser import CSVParser
from .utils.xlsx_parser import XLSXParser
from .services.bitrix_service import create_contacts_from_data, export_contacts_to_csv
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def upload_contacts(request):
    message = None
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join('media', file.name)
        os.makedirs('media', exist_ok=True)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            parser = XLSXParser(file_path)

            data = parser.parse()
            print("DEBUG XLSX PARSED DATA:", data)
            create_contacts_from_data(request.bitrix_user_token, data)
            message = "✅ Контакты успешно загружены!"
        except Exception as e:
            message = f"❌ Ошибка загрузки: {str(e)}"
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return render(request, 'contacts_import_export/upload.html', {'message': message})

@main_auth(on_cookies=True)
def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'
    export_contacts_to_csv(request.bitrix_user_token, response)
    print("DEBUG PARSED DATA:", response)
    return response