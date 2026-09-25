import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.file_io import StorageManager


class TestStorageManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), '_test_data')
        self.storage = StorageManager(data_dir=self.test_dir)

    def tearDown(self):
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load_json(self):
        data = {"key": "value", "number": 42}
        result = self.storage.save_json("test.json", data)
        self.assertTrue(result)
        loaded = self.storage.load_json("test.json")
        self.assertEqual(loaded, data)

    def test_load_nonexistent_file(self):
        loaded = self.storage.load_json("nonexistent.json")
        self.assertIsNone(loaded)

    def test_load_with_default(self):
        loaded = self.storage.load_json("nonexistent.json", default={"default": True})
        self.assertEqual(loaded, {"default": True})

    def test_delete_file(self):
        self.storage.save_json("to_delete.json", {"data": 1})
        result = self.storage.delete_file("to_delete.json")
        self.assertTrue(result)
        self.assertFalse(self.storage.file_exists("to_delete.json"))

    def test_file_exists(self):
        self.assertFalse(self.storage.file_exists("test.json"))
        self.storage.save_json("test.json", {"data": 1})
        self.assertTrue(self.storage.file_exists("test.json"))

    def test_save_user_data(self):
        data = {"user_name": "Test"}
        result = self.storage.save_user_data("user123", data)
        self.assertTrue(result)
        loaded = self.storage.load_user_data("user123")
        self.assertEqual(loaded, data)


if __name__ == '__main__':
    unittest.main()
