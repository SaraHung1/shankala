# Shankala Website

The website for Shankala, Hong Kong street food in Edmonton. It is a simple static site (plain HTML, CSS and JavaScript). No build step is needed.

## Files

| File / folder   | What it is                                                          |
|-----------------|---------------------------------------------------------------------|
| `index.html`    | The home page. Edit the text in `[brackets]`.                       |
| `css/styles.css`| Styling. Change the brand colors at the top of the file.            |
| `js/main.js`    | Mobile menu and footer year.                                        |
| `images/`       | Put your photos and logo here.                                      |
| `404.html`      | Shown when someone visits a page that doesn't exist.                |
| `favicon.svg`   | The small icon in the browser tab.                                  |
| `_headers`      | Security and caching settings that Cloudflare Pages applies.        |
| `robots.txt`, `sitemap.xml` | Help search engines find the site.                      |

## Preview on your computer

Open `index.html` in your browser, or run a local server from this folder so links like `/css/styles.css` work:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000

## Upload to GitHub

1. Go to https://github.com/new and create a repository named `shankala-website`. Don't add a README, because this folder already has one.
2. In Terminal, from this folder:

```bash
git remote add origin https://github.com/<your-username>/shankala-website.git
git push -u origin main
```

## Connect to Cloudflare Pages

1. Log in to https://dash.cloudflare.com, then go to **Workers & Pages → Create → Pages → Connect to Git**.
2. Pick the `shankala-website` repository.
3. Use these build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
4. Click **Save and Deploy**. Your site will be live at `https://shankala-website.pages.dev`.
5. Each time you push to `main`, Cloudflare redeploys the site automatically.

### Custom domain (optional)

In your Pages project, open **Custom domains → Set up a custom domain** and enter your domain (for example `shankala.com`).
After that, replace `https://shankala.com` in `index.html`, `robots.txt` and `sitemap.xml` if your domain is different.

## Before you launch

- [ ] Replace all `[placeholder]` text in `index.html`
- [ ] Update the email, phone and location in the Contact section
- [ ] Add photos to `images/` and swap out the image placeholder
- [ ] Add `images/og-image.png` (1200×630) for link previews on social media
- [ ] Set your brand colors in `css/styles.css`
- [ ] Update the domain in `index.html`, `robots.txt` and `sitemap.xml`
