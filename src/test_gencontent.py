import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_ok(self):
        md = "# Hello ziom"
        result = extract_title(md)
        expected = "Hello ziom"
        self.assertEqual(result, expected)

    def test_extract_title_bad(self):
        md = "NotHelloAtall"
        with self.assertRaises(ValueError):
            extract_title(md)
