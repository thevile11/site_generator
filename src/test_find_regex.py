import unittest
from find_regex import extract_markdown_images,extract_markdown_links

class FindRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to youtube](https://www.youtube.com)")
        self.assertListEqual([("to youtube", "https://www.youtube.com")], matches)