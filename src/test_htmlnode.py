import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode

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

children = [
    LeafNode("foo bar"),
    LeafNode("Link", "a"),
    LeafNode("Foo bar", "div", {"class": "container", "display": "inline-block"}),
]

nested_children = [
    ParentNode("div", children, {"class": "container"}),
    ParentNode("div", [ParentNode("p", children), ParentNode("section", children, {"class": "fancy", "style": "margin: 0 center; font: 2em;"})])
]

test_cases_parent = [
    (ParentNode("div", children), '<div>foo bar<a>Link</a><div class="container" display="inline-block">Foo bar</div></div>'),
    (ParentNode("p", children, {"id": "awesome", "selected": "true"}), '<p id="awesome" selected="true">foo bar<a>Link</a><div class="container" display="inline-block">Foo bar</div></p>'),
    (ParentNode("article", nested_children, {"id": "main", "class": "main-container"}),
                '<article id="main" class="main-container"><div class="container">' +
                'foo bar<a>Link</a><div class="container" display="inline-block">Foo bar</div></div><div>' +
                '<p>foo bar<a>Link</a><div class="container" display="inline-block">Foo bar</div></p>' +
                '<section class="fancy" style="margin: 0 center; font: 2em;">foo bar<a>Link</a>' +
                '<div class="container" display="inline-block">Foo bar</div></section></div></article>')
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

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        for test_case in test_cases_parent:
            expected_output = test_case[1]
            actual_output = test_case[0].to_html()
            self.assertEqual(expected_output, actual_output)

    




if __name__ == "__main__":
    unittest.main()