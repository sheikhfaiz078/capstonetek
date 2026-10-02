"""Build capstonetek-website.zip: everything that goes into public_html (no logo; it is already on the server)."""
import zipfile, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = ["index.html", "contact.php", "robots.txt", "sitemap.xml", "site.webmanifest", "favicon.ico", "favicon.svg",
         "apple-touch-icon.png", "images/og-image.jpg", "images/icon-192.png", "images/icon-512.png"]
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "capstonetek-website.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in FILES:
        z.write(ROOT / f, f)
print(out, out.stat().st_size, "bytes")
for i in zipfile.ZipFile(out).infolist():
    print(f"  {i.filename:28} {i.file_size:>8}")
