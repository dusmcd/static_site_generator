import unittest
from block_markdown import markdown_to_blocks

test_cases_markdown_blocks = [
    (markdown_to_blocks("This is a paragraph\n\nHere is another paragraph\n\n* List Item 1\n* List Item 2\n\nMore text"),
     ["This is a paragraph", "Here is another paragraph", "* List Item 1* List Item 2", "More text"]
    ),
    (markdown_to_blocks("    # My Blog\n\n## Today's Blog\n\nI am super smart. **You** should listen to what *I* have to say" +
                        "\n\n     ### Reasons Why I am awesome:\n\n- Smart\n- Beautiful\n- I have a dog"),
     ["# My Blog", "## Today's Blog", "I am super smart. **You** should listen to what *I* have to say", "### Reasons Why I am awesome:",
       "- Smart- Beautiful- I have a dog"]
    )
]
class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        for test_case in test_cases_markdown_blocks:
            for i in range(0, len(test_case[1])):
                actual_result = test_case[0][i]
                expected_result = test_case[1][i]
                self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()