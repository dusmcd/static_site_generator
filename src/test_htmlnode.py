import unittest
from htmlnode import HtmlNode, LeafNode

test_cases_props = [
    (HtmlNode(tag="a", props={"href": "https://www.google.com", "class": "center"}, value="link"), ' href="https://www.google.com" class="center"'),
    (HtmlNode("a", "link", None, {"href": "https://www.something.com"}), ' href="https://www.something.com"'),
    (HtmlNode(tag="a", props={"href": "https://www.google.com", "class": "center", "id": "pizza"}, value="link"), ' href="https://www.google.com" class="center" id="pizza"')
]

test_cases_html = [
    (LeafNode("foo bar"), "foo bar"),
    (LeafNode("Link", "a"), "<a>Link</a>"),
    (LeafNode("Foo bar", "div", {"class": "container", "display": "inline-block"}), '<div class="container" display="inline-block">Foo bar</div>')
]

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        for test_case in test_cases_props:
            expected_output = test_case[1]
            actual_output = test_case[0].props_to_html()

            self.assertEqual(expected_output, actual_output)
    
class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        for test_case in test_cases_html:
            expected_output = test_case[1]
            actual_output = test_case[0].to_html()
            self.assertEqual(expected_output, actual_output)

    




if __name__ == "__main__":
    unittest.main()