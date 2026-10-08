-- Migration 0002: starting menu. Prices are left NULL until confirmed.

INSERT INTO menu_items (name_en, name_zh, description, category, is_spicy, sort_order) VALUES
    ('Egg Waffles',        '雞蛋仔',   'Crispy outside, soft and fluffy inside. The classic Hong Kong street snack.', 'snack',   0, 10),
    ('Curry Fish Balls',   '咖喱魚蛋', 'Bouncy fish balls simmered in a rich, mildly spicy curry sauce.',             'snack',   1, 20),
    ('Siu Mai',            '燒賣',     'Street-style siu mai on a skewer with soy sauce and chili oil.',              'snack',   0, 30),
    ('Hong Kong Milk Tea', '港式奶茶', 'Strong black tea, pulled smooth with evaporated milk. Hot or iced.',           'drink',   0, 40);
