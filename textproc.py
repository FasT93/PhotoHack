import re

class TextProcessor():
    def __init__(self):
        self.cyril = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
        self.latin = 'abcdefghijklmnopqrstuvwxyz'
        self.symbols = ' ,.:!?1234567890-'
        self.resolved = self.cyril + self.latin + self.symbols

    # Основная функция
    def parse(self, text):
        text = self.trim_spaces(text)
        text = self.single_spaces(text)
        text = self.resolved_symbols(text)
        return text.split()

    # Удаление пробелов слева и справа
    def trim_spaces(self, text):
        return text.strip()

    # Замена мультипробелов на единичные
    def single_spaces(self, text):
        return re.sub(' +', ' ', text)

    # Удаление ненужных символов
    def resolved_symbols(self, text):
        return ''.join([s for s in text if s.lower() in self.resolved])

    # Разделение по пробелу
    def split(self, text):
        return text.split()
