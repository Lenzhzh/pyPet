import json
import os


class SettingManager:
    def __init__(self, schema_path, setting_path):
        self.schema_path = schema_path
        self.setting_path = setting_path

        self.schema = self._load_json(self.schema_path)
        if not(self.schema):
            print("Error: Schema file not found or is empty !")
            return

        self.settings = self._load_settings()
        print(self.settings)

    def _load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def _load_settings(self):
        settings = self._load_json(self.setting_path)

        defaults = { item['id'] : item['default'] for item in self.schema }

        if settings:
            defaults.update(settings)
        
        return defaults

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
    
    def save(self):
        try:
            with open(self.setting_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            print("INFO: Settings saved successfully")
            return True
        except :
            print(f"Error: Fail in loading settings: {Exception}")
            return False
    
    def get_schema(self):
        return self.schema