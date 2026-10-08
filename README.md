# Shankala 山卡拉

Website for **Shankala**, a Hong Kong street food business in Edmonton (YEG) that started at AsiaFest.

It runs entirely on Cloudflare's edge:

| Layer     | Tech                                   | Where                     |
|-----------|----------------------------------------|---------------------------|
| Front end | HTML, CSS, vanilla JavaScript           | `public/`                 |
| API       | **Python** (Cloudflare Python Worker)   | `src/`                    |
| Content   | Python data, in `src/content.py`        | `src/content.py`          |
| Database  | **SQL** schema, ready for Cloudflare D1 (not connected yet) | `migrations/` |
| Tests/CI  | Python `unittest` and GitHub Actions    | `tests/`, `.github/`      |

```
Browser ──► Cloudflare edge ──┬─► public/*  (static files, served directly)
                              └─► /api/*    (src/entry.py, Python)
```

## API

| Method | Path           | What it does                                                    |
|--------|----------------|-----------------------------------------------------------------|
| GET    | `/api/health`  | Health check                                                    |
| GET    | `/api/menu`    | Menu items (cached 5 min)                                       |
| GET    | `/api/events`  | Upcoming events, soonest first; past events are filtered out    |
| POST   | `/api/contact` | Validates a contact message (`201`, or `422` + field errors)    |

Design notes:
- **Validation lives in `src/validation.py`**, separate from Cloudflare code, so it can be unit tested with plain Python.
- **Spam:** a hidden "honeypot" field; bots that fill it get a fake success response.
- **Error handling:** unknown routes return `404`, wrong methods `405`, bad JSON `400`, and unexpected errors are logged and returned as `500`.
- **Contact messages** are written to **Workers Logs** for now (Cloudflare dashboard → Workers & Pages → shankala → Logs). They aren't stored anywhere else until the database is connected.

## Run it locally

You need Node.js and [uv](https://docs.astral.sh/uv/). On a Mac: `brew install node uv`.

```bash
npm install     # installs wrangler
uv sync         # installs the Python Workers SDK
npm run dev     # http://localhost:8787
npm test        # Python unit tests
```

## Deploy to Cloudflare

1. Push to GitHub.
2. In the Cloudflare dashboard, go to **Workers & Pages → Create → Import a repository** and pick this repo. Then set:
   - **Build command:** *(leave empty)*
   - **Deploy command:** `npx wrangler deploy` (the default)
3. Every push to `main` redeploys. The site goes live at `https://shankala.<your-subdomain>.workers.dev`.

**Custom domain:** in the Worker, open **Settings → Domains & Routes → Add → Custom domain**. Then update the domain in `public/index.html`, `public/robots.txt` and `public/sitemap.xml`.

> Note: This project uses a **Cloudflare Worker with static assets**, not Cloudflare *Pages*, because Pages can't run Python.

## Updating content

Edit `src/content.py` (menu items and events), then commit and push.

## Next step: connect the SQL database (Cloudflare D1)

`migrations/` already has the schema: `menu_items`, `events` and `contact_messages` tables, with `CHECK` constraints and indexes. CI checks that these files run cleanly on SQLite. To switch it on:

1. `npx wrangler login`, then `npx wrangler d1 create shankala-db`
2. Add the binding it prints to `wrangler.jsonc`, with `"migrations_dir": "migrations"`
3. `npx wrangler d1 migrations apply shankala-db --remote`
4. In `src/entry.py`, replace the `content.py` lookups with queries such as
   `await self.env.DB.prepare("SELECT ... FROM menu_items WHERE is_available = 1").all()`,
   and save contact messages with a parameterized `INSERT ... VALUES (?, ?, ?, ?)` and `.bind(...)`
5. Add `npx wrangler d1 migrations apply shankala-db --remote &&` to the start of the deploy command

## Before launch

- [ ] Confirm the menu items and add prices in `src/content.py`
- [ ] Add real events in `src/content.py`
- [ ] Add a team or stall photo (`public/images/`) and swap it into the "Our story" section
- [ ] Add `public/images/og-image.png` (1200×630) for social link previews
- [ ] Check the Instagram handle and domain
