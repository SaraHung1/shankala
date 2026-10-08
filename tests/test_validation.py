import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from validation import is_spam, validate_contact  # noqa: E402

VALID = {
    "name": "Ada",
    "email": "Ada@Example.com",
    "topic": "catering",
    "message": "Can you cater a party of 40?",
}


class ValidateContactTests(unittest.TestCase):
    def test_valid_input_is_cleaned(self):
        clean, errors = validate_contact({**VALID, "name": "  Ada  "})
        self.assertEqual(errors, {})
        self.assertEqual(clean["name"], "Ada")
        self.assertEqual(clean["email"], "ada@example.com")

    def test_missing_fields_report_errors(self):
        clean, errors = validate_contact({})
        self.assertIsNone(clean)
        self.assertEqual(set(errors), {"name", "email", "message"})

    def test_bad_email(self):
        _, errors = validate_contact({**VALID, "email": "not-an-email"})
        self.assertIn("email", errors)

    def test_unknown_topic(self):
        _, errors = validate_contact({**VALID, "topic": "refund"})
        self.assertIn("topic", errors)

    def test_message_too_long(self):
        _, errors = validate_contact({**VALID, "message": "x" * 2001})
        self.assertIn("message", errors)

    def test_non_object_body(self):
        _, errors = validate_contact(["not", "a", "dict"])
        self.assertIn("_form", errors)

    def test_sql_like_input_is_just_text(self):
        clean, errors = validate_contact({**VALID, "name": "Robert'); DROP TABLE events;--"})
        self.assertEqual(errors, {})
        self.assertIn("DROP TABLE", clean["name"])  # stored safely via bound parameters


class SpamTests(unittest.TestCase):
    def test_honeypot_filled_is_spam(self):
        self.assertTrue(is_spam({**VALID, "website": "http://spam.example"}))

    def test_honeypot_empty_is_not_spam(self):
        self.assertFalse(is_spam(VALID))


if __name__ == "__main__":
    unittest.main()
