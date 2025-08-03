class BaseParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        """Должен вернуть список словарей с ключами NAME, LAST_NAME, PHONE, EMAIL, COMPANY"""
        raise NotImplementedError