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

    




if __name__ == "__main__":
    unittest.main()