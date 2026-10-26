import os
import shutil
import tempfile
import unittest

from letterboxdpy.utils.utils_file import CsvFile


class TestCsvFile(unittest.TestCase):
    def setUp(self):
        # Keep temp files out of the working directory so parallel runs and
        # interrupted runs cannot leave artifacts behind in the repo.
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.path = os.path.join(self.tmpdir, 'data.csv')

    def test_round_trip_preserves_embedded_newlines(self):
        for newline in ('\r\n', '\r', '\n'):
            with self.subTest(newline=repr(newline)):
                headers = ['Title', 'Review' + newline + 'text']
                rows = [
                    ['Amélie', 'First' + newline + 'second, "quoted"'],
                    ['Another film', ''],
                ]
                CsvFile.save(self.path, rows, headers=headers)
                self.assertEqual(CsvFile.load(self.path), [headers] + rows)

    def test_save_writes_crlf_inside_quoted_fields(self):
        # The bug this guards against: reading with newline=None (universal
        # newlines) collapsed CRLF/CR embedded in quoted fields, so a file
        # written by CsvFile.save could not be read back unchanged.
        CsvFile.save(self.path, [['a\r\nb']])
        with open(self.path, 'rb') as f:
            self.assertIn(b'"a\r\nb"', f.read())

    def test_empty_file(self):
        CsvFile.save(self.path, [])
        self.assertEqual(CsvFile.load(self.path), [])

    def test_missing_file(self):
        self.assertIsNone(CsvFile.load(self.path))
        self.assertFalse(os.path.exists(self.path), 'load() must not create the file')


if __name__ == '__main__':
    unittest.main()
