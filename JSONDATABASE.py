import json

class JsonDataLoader:
    def __init__(self, json_file_path):

        self.json_file_path = json_file_path
        self.data = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке JSON файла: {e}")

    def get_data(self):
        return self.data
