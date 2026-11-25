# ELVORRA OPERATIONS — Website

Official website for **ELVORRA OPERATIONS**, an international BPO, call centre and managed business operations company based in Abuja, Nigeria.

*Global Reach. Operational Excellence. Human-Centred Service.*

Repository: https://github.com/LaGoodiee/Elvorra

## What's inside

A static site (plain HTML, CSS and JavaScript). No framework and no build step is needed to deploy.

```
docs/                          <- the website (this folder is what gets published)
  index.html                   Home (incl. paid pilot, capacity, industries)
  about.html                   About, trust & operations, onboarding workflow
  call-centre-customer-support.html
  multilingual-24-7-support.html
  back-office-administrative.html
  crm-case-management-qa.html  (incl. sample QA scorecard and KPI report, labelled as examples)
  managed-bpo-teams-partnerships.html  (paid pilot, engagement models, partnership enquiries)
  industries.html              Airlines & travel, fintech, SaaS, e-commerce
  contact.html                 Proposal / consultation / partnership enquiry form
  privacy.html                 Privacy Policy
  404.html, robots.txt, sitemap.xml, netlify.toml
  assets/
    style.css                  all styles (generated from base_from_v3.css + inner.css + site2.css)
    main.js                    menu, theme toggle, animations, globe, enquiry form
    config.js                  EDIT THIS: email, WhatsApp, booking link, form endpoint
    land.js, logo.png, favicon.png, apple-touch-icon.png, og-image.png
apps-script/Code.gs            enquiry form backend (Google Apps Script)
build_site.py                  page generator (see "Editing")
v3.html                        homepage template used by the generator
```

## Settings: `docs/assets/config.js`

```js
window.ELV_CONFIG = {
  email: "elvoraoperation@gmail.com",
  whatsapp: "",   // digits only with country code, e.g. "2348012345678"
  calendly: "",   // booking link; "Book a Consultation" opens it when set
  endpoint: ""    // Google Apps Script /exec URL (see below)
};
```

- **WhatsApp:** until a number is set, every WhatsApp button is hidden, so no visitor lands on a dead link. Set it and the floating button, footer link, contact card and form confirmation appear.
- **Consultation booking:** until a link is set, "Book a Consultation" opens the built-in consultation request form.
- **Email:** shown across the site from this one file (also set in `apps-script/Code.gs` and the JSON-LD in `build_site.py`).

## Enquiry form: direct submission to the business inbox

The form never opens the visitor's email app. It posts securely to a Google Apps Script web app that, for every enquiry:

1. blocks spam (hidden honeypot field, too-fast submissions, per-address rate limit, size limits, duplicate-submission protection)
2. **saves a backup row** in a Google Sheet ("ELVORRA Enquiries", created automatically in the owner's Drive)
3. **emails the complete enquiry** to the business inbox (reply-to is the enquirer)
4. **emails a confirmation** (with a copy of their request) to the prospective client
5. returns a result so the website shows either a confirmation with a reference number, or a clear error

### Setup (about 5 minutes, signed in as the ELVORRA Google account)

1. Go to script.google.com > New project and paste in `apps-script/Code.gs`.
2. Select the function **`setup`** and press Run. Approve the permissions. This creates the spreadsheet and sends a test email.
3. Deploy > New deployment > Web app. Execute as **Me**, access **Anyone**.
4. Copy the `/exec` URL into `endpoint` in `docs/assets/config.js`, commit and redeploy.
5. Open the `/exec` URL in a browser. You should see `{"ok":true,"service":"ELVORRA enquiry endpoint"}`.
6. **Test all three enquiry types** from the live site and confirm: the notification reaches the inbox with every field, the confirmation reaches the sender, and a row appears in the sheet.
7. Optional: add an hourly trigger for `retryUnsent` to re-send any notification that failed while email was temporarily unavailable.

After editing `Code.gs` later, use Deploy > Manage deployments > Edit > **New version**, otherwise the old code keeps running.
Free Gmail accounts can send about 100 emails a day through Apps Script (each enquiry uses 2). For higher volume use a Google Workspace address.

While `endpoint` is empty the form shows a "being connected" message and the email address instead of sending.

## Publishing

The site is published from the `docs/` folder.

**GitHub Pages (preview):** Settings > Pages > Source "Deploy from a branch", branch `main`, folder `/docs`. Live at https://lagoodiee.github.io/Elvorra/.

**Netlify (production):** Add new site > Import from GitHub, set **Publish directory** to `docs`, leave the build command empty. Add the client's .com under Domain settings; HTTPS is automatic.

## SEO and sharing

- Every page has a keyword-targeted title and description, Open Graph and Twitter tags, and `index, follow` (404 is `noindex`). Home also has Organization JSON-LD.
- `sitemap.xml` and `robots.txt` are generated by `build_site.py`.
- **When the domain is known:** set `DOMAIN` near the top of `build_site.py`, run `python3 build_site.py`, commit. That fills in canonical URLs, `og:url`, the social share image and the sitemap. Then submit the sitemap in Google Search Console.
- To keep a staging copy private, add `<meta name="robots" content="noindex, nofollow">` in `head()` in `build_site.py` and set `robots.txt` to `Disallow: /`.

## Editing

- **Content and layout:** edit `build_site.py` (shared header/footer and all page content), then run `python3 build_site.py`. This regenerates every file in `docs/` (and `style.css`).
- **Styles:** `docs/assets/base_from_v3.css`, `inner.css`, `site2.css` (merged into `style.css` by the generator). **Behaviour:** `docs/assets/main.js`.
- **Photos:** hotlinked from Unsplash (IDs in `build_site.py`). Replace with the client's own photos, or host them in `docs/assets/`, before or soon after launch.

## Items the client must confirm before launch

These statements are on the website but have not been verified by the client:

- [ ] Email address spelling `elvoraoperation@gmail.com`
- [ ] WhatsApp Business number and consultation booking link (add to `config.js`)
- [ ] Paid pilot: 20–30 personnel (as instructed) and what each pilot includes
- [ ] Talent pool wording: "100+ screened personnel" across operational roles, mobilised by role mix, language and availability
- [ ] Languages: English, French, German and Spanish, confirmed against assessed personnel
- [ ] The nine service lines and the four industry sections
- [ ] Confidentiality, data protection, business continuity and QA statements (About page "Operational trust" and service pages) match actual practice
- [ ] Management structure on the About page is accurate (no individual names are shown; add leadership profiles if wanted)
- [ ] Privacy Policy text (a general draft; legal review recommended)
- [ ] Sample QA scorecard, KPI report and onboarding workflow are marked as examples and contain no real client data. There are no client logos, testimonials, certifications or partnerships on the site and none should be added unless real.

## Final test checklist (client demonstration)

- [ ] All pages load; every nav, footer and CTA button works
- [ ] Looks correct on mobile and desktop, light and dark
- [ ] Proposal form submits; the full enquiry arrives in the inbox; the sender gets a confirmation; a row appears in the sheet
- [ ] Consultation and partnership enquiries work the same way
- [ ] WhatsApp and consultation links work
- [ ] Privacy Policy opens from the footer and the form
- [ ] Paid pilot shows 20–30 personnel everywhere; counters show 24/7, 4, 9 and 100+ only
- [ ] Company name reads ELVORRA OPERATIONS consistently

## Ownership and handover

The client owns the domain, this GitHub repository, hosting (GitHub Pages / Netlify) and the Google Apps Script project and spreadsheet. Share admin access to each at handover.
