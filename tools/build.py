"""Assemble index.html: splices the explainer stage into the page template and
generates the FAQ markup + schema.org JSON-LD from one list so they always match."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
tpl = (SRC / "index.template.html").read_text()
stage_css = (SRC / "stage.css").read_text()          # the 25-second explainer animation
stage_kf = (SRC / "stage-keyframes.css").read_text()
stage_html = (SRC / "stage.html").read_text().rstrip("\n")

SITE = "https://capstonetek.com/"
TITLE = "Capstone Tek | NFC Product Authentication & Anti-Counterfeit Stickers"
DESC = ("Capstone Tek combines branded NFC stickers with a secure verification page. Customers tap with their phone, "
        "see the product is genuine and land on your product page. No app needed.")
FAQ = [
    ("Do customers need to download an app?",
     "No. Customers tap their smartphone on the branded sticker and a secure notification appears straight away. There is nothing to install."),
    ("Which phones can read the stickers?",
     "Modern smartphones read them natively, including iPhone XS and newer and most Android phones with NFC turned on."),
    ("Can the stickers carry our brand logo?",
     "Yes. The NFC stickers are printed with your logo and are made to go directly on bottles or product packaging."),
    ("What does the customer see after tapping?",
     "A verification message confirms the product is genuine. They then land on your product page, where you can share usage instructions, ingredients, complementary products or promotions."),
    ("What customer information can we collect?",
     "The verification page can ask for contact or purchase details, so you can stay in touch, run promotions and build loyalty with the people who actually buy your products."),
    ("How do we get started?",
     "We design your stickers and set up your verification page, run a pilot on one flagship product line to measure engagement, then scale across your portfolio. Call +1 (984) 355-9541 or email support@capstonetek.com to book a demo."),
]

faq_html = []
for i, (q, a) in enumerate(FAQ, 1):
    op = i == 1
    faq_html.append(f'''<div class="acc-item{' open' if op else ''}">
            <h3><button class="acc-q" type="button" id="faq{i}q" aria-expanded="{'true' if op else 'false'}" aria-controls="faq{i}">{html.escape(q)}<span class="pm" aria-hidden="true"></span></button></h3>
            <div class="acc-a" id="faq{i}" role="region" aria-labelledby="faq{i}q"><div><p>{html.escape(a)}</p></div></div>
          </div>''')

org_id, web_id, page_id = SITE + "#organization", SITE + "#website", SITE + "#webpage"
address = {"@type": "PostalAddress", "streetAddress": "3510 Hobson Road, Suite #204", "addressLocality": "Woodridge",
           "addressRegion": "IL", "postalCode": "60517", "addressCountry": "US"}
og = SITE + "images/og-image.jpg"
schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": org_id, "name": "Capstone Tek", "url": SITE,
     "logo": {"@type": "ImageObject", "@id": SITE + "#logo", "url": SITE + "images/logo.jpeg", "caption": "Capstone Tek"},
     "image": og,
     "description": "Integrated NFC hardware and web interface solutions for product verification and consumer engagement.",
     "slogan": "Make every product prove it's real.",
     "email": "support@capstonetek.com", "telephone": "+1-984-355-9541", "address": address,
     "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support", "telephone": "+1-984-355-9541",
                       "email": "support@capstonetek.com", "areaServed": "US", "availableLanguage": ["English"]},
                      {"@type": "ContactPoint", "contactType": "sales", "telephone": "+1-984-355-9541",
                       "email": "support@capstonetek.com", "areaServed": "US", "availableLanguage": ["English"]}],
     "knowsAbout": ["NFC authentication", "Anti-counterfeiting", "Product verification", "Brand protection", "Consumer engagement"]},
    {"@type": "ProfessionalService", "@id": SITE + "#localbusiness", "name": "Capstone Tek", "url": SITE, "image": og,
     "logo": SITE + "images/logo.jpeg", "telephone": "+1-984-355-9541", "email": "support@capstonetek.com",
     "address": address, "areaServed": {"@type": "Country", "name": "United States"}, "parentOrganization": {"@id": org_id}},
    {"@type": "WebSite", "@id": web_id, "url": SITE, "name": "Capstone Tek", "description": DESC,
     "publisher": {"@id": org_id}, "inLanguage": "en-US"},
    {"@type": "WebPage", "@id": page_id, "url": SITE, "name": TITLE, "description": DESC, "isPartOf": {"@id": web_id},
     "about": {"@id": org_id}, "inLanguage": "en-US", "dateModified": "2026-10-02",
     "primaryImageOfPage": {"@type": "ImageObject", "url": og, "width": 1200, "height": 630}},
    {"@type": "Service", "@id": SITE + "#service", "name": "NFC product authentication and consumer engagement",
     "serviceType": "Product authentication", "provider": {"@id": org_id},
     "areaServed": {"@type": "Country", "name": "United States"},
     "description": "Branded NFC stickers and a custom web interface that verifies products are genuine, captures customer details and routes buyers to the brand's product pages.",
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Capstone Tek solutions", "itemListElement": [
         {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Branded NFC stickers",
          "description": "High-quality NFC stickers featuring your brand logo, adhered directly to bottles or product packaging."}},
         {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Custom verification web interface",
          "description": "A custom web interface that authenticates products and securely routes customer traffic to your digital properties."}}]}},
    {"@type": "FAQPage", "@id": SITE + "#faq", "isPartOf": {"@id": page_id},
     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}

out = (tpl.replace("/*__STAGE_CSS__*/", stage_css.strip())
          .replace("/*__STAGE_KEYFRAMES__*/", stage_kf.strip())
          .replace("<!--__STAGE_HTML__-->", stage_html)
          .replace("<!--__FAQ_HTML__-->", "\n          ".join(faq_html))
          .replace("/*__SCHEMA__*/", json.dumps(schema, indent=2, ensure_ascii=False).replace("\n", "\n  ")))
for marker in ("__STAGE_CSS__", "__STAGE_KEYFRAMES__", "__STAGE_HTML__", "__FAQ_HTML__", "__SCHEMA__"):
    assert marker not in out, marker
(ROOT / "index.html").write_text(out)
print("index.html", len(out), "bytes")
