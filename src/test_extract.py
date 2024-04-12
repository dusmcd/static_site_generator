import unittest
from extract import extract_markdown_images, extract_markdown_links

test_cases_images = [
    ("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", [
        ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
    ]),
    ("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
      "and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", [
        ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ("another","https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png" )
      ])
]
test_cases_links = [
    ("Here is some text with a [link](https://www.google.com)", [("link", "https://www.google.com")]),
    ("Here is some text with a [link](https://www.google.com) and here is another [thing to click on](http://scarysite.com)",
        [("link", "https://www.google.com"), ("thing to click on", "http://scarysite.com")])
]
class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        for test_case in test_cases_images:
            actual_value = extract_markdown_images(test_case[0])
            expected_value = test_case[1]
            self.assertEqual(actual_value, expected_value)

    def test_extract_markdown_links(self):
        for test_case in test_cases_links:
            actual_value = extract_markdown_links(test_case[0])
            expected_value = test_case[1]
            self.assertEqual(actual_value, expected_value)

if __name__ == "__main__":
    unittest.main()