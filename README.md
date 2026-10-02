# capstonetek

One-page website for **Capstone Tek**: NFC product authentication and consumer engagement.

The repository root is the website. Upload these files to `public_html` on Hostinger:

| File | What it does |
| --- | --- |
| `index.html` | The whole page: styles, scripts, icons and the animated explainer are built in. |
| `contact.php` | Emails contact-form messages to support@capstonetek.com. |
| `images/og-image.jpg` | The 1200×630 picture shown when the link is shared on WhatsApp, Facebook, LinkedIn, X or iMessage. |
| `images/icon-192.png`, `images/icon-512.png` | App icons used by `site.webmanifest`. |
| `favicon.ico`, `favicon.svg`, `apple-touch-icon.png` | Browser-tab and home-screen icons. |
| `site.webmanifest` | Name, colours and icons for phones that save the site to the home screen. |
| `robots.txt`, `sitemap.xml` | Tell search engines what to index. |

Not part of the website:

- `capstone-tek-explainer.mp4`: a 25-second 1080p video of the explainer animation, for social media and presentations.
- `src/` and `tools/`: the sources that build `index.html` (`python3 tools/build.py`). Don't upload them.

## Upload to Hostinger

1. Open **hPanel → Websites → Manage → File Manager** and go to `public_html`.
2. Rename or delete the old `index.html` (the maintenance page).
3. Upload `capstonetek-website.zip`, right-click it, choose **Extract**, and extract into `public_html`. Delete the ZIP afterwards.
4. Keep `public_html/images/logo.jpeg`. The page loads the logo from `https://capstonetek.com/images/logo.jpeg`.
5. Open https://capstonetek.com and press Ctrl + F5.

## After going live

- **Contact form:** send yourself a test message. It is delivered to support@capstonetek.com, so that mailbox has to exist in Hostinger's Email section.
- **Link previews:** paste https://capstonetek.com into the [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) and press **Scrape Again**. WhatsApp and LinkedIn cache previews too. LinkedIn has its own [Post Inspector](https://www.linkedin.com/post-inspector/).
- **Schema check:** run the page through Google's [Rich Results Test](https://search.google.com/test/rich-results) to see the Organization, LocalBusiness and FAQ markup.
- **Google:** add the site in [Search Console](https://search.google.com/search-console) and submit `https://capstonetek.com/sitemap.xml`.

## Editing

Edit `src/index.template.html` (page) and `tools/build.py` (FAQ text and schema.org data, kept in one list so they always match), then run `python3 tools/build.py` to regenerate `index.html`.
