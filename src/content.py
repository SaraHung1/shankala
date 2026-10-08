"""Site content served by the API.

Kept in code for now. The SQL schema in migrations/ describes the same shape,
for when this moves into a Cloudflare D1 database.
"""

# price_cents = None means the price isn't shown on the site.
MENU_ITEMS = [
    {
        "id": 1,
        "name_en": "Egg Waffles",
        "name_zh": "雞蛋仔",
        "description": "Crispy outside, soft and fluffy inside. The classic Hong Kong street snack.",
        "category": "snack",
        "price_cents": None,
        "is_spicy": False,
    },
    {
        "id": 2,
        "name_en": "Curry Fish Balls",
        "name_zh": "咖喱魚蛋",
        "description": "Bouncy fish balls simmered in a rich, mildly spicy curry sauce.",
        "category": "snack",
        "price_cents": None,
        "is_spicy": True,
    },
    {
        "id": 3,
        "name_en": "Siu Mai",
        "name_zh": "燒賣",
        "description": "Street-style siu mai on a skewer with soy sauce and chili oil.",
        "category": "snack",
        "price_cents": None,
        "is_spicy": False,
    },
    {
        "id": 4,
        "name_en": "Hong Kong Milk Tea",
        "name_zh": "港式奶茶",
        "description": "Strong black tea, pulled smooth with evaporated milk. Hot or iced.",
        "category": "drink",
        "price_cents": None,
        "is_spicy": False,
    },
]

# Dates are ISO strings: "YYYY-MM-DD". Past events are filtered out automatically.
EVENTS = [
    # {
    #     "id": 1,
    #     "name": "AsiaFest Edmonton",
    #     "location": "Edmonton, AB",
    #     "starts_on": "2027-08-14",
    #     "ends_on": "2027-08-15",
    #     "url": None,
    # },
]
