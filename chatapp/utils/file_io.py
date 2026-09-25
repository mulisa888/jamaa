import json
import os
from datetime import datetime


class StorageManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self._ensure_dir(data_dir)

    def _ensure_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _get_path(self, filename):
        return os.path.join(self.data_dir, filename)

    def save_json(self, filename, data):
        path = self._get_path(filename)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load_json(self, filename, default=None):
        path = self._get_path(filename)
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return default

    def delete_file(self, filename):
        path = self._get_path(filename)
        try:
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception:
            return False

    def file_exists(self, filename):
        return os.path.exists(self._get_path(filename))

    def save_user_data(self, user_id, data):
        return self.save_json(f"user_{user_id}.json", data)

    def load_user_data(self, user_id, default=None):
        return self.load_json(f"user_{user_id}.json", default)

    def save_app_state(self, data):
        return self.save_json("app_state.json", data)

    def load_app_state(self, default=None):
        return self.load_json("app_state.json", default)
