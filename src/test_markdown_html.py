import unittest
from markdown_html import markdown_to_html

test_cases_markdown_html = [
    ("This is a paragraph", "<div><p>This is a paragraph</p></div>"),
    ("This is a **bold** paragraph with *emphasis* on style!", "<div><p>This is a <b>bold</b> paragraph with <i>emphasis</i> on style!</p></div>"),
    ("# My Document", "<div><h1>My Document</h1></div>"),
    ("## Sub Heading", "<div><h2>Sub Heading</h2></div>"),
    ("* Item 1\n* Item 2\n* Item 3", "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"),
    ("- Item 1\n- Another *item*", "<div><ul><li>Item 1</li><li>Another <i>item</i></li></ul></div>"),
    ("1. Item 1\n2. Item 2\n3. Item 3", "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"),
    (">Ask not what your country can do for you\n>But what you can do for your country", "<div><blockquote>Ask not what your country can do for you" +
     "<br>But what you can do for your country</blockquote></div>"),
     ("```function printName(name) {\n  console.log('My name is ' + name);\n}```", "<div><pre><code>function printName(name) {<br>  console.log('My name is ' + name);<br>}</code></pre></div>"),
     (">Ask **not** what *your* country can do for you\n>But what **you** can do for *your* country",
       "<div><blockquote>Ask <b>not</b> what <i>your</i> country can do for you<br>But what <b>you</b> can do for <i>your</i> country</blockquote></div>"),
    ("# My Blog\n\nHere are some things that I think about sometimes:\n\n* Work\n* School\n* Family\n\nWhat kind of stuff do *you* think about? Do you like to write `code`?" + 
      "\n\n## My code\n\n```def print_numbers(nums):\n  for number in nums:\n    print(number)```", "<div><h1>My Blog</h1><p>" +
      "Here are some things that I think about sometimes:</p><ul><li>Work</li><li>School</li><li>Family</li></ul>" +
      "<p>What kind of stuff do <i>you</i> think about? Do you like to write <code>code</code>?</p>" + 
      "<h2>My code</h2><pre><code>def print_numbers(nums):<br>  for number in nums:<br>    print(number)</code></pre></div>")
]
class TestMarkdownHtml(unittest.TestCase):
    def test_markdown_to_html(self):
        for test_case in test_cases_markdown_html:
            actual_result = markdown_to_html(test_case[0])
            expected_result = test_case[1]
            self.maxDiff = None
            self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()