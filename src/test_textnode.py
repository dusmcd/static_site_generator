import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_images

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

old_nodes = {
    "test1": [TextNode("foo bar", TextType.TEXT)],
    "test2": [TextNode("That is a **awesome** jacket!", TextType.TEXT)],
    "test3": [TextNode("**That** is a **awesome** jacket!", TextType.TEXT)],
    "test4": [TextNode("That is a *awesome* jacket!", TextType.TEXT)],
    "test5": [TextNode("Here is some great code: `const foo = 'bar'`", TextType.TEXT)],
    "test6": [TextNode("`amazing code` Wasn't that some great code? Here is some more: `functionCall()`", TextType.TEXT)],
    "test7": [TextNode("*That* is a *awesome* jacket!", TextType.TEXT)],
    "test8": [
        TextNode("Here is some great code: `const foo = 'bar'`", TextType.TEXT), 
        TextNode("Doesn't matter", TextType.IMAGE), 
        TextNode("Linke", TextType.LINK), 
        TextNode("I am a man.", TextType.TEXT)
        ],
    "test9": [TextNode("`function getName(name) {console.log('My name is ' + name)}` Wow! That was a lot of code!", TextType.TEXT)]
}

test_cases_split = [
    (split_nodes_delimiter(old_nodes["test1"], "*", None), [TextNode("foo bar", TextType.TEXT)]),
    (split_nodes_delimiter(old_nodes["test2"], "**", TextType.BOLD), 
        [TextNode("That is a ", TextType.TEXT), TextNode("awesome", TextType.BOLD), 
         TextNode(" jacket!", TextType.TEXT)]),
    (split_nodes_delimiter(old_nodes["test3"], "**", TextType.BOLD), 
        [TextNode("That", TextType.BOLD), TextNode(" is a ", TextType.TEXT), 
         TextNode("awesome", TextType.BOLD), TextNode(" jacket!", TextType.TEXT)]),
    (split_nodes_delimiter(old_nodes["test4"], "*", TextType.ITALIC), 
        [TextNode("That is a ", TextType.TEXT), TextNode("awesome", TextType.ITALIC), 
         TextNode(" jacket!", TextType.TEXT)]),
    (split_nodes_delimiter(old_nodes["test5"], "`", TextType.CODE), 
        [TextNode("Here is some great code: ", TextType.TEXT), 
         TextNode("const foo = 'bar'", TextType.CODE)]),
    (split_nodes_delimiter(old_nodes["test6"], "`", TextType.CODE), 
        [TextNode("amazing code", TextType.CODE), 
         TextNode(" Wasn't that some great code? Here is some more: ", TextType.TEXT), 
         TextNode("functionCall()", TextType.CODE)]),
    (split_nodes_delimiter(old_nodes["test7"], "*", TextType.ITALIC), 
        [TextNode("That", TextType.ITALIC), 
         TextNode(" is a ", TextType.TEXT), 
         TextNode("awesome", TextType.ITALIC), 
         TextNode(" jacket!", TextType.TEXT)]),
    (split_nodes_delimiter(old_nodes["test8"], "`", TextType.CODE), 
        [TextNode("Here is some great code: ", TextType.TEXT),
         TextNode("const foo = 'bar'", TextType.CODE),
         TextNode("Doesn't matter", TextType.IMAGE),
         TextNode("Linke", TextType.LINK),
         TextNode("I am a man.", TextType.TEXT)]),
    (split_nodes_delimiter(old_nodes["test9"], "`", TextType.CODE),
     [TextNode("function getName(name) {console.log('My name is ' + name)}", TextType.CODE),
      TextNode(" Wow! That was a lot of code!", TextType.TEXT)
      ]) 

]

old_nodes_imgs = {
    "test1": [TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", TextType.TEXT)],
    "test2": [TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" This is text with an and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", TextType.TEXT)],
    "test3": [TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) and here is some more text", TextType.TEXT)],
    "test4": [
        TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", TextType.TEXT),
        TextNode("This is some **bold** text", TextType.TEXT),
        TextNode("Regular text", TextType.TEXT)
            ],

}
test_cases_images = [
    (split_nodes_images(old_nodes_imgs["test1"]),
      [TextNode("This is text with an ", TextType.TEXT),
       TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
       TextNode(" and ", TextType.TEXT),
       TextNode("another", TextType.IMAGE,"https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]),
    (split_nodes_images(old_nodes_imgs["test2"]), 
     [
         TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
         TextNode(" This is text with an and ", TextType.TEXT),
         TextNode("another", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
     ]
     ),
     (split_nodes_images(old_nodes_imgs["test3"]),
      [
          TextNode("This is text with an ", TextType.TEXT),
          TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
          TextNode(" and ", TextType.TEXT),
          TextNode("another", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
          TextNode(" and here is some more text", TextType.TEXT)
      ]
      ),
      (split_nodes_images(old_nodes_imgs["test4"]),
      [
       TextNode("This is text with an ", TextType.TEXT),
       TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
       TextNode(" and ", TextType.TEXT),
       TextNode("another", TextType.IMAGE,"https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
       TextNode("This is some **bold** text", TextType.TEXT),
       TextNode("Regular text", TextType.TEXT) 
      ] 
       )

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

    def test_split_node_delimiter(self):
        for test_case in test_cases_split:
            for i in range(0, len(test_case[1])):
                actual_result = str(test_case[0][i])
                expected_result = str(test_case[1][i])
                self.assertEqual(expected_result, actual_result)
        
        try:
            split_nodes_delimiter([TextNode("I am a **bold man", TextType.TEXT)], "**", TextType.BOLD)
        except Exception as e:
            self.assertRaises(Exception)
            self.assertEqual(str(e), "Need a closing and an opening delimiter")

        try:
            split_nodes_delimiter([TextNode("here is some code: `const name = 'Bob'", TextType.TEXT)], "`", TextType.CODE)
        except Exception as e:
            self.assertRaises(Exception)
            self.assertEqual(str(e), "Need a closing and an opening delimiter")

    def test_split_node_images(self):
        for test_case in test_cases_images:
            for i in range(0, len(test_case[1])):
                actual_result = str(test_case[0][i])
                expected_result = str(test_case[1][i])
                self.assertEqual(expected_result, actual_result)

if __name__ == "main":
    unittest.main()