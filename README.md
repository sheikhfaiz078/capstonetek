# capstonetek

One-page website for **Capstone Tek**: NFC product authentication and consumer engagement.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The complete website: all styles, scripts, icons and the animated explainer are inside this one file. |
| `capstone-tek-explainer.mp4` | A 25-second 1080p MP4 of the explainer animation, for social media, YouTube or presentations (optional for the website). |

## Upload to Hostinger

1. Open **hPanel → Websites → File Manager** and go to `public_html`.
2. If `public_html` has an old `index.html` (for example the maintenance page), rename it to something like `maintenance.html` or delete it.
3. Upload `index.html` into `public_html`.
4. Visit https://capstonetek.com. Hard-refresh with Ctrl + F5 if you still see the old page.

The logo is loaded from `https://capstonetek.com/images/logo.jpeg`, so keep that file in `public_html/images/`. If it can't be loaded, the page shows a text logo instead.

## Contact form email

The form opens the visitor's email app with the message already filled in. To choose which inbox receives it, open `index.html`, search for `CONTACT_EMAIL` and replace `info@capstonetek.com` with the address you want.
