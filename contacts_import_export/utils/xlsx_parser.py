import openpyxl

class XLSXParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        wb = openpyxl.load_workbook(self.file_path)
        sheet = wb.active

        data = []
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return data

        # Заголовки
        headers = [str(h).strip().lower() for h in rows[0]]
        header_map = {
            'имя': 'имя',
            'фамилия': 'фамилия',
            'телефон': 'номер телефона',
            'номер телефона': 'номер телефона',
            'email': 'почта',
            'почта': 'почта',
            'компания': 'компания'
        }
        mapped_headers = [header_map.get(h, h) for h in headers]

        for row in rows[1:]:
            if not row or all(v is None or str(v).strip() == "" for v in row):
                continue

            row_dict = {}
            for i, key in enumerate(mapped_headers):
                value = row[i] if i < len(row) else ""
                value = str(value).strip() if value is not None else ""

                # Приводим телефон к формату
                if key == 'номер телефона' and value:
                    value = value if value.startswith("+") else f"+{value}"

                row_dict[key] = value

            # ❗ фильтруем только строки, где есть и имя, и телефон
            if row_dict.get('имя') and row_dict.get('номер телефона'):
                data.append(row_dict)

        print("DEBUG XLSX PARSED DATA:", data)
        return data