import unittest
from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HtmlNode(tag="a", props={"href": "https://www.google.com", "class": "center"}, value="link")
        expected_output = ' href="https://www.google.com" class="center"'
        actual_output = html_node.props_to_html()
        self.assertEqual(expected_output, actual_output)

        html_node2 = HtmlNode("a", "link", None, {"href": "https://www.something.com"})
        expected_output2 = ' href="https://www.something.com"'
        actual_output2 = html_node2.props_to_html()
        self.assertEqual(expected_output2, actual_output2)

        html_node3 = HtmlNode(tag="a", props={"href": "https://www.google.com", "class": "center", "id": "pizza"}, value="link")
        expected_output3 = ' href="https://www.google.com" class="center" id="pizza"'
        actual_output3 = html_node3.props_to_html()

        self.assertEqual(expected_output3, actual_output3)

    def test_repr(self):
        html_node = HtmlNode("p", "This is an awesome paragraph", None, {"id": "main", "display": "block"})
        expected_output = '<p id="main" display="block">This is an awesome paragraph</p>'
        actual_output = str(html_node)
        self.assertEqual(expected_output, actual_output)
        children = [
            HtmlNode("div", "Hello", None, {"class": "something"}),
            HtmlNode("a", "Home", None, {"href": "/landing"})    
        ]
        html_node2 = HtmlNode("p", None, children, {"id": "main", "display": "block"})
        expected_output = '<p id="main" display="block"><div class="something">Hello</div><a href="/landing">Home</a></p>'
        actual_output = str(html_node2)
        self.assertEqual(expected_output, actual_output)
    
    def test_init(self):
        try:
            HtmlNode(children=[], props={})
        except Exception as e:
            self.assertRaises(Exception)
            self.assertEqual(str(e), "No tag requires a value property")
        try:
            HtmlNode("div", None, None, {})
        except Exception as e:
            self.assertRaises(Exception)
            self.assertEqual(str(e), "Must have at least either chidren or a value")
        try:
            HtmlNode(None, "something", [], {"key": "value"})
        except Exception as e:
            self.assertRaises(Exception)
            self.assertEqual(str(e), "Cannot have attributes without a tag")




if __name__ == "__main__":
    unittest.main()