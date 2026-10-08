"""Input validation for the contact form.

Kept free of Cloudflare imports so it can be unit-tested with plain Python.
"""

import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TOPICS = ("general", "catering", "event")

MAX_NAME = 100
MAX_EMAIL = 254
MAX_MESSAGE = 2000


def validate_contact(data):
    """Return (clean_data, errors). `errors` maps field name -> message."""
    if not isinstance(data, dict):
        return None, {"_form": "Expected a JSON object."}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    topic = str(data.get("topic", "general")).strip().lower()
    message = str(data.get("message", "")).strip()

    errors = {}
    if not name:
        errors["name"] = "Please enter your name."
    elif len(name) > MAX_NAME:
        errors["name"] = f"Name must be {MAX_NAME} characters or fewer."

    if not EMAIL_RE.match(email) or len(email) > MAX_EMAIL:
        errors["email"] = "Please enter a valid email address."

    if topic not in TOPICS:
        errors["topic"] = "Please choose a topic."

    if len(message) < 10:
        errors["message"] = "Message should be at least 10 characters."
    elif len(message) > MAX_MESSAGE:
        errors["message"] = f"Message must be {MAX_MESSAGE} characters or fewer."

    if errors:
        return None, errors
    return {"name": name, "email": email, "topic": topic, "message": message}, {}


def is_spam(data):
    """Bots tend to fill every field, including the hidden 'website' honeypot."""
    return isinstance(data, dict) and bool(str(data.get("website", "")).strip())
