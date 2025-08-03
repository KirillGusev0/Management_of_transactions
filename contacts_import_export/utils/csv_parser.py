import csv
from .base_parser import BaseParser

class CSVParser(BaseParser):
    def parse(self):
        contacts = []
        with open(self.file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contacts.append({
                    "NAME": row.get("имя", "").strip(),
                    "LAST_NAME": row.get("фамилия", "").strip(),
                    "PHONE": row.get("номер телефона", "").strip(),
                    "EMAIL": row.get("почта", "").strip(),
                    "COMPANY": row.get("компания", "").strip(),
                })

        return contacts
