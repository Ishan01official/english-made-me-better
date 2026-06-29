import unittest

from scripts.check_paragraph import check_paragraph, split_sentences


class CheckParagraphTests(unittest.TestCase):
    def test_split_sentences(self):
        self.assertEqual(split_sentences("One. Two? Three!"), ["One.", "Two?", "Three!"])

    def test_paragraph_correction(self):
        result = check_paragraph("Today morning I completed it. Please revert back.")
        self.assertEqual(result["sentence_count"], 2)
        self.assertIn("This morning I completed it.", result["clearer_version"])
        self.assertIn("Please reply.", result["clearer_version"])

    def test_long_sentence_detection(self):
        paragraph = (
            "This paragraph contains many different words because the checker should "
            "detect sentences that become difficult for beginners to read clearly "
            "without a pause or a shorter structure."
        )
        result = check_paragraph(paragraph)
        self.assertEqual(len(result["long_sentences"]), 1)


if __name__ == "__main__":
    unittest.main()
