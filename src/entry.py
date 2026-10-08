"""Shankala API — a Cloudflare Python Worker.

Static files in /public are served by Cloudflare directly; only /api/* reaches
this code (see `run_worker_first` in wrangler.jsonc).
"""

import json
from datetime import date
from urllib.parse import urlparse

from workers import Response, WorkerEntrypoint

from content import EVENTS, MENU_ITEMS
from validation import is_spam, validate_contact

JSON_HEADERS = {"content-type": "application/json; charset=utf-8"}


def json_response(payload, status=200, cache_seconds=0):
    headers = dict(JSON_HEADERS)
    headers["cache-control"] = f"public, max-age={cache_seconds}" if cache_seconds else "no-store"
    return Response(json.dumps(payload, ensure_ascii=False), status=status, headers=headers)


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        path = urlparse(request.url).path.rstrip("/")
        method = request.method

        routes = {
            ("GET", "/api/health"): self.health,
            ("GET", "/api/menu"): self.get_menu,
            ("GET", "/api/events"): self.get_events,
            ("POST", "/api/contact"): self.post_contact,
        }

        handler = routes.get((method, path))
        if handler is None:
            known_path = any(p == path for _, p in routes)
            if known_path:
                return json_response({"error": "Method not allowed"}, status=405)
            return json_response({"error": "Not found"}, status=404)

        try:
            return await handler(request)
        except Exception as exc:  # noqa: BLE001 - last-resort guard for the API
            print(f"Unhandled error on {method} {path}: {exc!r}")
            return json_response({"error": "Something went wrong"}, status=500)

    async def health(self, request):
        return json_response({"status": "ok"})

    async def get_menu(self, request):
        return json_response({"items": MENU_ITEMS}, cache_seconds=300)

    async def get_events(self, request):
        today = date.today().isoformat()
        upcoming = sorted((e for e in EVENTS if e["ends_on"] >= today), key=lambda e: e["starts_on"])
        return json_response({"events": upcoming[:10]}, cache_seconds=300)

    async def post_contact(self, request):
        try:
            data = json.loads(await request.text())
        except ValueError:
            return json_response({"error": "Invalid JSON"}, status=400)

        # Pretend success to bots so they don't retry.
        if is_spam(data):
            return json_response({"ok": True}, status=201)

        clean, errors = validate_contact(data)
        if errors:
            return json_response({"error": "Validation failed", "fields": errors}, status=422)

        # No database yet: write the message to Workers Logs
        # (Cloudflare dashboard → Workers → shankala → Logs).
        print(json.dumps({"type": "contact_message", **clean}, ensure_ascii=False))

        return json_response({"ok": True}, status=201)
