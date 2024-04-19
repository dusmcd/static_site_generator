from textnode import TextNode, TextType
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_links,
    split_nodes_images,
    text_to_text_nodes)
import unittest

test_cases_extract_images = [
    ("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", [
        ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
    ]),
    ("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
      "and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", [
        ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ("another","https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png" )
      ])
]
test_cases_extract_links = [
    ("Here is some text with a [link](https://www.google.com)", [("link", "https://www.google.com")]),
    ("Here is some text with a [link](https://www.google.com) and here is another [thing to click on](http://scarysite.com)",
        [("link", "https://www.google.com"), ("thing to click on", "http://scarysite.com")])
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
    "test9": [TextNode("`function getName(name) {console.log('My name is ' + name)}` Wow! That was a lot of code!", TextType.TEXT)],
    "test10": [TextNode("**The Lord of the Rings** is a great film.", TextType.TEXT)]
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
      ]),
    (split_nodes_delimiter(old_nodes["test10"], "**", TextType.BOLD),
     [
         TextNode("The Lord of the Rings", TextType.BOLD),
         TextNode(" is a great film.", TextType.TEXT)
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
old_nodes_links = {
    "test1": [TextNode("This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", TextType.TEXT)],
    "test2": [TextNode("[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" This is text with an and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", TextType.TEXT)],
    "test3": [TextNode("This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) and here is some more text", TextType.TEXT)],
    "test4": [
        TextNode("This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
" and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)", TextType.TEXT),
        TextNode("This is some **bold** text", TextType.TEXT),
        TextNode("Regular text", TextType.TEXT)
            ],

}
test_cases_links = [
    (split_nodes_links(old_nodes_links["test1"]),
      [TextNode("This is text with an ", TextType.TEXT),
       TextNode("image", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
       TextNode(" and ", TextType.TEXT),
       TextNode("another", TextType.LINK,"https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]),
    (split_nodes_links(old_nodes_links["test2"]), 
     [
         TextNode("image", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
         TextNode(" This is text with an and ", TextType.TEXT),
         TextNode("another", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
     ]
     ),
     (split_nodes_links(old_nodes_links["test3"]),
      [
          TextNode("This is text with an ", TextType.TEXT),
          TextNode("image", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
          TextNode(" and ", TextType.TEXT),
          TextNode("another", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
          TextNode(" and here is some more text", TextType.TEXT)
      ]
      ),
      (split_nodes_links(old_nodes_links["test4"]),
      [
       TextNode("This is text with an ", TextType.TEXT),
       TextNode("image", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
       TextNode(" and ", TextType.TEXT),
       TextNode("another", TextType.LINK,"https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
       TextNode("This is some **bold** text", TextType.TEXT),
       TextNode("Regular text", TextType.TEXT) 
      ] 
       )

]

test_cases_text_node = [
    (text_to_text_nodes("This is **text** with an *italic* word and a `code block`" + 
    " and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"),
    [

    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),


    ]),
    (text_to_text_nodes("![amazing](https://www.google.com/amazing_image.jpeg) That was an **amazing** image! *What* did you think of this code: `console.log('Here it is')`" +
                        " Here is a link: [Home](https://www.homepage.com) and here is another link [Contact](https://www.homepage.com/contact) and here is **one** more image:" +
                         " ![image](https://www.something.com/amazing.jpeg)"),
   [
       TextNode("amazing", TextType.IMAGE,"https://www.google.com/amazing_image.jpeg"),
       TextNode(" That was an ", TextType.TEXT),
       TextNode("amazing", TextType.BOLD),
       TextNode(" image! ", TextType.TEXT),
       TextNode("What", TextType.ITALIC),
       TextNode(" did you think of this code: ", TextType.TEXT),
       TextNode("console.log('Here it is')", TextType.CODE),
       TextNode(" Here is a link: ", TextType.TEXT),
       TextNode("Home", TextType.LINK,"https://www.homepage.com"),
       TextNode(" and here is another link ", TextType.TEXT),
       TextNode("Contact", TextType.LINK,"https://www.homepage.com/contact"),
       TextNode(" and here is ", TextType.TEXT),
       TextNode("one", TextType.BOLD),
       TextNode(" more image: ", TextType.TEXT),
       TextNode("image", TextType.IMAGE,"https://www.something.com/amazing.jpeg" )
   ] 
    
    )
]
class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        for test_case in test_cases_extract_images:
            actual_value = extract_markdown_images(test_case[0])
            expected_value = test_case[1]
            self.assertEqual(actual_value, expected_value)

    def test_extract_markdown_links(self):
        for test_case in test_cases_extract_links:
            actual_value = extract_markdown_links(test_case[0])
            expected_value = test_case[1]
            self.assertEqual(actual_value, expected_value)
   
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
    def test_split_nodes_links(self):
        for test_case in test_cases_links:
            for i in range(0, len(test_case[1])):
                actual_result = str(test_case[0][i])
                expected_result = str(test_case[1][i])
                self.assertEqual(expected_result, actual_result)
    def test_text_to_text_node(self):
        for test_case in test_cases_text_node:
            for i in range(0, len(test_case[1])):
                actual_result = str(test_case[0][i])
                expected_result = str(test_case[1][i])
                self.assertEqual(expected_result, actual_result)

if __name__ == "__main__":
    unittest.main()