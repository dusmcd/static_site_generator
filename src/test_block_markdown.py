import unittest
from block_markdown import markdown_to_blocks, get_block_type, BlockType

test_cases_markdown_blocks = [
    (markdown_to_blocks("This is a paragraph\n\nHere is another paragraph\n\n* List Item 1\n* List Item 2\n\nMore text"),
     ["This is a paragraph", "Here is another paragraph", "* List Item 1\n* List Item 2", "More text"]
    ),
    (markdown_to_blocks("    # My Blog\n\n## Today's Blog\n\nI am super smart. **You** should listen to what *I* have to say" +
                        "\n\n     ### Reasons Why I am awesome:\n\n- Smart\n- Beautiful\n- I have a dog"),
     ["# My Blog", "## Today's Blog", "I am super smart. **You** should listen to what *I* have to say", "### Reasons Why I am awesome:",
       "- Smart\n- Beautiful\n- I have a dog"]
    )
]
test_cases_block_type = [
    (get_block_type("This is a paragraph"), BlockType.PARAGRAPH),
    (get_block_type("## My Page"), BlockType.HEADING),
    (get_block_type("###### My Page"), BlockType.HEADING),
    (get_block_type("####### My Page"), BlockType.PARAGRAPH),
    (get_block_type("##Not a heading"), BlockType.PARAGRAPH),
    (get_block_type("* Cheese\n* Potatoes\n* Tomatoes"), BlockType.UNORDERED_LIST),
    (get_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST),
    (get_block_type("```function() {\nconsole.log('Get Wrecked');\n}```"), BlockType.CODE_BLOCK),
    (get_block_type("- Cheese\n- Potatoes\n- Tomatoes"), BlockType.UNORDERED_LIST),
    (get_block_type("* Accounting\nMarketing\n* Finance"), BlockType.PARAGRAPH),
    (get_block_type("1.First\n2. Second\n3.Third"), BlockType.PARAGRAPH),
    (get_block_type("```some code"), BlockType.PARAGRAPH),
    (get_block_type(">This is a quote\n>More of the quote"), BlockType.QUOTE_BLOCK),
    (get_block_type("> This is a quote\nThis thinks it's a quote\n> This won't end up being a quote"), BlockType.PARAGRAPH),
    (get_block_type("1. First\n3. Third\n 2. Second"), BlockType.PARAGRAPH)
]
class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        for test_case in test_cases_markdown_blocks:
            for i in range(0, len(test_case[1])):
                actual_result = test_case[0][i]
                expected_result = test_case[1][i]
                self.assertEqual(expected_result, actual_result)
    def test_get_block_type(self):
        for test_case in test_cases_block_type:
            actual_value = test_case[0]
            expected_value = test_case[1]
            self.assertEqual(expected_value,actual_value)

if __name__ == "__main__":
    unittest.main()