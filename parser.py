import os

import PyPDF2


class KnowledgeBaseParser:
    def __init__(self, knowledge_base_path="knowledge_base"):
        self.knowledge_base_path = knowledge_base_path

    def parse_text_file(self, file_path):
        """Парсит обычные текстовые файлы"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Ошибка чтения файла {file_path}: {str(e)}"

    def parse_pdf(self, file_path):
        """Парсит PDF файлы"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            return f"Ошибка чтения PDF {file_path}: {str(e)}"

    def scan_knowledge_base(self):
        """Сканирует всю базу знаний и возвращает структуру"""
        knowledge_structure = {}

        for root, dirs, files in os.walk(self.knowledge_base_path):
            category = os.path.basename(root)
            knowledge_structure[category] = {
                'files': files,
                'file_count': len(files),
                'path': root
            }

        return knowledge_structure

    def get_total_stats(self):
        """Возвращает статистику по базе знаний"""
        structure = self.scan_knowledge_base()
        total_files = 0
        categories = []

        for category, data in structure.items():
            total_files += data['file_count']
            categories.append(category)

        return {
            'total_categories': len(categories),
            'total_files': total_files,
            'categories': categories
        }


if __name__ == "__main__":
    parser = KnowledgeBaseParser()
    stats = parser.get_total_stats()

    print("=== СТАТИСТИКА БАЗЫ ЗНАНИЙ ===")
    print(f"Категории: {stats['categories']}")
    print(f"Всего категорий: {stats['total_categories']}")
    print(f"Всего файлов: {stats['total_files']}")

    structure = parser.scan_knowledge_base()
    for category, data in structure.items():
        print(f"\n{category}: {data['file_count']} файлов")
        for file in data['files']:
            print(f"  - {file}")