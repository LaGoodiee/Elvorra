#!/usr/bin/env python3
# ELVORRA OPERATIONS — static site generator. Run: python3 build_site.py
import re, os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site')
v3 = open(os.path.join(ROOT, 'v3.html'), encoding='utf-8').read()

# ---------------------------------------------------------------- assets
base_css = open(os.path.join(OUT, 'assets', 'base_from_v3.css'), encoding='utf-8').read()
inner_css = open(os.path.join(OUT, 'assets', 'inner.css'), encoding='utf-8').read()
extra_css = """
.tzgrid{grid-template-columns:repeat(6,minmax(0,1fr))}
@media (max-width:1100px){.tzgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:700px){.tzgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:420px){.tzgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.tz{padding:14px}.tz b{font-size:22px}}
.error-page{min-height:70vh;display:grid;place-items:center;text-align:center;padding:160px 0 80px}
.error-page h1{font-size:clamp(80px,18vw,200px);letter-spacing:-.07em;line-height:.9}
"""
open(os.path.join(OUT, 'assets', 'style.css'), 'w', encoding='utf-8').write(base_css + '\n' + inner_css + '\n' + extra_css)

# ---------------------------------------------------------------- helpers
PAGES = {
    'home': 'index.html',
    'about': 'about.html',
    'cc': 'call-centre-customer-support.html',
    'ml': 'multilingual-24-7-support.html',
    'bo': 'back-office-administrative.html',
    'crm': 'crm-case-management-qa.html',
    'mt': 'managed-bpo-teams-partnerships.html',
    'contact': 'contact.html',
}
TITLES = {
    'home': 'ELVORRA OPERATIONS | International BPO, Call Centre & Managed Business Operations',
    'about': 'About ELVORRA OPERATIONS | International BPO & Managed Operations Partner',
    'cc': 'Call Centre & Customer Support Outsourcing | ELVORRA OPERATIONS',
    'ml': 'Multilingual & 24/7 Support Operations | ELVORRA OPERATIONS',
    'bo': 'Back-Office & Administrative Outsourcing | ELVORRA OPERATIONS',
    'crm': 'CRM, Case Management & Quality Assurance | ELVORRA OPERATIONS',
    'mt': 'Managed BPO Teams & Business Partnerships | ELVORRA OPERATIONS',
    'contact': 'Contact Us & Request a Proposal | ELVORRA OPERATIONS',
}
DESCS = {
    'home': 'ELVORRA OPERATIONS is an international BPO and managed business operations partner: call centre, multilingual customer support, 24/7 operations, back-office, CRM and managed teams for businesses worldwide.',
    'about': 'Learn about ELVORRA OPERATIONS, an international BPO, call centre and managed business operations company headquartered in Abuja, Nigeria and serving businesses worldwide.',
    'cc': 'Inbound and outbound call centre services plus email, live chat and multichannel customer support, delivered by dedicated, professionally managed teams.',
    'ml': 'English, French, German and Spanish customer support delivered by shift-based teams with live supervision, workforce scheduling and escalation management.',
    'bo': 'Data entry, document and records management, order processing and virtual assistance delivered by managed teams, so your business can focus on growth.',
    'crm': 'CRM administration, ticket and case management, call monitoring, QA reporting and KPI/SLA monitoring from ELVORRA OPERATIONS.',
    'mt': 'Dedicated customer support agents, team leaders, QA specialists and operational management, plus partnership options for BPO providers, agencies and technology firms.',
    'contact': 'Request a proposal or book a consultation with ELVORRA OPERATIONS. Tell us about your outsourcing needs and our team will respond within one business day.',
}

IMG = {
    'support': 'photo-1626863905121-3b0c0ed7b94c',
    'meeting': 'photo-1758691737543-09a1b2b715fa',
    'desks': 'photo-1560264280-88b68371db39',
    'team': 'photo-1758518731706-be5d5230e5a5',
    'agent': 'photo-1766066014237-00645c74e9c6',
    'phonedesk': 'photo-1758876018602-a22311f70109',
    'laptop': 'photo-1714079761488-e0c9b9ac4138',
    'speaking': 'photo-1758873272222-ccd8c4296864',
    'docs': 'photo-1454165804606-c3d57bc86b40',
    'charts': 'photo-1758519289074-9de36003622b',
    'table': 'photo-1573164574572-cb89e39749b4',
    'handshake': 'photo-1521791136064-7986c2920216',
}
def u(key, w): return f'https://images.unsplash.com/{IMG[key]}?auto=format&fit=crop&w={w}&q=75'
def pic(key, w, alt, eager=False):
    pri = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return f'<img src="{u(key, w)}" alt="{html.escape(alt)}" width="{w}" height="{int(w*0.75)}"{pri} onerror="this.style.visibility=\'hidden\'">'

def svg(d, extra=''): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{d}</svg>'
IC = {
 'headset': svg('<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>'),
 'phone-in': svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/><path d="M15 3v5h5M21 3l-6 6"/>'),
 'phone-out': svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/><path d="M16 8V3h5M16 8l6-6"/>'),
 'alert': svg('<path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17.5v.01"/>'),
 'trend': svg('<path d="M3 17 9 11l4 4 8-8"/><path d="M15 7h6v6"/>'),
 'calendar': svg('<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>'),
 'heart': svg('<path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 22l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>'),
 'users': svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17.5" cy="9" r="2.5"/><path d="M16 14.2a5 5 0 0 1 6 4.8"/>'),
 'mail': svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
 'chat': svg('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/><path d="M8 11h8M8 14h5"/>'),
 'layers': svg('<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>'),
 'wrench': svg('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4 2.6-2.6Z"/>'),
 'smile': svg('<circle cx="12" cy="12" r="9"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9.5v.01M15 9.5v.01"/>'),
 'ticket': svg('<path d="M3 8a2 2 0 0 0 0 8v2a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-2a2 2 0 0 1 0-8V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1Z"/><path d="M13 5v14"/>'),
 'globe': svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
 'clock': svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 'shield': svg('<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>'),
 'eye': svg('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>'),
 'route': svg('<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>'),
 'sched': svg('<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M8 14h3M13 14h3M8 17h3"/>'),
 'file': svg('<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9l-6-6Z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>'),
 'db': svg('<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'),
 'folder': svg('<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'),
 'cart': svg('<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a1 1 0 0 0 1 .8h8.9a1 1 0 0 0 1-.8L20 7H6"/>'),
 'cog': svg('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>'),
 'search': svg('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>'),
 'send': svg('<path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M22 2 11 13"/>'),
 'chart': svg('<path d="M4 19V5M4 19h16M8 15l4-4 3 3 5-6"/>'),
 'target': svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
 'book': svg('<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5Z"/><path d="M4 21.5V4.5"/>'),
 'star': svg('<path d="m12 2 3 6.5 7 .8-5.2 4.8 1.5 7-6.3-3.6L5.7 21l1.5-7L2 9.3l7-.8L12 2Z"/>'),
 'badge': svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="m16 11 2 2 4-4"/>'),
 'user': svg('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
 'rows': svg('<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/>'),
 'lock': svg('<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'),
 'handshake': svg('<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L15 11"/><path d="M8 14l-4-4 5-5 4 1 2-1 5 5-1.5 1.5"/>'),
 'arrow': svg('<path d="M5 12h14M13 5l7 7-7 7"/>'),
 'building': svg('<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>'),
 'code': svg('<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>'),
}

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- shared shell
def head(key, extra=''):
    t, d, f = TITLES[key], DESCS[key], PAGES[key]
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t)}</title>
<meta name="description" content="{esc(d)}">
<meta name="theme-color" content="#061229">
<!-- PRIVATE PREVIEW: remove the next line when the client approves publishing -->
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ELVORRA OPERATIONS">
<meta property="og:title" content="{esc(t)}">
<meta property="og:description" content="{esc(d)}">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" sizes="64x64" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<script>try{{var s=localStorage.getItem('elvorra-theme');document.documentElement.dataset.theme=s||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress"></div>
<div class="glow" id="glow"></div>
'''

SERVICES_NAV = [
    ('cc', 'headset', 'Call Centre &amp; Customer Support', 'Voice, email, chat, helpdesk'),
    ('ml', 'globe', 'Multilingual &amp; 24/7 Operations', 'EN · FR · DE · ES, round the clock'),
    ('bo', 'file', 'Back-Office &amp; Administrative', 'Data, documents, orders, VA'),
    ('crm', 'db', 'CRM, Case Management &amp; QA', 'Workflows, tickets, quality'),
    ('mt', 'users', 'Managed BPO Teams', 'Dedicated, fully managed teams'),
]

def header(active):
    cur = lambda k: ' class="cur"' if active == k else ''
    mega = ''.join(f'<a href="{PAGES[k]}"><span class="mi">{IC[ic]}</span><span><b>{t}</b><small>{s}</small></span></a>' for k, ic, t, s in SERVICES_NAV)
    mega += f'<a href="{PAGES["contact"]}#proposal"><span class="mi">{IC["arrow"]}</span><span><b>Request a Proposal</b><small>Get a tailored operations plan</small></span></a>'
    mm_sub = ''.join(f'<a class="s" href="{PAGES[k]}">{t}</a>' for k, ic, t, s in SERVICES_NAV)
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m6 9 6 9-6-9"/></svg>'.replace('m6 9 6 9-6-9', 'm6 9 6 6 6-6')
    return f'''<header class="nav" id="nav">
  <a href="{PAGES['home']}" class="logo" aria-label="ELVORRA OPERATIONS — home">
    <img src="assets/logo.png" alt="" width="72" height="34">
    <span class="wm"><b>ELVORRA</b><span>OPERATIONS</span></span>
  </a>
  <nav class="links" aria-label="Main">
    <a href="{PAGES['home']}"{cur('home')}>Home</a>
    <a href="{PAGES['about']}"{cur('about')}>About</a>
    <div class="mega-w{' cur' if active == 'services' else ''}">
      <a href="{PAGES['home']}#services" class="mega-t">Services {chev}</a>
      <div class="mega">{mega}</div>
    </div>
    <a href="{PAGES['mt']}#partnerships">Partnerships</a>
    <a href="{PAGES['contact']}"{cur('contact')}>Contact</a>
  </nav>
  <div class="nav-r">
    <button class="tgl" id="tgl" aria-label="Switch between light and dark mode" aria-pressed="false">
      <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>
      <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
    <a href="{PAGES['contact']}#proposal" class="btn btn-gold mag">Request a Proposal <span class="ar">→</span></a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mm"><span></span><span></span></button>
  </div>
</header>
<div class="mm" id="mm">
  <a href="{PAGES['home']}">Home</a><a href="{PAGES['about']}">About</a><a href="{PAGES['home']}#services">Services</a>
  {mm_sub}
  <a href="{PAGES['mt']}#partnerships">Partnerships</a><a href="{PAGES['contact']}">Contact</a>
  <a href="{PAGES['contact']}#consultation" data-consult class="btn btn-line" style="margin-top:22px;justify-content:space-between;color:var(--text);border-color:var(--border2)">Book a Consultation <span class="ar" style="background:var(--text);color:var(--bg)">→</span></a>
  <a href="{PAGES['contact']}#proposal" class="btn btn-gold" style="margin-top:12px;border:0;justify-content:space-between;font-size:16px">Request a Proposal <span class="ar">→</span></a>
</div>
<main id="main">
'''

def footer():
    svcs = ''.join(f'<li><a href="{PAGES[k]}">{t}</a></li>' for k, ic, t, s in SERVICES_NAV)
    return f'''</main>
<footer class="frame">
  <div class="wrap">
    <div class="ftop">
      <div>
        <a href="{PAGES['home']}" class="logo" aria-label="ELVORRA OPERATIONS — home"><img src="assets/logo.png" alt="" width="96" height="38" style="height:38px"><span class="wm"><b>ELVORRA</b><span>OPERATIONS</span></span></a>
        <p class="claim">Global Reach. Operational Excellence. <span class="gold">Human-Centred Service.</span></p>
        <a href="{PAGES['contact']}#proposal" class="btn btn-ink mag">Request a Proposal <span class="ar">→</span></a>
      </div>
      <div><h5>Company</h5><ul><li><a href="{PAGES['home']}">Home</a></li><li><a href="{PAGES['about']}">About ELVORRA</a></li><li><a href="{PAGES['mt']}#partnerships">Partnerships</a></li><li><a href="{PAGES['contact']}">Contact Us</a></li><li><a href="{PAGES['contact']}#consultation" data-consult>Book a Consultation</a></li></ul></div>
      <div><h5>Services</h5><ul>{svcs}</ul></div>
      <div><h5>Contact</h5><ul><li><a href="mailto:" data-email data-email-text></a></li><li><a href="contact.html#whatsapp" data-wa>WhatsApp Business</a></li><li>Abuja, Nigeria</li><li>Serving clients worldwide</li></ul></div>
    </div>
  </div>
  <div class="giant" aria-hidden="true">ELVORRA</div>
  <div class="wrap"><div class="fbot"><span>© 2026 ELVORRA OPERATIONS. All rights reserved.</span><span>Global Reach · Operational Excellence · Human-Centred Service</span></div></div>
</footer>
<a class="wa" href="contact.html#whatsapp" data-wa aria-label="Chat with us on WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3Zm0 23.7c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7Zm5.9-8c-.3-.2-1.9-1-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.3-.7.1a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5.1 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5l-.6-.4Z"/></svg></a>
<script src="assets/config.js"></script>
<script src="assets/land.js"></script>
<script src="assets/main.js"></script>
</body>
</html>
'''

def page(key, body, active, extra_head=''):
    return head(key, extra_head) + header(active) + body + footer()

# ---------------------------------------------------------------- components
def pill(t): return f'<span class="pill">{t}</span>'
def page_hero(label, pill_t, h1, lead, img=None, alt='', chips=(), ctas=True, crumbs=True):
    crumb = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{PAGES["home"]}">Home</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>' if crumbs else ''
    c = ''
    if ctas:
        c = f'<div class="ctas"><a href="{PAGES["contact"]}#proposal" class="btn btn-gold mag">Request a Proposal <span class="ar">→</span></a><a href="{PAGES["contact"]}#consultation" data-consult class="btn btn-line mag">Book a Consultation <span class="ar">→</span></a></div>'
    media = ''
    if img:
        ch = ''
        if len(chips) > 0: ch += f'<div class="ph-chip c1">{chips[0][0]}<b>{chips[0][1]}</b></div>'
        if len(chips) > 1: ch += f'<div class="ph-chip c2">{chips[1][0]}<b>{chips[1][1]}</b></div>'
        media = f'<div class="ph-media rv"><div class="ph-img">{pic(img, 900, alt, True)}</div>{ch}</div>'
    grid = 'ph-grid' if img else ''
    inner = f'<div>{crumb}{pill(pill_t)}<h1>{h1}</h1><p class="lead">{lead}</p>{c}</div>{media}'
    return f'<section class="page-hero"><div class="wrap {grid}">{inner}</div></section>'

def sec_head(p, h2, sub='', center=True, row=False):
    cls = 'sec-head' + (' center' if center else '') + (' row' if row else '')
    s = f'<p class="sub">{sub}</p>' if sub else ''
    if row: return f'<div class="{cls} rv"><div>{pill(p)}<h2 class="h2">{h2}</h2></div>{s}</div>'
    return f'<div class="{cls} rv">{pill(p)}<h2 class="h2">{h2}</h2>{s}</div>'

def fcards(items, cols=3, numbered=False):
    out = []
    for i, (ic, t, d) in enumerate(items, 1):
        n = f'<span class="fn">{i:02d}</span>' if numbered else ''
        out.append(f'<article class="fcard rv">{n}<div class="fi">{IC[ic]}</div><h3>{t}</h3><p>{d}</p></article>')
    return f'<div class="grid-{cols}">{"".join(out)}</div>'

def steps(items):
    return '<div class="steps">' + ''.join(f'<div class="step-c rv"><h3>{t}</h3><p>{d}</p></div>' for t, d in items) + '</div>'

def faq(items):
    return '<div class="faq rv">' + ''.join(f'<details><summary>{q}<i aria-hidden="true">+</i></summary><div class="ans">{a}</div></details>' for q, a in items) + '</div>'

def cta_band(h2='Ready to outsource with <span class="gold">confidence?</span>', text='Tell us what you need and our team will come back with a tailored proposal. Prefer to talk first? Book a consultation.'):
    return f'''<section class="sec tight"><div class="wrap"><div class="cta-band rv">
  <div>{pill('Get started')}<h2>{h2}</h2><p>{text}</p></div>
  <div class="ctas"><a href="{PAGES['contact']}#proposal" class="btn btn-gold mag">Request a Proposal <span class="ar">→</span></a><a href="{PAGES['contact']}#consultation" data-consult class="btn btn-line mag">Book a Consultation <span class="ar">→</span></a></div>
</div></div></section>'''

def checks(items): return '<ul class="checks">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def split(p, h2, paras, items=None, img=None, alt='', over=None, rev=False, extra=''):
    body = f'{pill(p)}<h2 class="h2">{h2}</h2>' + ''.join(f'<p>{x}</p>' for x in paras) + (checks(items) if items else '') + extra
    o = f'<div class="over"><b>{over[0]}</b><span>{over[1]}</span></div>' if over else ''
    media = f'<div class="media rv">{pic(img, 1000, alt)}{o}</div>'
    return f'<section class="sec"><div class="wrap split{" rev" if rev else ""}"><div class="rv">{body}</div>{media}</div></section>'

# ---- reusable chunks sliced from the v3 concept
def v3seg(a, b):
    i = v3.index(a); j = v3.index(b, i)
    return v3[i:j]

LIVE_ROW = re.search(r'<div class="live-row">.*?</div>\n\n    <div class="team rv">', v3, re.S).group(0).replace('\n\n    <div class="team rv">', '')
PARTNERS = v3seg('<!-- PARTNERS -->', '<!-- PROPOSAL -->')
MODELS = v3seg('<!-- MODELS -->', '<!-- PARTNERS -->')
for old, new in [('<li>6, 12 or 24-month terms</li>', '<li>Flexible terms agreed in your proposal</li>')]:
    MODELS = MODELS.replace(old, new)
PARTNERS = PARTNERS.replace('href="#proposal" class="prow"', f'href="{PAGES["contact"]}#proposal" class="prow"')

GCARD = '''<div class="gcard rv">
      <canvas id="globe" aria-label="Rotating globe showing our operations hub in Abuja connected to major business regions" role="img"></canvas>
      <span class="gc-t">Global Operations Desk</span><span class="gc-hint">Drag to rotate ↔</span>
      <div class="zones">
        <div class="z">New York<b data-tz="America/New_York">--:--</b></div>
        <div class="z">London<b data-tz="Europe/London">--:--</b></div>
        <div class="z">Dubai<b data-tz="Asia/Dubai">--:--</b></div>
        <div class="z hq">Abuja · HQ<b data-tz="Africa/Lagos">--:--</b></div>
      </div>
    </div>'''

def tz_grid():
    z = [('Abuja · HQ', 'Africa/Lagos', 'Operations hub', ' hq'), ('New York', 'America/New_York', 'United States', ''), ('London', 'Europe/London', 'United Kingdom', ''),
         ('Amsterdam', 'Europe/Amsterdam', 'Netherlands · Germany', ''), ('Dubai', 'Asia/Dubai', 'Middle East', ''), ('Singapore', 'Asia/Singapore', 'Asia', '')]
    return '<div class="tzgrid">' + ''.join(f'<div class="tz rv{h}"><small>{n}</small><b data-tz="{tz}">--:--</b><span>{r}</span></div>' for n, tz, r, h in z) + '</div>'

def pipe(cols, cards):
    out = ''
    for (h, n), (a, b) in zip(cols, cards):
        out += f'<div class="pcol"><h4><span>{h}</span><span>{n}</span></h4><div class="pcard">{a}<small>{b}</small></div></div>'
    return f'<div class="pipe">{out}</div>'

# ================================================================ HOME
def build_home():
    seg = v3seg('<!-- HERO -->', '<!-- PROPOSAL -->')
    # link patching
    seg = seg.replace('href="#proposal" class="btn btn-line mag">Book a Consultation', f'href="{PAGES["contact"]}#consultation" data-consult class="btn btn-line mag">Book a Consultation')
    seg = seg.replace('href="#proposal"', f'href="{PAGES["contact"]}#proposal"')
    def seq(s, old, news):
        for n in news: s = s.replace(old, n, 1)
        return s
    seg = seq(seg, '<a href="#" class="tc rv">', [f'<a href="{PAGES["about"]}" class="tc rv">', f'<a href="{PAGES["ml"]}" class="tc rv">'])
    seg = seg.replace('<a href="#" class="tc acc rv">', f'<a href="{PAGES["about"]}#approach" class="tc acc rv">')
    seg = seq(seg, '<a href="#" class="sc rv">', [f'<a href="{PAGES[k]}" class="sc rv">' for k in ('cc', 'ml', 'bo', 'crm')])
    seg = seg.replace('<a href="#" class="btn btn-gold mag" style="align-self:flex-start">Build your team', f'<a href="{PAGES["mt"]}" class="btn btn-gold mag" style="align-self:flex-start">Build your team')
    seg = seg.replace('<li>6, 12 or 24-month terms</li>', '<li>Flexible terms agreed in your proposal</li>')
    seg = seg.replace('href="#partners"', f'href="{PAGES["mt"]}#partnerships"')
    seg = seg.replace('<a href="#proposal" class="prow">', f'<a href="{PAGES["contact"]}#proposal" class="prow">')
    seg = seg.replace('<img src="{{IMG:photo-1626863905121-3b0c0ed7b94c:2000}}" alt="Customer support professionals with headsets in a bright office">',
                      '<img src="{{IMG:photo-1626863905121-3b0c0ed7b94c:2000}}" alt="Customer support professionals with headsets in a bright office" fetchpriority="high" onerror="this.style.visibility=\'hidden\'">')
    # services section: add "view all" links
    cta = f'''<section class="prop" id="start"><div class="wrap"><div class="cta-band rv">
  <div>{pill('Request a proposal')}<h2>Ready to outsource with <span class="gold">confidence?</span></h2><p>Tell us what you need in a few quick steps. We respond within one business day, or book a consultation to talk it through.</p></div>
  <div class="ctas"><a href="{PAGES['contact']}#proposal" class="btn btn-gold mag">Request a Proposal <span class="ar">→</span></a><a href="{PAGES['contact']}#consultation" data-consult class="btn btn-line mag">Book a Consultation <span class="ar">→</span></a></div>
</div></div></section>'''
    ld = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"ELVORRA OPERATIONS","description":"International BPO, call centre and managed business operations company.","address":{"@type":"PostalAddress","addressLocality":"Abuja","addressCountry":"NG"},"email":"elevoraoperation@gmail.com"}</script>\n'''
    return page('home', seg + cta, 'home', ld)

# ================================================================ ABOUT
def build_about():
    svc = [('headset', 'Call Centre Outsourcing', 'cc'), ('chat', 'Customer Support Outsourcing', 'cc'), ('globe', 'Multilingual Customer Support', 'ml'), ('clock', '24/7 Support Operations', 'ml'),
           ('shield', 'Quality Assurance & Performance', 'crm'), ('file', 'Back-Office & Administrative', 'bo'), ('db', 'CRM & Case Management', 'crm'), ('users', 'Managed BPO Teams', 'mt'), ('calendar', 'Virtual Assistance', 'bo')]
    svc_html = '<div class="grid-3">' + ''.join(f'<a href="{PAGES[k]}" class="fcard rv"><span class="fn">{i:02d}</span><div class="fi">{IC[ic]}</div><h3>{t}</h3><p style="color:var(--gold3);font-weight:600;font-size:14px">Explore →</p></a>' for i, (ic, t, k) in enumerate(svc, 1)) + '</div>'
    body = page_hero('About', 'About ELVORRA OPERATIONS', 'A managed operations partner, <em class="gold">built for global business.</em>',
                     'ELVORRA OPERATIONS is an international Business Process Outsourcing, call centre and managed business operations company providing reliable, scalable and professionally managed outsourcing solutions to businesses worldwide.',
                     'table', 'Team collaborating around a table with laptops', [('Headquartered in', 'Abuja, Nigeria'), ('Serving', 'Businesses worldwide')])
    body += split('Who we are', 'We run the operations <span class="gold">behind your customers.</span>',
        ['We partner with companies to manage their customer interactions, streamline business processes, improve operational efficiency and deliver exceptional customer experiences through dedicated teams, technology and professional operational management.',
         'Our goal is to become a trusted outsourcing partner for businesses seeking dependable customer support, call centre operations and comprehensive business process management solutions.'],
        ['A managed operations partner, not a recruitment agency', 'More than a call centre: customer support, back-office, CRM and quality under one roof', 'Dedicated teams with real supervision and reporting', 'Built to scale as your volumes and markets grow'],
        'team', 'Diverse business team collaborating', ('Managed People. Structured Operations.', 'Scalable Business Support.'))
    body += f'''<section class="sec band soft" style="padding:100px 0"><div class="wrap">{sec_head('Our brand promise', 'Global Reach. Operational Excellence. <span class="gold">Human-Centred Service.</span>')}
{fcards([('globe', 'Global Reach', 'We support businesses in the United States, United Kingdom, Canada, Germany, the Netherlands, wider Europe, the Middle East and Asia, with shift-based coverage across time zones.'),
         ('target', 'Operational Excellence', 'Defined processes, live supervision, quality assurance and KPI and SLA reporting on every engagement, so performance is measured, not assumed.'),
         ('heart', 'Human-Centred Service', 'Behind every interaction is a trained person. We invest in coaching and clear communication so your customers feel heard and helped.')], 3, True)}
</div></section>'''
    body += f'<section class="sec"><div class="wrap">{sec_head("What we do", "Nine service lines, <span class=\"gold\">one accountable partner.</span>", "From the first customer call to the last line of back-office processing, we design, staff, supervise and continuously improve the operations you entrust to us.")}{svc_html}</div></section>'
    body += f'''<section class="sec band navy" id="approach" style="padding:100px 0"><div class="wrap">{sec_head('How we work', 'Managed People. Structured Operations. <span class="gold">Scalable Support.</span>', 'Every engagement follows the same disciplined approach.')}
{steps([('Understand', 'We learn your customers, channels, volumes, languages and goals before we design anything.'), ('Structure', 'We define the team, processes, SLAs, KPIs and escalation paths in writing.'), ('Deliver', 'Dedicated, trained teams go live on your systems under named team leaders.'), ('Improve', 'Regular QA, reporting and reviews keep the operation getting better.')])}
</div></section>'''
    body += f'''<section class="sec"><div class="wrap split"><div class="rv">{pill('Where we serve')}<h2 class="h2">Based in Abuja. <span class="gold">Built for the world.</span></h2>
<p>Our operations hub in Abuja (GMT+1) shares UK and European business hours and overlaps with US mornings. Shift-based teams extend coverage across other time zones.</p>
{checks(['United States and Canada', 'United Kingdom, Germany, the Netherlands and wider Europe', 'Middle East and Asia', 'Any international business seeking reliable outsourced operations'])}</div>
<div class="rv">{GCARD}</div></div></section>'''
    body += cta_band()
    return page('about', body, 'about')

# ================================================================ CALL CENTRE
def build_cc():
    body = page_hero('Call Centre & Customer Support', 'Call Centre & Customer Support Outsourcing', 'Every customer conversation, <em class="gold">professionally managed.</em>',
        'Dedicated inbound and outbound call centre teams and multichannel customer support, supervised and quality-assured by ELVORRA OPERATIONS.',
        'laptop', 'Support agent wearing headphones working at a laptop', [('Channels', 'Voice · Email · Chat'), ('Managed by', 'Dedicated team leaders')])
    body += f'<section class="sec" id="call-centre"><div class="wrap">{sec_head("Call Centre Outsourcing", "Voice operations that <span class=\"gold\">sound like your brand.</span>", "Dedicated, professionally managed call centre teams for every kind of customer conversation.")}'
    body += fcards([('phone-in', 'Inbound call centre', 'Professional handling of incoming customer calls with trained agents who know your products and tone of voice.'),
        ('phone-out', 'Outbound call centre', 'Structured outbound campaigns for follow-ups, surveys, reminders and customer outreach.'),
        ('alert', 'Enquiries & complaint handling', 'Calm, accurate handling of customer enquiries and complaints, with clear escalation to the right people.'),
        ('trend', 'Telephone sales & lead generation', 'Outbound telesales and lead qualification run against agreed targets and scripts.'),
        ('calendar', 'Appointment scheduling & follow-ups', 'Booking, confirming and following up appointments so your calendar stays full.'),
        ('heart', 'Customer retention & engagement', 'Proactive contact that keeps customers informed, engaged and loyal.'),
        ('users', 'Dedicated & managed call centre teams', 'Agents, team leaders and quality specialists working exclusively on your account.')], 3, True)
    body += '</div></section>'
    body += f'<section class="sec band soft" id="customer-support" style="padding:100px 0"><div class="wrap">{sec_head("Customer Support Outsourcing", "Consistent support on <span class=\"gold\">every channel.</span>", "One team, one standard of service, whether customers call, write or chat.")}'
    body += fcards([('mail', 'Email support', 'Timely, well-written email responses tracked through to resolution.'),
        ('chat', 'Live chat support', 'Real-time chat support on your website and messaging channels.'),
        ('layers', 'Multichannel customer service', 'Voice, email and chat handled together with a consistent customer view.'),
        ('wrench', 'Technical & product support', 'First-line technical and product support, with structured escalation to your specialists.'),
        ('smile', 'Customer experience management', 'Monitoring and improving the whole customer journey, not just individual contacts.'),
        ('ticket', 'Helpdesk & ticket management', 'Every request logged, prioritised, tracked and closed, with nothing falling through the cracks.')], 3, True)
    body += '</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("An operation in motion", "See how a <span class=\"gold\">managed desk</span> looks.", "An illustration of the live view, case tracking and shift coverage that sit behind every ELVORRA engagement.")}{LIVE_ROW.replace(" mt", " mt")}</div></section>'
    body += split('What you get', 'Every programme comes with <span class="gold">management built in.</span>',
        ['Our teams are never left to run unsupervised. Every programme is set up with the structure needed to keep quality high and results visible.'],
        ['A dedicated team leader accountable for your account', 'Call monitoring and quality assurance scorecards', 'Agreed KPIs and SLAs with regular reporting', 'Scripts, knowledge base and escalation paths', 'The ability to scale up or down with your volumes'],
        'speaking', 'Professional speaking on the phone in a modern office', ('Dedicated and managed', 'Teams built around your brand'), rev=True)
    body += f'''<section class="sec band navy" style="padding:100px 0"><div class="wrap">{sec_head('How we launch', 'From first conversation to <span class="gold">go-live.</span>')}
{steps([('Scope', 'We agree channels, volumes, hours, languages and success measures.'), ('Staff & train', 'We assemble your team and train them on your products, systems and brand voice.'), ('Go live', 'Your team starts handling real customers under close supervision.'), ('Manage & improve', 'QA, reporting and coaching keep performance improving month after month.')])}
</div></section>'''
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">call centre &amp; support.</span>")}' + faq([
        ('Which channels can you support?', 'We handle inbound and outbound voice, email, live chat and multichannel support, as well as helpdesk and ticket management. Tell us the channels you need and we will design the team around them.'),
        ('Can you handle both inbound and outbound calls?', 'Yes. We run inbound customer service as well as outbound programmes such as telephone sales, lead generation, appointment scheduling, follow-ups and customer retention.'),
        ('Do we get a dedicated team?', 'Yes. Our managed teams include dedicated agents, team leaders and quality specialists who work on your account.'),
        ('Can we start small and grow?', 'Yes. Many clients begin with a focused pilot and scale as volumes and confidence grow. See our engagement models on the Managed BPO Teams page.'),
        ('How will we know how the team is performing?', 'Through agreed KPIs and SLAs, call monitoring and QA scorecards, and regular performance reports.')]) + '</div></section>'
    body += cta_band()
    return page('cc', body, 'services')

# ================================================================ MULTILINGUAL
def build_ml():
    body = page_hero('Multilingual & 24/7 Support', 'Multilingual & 24/7 Support Operations', 'Support in your customers’ language, <em class="gold">around the clock.</em>',
        'English, French, German and Spanish support delivered by shift-based teams with live supervision, workforce scheduling and clear escalation.',
        'phonedesk', 'Support professional on the phone at a desk', [('Coverage', '24/7 shift model'), ('Languages', 'EN · FR · DE · ES')])
    langs = [('EN', 'Hello', 'English-language customer support for international audiences.'), ('FR', 'Bonjour', 'French-language support for customers in France and beyond.'),
             ('DE', 'Hallo', 'German-language support for customers in Germany and German-speaking markets.'), ('ES', 'Hola', 'Spanish-language support for Spain, Latin America and Spanish-speaking customers.')]
    lg = '<div class="langs">' + ''.join(f'<div class="lang rv"><span class="code">{c}</span><div class="big gold">{g}</div><p>{p}</p></div>' for c, g, p in langs) + '</div>'
    body += f'<section class="sec" id="multilingual"><div class="wrap">{sec_head("Multilingual Customer Support", "Speak your customers’ <span class=\"gold\">language.</span>", "Customers are happier, and stay longer, when support feels native.")}{lg}'
    body += '<div class="rv" style="margin-top:16px"><div class="fcard dark"><div class="fi">' + IC['globe'] + '</div><h3>More languages on request</h3><p>We can add further languages based on your requirements and verified personnel availability. Tell us what you need in your proposal request.</p></div></div></div></section>'
    body += split('24/7 Support Operations', 'Always on. <span class="gold">Always supervised.</span>',
        ['Round-the-clock customer service is more than extended opening hours. It needs dedicated shift teams, live supervision and a plan for when things go wrong.'],
        ['Round-the-clock customer service', 'Dedicated shift-based support teams', 'Global customer support coverage', 'Operational supervision on every shift', 'Workforce coordination and scheduling', 'Service continuity and escalation management'],
        'meeting', 'Business team meeting in a modern office', ('Shift-based teams', 'Coordinated, supervised, continuous'), rev=True)
    body += f'<section class="sec band soft" style="padding:100px 0"><div class="wrap">{sec_head("Coverage across time zones", "Your customers are <span class=\"gold\">never out of hours.</span>", "Live local times in the markets we support. Our Abuja hub runs on GMT+1, sharing UK and European business hours.")}{tz_grid()}</div></section>'
    body += f'''<section class="sec"><div class="wrap split"><div class="rv">{pill('Global support coverage')}<h2 class="h2">One operations desk. <span class="gold">Many markets.</span></h2>
<p>From our Abuja hub we coordinate shift teams that support businesses in the United States, United Kingdom, Canada, Germany, the Netherlands, wider Europe, the Middle East and Asia.</p>
<p>Drag the globe to explore.</p></div><div class="rv">{GCARD}</div></div></section>'''
    body += f'<section class="sec band navy" style="padding:100px 0"><div class="wrap">{sec_head("How 24/7 works", "Coverage that <span class=\"gold\">holds together.</span>")}{steps([("Workforce planning", "We forecast volumes and build shift patterns around your busiest hours."), ("Shift teams", "Dedicated teams cover each shift with the right language skills."), ("Live supervision", "Team leaders monitor queues, quality and attendance in real time."), ("Escalation & continuity", "Clear escalation paths and cover plans keep service running when issues arise.")])}</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">multilingual &amp; 24/7 support.</span>")}' + faq([
        ('Which languages do you support?', 'Our core languages are English, French, German and Spanish. Additional languages can be added based on your requirements and verified personnel availability.'),
        ('Can you cover nights, weekends and holidays?', 'Yes. We build shift-based teams and schedules around the hours your customers need support, including round-the-clock coverage.'),
        ('How do you keep quality consistent across shifts?', 'Each shift has team leaders and quality monitoring, and every team works to the same scripts, knowledge base and KPIs.'),
        ('What happens when there is an urgent issue overnight?', 'We agree escalation paths with you in advance, so urgent cases reach the right person quickly at any hour.'),
        ('Can we combine languages in one team?', 'Yes. We can build teams that cover several languages and route customers to the right agents.')]) + '</div></section>'
    body += cta_band()
    return page('ml', body, 'services')

# ================================================================ BACK OFFICE
def build_bo():
    body = page_hero('Back-Office & Administrative', 'Back-Office & Administrative Outsourcing', 'The work behind the scenes, <em class="gold">handled accurately.</em>',
        'Data processing, document and records management, order processing and virtual assistance, delivered by managed teams so your people can focus on growth.',
        'docs', 'Person working on documents near a laptop', [('Delivery', 'Managed & supervised'), ('Focus', 'Accuracy & confidentiality')])
    body += f'<section class="sec" id="back-office"><div class="wrap">{sec_head("Back-Office Support", "Accurate processing, <span class=\"gold\">on time.</span>", "Reliable back-office teams that keep your business running smoothly.")}'
    body += fcards([('rows', 'Data entry & processing', 'Fast, accurate data entry and processing, checked before it reaches your systems.'),
        ('folder', 'Document management', 'Organising, indexing, digitising and maintaining your business documents.'),
        ('user', 'Administrative assistance', 'General administrative support that clears the backlog from your in-house team.'),
        ('file', 'Records management', 'Accurate, up-to-date, well-organised customer and business records.'),
        ('cart', 'Order processing', 'Capturing, validating and processing orders from receipt to completion.'),
        ('cog', 'Business process support', 'Hands-on support for recurring processes, following your documented procedures.')], 3, True)
    body += '</div></section>'
    body += f'<section class="sec band soft" id="virtual-assistance" style="padding:100px 0"><div class="wrap">{sec_head("Virtual Assistance & Business Operations Support", "Leaders stay organised. <span class=\"gold\">Operations keep moving.</span>")}'
    body += fcards([('star', 'Executive & administrative assistance', 'Day-to-day support for executives and teams.'), ('mail', 'Email & calendar management', 'Inboxes triaged and calendars kept in order.'),
        ('layers', 'Business coordination', 'Following up, coordinating people and keeping projects moving.'), ('search', 'Research & data management', 'Research tasks and structured data kept accurate and up to date.'),
        ('code', 'Remote operational support', 'Flexible remote support for your operational needs.')], 3, True)
    body += '</div></section>'
    pc = pipe([('Received', '12'), ('Processing', '8'), ('Quality check', '5'), ('Completed', '47')],
              [('Order #1042', 'Awaiting entry'), ('Order #1038', 'Data entry'), ('Order #1035', 'Second check'), ('Order #1029', 'Delivered')])
    body += f'<section class="sec"><div class="wrap split"><div class="rv">{pill("Process control")}<h2 class="h2">Every task tracked <span class=\"gold\">from receipt to completion.</span></h2><p>Work moves through clear stages with checks along the way, so you always know where things stand and nothing is lost between hand-offs.</p>{checks(["Defined workflows for each type of task", "Quality checks before work is delivered", "Progress and turnaround reporting", "Easy to scale up for busy periods"])}</div><div class="vis-card rv"><div class="lt"><span>Example order workflow</span><span class="live">Live</span></div>{pc}<p class="note">Illustrative example of how work is tracked.</p></div></div></section>'
    body += split('Accuracy & confidentiality', 'Your data, <span class="gold">handled with care.</span>',
        ['Back-office work often involves sensitive customer and business information. We treat protecting it as part of the job, not an extra.'],
        ['Confidentiality agreements for team members', 'Controlled access to your systems and data', 'Documented procedures for every process', 'Quality checks and error tracking'],
        'charts', 'Two professionals reviewing charts on a laptop', ('Documented & checked', 'Processes you can rely on'), rev=True)
    body += f'<section class="sec band navy" style="padding:100px 0"><div class="wrap">{sec_head("Getting started", "Simple to start, <span class=\"gold\">easy to scale.</span>")}{steps([("Define", "We agree the tasks, volumes, turnaround times and quality standards."), ("Document", "Your processes are written down so work is done consistently."), ("Deploy", "A managed team begins, with supervision and quality checks."), ("Review", "Regular reports let us improve accuracy and speed together.")])}</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">back-office &amp; admin.</span>")}' + faq([
        ('What kinds of back-office work can you take on?', 'Data entry and processing, document and records management, order processing, administrative assistance and wider business process support.'),
        ('Can you work inside our own systems?', 'Yes. Our teams can work in your CRM and business systems under controlled access, following your procedures.'),
        ('How do you keep information secure?', 'We use confidentiality agreements, controlled system access and documented procedures. We will go through your specific requirements with you.'),
        ('Do you offer virtual assistants?', 'Yes. We provide executive and administrative assistance, email and calendar management, business coordination, research and remote operational support.'),
        ('Can the team grow with our workload?', 'Yes. Teams can be scaled up or down as your volumes change.')]) + '</div></section>'
    body += cta_band()
    return page('bo', body, 'services')

# ================================================================ CRM / QA
def build_crm():
    body = page_hero('CRM, Case Management & QA', 'CRM, Case Management & Quality Assurance', 'Clean data. Tracked cases. <em class="gold">Measured quality.</em>',
        'We administer your CRM, manage every ticket and case through to resolution, and monitor quality and performance against agreed KPIs and SLAs.',
        'charts', 'Two professionals reviewing charts on a laptop', [('Every case', 'Tracked to resolution'), ('Quality', 'Monitored & reported')])
    body += f'<section class="sec" id="crm"><div class="wrap">{sec_head("CRM & Case Management", "Every customer record, <span class=\"gold\">every case, under control.</span>", "Structured administration that keeps your customer data clean and your cases moving.")}'
    body += fcards([('db', 'CRM administration', 'Day-to-day administration of your CRM so it stays accurate and usable.'), ('users', 'Customer database management', 'Keeping customer databases clean, complete and up to date.'),
        ('ticket', 'Ticket & case management', 'Logging, prioritising, tracking and resolving every ticket and case.'), ('file', 'Customer records administration', 'Accurate administration of customer records and account changes.'),
        ('route', 'Workflow management', 'Defining and running the workflows that move cases from first contact to closure.'), ('chart', 'Reporting & documentation', 'Clear reporting and documentation of cases, activity and outcomes.')], 3, True)
    body += '</div></section>'
    pc = pipe([('New', '14'), ('In progress', '9'), ('Escalated', '2'), ('Resolved', '63')],
              [('Refund request', '#4823'), ('Account update', '#4822'), ('Billing dispute', '#4819'), ('Delivery query', '#4815')])
    sc = '<div class="score">' + ''.join(f'<div class="srow"><span>{n}</span><div class="sb"><i style="--v:{v/100}"></i></div><b>{v}%</b></div>' for n, v in [('Greeting & tone', 94), ('Understanding the issue', 90), ('Accuracy of resolution', 88), ('Process compliance', 92), ('Closing & next steps', 86)]) + '</div>'
    body += f'<section class="sec band soft" style="padding:100px 0"><div class="wrap">{sec_head("In practice", "From first contact to <span class=\"gold\">measured outcome.</span>", "Illustrations of case tracking and a quality scorecard.")}<div class="grid-2"><div class="vis-card rv"><div class="lt"><span>Case pipeline</span><span class="live">Live</span></div>{pc}<p class="note">Illustrative example of case tracking.</p></div><div class="vis-card rv" data-score><div class="lt"><span>QA scorecard</span><span>Sample interaction review</span></div>{sc}<p class="note">Illustrative example scorecard.</p></div></div></div></section>'
    body += f'<section class="sec" id="quality-assurance"><div class="wrap">{sec_head("Quality Assurance & Performance Management", "Quality you can <span class=\"gold\">measure and improve.</span>", "Every interaction can be reviewed against agreed standards, and every insight feeds back into better performance.")}'
    body += fcards([('headset', 'Call monitoring & evaluation', 'Regular monitoring and evaluation of customer calls against agreed standards.'), ('smile', 'Customer interaction quality assessments', 'Assessing calls, emails and chats for accuracy, tone and resolution.'),
        ('user', 'Agent performance monitoring', 'Tracking individual and team performance so coaching is targeted.'), ('chart', 'Quality assurance reporting', 'Clear QA reports showing trends, strengths and areas to improve.'),
        ('target', 'KPI & SLA monitoring', 'Monitoring performance against the KPIs and SLAs agreed with you.'), ('book', 'Training recommendations & improvement', 'Practical training recommendations that drive continuous improvement.')], 3, True)
    body += '</div></section>'
    body += f'<section class="sec band navy" style="padding:100px 0"><div class="wrap">{sec_head("The improvement loop", "Monitor. Evaluate. Coach. <span class=\"gold\">Improve.</span>")}{steps([("Monitor", "We review calls, chats, emails and cases against your standards."), ("Evaluate", "Scorecards and KPIs show where performance is strong and where it slips."), ("Coach", "Team leaders coach agents with specific, evidence-based feedback."), ("Improve", "Reports and recommendations feed back into training and process changes.")])}</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">CRM &amp; quality.</span>")}' + faq([
        ('Can you work inside our existing CRM?', 'Yes. We administer and work within your CRM and case management tools under controlled access.'),
        ('What does case management include?', 'Ticket and case logging, prioritisation, tracking, escalation, resolution and reporting, using defined workflows.'),
        ('How is quality measured?', 'Through call monitoring, interaction assessments and QA scorecards, alongside KPI and SLA monitoring agreed with you.'),
        ('Will we see the results?', 'Yes. Quality assurance and performance reports are shared with you on an agreed schedule.'),
        ('Do you recommend training?', 'Yes. QA findings turn into training recommendations and coaching plans for continuous improvement.')]) + '</div></section>'
    body += cta_band()
    return page('crm', body, 'services')

# ================================================================ MANAGED TEAMS
def build_mt():
    body = page_hero('Managed BPO Teams & Partnerships', 'Managed BPO Teams & Business Partnerships', 'A complete team, <em class="gold">fully managed by us.</em>',
        'Dedicated agents, team leaders, QA specialists and operational management, deployed and managed for your business, plus partnership options for BPO providers, agencies and technology firms.',
        'meeting', 'Business team meeting in a modern office', [('Team', 'Agents · Leaders · QA'), ('Partnerships', 'Direct · BPO · Tech')])
    body += f'<section class="sec" id="managed-teams"><div class="wrap">{sec_head("Managed BPO Teams & Workforce Solutions", "Everything a team needs. <span class=\"gold\">Managed for you.</span>", "We assemble, deploy and manage the whole team so you get results, not management overhead.")}'
    body += fcards([('headset', 'Dedicated customer support agents', 'Agents working exclusively on your brand, products and customers.'), ('users', 'Team leaders & supervisors', 'Named leaders who supervise, coach and are accountable for performance.'),
        ('shield', 'Quality assurance specialists', 'Specialists who monitor and improve quality on your account.'), ('cog', 'Operational management', 'Day-to-day management of the operation, from scheduling to escalations.'),
        ('route', 'Recruitment coordination & workforce deployment', 'We coordinate recruitment and deploy people into your managed operation. This supports your team, not a stand-alone recruitment service.'), ('chart', 'Performance monitoring & reporting', 'Regular reporting against agreed KPIs and SLAs.')], 3, True)
    body += '</div></section>'
    body += f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="team rv">
  <div class="tp"><span class="pill" style="background:rgba(255,255,255,.08);color:rgba(255,255,255,.8);border-color:rgba(255,255,255,.18);align-self:flex-start">How a managed team is structured</span>
  <h3>One accountable structure, <span class="gold">from agent to manager.</span></h3>
  <p>Every managed team has clear roles and reporting lines, so there is always someone responsible for quality, attendance and results.</p>
  <div class="chips"><span>Dedicated agents</span><span>Team leaders</span><span>QA specialists</span><span>Operations manager</span></div>
  <a href="{PAGES['contact']}#proposal" class="btn btn-gold mag" style="align-self:flex-start">Build your team <span class="ar">→</span></a></div>
  <div class="pic">{pic('table', 1200, 'Team working together at a table with laptops')}
  <div class="org"><div class="node top">Operations Manager</div><div class="lvl"><div class="node"><i></i>Team Leader</div><div class="node"><i></i>QA Specialist</div></div><div class="agents"><i></i><i></i><i></i><i></i><i></i></div></div></div>
</div></div></section>'''
    body += MODELS.replace('class="frame models-s"', 'class="frame models-s" id="engagement"')
    body += f'<section class="sec" id="partnerships" style="padding-bottom:0"><div class="wrap">{sec_head("Business Partnerships", "Strategic partnerships, <span class=\"gold\">built to last.</span>", "We work with businesses, BPO providers and technology firms worldwide who need a dependable operations partner.")}</div></section>'
    body += PARTNERS.replace('class="partners" id="partners"', 'class="partners"')
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">managed teams &amp; partnerships.</span>")}' + faq([
        ('What is a managed BPO team?', 'A team of dedicated agents, team leaders, QA specialists and operational management that we recruit, deploy, supervise and report on for your business.'),
        ('Are you a recruitment agency?', 'No. ELVORRA OPERATIONS is a managed operations partner. Recruitment coordination and workforce deployment exist to build and run your managed operation.'),
        ('Can we start with a pilot?', 'Yes. A pilot programme lets you validate quality and fit before scaling into a dedicated team or managed service.'),
        ('Do you partner with other BPO providers?', 'Yes. We offer overflow, multilingual and after-hours capacity to established providers through subcontracting partnerships.'),
        ('How do we begin a partnership?', 'Start with an introductory call, then we scope the work, prepare a tailored proposal and agree a pilot or go-live plan.')]) + '</div></section>'
    body += cta_band()
    return page('mt', body, 'services')

# ================================================================ CONTACT
def build_contact():
    opts = ['Call centre', 'Customer support', 'Multilingual support', '24/7 operations', 'Quality assurance', 'Back-office', 'CRM & case management', 'Managed BPO team', 'Virtual assistance', 'Partnership']
    o = ''.join(f'<span class="opt" role="button" tabindex="0">{x}</span>' for x in opts)
    countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 'Netherlands', 'France', 'Spain', 'Other Europe', 'Middle East', 'Asia', 'Africa', 'Other']
    co = ''.join(f'<option>{c}</option>' for c in countries)
    body = page_hero('Contact', 'Contact us', 'Request a proposal or <em class="gold">book a consultation.</em>',
        'Tell us about your business and what you want to outsource. We will respond within one business day with next steps.', ctas=False)
    body += f'''<section class="sec" style="padding-top:60px" id="start"><div class="wrap contact-grid">
<aside class="cside rv" aria-label="Contact details">
  <a class="cc" href="mailto:" data-email><span class="ic">{IC['mail']}</span><div><small>BUSINESS EMAIL</small><b data-email-text></b></div></a>
  <a class="cc wsp" id="whatsapp" href="#" data-wa data-wa-fallback="#whatsapp"><span class="ic">{IC['chat']}</span><div><small>WHATSAPP BUSINESS</small><b>Chat with our team</b></div></a>
  <a class="cc" href="#consultation" data-consult><span class="ic">{IC['calendar']}</span><div><small>BOOK A CONSULTATION</small><b>30-minute discovery call</b></div></a>
  <div class="cc"><span class="ic">{IC['building']}</span><div><small>HEADQUARTERS</small><b>Abuja, Nigeria</b></div></div>
  <div class="cc"><span class="ic">{IC['clock']}</span><div><small>RESPONSE TIME</small><b>Within one business day</b></div></div>
</aside>
<div class="formcard rv" id="lead" data-mode="proposal">
  <div class="mode" role="group" aria-label="Choose request type"><button type="button" class="on" data-mode="proposal" id="proposal">Request a Proposal</button><button type="button" data-mode="consult" id="consultation">Book a Consultation</button></div>
  <div class="wiz-top"><b id="wtitle">What do you need?</b><span id="wcount">Step 1 of 3</span></div>
  <div class="wbar"><i id="wbar"></i></div>
  <form id="leadform" novalidate autocomplete="on">
    <div class="step on" data-s="1"><p class="hint" id="hint">Select every service you are interested in.</p><div class="opts" data-multi data-name="services">{o}</div></div>
    <div class="step" data-s="2">
      <div class="mode-p">
        <span class="lbl" style="margin-top:0">Estimated team size</span><div class="opts" data-single data-name="teamSize"><span class="opt" role="button" tabindex="0">1–5</span><span class="opt" role="button" tabindex="0">6–15</span><span class="opt" role="button" tabindex="0">16–50</span><span class="opt" role="button" tabindex="0">50+</span><span class="opt" role="button" tabindex="0">Not sure</span></div>
        <span class="lbl">Coverage needed</span><div class="opts" data-single data-name="coverage"><span class="opt" role="button" tabindex="0">Business hours</span><span class="opt" role="button" tabindex="0">Extended hours</span><span class="opt" role="button" tabindex="0">24/7</span></div>
        <span class="lbl">Languages</span><div class="opts" data-multi data-name="languages"><span class="opt" role="button" tabindex="0">English</span><span class="opt" role="button" tabindex="0">French</span><span class="opt" role="button" tabindex="0">German</span><span class="opt" role="button" tabindex="0">Spanish</span><span class="opt" role="button" tabindex="0">Other</span></div>
      </div>
      <div class="mode-c"><div class="fields">
        <div class="fld"><label for="f-date">Preferred date</label><input id="f-date" type="date" name="date"></div>
        <div class="fld"><label for="f-time">Preferred time</label><select id="f-time" name="time"><option value="">Any time</option><option>Morning (8am–12pm)</option><option>Afternoon (12pm–4pm)</option><option>Evening (4pm–8pm)</option></select></div>
        <div class="fld full"><label for="f-tz">Your time zone</label><input id="f-tz" type="text" name="timezone" placeholder="e.g. Europe/London"></div>
      </div></div>
    </div>
    <div class="step" data-s="3"><div class="fields">
      <div class="fld"><label for="f-name">Full name *</label><input id="f-name" name="name" placeholder="Jane Smith" autocomplete="name" required></div>
      <div class="fld"><label for="f-co">Company *</label><input id="f-co" name="company" placeholder="Company Ltd" autocomplete="organization" required></div>
      <div class="fld"><label for="f-em">Business email *</label><input id="f-em" name="email" type="email" inputmode="email" placeholder="jane@company.com" autocomplete="email" required></div>
      <div class="fld"><label for="f-cn">Country</label><select id="f-cn" name="country">{co}</select></div>
      <div class="fld full"><label for="f-msg">Anything else we should know?</label><textarea id="f-msg" name="message" placeholder="Volumes, start date, systems, languages…"></textarea></div>
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    </div></div>
    <div class="step done" data-s="4"><div class="chk">{svg('<path d="m5 12 5 5 9-10"/>')}</div><h4>Request received</h4><p id="donemsg">Thank you. Our team will be in touch within one business day.</p>
      <div class="actions"><a class="btn btn-gold" href="{PAGES['home']}">Back to home <span class="ar">→</span></a><a class="btn btn-line" id="donewa" href="#" data-wa hidden>Message us on WhatsApp <span class="ar">→</span></a></div></div>
    <div class="errmsg" id="err" role="alert" aria-live="polite"></div>
    <div class="wiz-nav" id="wnav"><button type="button" class="back" id="wback" style="visibility:hidden">← Back</button><button type="button" class="btn btn-gold" id="wnext">Continue <span class="ar">→</span></button></div>
    <span id="submitlabel" hidden>Submit request </span>
  </form>
  <p class="legal-note">By submitting you agree to be contacted about your enquiry. We never share your details.</p>
</div></div></section>'''
    body += f'''<section class="sec band soft" style="padding:90px 0"><div class="wrap">{sec_head("What happens next", "Simple, <span class=\"gold\">no-pressure steps.</span>")}
<div class="mini-steps">{''.join(f'<div class="step-c rv"><h3>{t}</h3><p>{d}</p></div>' for t, d in [("We review", "A member of our team reads your request and any details you share."), ("We respond", "Within one business day, with questions or a suggested call."), ("We propose", "You receive a tailored proposal covering team, coverage, SLAs and timelines.")])}</div></div></section>'''
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Before you <span class=\"gold\">get in touch.</span>")}' + faq([
        ('How quickly will you respond?', 'We aim to respond within one business day.'),
        ('Do I need to know exactly what I need?', 'No. Share what you know. We will help you shape the scope on a consultation call.'),
        ('Can I request a proposal for several services?', 'Yes. Select every service you are interested in and add detail in the message box.'),
        ('Is my information kept confidential?', 'Yes. We use your details only to respond to your enquiry and never share them.')]) + '</div></section>'
    return page('contact', body, 'contact')

def build_404():
    t = '''<section class="error-page"><div class="wrap"><h1 class="gold">404</h1><h2 class="h2" style="margin:10px 0 18px">Page not found</h2><p class="sub" style="margin:0 auto 28px">The page you are looking for does not exist or has moved.</p><a href="index.html" class="btn btn-gold">Back to home <span class="ar">→</span></a></div></section>'''
    TITLES['404'] = 'Page not found | ELVORRA OPERATIONS'; DESCS['404'] = 'Page not found.'; PAGES['404'] = '404.html'
    return page('404', t, 'none')

# ---------------------------------------------------------------- write
def finish(s):
    s = re.sub(r'\{\{IMG:([\w-]+):(\d+)\}\}', lambda m: f'https://images.unsplash.com/{m.group(1)}?auto=format&fit=crop&w={m.group(2)}&q=75', s)
    return s

builders = {'home': build_home, 'about': build_about, 'cc': build_cc, 'ml': build_ml, 'bo': build_bo, 'crm': build_crm, 'mt': build_mt, 'contact': build_contact}
for k, fn in builders.items():
    open(os.path.join(OUT, PAGES[k]), 'w', encoding='utf-8').write(finish(fn()))
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(finish(build_404()))
print('built', len(builders) + 1, 'pages')
