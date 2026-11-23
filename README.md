# ELVORRA OPERATIONS — website

Static 8-page site (plus 404). No build step needed to deploy: upload the `site/` folder.

## Deploy (Netlify)
1. Drag the `site/` folder into app.netlify.com > Add new site > Deploy manually (or connect the GitHub repo, publish dir `site`).
2. Add the client's .com domain under Domain settings. HTTPS is automatic.

## Before going live (client must approve)
- **Remove noindex:** delete the `<meta name="robots" ...>` line from every page (or in `build_site.py`, then rerun it) and replace `site/robots.txt` with `User-agent: *\nAllow: /`.
- **Forms:** see below, then test BOTH "Request a Proposal" and "Book a Consultation" and confirm the email arrives.
- **WhatsApp:** set `whatsapp` in `site/assets/config.js` (digits only, with country code, e.g. `2348012345678`). Until set, WhatsApp buttons link to the contact page.
- **Calendly/booking link:** set `calendly` in `config.js`; "Book a Consultation" buttons then open it.
- **Photos:** images are hotlinked from Unsplash. Replace with the client's own photos (or download and host them) before launch.

## Make the form send email (free)
1. Go to script.google.com > New project, paste `apps-script/Code.gs`.
2. Set `NOTIFY_EMAIL` (and optional `SHEET_ID` to log rows).
3. Deploy > New deployment > Web app > Execute as: Me, Access: Anyone. Authorise when asked.
4. Copy the `/exec` URL into `endpoint` in `site/assets/config.js`.
Without an endpoint the form falls back to opening the visitor's email app addressed to the business email.

## Editing
Edit pages via `build_site.py` then run `python3 build_site.py`, or edit the HTML in `site/` directly (the generator overwrites them).
Styles: `site/assets/style.css`. Behaviour: `site/assets/main.js`. Settings: `site/assets/config.js`.

## Handover checklist
Client owns the domain, GitHub repo, Netlify/hosting and Google Apps Script accounts; share admin access to them.
