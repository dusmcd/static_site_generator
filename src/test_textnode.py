import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("Text Node", "bold")
        node2 = TextNode("Text Node", "bold")
        self.assertEqual(node, node2)
        node3 = TextNode("Some other text", "underline", "http://example.com")
        self.assertNotEqual(node2, node3)

        node4 = TextNode("Text Node", "italics")
        node5 = TextNode("Text Node", "bold", "https://www.google.com")
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)

if __name__ == "main":
    unittest.main()