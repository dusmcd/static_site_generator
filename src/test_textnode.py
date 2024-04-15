import unittest

from textnode import (
     TextNode, 
     TextType, 
)

test_cases_eq = [
    (TextNode("Text Node", "bold"), TextNode("Text Node", "bold")),
]

test_cases_not_eq = [
    (TextNode("Text Node", "bold"), TextNode("Some other text", "underline", "http://example.com")),
    (TextNode("Text Node", "italics"), TextNode("Text Node", "bold", "https://www.google.com")),
    (TextNode("Text Node", "bold"), TextNode("Text Node", "italics")),
    (TextNode("Text Node", "bold"), TextNode("Text Node", "bold", "https://www.google.com"))   
]

test_cases_text_html = [
    (TextNode("foo bar", TextType.TEXT), "LeafNode(foo bar, None, None)"),
    (TextNode("Tax exam", TextType.BOLD), "LeafNode(Tax exam, b, None)"),
    (TextNode("Link", TextType.LINK, "http://sc.edu"), "LeafNode(Link, a, {'href': 'http://sc.edu'})"),
    (TextNode("puppy", TextType.IMAGE, "/puppy.jpg"), "LeafNode(puppy, img, {'src': '/puppy.jpg', 'alt': 'puppy'})"),
    (TextNode("Tax exam", TextType.ITALIC), "LeafNode(Tax exam, i, None)"),
    (TextNode("const foo = 'bar'", TextType.CODE), "LeafNode(const foo = 'bar', code, None)"),
]

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        for test_case in test_cases_eq:
            node1 = test_case[0]
            node2 = test_case[1]
            self.assertEqual(node1, node2)
        for test_case in test_cases_not_eq:
            node1 = test_case[0]
            node2 = test_case[1]
            self.assertNotEqual(node1, node2)

    def test_text_node_html_node(self):
        for test_case in test_cases_text_html:
            actual_value = str(test_case[0].text_node_to_html_node())
            expected_value = test_case[1]
            self.assertEqual(actual_value, expected_value)
        try:
            TextNode("We've got a problem", None)
        except Exception as e:
            self.assertRaises(Exception)
            self.assertEqual(str(e), "Given type not recognized")

    
if __name__ == "main":
    unittest.main()