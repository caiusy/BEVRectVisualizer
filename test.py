import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from main import MainWindow

class MainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = MainWindow()

    @patch('os.listdir')
    @patch('builtins.open', new_callable=MagicMock)
    def test_read_data(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['file1.json', 'file2.json']
        mock_open.return_value.__enter__.return_value.read.return_value = '[{"x": 10, "y": 20, "width": 30, "height": 40}]'
        data = self.window.read_data('data_folder')
        self.assertEqual(len(data), 2)
        self.assertEqual(data['file1.json'][0]['x'], 10)

    def test_create_layer(self):
        data = [{"x": 10, "y": 20, "width": 30, "height": 40}]
        items = self.window.create_layer(data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].rect().x(), 10)

    def test_toggle_layer(self):
        data = {"layer1": [{"x": 10, "y": 20, "width": 30, "height": 40}]}
        self.window.layers = {key: self.window.create_layer(value) for key, value in data.items()}
        self.window.create_button(0, "layer1")
        self.window.toggle_layer(0)
        self.assertTrue(self.window.layers["layer1"][0].isVisible())

    def test_show_prev(self):
        self.window.data = {"file1.json": [{"x": 10, "y": 20, "width": 30, "height": 40}], "file2.json": [{"x": 50, "y": 60, "width": 70, "height": 80}]}
        self.window.index = 1
        self.window.show_prev()
        self.assertEqual(self.window.index, 0)

    def test_show_next(self):
        self.window.data = {"file1.json": [{"x": 10, "y": 20, "width": 30, "height": 40}], "file2.json": [{"x": 50, "y": 60, "width": 70, "height": 80}]}
        self.window.index = 0
        self.window.show_next()
        self.assertEqual(self.window.index, 1)

if __name__ == '__main__':
    unittest.main()