// ---------- Navigation ----------
const header = document.querySelector(".site-header");
const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");

function setMenu(open) {
  links.classList.toggle("open", open);
  toggle.setAttribute("aria-expanded", String(open));
}

toggle.addEventListener("click", () => setMenu(!links.classList.contains("open")));
links.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
window.addEventListener("scroll", () => header.classList.toggle("scrolled", window.scrollY > 40), { passive: true });

// ---------- Marquee: repeat items so the strip always fills wide screens ----------
const track = document.querySelector(".marquee-track");
if (track) track.innerHTML = track.innerHTML.repeat(3);

// ---------- Scroll reveal ----------
const observer = new IntersectionObserver(
  (entries) => entries.forEach((e) => {
    if (e.isIntersecting) {
      e.target.classList.add("visible");
      observer.unobserve(e.target);
    }
  }),
  { threshold: 0.15 }
);
document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));

// ---------- Helpers ----------
const escapeHtml = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const money = (cents) => `$${(cents / 100).toFixed(2)}`;

async function getJson(url) {
  const res = await fetch(url, { headers: { accept: "application/json" } });
  if (!res.ok) throw new Error(`${url} → ${res.status}`);
  return res.json();
}

// ---------- Menu (GET /api/menu) ----------
async function loadMenu() {
  const grid = document.getElementById("menu-grid");
  try {
    const { items } = await getJson("/api/menu");
    if (!items.length) {
      grid.innerHTML = `<p class="muted">Menu coming soon.</p>`;
      return;
    }
    grid.innerHTML = items
      .map(
        (item) => `
        <article class="menu-card">
          <p class="menu-zh" lang="zh-Hant-HK">${escapeHtml(item.name_zh)}</p>
          <h3>${escapeHtml(item.name_en)}</h3>
          <p>${escapeHtml(item.description)}</p>
          <div class="menu-meta">
            <span>
              <span class="tag">${escapeHtml(item.category)}</span>
              ${item.is_spicy ? `<span class="tag tag-spicy">Spicy</span>` : ""}
            </span>
            ${item.price_cents != null ? `<span class="price">${money(item.price_cents)}</span>` : ""}
          </div>
        </article>`
      )
      .join("");
  } catch (err) {
    console.error(err);
    grid.innerHTML = `<p class="muted">Sorry, the menu couldn't load right now. Please try again later.</p>`;
  }
}

// ---------- Events (GET /api/events) ----------
async function loadEvents() {
  const list = document.getElementById("events-list");
  const instagram = `<a href="https://instagram.com/shankala" target="_blank" rel="noopener">@shankala</a>`;
  try {
    const { events } = await getJson("/api/events");
    if (!events.length) {
      list.innerHTML = `<div class="empty-state">No dates announced yet. Follow ${instagram} on Instagram to hear first.</div>`;
      return;
    }
    list.innerHTML = events
      .map((ev) => {
        // Dates are plain YYYY-MM-DD; parse as local dates to avoid timezone shifts.
        const [y, m, d] = ev.starts_on.split("-").map(Number);
        const start = new Date(y, m - 1, d);
        const month = start.toLocaleString("en-CA", { month: "short" });
        const range = ev.starts_on === ev.ends_on ? "" : ` – ${ev.ends_on}`;
        return `
        <article class="event">
          <div class="event-date"><div><div class="m">${month}</div><div class="d">${d}</div></div></div>
          <div>
            <h3>${escapeHtml(ev.name)}</h3>
            <p>${escapeHtml(ev.location)} · ${escapeHtml(ev.starts_on + range)}</p>
          </div>
          ${/^https?:\/\//.test(ev.url || "") ? `<a href="${escapeHtml(ev.url)}" target="_blank" rel="noopener">Details →</a>` : ""}
        </article>`;
      })
      .join("");
  } catch (err) {
    console.error(err);
    list.innerHTML = `<div class="empty-state">Couldn't load events. Check ${instagram} for the latest dates.</div>`;
  }
}

// ---------- Contact form (POST /api/contact) ----------
const form = document.getElementById("contact-form");
const statusEl = document.getElementById("form-status");

function showFieldErrors(fields = {}) {
  form.querySelectorAll(".field-error").forEach((el) => {
    const msg = fields[el.dataset.for] || "";
    el.textContent = msg;
    el.closest(".field").classList.toggle("has-error", Boolean(msg));
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const button = form.querySelector("button[type=submit]");
  const data = Object.fromEntries(new FormData(form));

  showFieldErrors();
  statusEl.className = "form-status";
  statusEl.textContent = "Sending…";
  button.disabled = true;

  try {
    const res = await fetch("/api/contact", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(data),
    });
    const body = await res.json().catch(() => ({}));

    if (res.ok) {
      form.reset();
      statusEl.classList.add("ok");
      statusEl.textContent = "Thanks! We'll get back to you soon.";
    } else if (res.status === 422) {
      showFieldErrors(body.fields);
      statusEl.classList.add("err");
      statusEl.textContent = "Please fix the highlighted fields.";
    } else {
      throw new Error(body.error || res.status);
    }
  } catch (err) {
    console.error(err);
    statusEl.classList.add("err");
    statusEl.textContent = "Something went wrong. Please try again, or message us on Instagram.";
  } finally {
    button.disabled = false;
  }
});

// ---------- Init ----------
document.getElementById("year").textContent = new Date().getFullYear();
loadMenu();
loadEvents();
