import unittest

from scripts.check_sentence import check_sentence


class CheckSentenceTests(unittest.TestCase):
    def test_subject_verb_and_base_verb_are_fixed(self):
        result = check_sentence("He do not knows about this issue")
        self.assertEqual(result["corrected"], "He does not know about this issue.")
        self.assertIn("subject-verb agreement", result["mistakes_found"])

    def test_common_indian_english_phrase_is_fixed(self):
        result = check_sentence("Today morning I completed it")
        self.assertEqual(result["corrected"], "This morning I completed it.")

    def test_professional_phrase_is_fixed(self):
        result = check_sentence("Kindly do the needful")
        self.assertEqual(result["corrected"], "Please take the required action.")


if __name__ == "__main__":
    unittest.main()
