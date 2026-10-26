import os
import tempfile
import unittest

from letterboxdpy.utils.utils_file import CsvFile


class TestCsvFile(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile(suffix='.csv', dir=os.getcwd(), delete=False) as f:
            self.path = f.name
        self.addCleanup(lambda: os.path.exists(self.path) and os.remove(self.path))

    def test_round_trip_preserves_embedded_newlines(self):
        path = self.path[:-4]
        for newline in ('\r\n', '\r', '\n'):
            with self.subTest(newline=repr(newline)):
                headers = ['Title', 'Review' + newline + 'text']
                rows = [
                    ['Amélie', 'First' + newline + 'second, "quoted"'],
                    ['Another film', ''],
                ]
                CsvFile.save(path, rows, headers=headers)
                self.assertEqual(CsvFile.load(path), [headers] + rows)

    def test_empty_file(self):
        CsvFile.save(self.path, [])
        self.assertEqual(CsvFile.load(self.path), [])

    def test_missing_file(self):
        os.remove(self.path)
        self.assertIsNone(CsvFile.load(self.path))


if __name__ == '__main__':
    unittest.main()
