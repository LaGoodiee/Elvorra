#!/usr/bin/env python3
# ELVORRA OPERATIONS — static site generator. Run: python3 build_site.py
import re, os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')
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
open(os.path.join(OUT, 'assets', 'style.css'), 'w', encoding='utf-8').write(base_css + '\n' + inner_css + '\n' + extra_css + '\n' + open(os.path.join(OUT, 'assets', 'site2.css'), encoding='utf-8').read())

# ---------------------------------------------------------------- helpers
DOMAIN = 'https://YOUR-DOMAIN.com'   # set to the live .com (no trailing slash), then rerun this script
PAGES = {
    'home': 'index.html', 'about': 'about.html', 'cc': 'call-centre-customer-support.html', 'ml': 'multilingual-24-7-support.html',
    'bo': 'back-office-administrative.html', 'crm': 'crm-case-management-qa.html', 'mt': 'managed-bpo-teams-partnerships.html',
    'ind': 'industries.html', 'contact': 'contact.html', 'privacy': 'privacy.html',
}
TITLES = {
    'home': 'ELVORRA OPERATIONS | International BPO Services, Call Centre Outsourcing & Managed Teams',
    'about': 'About ELVORRA OPERATIONS | International BPO & Managed Business Operations Partner',
    'cc': 'Call Centre & Customer Support Outsourcing | ELVORRA OPERATIONS',
    'ml': 'Multilingual Customer Service & 24/7 Customer Support | ELVORRA OPERATIONS',
    'bo': 'Back-Office Outsourcing & Data Entry Services | ELVORRA OPERATIONS',
    'crm': 'CRM & Case Management Outsourcing, Quality Assurance | ELVORRA OPERATIONS',
    'mt': 'Managed BPO Teams, Paid Pilot & Outsourcing Partnerships | ELVORRA OPERATIONS',
    'ind': 'Airline Customer Support Outsourcing & Industry BPO Solutions | ELVORRA OPERATIONS',
    'contact': 'Request a Proposal, Book a Consultation or Discuss a Partnership | ELVORRA OPERATIONS',
    'privacy': 'Privacy Policy | ELVORRA OPERATIONS',
}
DESCS = {
    'home': 'ELVORRA OPERATIONS is an international BPO and managed business operations company. Outsource call centre, customer support, back-office and CRM operations, starting with a paid pilot of 20-30 personnel.',
    'about': 'ELVORRA OPERATIONS is an international BPO, call centre and managed operations company based in Abuja, Nigeria. Not a recruitment agency: we manage the people, processes, quality and delivery.',
    'cc': 'Inbound and outbound call centre outsourcing plus email, live chat and multichannel customer support from dedicated, professionally managed teams with QA and KPI/SLA reporting.',
    'ml': '24/7 customer support and multilingual customer service in English, French, German and Spanish, delivered by shift-based teams with live supervision, workforce coordination and escalation management.',
    'bo': 'Back-office and administrative outsourcing: data entry and processing, document and records management, order processing and virtual assistance from managed teams.',
    'crm': 'CRM administration, ticket and case management outsourcing, call monitoring, quality assurance and KPI/SLA reporting from ELVORRA OPERATIONS.',
    'mt': 'Dedicated managed BPO teams, structured paid pilots starting at 20-30 personnel, and partnership options for BPO companies: subcontracting, overflow and long-term delivery partnerships.',
    'ind': 'Airline and travel customer support outsourcing, plus dedicated BPO solutions for fintech, technology and SaaS, and e-commerce businesses.',
    'contact': 'Request a proposal, book a consultation or start a partnership discussion with ELVORRA OPERATIONS. Tell us about your outsourcing needs and our team will respond.',
    'privacy': 'How ELVORRA OPERATIONS collects, uses and protects information submitted through this website.',
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

IC.update({
 'plane': svg('<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2Z"/>'),
 'credit': svg('<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>'),
 'cloud': svg('<path d="M17.5 19H9a7 7 0 1 1 6.7-9h1.8a4.5 4.5 0 1 1 0 9Z"/>'),
 'pin': svg('<path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5"/>'),
})
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- shared shell
def head(key, extra=''):
    t, d, f = TITLES[key], DESCS[key], PAGES[key]
    live = 'YOUR-DOMAIN' not in DOMAIN
    seo = ''
    if live:
        url = f'{DOMAIN}/' + ('' if key == 'home' else f)
        seo = (f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
               f'<meta property="og:image" content="{DOMAIN}/assets/og-image.png">\n<meta name="twitter:image" content="{DOMAIN}/assets/og-image.png">\n')
    card = 'summary_large_image' if live else 'summary'
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t)}</title>
<meta name="description" content="{esc(d)}">
<meta name="theme-color" content="#061229">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:locale" content="en">
<meta property="og:site_name" content="ELVORRA OPERATIONS">
<meta property="og:title" content="{esc(t)}">
<meta property="og:description" content="{esc(d)}">
<meta name="twitter:card" content="{card}">
<meta name="twitter:title" content="{esc(t)}">
<meta name="twitter:description" content="{esc(d)}">
{seo}<link rel="icon" type="image/png" sizes="64x64" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<script>try{{var s=localStorage.getItem('elvorra-theme');document.documentElement.dataset.theme=s||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress"></div>
<div class="glow" id="glow"></div>
'''

SERVICES_NAV = [
    ('cc', 'headset', 'Call Centre &amp; Customer Support', 'Inbound, outbound, email, chat'),
    ('ml', 'globe', 'Multilingual &amp; 24/7 Operations', 'EN · FR · DE · ES, shift-based'),
    ('bo', 'file', 'Back-Office &amp; Administrative', 'Data, documents, orders, VA'),
    ('crm', 'db', 'CRM, Case Management &amp; QA', 'Workflows, tickets, quality'),
    ('mt', 'users', 'Managed BPO Teams', 'Dedicated, fully managed teams'),
]

def header(active):
    cur = lambda k: ' class="cur"' if active == k else ''
    mega = ''.join(f'<a href="{PAGES[k]}"><span class="mi">{IC[ic]}</span><span><b>{t}</b><small>{s}</small></span></a>' for k, ic, t, s in SERVICES_NAV)
    mega += f'<a href="{PAGES["mt"]}#pilot"><span class="mi">{IC["star"]}</span><span><b>Paid Pilot Programme</b><small>Start with 20–30 personnel</small></span></a>'
    mega += f'<a href="{PAGES["contact"]}#proposal"><span class="mi">{IC["arrow"]}</span><span><b>Request a Proposal</b><small>Get a tailored operations plan</small></span></a>'
    mm_sub = ''.join(f'<a class="s" href="{PAGES[k]}">{t}</a>' for k, ic, t, s in SERVICES_NAV)
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
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
    <a href="{PAGES['ind']}"{cur('ind')}>Industries</a>
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
  <a href="{PAGES['ind']}">Industries</a><a href="{PAGES['mt']}#pilot">Paid Pilot Programme</a><a href="{PAGES['mt']}#partnerships">Partnerships</a><a href="{PAGES['contact']}">Contact</a>
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
      <div><h5>Company</h5><ul><li><a href="{PAGES['home']}">Home</a></li><li><a href="{PAGES['about']}">About</a></li><li><a href="{PAGES['ind']}">Industries</a></li><li><a href="{PAGES['mt']}#partnerships">Partnerships</a></li><li><a href="{PAGES['contact']}">Contact Us</a></li><li><a href="{PAGES['contact']}#consultation" data-consult>Book a Consultation</a></li></ul></div>
      <div><h5>Services</h5><ul>{svcs}<li><a href="{PAGES['mt']}#pilot">Paid Pilot Programme</a></li></ul></div>
      <div><h5>Contact</h5><ul><li><a href="mailto:" data-email data-email-text></a></li><li><a href="contact.html#whatsapp" data-wa>WhatsApp Business</a></li><li>Abuja, Nigeria</li><li>Serving clients worldwide</li></ul></div>
    </div>
  </div>
  <div class="giant" aria-hidden="true">ELVORRA</div>
  <div class="wrap"><div class="fbot"><span>© 2026 ELVORRA OPERATIONS. All rights reserved. · <a href="{PAGES['privacy']}" style="text-decoration:underline;text-underline-offset:3px">Privacy Policy</a></span><span>Global Reach · Operational Excellence · Human-Centred Service</span></div></div>
</footer>
<a class="wa" href="contact.html#whatsapp" data-wa aria-label="Chat with us on WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3Zm0 23.7c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7Zm5.9-8c-.3-.2-1.9-1-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.3-.7.1a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5.1 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5l-.6-.4Z"/></svg></a>
<script src="assets/config.js" defer></script>
<script src="assets/land.js" defer></script>
<script src="assets/main.js" defer></script>
</body>
</html>
'''

def page(key, body, active, extra_head=''):
    s = head(key, extra_head) + header(active) + body + footer()
    if 'id="globe"' not in body:
        s = s.replace('<script src="assets/land.js" defer></script>\n', '')
    return s

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

# ================================================================ SHARED v2 BLOCKS
EX_TAG = '<span class="ex-tag">Example only · not actual client results</span>'
PILOT_ITEMS = ['Dedicated operational personnel', 'Team leadership and supervision', 'Quality assurance', 'Performance monitoring', 'Operational reporting',
               'Defined service expectations', 'Agreed KPIs and SLAs', 'A structured transition into longer-term BPO contracts']

def pilot_block(sid='pilot'):
    return f'''<section class="sec" id="{sid}"><div class="wrap"><div class="pilot rv">
  <div class="pl"><span class="pill">Paid pilot programme</span>
    <div class="big">20–30</div><div class="bl">dedicated personnel</div>
    <p>ELVORRA OPERATIONS offers structured paid pilot engagements starting with 20–30 personnel, depending on your operational requirements.</p>
    <div class="path3"><span>Paid pilot</span><i>→</i><span>Review results</span><i>→</i><span>Expand into a larger contract</span></div>
    <div class="ctas" style="margin-top:22px"><a href="{PAGES['contact']}?type=pilot#proposal" class="btn btn-gold mag">Start with a Paid Pilot <span class="ar">→</span></a></div>
  </div>
  <div class="pr"><h3>Every pilot includes</h3>{checks(PILOT_ITEMS)}
    <p class="pnote">We encourage companies to begin with a paid pilot and expand into larger outsourcing arrangements following successful delivery.</p></div>
</div></div></section>'''

def capacity_block():
    return f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="cap rv">
  <div class="cn"><b class="gold">100+</b><span>screened personnel in our combined talent pool</span></div>
  <div><h3>Across different operational roles, not only customer support agents.</h3>
  <p>Our talent pool includes customer support personnel and other supporting functions. We mobilise teams according to your requirements, role mix, language needs, staffing availability and agreed onboarding timeline.</p>
  <p class="note">Language availability is confirmed against assessed personnel before each engagement.</p></div>
</div></div></section>'''

def callout(pill_t, h, text, href, label):
    return f'<section class="sec tight"><div class="wrap"><div class="callout rv"><div>{pill(pill_t)}<h3>{h}</h3><p>{text}</p></div><a href="{href}" class="btn btn-gold mag">{label} <span class="ar">→</span></a></div></div></section>'

AIR = ['Passenger customer support', 'Flight enquiries', 'Booking assistance', 'Reservation support', 'Ticketing enquiries', 'Complaints handling',
       'Flight disruption communication', 'Travel assistance', 'Email, chat and telephone support', 'Multilingual passenger support, subject to verified staffing availability']
FIN = [('chat', 'Customer enquiries', 'Clear, courteous handling of customer questions.'), ('user', 'Account-related support', 'Support for account questions, following your procedures.'),
       ('alert', 'Transaction enquiry escalation', 'Transaction questions routed and escalated to the right team.'), ('heart', 'Complaint management', 'Complaints logged, tracked and escalated to resolution.'),
       ('db', 'CRM and ticket administration', 'Records and tickets kept accurate and up to date.'), ('mail', 'Customer communication', 'Consistent, professional communication across channels.')]
SAAS = [('wrench', 'Technical customer support', 'First-line technical support with structured escalation.'), ('ticket', 'Helpdesk operations', 'Day-to-day helpdesk management and queue ownership.'),
        ('search', 'Product enquiries', 'Accurate answers about your product and plans.'), ('chat', 'Email and live chat support', 'Responsive written support on the channels customers use.'),
        ('route', 'Customer onboarding assistance', 'Helping new customers get set up and started.'), ('layers', 'Case management', 'Every case tracked from first contact to closure.')]
ECOM = [('cart', 'Order enquiries', 'Order status and delivery questions handled promptly.'), ('alert', 'Returns and complaints', 'Returns and complaints handled with clear escalation.'),
        ('mail', 'Customer communication', 'Proactive, consistent customer updates.'), ('rows', 'Order processing', 'Orders captured, validated and processed.'),
        ('file', 'Back-office administration', 'Behind-the-scenes administration that keeps orders moving.'), ('heart', 'Customer retention support', 'Contact that keeps customers informed and loyal.')]

def ind_cards():
    return f'''<div class="ind-grid">
<a href="{PAGES['ind']}#airlines" class="fcard feat rv"><span class="tagp">Priority industry</span><div class="fi">{IC['plane']}</div><h3>Airlines &amp; Travel Companies</h3><p>Passenger support, booking and reservation assistance, ticketing enquiries and disruption communication.</p><ul class="minilist"><li>Passenger &amp; flight enquiries</li><li>Booking &amp; reservation support</li><li>Complaints &amp; disruption communication</li></ul><span class="more">Explore airline support →</span></a>
<a href="{PAGES['ind']}#fintech" class="fcard rv"><div class="fi">{IC['credit']}</div><h3>Fintech &amp; Financial Technology</h3><p>Customer enquiries, account-related support, complaint management and CRM administration.</p><span class="more">Explore fintech support →</span></a>
<a href="{PAGES['ind']}#saas" class="fcard rv"><div class="fi">{IC['cloud']}</div><h3>Technology &amp; SaaS</h3><p>Technical support, helpdesk operations, onboarding assistance and case management.</p><span class="more">Explore SaaS support →</span></a>
<a href="{PAGES['ind']}#ecommerce" class="fcard rv"><div class="fi">{IC['cart']}</div><h3>E-commerce &amp; Online Business</h3><p>Order enquiries, returns, order processing, back-office administration and retention support.</p><span class="more">Explore e-commerce support →</span></a>
</div>'''

PARTNER_OPTS = [('direct', 'handshake', 'Direct BPO outsourcing contracts', 'Outsource a defined function or team directly to ELVORRA OPERATIONS.'),
    ('intl', 'globe', 'International BPO partnerships', 'Partner with us as a dependable international delivery partner.'),
    ('sub', 'layers', 'Subcontracting opportunities', 'Capacity and delivery for established BPO providers.'),
    ('overflow', 'phone-in', 'Overflow customer support operations', 'Extra capacity when your own volumes spike.'),
    ('managed', 'users', 'Managed customer service operations', 'We run a defined customer service operation for you end to end.'),
    ('backoffice', 'file', 'Back-office outsourcing partnerships', 'Dependable back-office delivery for you or your clients.'),
    ('longterm', 'star', 'Long-term business partnerships', 'Strategic, multi-year relationships built on delivery.')]
def partner_grid():
    cards = ''.join(f'<a href="{PAGES["contact"]}?type={k}#proposal" class="fcard rv"><div class="fi">{IC[ic]}</div><h3>{t}</h3><p>{d}</p><span class="more">Start a discussion →</span></a>' for k, ic, t, d in PARTNER_OPTS)
    return f'<div class="grid-3">{cards}</div>'

def kpi_sample():
    rows = [('First response time (voice)', '≤ 60 sec', '48 sec'), ('Service level: contacts answered in target', '80%', '83%'), ('Customer satisfaction (CSAT)', '≥ 90%', '92%'),
            ('QA score', '≥ 90%', '91%'), ('First contact resolution', '≥ 75%', '78%'), ('Schedule adherence', '≥ 95%', '96%')]
    r = '<div class="krow h"><span>Metric</span><span>Target</span><span>Sample</span></div>' + ''.join(f'<div class="krow"><span>{m}</span><span>{t}</span><b class="gold">{v}</b></div>' for m, t, v in rows)
    return f'''<section class="sec"><div class="wrap">{sec_head("Sample reporting", "What your <span class=\"gold\">KPI &amp; SLA report</span> can look like.", "Reporting is agreed with each client. This is an anonymised example layout.")}
<div class="vis-card rv" style="max-width:860px;margin:0 auto"><div class="lt"><span>Sample monthly KPI report</span>{EX_TAG}</div><div class="ktable">{r}</div>
<p class="note">Illustrative figures only. Real targets, metrics and reporting frequency are agreed with each client.</p></div></div></section>'''

# ================================================================ HOME
def build_home():
    seg = v3seg('<!-- HERO -->', '<!-- MODELS -->')
    def rep(old, new, cnt=1):
        nonlocal seg
        assert seg.count(old) >= 1, old[:80]
        seg = seg.replace(old, new) if cnt == 0 else seg.replace(old, new, cnt)
    rep('We run call centre, customer support, back-office and CRM operations for businesses worldwide, with dedicated teams, structured processes and accountable management.',
        'Outsource entire business functions to ELVORRA OPERATIONS. We manage the people, processes, quality and service delivery behind your call centre, customer support, back-office and CRM operations.')
    rep('href="#proposal" class="btn btn-line mag">Book a Consultation', f'href="{PAGES["contact"]}#consultation" data-consult class="btn btn-line mag">Book a Consultation')
    rep('href="#proposal"', f'href="{PAGES["contact"]}#proposal"', 0)
    for n in [f'<a href="{PAGES["about"]}" class="tc rv">', f'<a href="{PAGES["ml"]}" class="tc rv">']:
        seg = seg.replace('<a href="#" class="tc rv">', n, 1)
    rep('<a href="#" class="tc acc rv">', f'<a href="{PAGES["about"]}#approach" class="tc acc rv">')
    for k in ('cc', 'ml', 'bo', 'crm'):
        seg = seg.replace('<a href="#" class="sc rv">', f'<a href="{PAGES[k]}" class="sc rv">', 1)
    rep('<a href="#" class="btn btn-gold mag" style="align-self:flex-start">Build your team', f'<a href="{PAGES["mt"]}" class="btn btn-gold mag" style="align-self:flex-start">Build your team')
    for w in ('2000',): seg = seg.replace(f':{w}}}}}', ':1600}}')
    rep('alt="Customer support professionals with headsets in a bright office">', 'alt="Customer support professionals with headsets in a bright office" fetchpriority="high" onerror="this.style.visibility=\'hidden\'">')
    # static, accurate counters (no animated zero values)
    rep('<div class="stat"><strong><span class="gold" data-count="24">0</span><span class="gold">/7</span></strong><span>Shift-based coverage model</span></div>',
        '<div class="stat"><strong><span class="gold">24</span><span class="gold">/7</span></strong><span>Shift-based coverage model</span></div>')
    rep('<div class="stat"><strong><span data-count="4">0</span>+</strong><span>Core support languages</span></div>',
        '<div class="stat"><strong>4</strong><span>Languages: EN · FR · DE · ES, confirmed against assessed personnel</span></div>')
    rep('<div class="stat"><strong><span data-count="9">0</span></strong><span>Integrated service lines</span></div>',
        '<div class="stat"><strong>9</strong><span>Integrated service lines</span></div>')
    rep('<div class="stat"><strong><span data-count="1">0</span></strong><span>Accountable lead per client</span></div>',
        '<div class="stat"><strong>100+</strong><span>Screened personnel in our combined talent pool</span></div>')
    rep('ELVORRA is the operations partner', 'ELVORRA OPERATIONS is the operations partner')
    rep('>Why ELVORRA<', '>Why ELVORRA OPERATIONS<')
    rep('ELVORRA managed operations', 'ELVORRA OPERATIONS managed operations')
    rep('We recruit, train and onboard your dedicated team', 'We mobilise, train and onboard your dedicated team')
    rep('Every agent is screened, language-assessed where required and trained on your products and tone of voice.',
        'Personnel are screened and, where languages are required, assessed before deployment, then trained on your products and tone of voice.')
    rep('Confidentiality agreements, controlled system access and documented processes protect your customers’ information.',
        'Confidentiality commitments, controlled system access and documented processes help protect your customers’ information.')
    rep('recruited, deployed, supervised and reported on by ELVORRA.', 'assembled, deployed, supervised and reported on by ELVORRA OPERATIONS.')
    rep('Nine integrated service lines under one accountable partner. Start with one, then scale into the rest.',
        'Nine integrated service lines under one accountable partner, from inbound and outbound support to back-office, CRM and managed teams.')
    bar = f'<a class="pilot-bar" href="#pilot"><b>Paid pilot programme: start with 20–30 dedicated personnel</b><span>See what’s included →</span></a>\n\n<!-- TRIO -->'
    rep('<!-- TRIO -->', bar)
    ind = f'<section class="sec" id="industries"><div class="wrap">{sec_head("Industry solutions", "Built for <span class=\"gold\">your industry.</span>", "Dedicated support for airlines and travel companies, fintech, technology and SaaS, and e-commerce businesses.")}{ind_cards()}</div></section>\n\n<!-- GLOBAL -->'
    rep('<!-- GLOBAL -->', ind)
    part = f'''<section class="sec"><div class="wrap">{sec_head("Partnerships", "Direct clients and <span class=\"gold\">BPO partners</span> welcome.", "Direct outsourcing contracts, subcontracting, overflow support and long-term international partnerships.")}
<div class="ctas rv" style="justify-content:center"><a href="{PAGES['mt']}#partnerships" class="btn btn-line mag" style="color:var(--text);border-color:var(--border2)">See partnership options <span class="ar" style="background:var(--text);color:var(--bg)">→</span></a><a href="{PAGES['contact']}?type=intl#proposal" class="btn btn-gold mag">Request a partnership discussion <span class="ar">→</span></a></div></div></section>'''
    cta = f'''<section class="prop" id="start"><div class="wrap"><div class="cta-band rv">
  <div>{pill('Request a proposal')}<h2>Ready to outsource with <span class="gold">confidence?</span></h2><p>Tell us what you need in a few quick steps, or book a consultation to talk it through.</p></div>
  <div class="ctas"><a href="{PAGES['contact']}#proposal" class="btn btn-gold mag">Request a Proposal <span class="ar">→</span></a><a href="{PAGES['contact']}#consultation" data-consult class="btn btn-line mag">Book a Consultation <span class="ar">→</span></a></div>
</div></div></section>'''
    ld = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"ELVORRA OPERATIONS","description":"International BPO, call centre and managed business operations company.","address":{"@type":"PostalAddress","addressLocality":"Abuja","addressCountry":"NG"},"email":"elvoraoperation@gmail.com"}</script>\n'''
    return page('home', seg + pilot_block() + capacity_block() + part + cta, 'home', ld)

# ================================================================ ABOUT
def build_about():
    svc = [('headset', 'Call Centre Outsourcing', 'cc'), ('chat', 'Customer Support Outsourcing', 'cc'), ('globe', 'Multilingual Customer Support', 'ml'), ('clock', '24/7 Support Operations', 'ml'),
           ('shield', 'Quality Assurance & Performance', 'crm'), ('file', 'Back-Office & Administrative', 'bo'), ('db', 'CRM & Case Management', 'crm'), ('users', 'Managed BPO Teams', 'mt'), ('calendar', 'Virtual Assistance', 'bo')]
    svc_html = '<div class="grid-3">' + ''.join(f'<a href="{PAGES[k]}" class="fcard rv"><span class="fn">{i:02d}</span><div class="fi">{IC[ic]}</div><h3>{t}</h3><p style="color:var(--gold3);font-weight:600;font-size:14px">Explore →</p></a>' for i, (ic, t, k) in enumerate(svc, 1)) + '</div>'
    body = page_hero('About', 'About ELVORRA OPERATIONS', 'A managed operations partner, <em class="gold">built for global business.</em>',
                     'ELVORRA OPERATIONS is an international Business Process Outsourcing, call centre and managed business operations company, headquartered in Abuja, Nigeria. You can outsource entire business functions to us while we manage the people, processes, quality and service delivery.',
                     'table', 'Team collaborating around a table with laptops', [('Headquartered in', 'Abuja, Nigeria'), ('Serving', 'Businesses worldwide')])
    body += split('Who we are', 'We run the operations <span class="gold">behind your customers.</span>',
        ['We partner with companies to manage their customer interactions, streamline business processes, improve operational efficiency and deliver exceptional customer experiences through dedicated teams, technology and professional operational management.',
         'Our goal is to be a trusted, dependable international operations partner for businesses that need reliable customer support, call centre operations and complete business process management.'],
        ['Managed outsourcing solutions and dedicated operational teams', 'Customer support, back-office services, CRM administration and quality assurance', 'Operational supervision and workforce coordination', 'Built to scale as your volumes and markets grow'],
        'team', 'Diverse business team collaborating', ('Managed People. Structured Operations.', 'Scalable Business Support.'))
    body += f'''<section class="sec band soft" style="padding:100px 0"><div class="wrap">{sec_head('What we are, and what we are not', 'A partner that <span class="gold">owns the outcome.</span>')}
<div class="vs vs-wrap"><div class="vs-col rv"><h4>✕ &nbsp;What we are not</h4><ul><li><i>✕</i>A recruitment agency</li><li><i>✕</i>A supplier of manpower</li><li><i>✕</i>Just a call centre</li><li><i>✕</i>Agents handed over for you to manage</li></ul></div>
<div class="vs-col us rv"><h4>✦ &nbsp;What we are</h4><ul><li><i>✓</i>An international BPO and managed operations company</li><li><i>✓</i>Dedicated teams with supervision and quality assurance</li><li><i>✓</i>Accountable for people, processes, quality and service delivery</li><li><i>✓</i>A partner for entire business functions</li></ul></div></div></div></section>'''
    body += f'''<section class="sec" id="approach"><div class="wrap">{sec_head('Our brand promise', 'Global Reach. Operational Excellence. <span class="gold">Human-Centred Service.</span>')}
{fcards([('globe', 'Global Reach', 'We support businesses in the United States, United Kingdom, Canada, Germany, the Netherlands, wider Europe, the Middle East, Asia and other international markets, with shift-based coverage across time zones.'),
         ('target', 'Operational Excellence', 'Defined processes, live supervision, quality assurance and KPI and SLA reporting on every engagement, so performance is measured, not assumed.'),
         ('heart', 'Human-Centred Service', 'Behind every interaction is a trained person. We invest in coaching and clear communication so your customers feel heard and helped.')], 3, True)}
</div></section>'''
    body += capacity_block()
    body += f'<section class="sec band soft" style="padding:100px 0"><div class="wrap">{sec_head("What we do", "Nine service lines, <span class=\"gold\">one accountable partner.</span>", "From the first customer call to the last line of back-office processing, we design, staff, supervise and continuously improve the operations you entrust to us.")}{svc_html}</div></section>'
    # trust
    trust = [('route', 'Operational delivery model', 'A structured model from discovery to go-live and continuous improvement, with one accountable lead for your account.'),
        ('badge', 'Client onboarding', 'A defined onboarding workflow covering scoping, team mobilisation, training, systems access and a supervised go-live.'),
        ('users', 'Supervision &amp; accountability', 'Team leaders and supervisors are named and accountable for attendance, quality and results on every shift.'),
        ('shield', 'Quality assurance', 'Call, chat and email monitoring against agreed scorecards, with coaching and training recommendations.'),
        ('eye', 'Performance monitoring', 'Live queue and performance monitoring, so issues are spotted and addressed quickly.'),
        ('chart', 'KPI &amp; SLA reporting', 'Agreed KPIs and SLAs, reported to you on a regular schedule.'),
        ('lock', 'Confidentiality &amp; data protection', 'Confidentiality commitments, controlled access to systems and data, and documented procedures for handling customer information.'),
        ('alert', 'Business continuity &amp; escalation', 'Agreed escalation paths, shift cover planning and clear communication when issues arise.'),
        ('mail', 'Client communication', 'Named contacts, regular reviews and reporting arrangements agreed up front.')]
    body += f'<section class="sec" id="trust"><div class="wrap">{sec_head("Operational trust", "How we run <span class=\"gold\">dependable operations.</span>", "The practices international decision-makers ask about, in one place.")}{fcards(trust, 3, True)}</div></section>'
    body += f'''<section class="sec band navy" id="management" style="padding:100px 0"><div class="wrap">{sec_head('Management structure', 'Clear roles. <span class="gold">Clear accountability.</span>', 'Every managed operation has defined layers of responsibility.')}
{steps([('Leadership &amp; account management', 'Senior oversight of your engagement, commercial terms and escalations.'), ('Operations management', 'Day-to-day running of the operation, scheduling and service delivery.'), ('Team leaders &amp; supervisors', 'Coaching, live supervision and accountability for each shift.'), ('QA specialists &amp; delivery teams', 'Quality monitoring and the dedicated personnel who serve your customers.')])}
</div></section>'''
    ob = steps([('1 · Discovery', 'Understand your goals, channels, volumes, languages and systems.'), ('2 · Scoping &amp; agreement', 'Agree scope, KPIs, SLAs, escalation paths and commercial terms.'), ('3 · Team mobilisation', 'Mobilise the team based on role mix, languages and availability.'),
                ('4 · Training &amp; access', 'Train on your products, scripts and systems, with controlled access.'), ('5 · Supervised go-live', 'Launch under close supervision with QA from day one.'), ('6 · Review &amp; scale', 'Review results against KPIs, then expand as agreed.')]).replace('class="steps"', 'class="steps n3"')
    body += f'<section class="sec" id="onboarding"><div class="wrap">{sec_head("Client onboarding process", "From first call to <span class=\"gold\">supervised go-live.</span>")}<div class="rv" style="text-align:center;margin:-10px 0 24px">{EX_TAG}</div>{ob}<p class="note rv" style="text-align:center;margin-top:18px;color:var(--muted);font-size:14px">An example workflow. Stages and timelines are tailored to each engagement.</p></div></section>'
    body += f'''<section class="sec"><div class="wrap split"><div class="rv">{pill('Where we serve')}<h2 class="h2">Based in Abuja. <span class="gold">Built for the world.</span></h2>
<p>Our operations hub in Abuja (GMT+1) shares UK and European business hours and overlaps with US mornings. Shift-based teams extend coverage across other time zones.</p>
{checks(['United States and Canada', 'United Kingdom, Germany, the Netherlands and wider Europe', 'Middle East and Asia', 'Other international markets'])}</div>
<div class="rv">{GCARD}</div></div></section>'''
    body += cta_band()
    return page('about', body, 'about')

# ================================================================ CALL CENTRE
def build_cc():
    body = page_hero('Call Centre & Customer Support', 'Call Centre & Customer Support Outsourcing', 'Every customer conversation, <em class="gold">professionally managed.</em>',
        'Dedicated inbound and outbound call centre teams and multichannel customer support, supervised and quality-assured by ELVORRA OPERATIONS.',
        'laptop', 'Support agent wearing headphones working at a laptop', [('Channels', 'Voice · Email · Chat'), ('Managed by', 'Dedicated team leaders')])
    body += f'<section class="sec" id="call-centre"><div class="wrap">{sec_head("Call Centre Outsourcing", "Voice operations that <span class=\"gold\">sound like your brand.</span>", "Dedicated, professionally managed call centre teams for every kind of customer conversation.")}'
    body += fcards([('phone-in', 'Inbound customer support', 'Professional handling of incoming customer calls with trained agents who know your products and tone of voice.'),
        ('phone-out', 'Outbound customer support', 'Structured outbound campaigns for follow-ups, surveys, reminders and customer outreach.'),
        ('alert', 'Complaints & escalation management', 'Calm, accurate handling of customer enquiries and complaints, with clear escalation paths to the right people.'),
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
        ('smile', 'Customer success support', 'Proactive support that helps customers get value from your product or service and stay with your brand.'),
        ('ticket', 'Helpdesk & ticket management', 'Every request logged, prioritised, tracked and closed, with nothing falling through the cracks.')], 3, True)
    body += '</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("An operation in motion", "See how a <span class=\"gold\">managed desk</span> looks.", "An illustration of the live view, case tracking and shift coverage that sit behind every ELVORRA OPERATIONS engagement.")}{LIVE_ROW.replace(" mt", " mt")}</div></section>'
    body += callout('Airline & travel', 'Airline and travel customer support', 'Passenger enquiries and assistance, booking and reservation support, ticketing enquiries and complaints handling across email, chat and telephone.', PAGES['ind'] + '#airlines', 'Explore airline support')
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
        ('Can we start small and grow?', 'Yes. We offer structured paid pilot engagements starting with 20–30 personnel, then expand into larger arrangements following successful delivery. See the paid pilot programme on the Managed BPO Teams page.'),
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
    body += '<div class="rv" style="margin-top:16px"><div class="fcard dark"><div class="fi">' + IC['globe'] + '</div><h3>More languages on request</h3><p>We can consider further languages based on your requirements and verified personnel availability. Language availability for every engagement is confirmed against assessed personnel before we agree your service.</p></div></div></div></section>'
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
        ('Which languages do you support?', 'Our advertised languages are English, French, German and Spanish. We confirm language availability against assessed personnel before agreeing each engagement and do not promise coverage we cannot verify. Other languages are considered on request.'),
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
        ['Confidentiality commitments for team members', 'Controlled access to your systems and data', 'Documented procedures for every process', 'Quality checks and error tracking'],
        'charts', 'Two professionals reviewing charts on a laptop', ('Documented & checked', 'Processes you can rely on'), rev=True)
    body += f'<section class="sec band navy" style="padding:100px 0"><div class="wrap">{sec_head("Getting started", "Simple to start, <span class=\"gold\">easy to scale.</span>")}{steps([("Define", "We agree the tasks, volumes, turnaround times and quality standards."), ("Document", "Your processes are written down so work is done consistently."), ("Deploy", "A managed team begins, with supervision and quality checks."), ("Review", "Regular reports let us improve accuracy and speed together.")])}</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">back-office &amp; admin.</span>")}' + faq([
        ('What kinds of back-office work can you take on?', 'Data entry and processing, document and records management, order processing, administrative assistance and wider business process support.'),
        ('Can you work inside our own systems?', 'Yes. Our teams can work in your CRM and business systems under controlled access, following your procedures.'),
        ('How do you keep information secure?', 'We use confidentiality commitments, controlled system access and documented procedures. We will go through your specific requirements with you.'),
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
    body += f'<section class="sec band soft" style="padding:100px 0"><div class="wrap">{sec_head("In practice", "From first contact to <span class=\"gold\">measured outcome.</span>", "Illustrations of case tracking and a quality scorecard.")}<div class="grid-2"><div class="vis-card rv"><div class="lt"><span>Case pipeline</span><span class="live">Live</span></div>{pc}<p class="note">Example only. Anonymised sample, not actual client results.</p></div><div class="vis-card rv" data-score><div class="lt"><span>QA scorecard</span><span>Sample interaction review</span></div>{sc}<p class="note">Example only. Anonymised sample, not actual client results.</p></div></div></div></section>'
    body += kpi_sample()
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
def models_block():
    return f'''<section class="frame models-s" id="engagement"><div class="wrap">
<div class="center rv">{pill('Engagement models')}<h2 class="h2" style="margin:18px auto 14px">Start with a paid pilot. <span class="gold">Scale with confidence.</span></h2><p class="sub">Every model includes supervision, quality assurance and performance reporting.</p></div>
<div class="models" style="padding-bottom:70px">
<div class="model feat rv"><span class="badge">Recommended start</span><span class="mt">Prove it first</span><h3>Paid Pilot Programme</h3><p>A structured paid pilot starting with 20–30 personnel, depending on your operational requirements.</p><ul><li>Dedicated personnel &amp; team leadership</li><li>Agreed KPIs and SLAs</li><li>Structured transition into longer-term contracts</li></ul></div>
<div class="model rv"><span class="mt">Your extended operation</span><h3>Dedicated Team</h3><p>A fully managed team working exclusively on your brand, systems and customers.</p><ul><li>Dedicated personnel &amp; team leader</li><li>QA, KPI &amp; SLA reporting</li><li>Flexible terms agreed in your proposal</li></ul></div>
<div class="model rv"><span class="mt">Outcome-based</span><h3>Managed Service</h3><p>We take full ownership of a defined function: support, CRM or back-office.</p><ul><li>End-to-end process ownership</li><li>Agreed service levels</li><li>Continuous improvement plan</li></ul></div>
</div></div></section>'''

def build_mt():
    body = page_hero('Managed BPO Teams & Partnerships', 'Managed BPO Teams, Paid Pilot & Partnerships', 'Start with a paid pilot. <em class="gold">Scale into a managed team.</em>',
        'Dedicated personnel, team leaders, QA specialists and operational management, deployed and managed by us, plus partnership options for BPO companies and international businesses.',
        'meeting', 'Business team meeting in a modern office', [('Paid pilot', 'From 20–30 personnel'), ('Partnerships', 'Direct · BPO · Long-term')])
    body += pilot_block()
    body += models_block()
    body += f'<section class="sec" id="managed-teams" style="padding-top:0"><div class="wrap">{sec_head("Managed BPO Teams & Workforce Solutions", "Everything a team needs. <span class=\"gold\">Managed for you.</span>", "We assemble, deploy and manage the whole team so you get results, not management overhead.")}'
    body += fcards([('headset', 'Dedicated customer support teams', 'Personnel working exclusively on your brand, products and customers.'), ('users', 'Team leaders & supervisors', 'Named leaders who supervise, coach and are accountable for performance.'),
        ('shield', 'Quality assurance specialists', 'Specialists who monitor and improve quality on your account.'), ('cog', 'Operational supervision', 'Day-to-day management of the operation, from scheduling to escalations.'),
        ('route', 'Workforce coordination & deployment', 'We coordinate people, shifts and deployment into your managed operation. This supports your team and is not a stand-alone recruitment service.'), ('chart', 'Performance monitoring & reporting', 'Regular reporting against agreed KPIs and SLAs.')], 3, True)
    body += '</div></section>'
    body += f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="team rv">
  <div class="tp"><span class="pill" style="background:rgba(255,255,255,.08);color:rgba(255,255,255,.8);border-color:rgba(255,255,255,.18);align-self:flex-start">How a managed team is structured</span>
  <h3>One accountable structure, <span class="gold">from team to manager.</span></h3>
  <p>Every managed team has clear roles and reporting lines, so there is always someone responsible for quality, attendance and results.</p>
  <div class="chips"><span>Dedicated personnel</span><span>Team leaders</span><span>QA specialists</span><span>Operations manager</span></div>
  <a href="{PAGES['contact']}?type=pilot#proposal" class="btn btn-gold mag" style="align-self:flex-start">Build your team <span class="ar">→</span></a></div>
  <div class="pic">{pic('table', 1200, 'Team working together at a table with laptops')}
  <div class="org"><div class="node top">Operations Manager</div><div class="lvl"><div class="node"><i></i>Team Leader</div><div class="node"><i></i>QA Specialist</div></div><div class="agents"><i></i><i></i><i></i><i></i><i></i></div></div></div>
</div></div></section>'''
    body += capacity_block()
    body += f'<section class="sec band soft" id="partnerships" style="padding:100px 0"><div class="wrap">{sec_head("International partnership enquiries", "Direct clients and <span class=\"gold\">BPO partners</span> welcome.", "Choose the discussion you would like to start. Each option opens our enquiry form with it pre-selected.")}{partner_grid()}'
    body += f'<div class="ctas rv" style="justify-content:center;margin-top:34px"><a href="{PAGES["contact"]}?type=intl#proposal" class="btn btn-gold mag">Request a partnership discussion <span class="ar">→</span></a></div></div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("Partnership pathway", "From introduction to <span class=\"gold\">long-term delivery.</span>")}{steps([("Introductory call", "30 minutes on your goals and requirements."), ("Confidentiality &amp; scoping", "We handle your information with care and define the operation."), ("Tailored proposal", "Staffing, SLAs, timelines and commercial terms."), ("Pilot or go-live", "Then ongoing reviews and continuous improvement.")])}</div></section>'
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">pilots, teams &amp; partnerships.</span>")}' + faq([
        ('How large is the paid pilot?', 'ELVORRA OPERATIONS offers structured paid pilot engagements starting with 20–30 personnel, depending on your operational requirements.'),
        ('What happens after the pilot?', 'The pilot includes agreed KPIs and SLAs and a structured transition into longer-term BPO contracts. Following successful delivery, you can expand into larger outsourcing arrangements.'),
        ('What is a managed BPO team?', 'A team of dedicated personnel, team leaders, QA specialists and operational management that we mobilise, supervise and report on for your business.'),
        ('Are you a recruitment agency?', 'No. ELVORRA OPERATIONS is a managed operations partner. We do not simply supply manpower: we manage the people, processes, quality and service delivery.'),
        ('How quickly can a team be mobilised?', 'We mobilise teams according to your requirements, role mix, language needs, staffing availability and an agreed onboarding timeline.'),
        ('Do you partner with other BPO companies?', 'Yes. We welcome subcontracting, overflow support and long-term delivery partnerships with established BPO companies.')]) + '</div></section>'
    body += cta_band()
    return page('mt', body, 'services')

# ================================================================ INDUSTRIES
def build_ind():
    body = page_hero('Industries', 'Industry solutions', 'Customer support built for <em class="gold">your industry.</em>',
        'Dedicated support for airlines and travel companies, fintech, technology and SaaS, and e-commerce businesses, run by managed teams with supervision and quality assurance.',
        'phonedesk', 'Support professional on the phone at a desk', [('Priority industry', 'Airlines & travel'), ('Channels', 'Email · Chat · Phone')], ctas=False)
    body = body.replace('</div></section>', f'<div class="chipnav rv"><a href="#airlines">Airlines &amp; Travel</a><a href="#fintech">Fintech</a><a href="#saas">Technology &amp; SaaS</a><a href="#ecommerce">E-commerce</a></div></div></section>', 1) if False else body
    body += f'''<section class="sec" id="airlines"><div class="wrap split"><div class="rv">{pill('A · Airlines and travel companies')}<h2 class="h2">Passenger support, <span class="gold">handled with care.</span></h2>
<p>Passengers contact airlines and travel companies at stressful moments. Our managed teams handle enquiries, bookings and complaints calmly and clearly, through the channels your passengers use.</p>
{checks(AIR)}
<div class="ctas" style="margin-top:22px"><a href="{PAGES['contact']}?service=Airline#proposal" class="btn btn-gold mag">Discuss airline &amp; travel support <span class="ar">→</span></a></div></div>
<div class="media rv">{pic('support', 1000, 'Customer support professionals with headsets in a bright office')}<div class="over"><b>Email, chat and telephone</b><span>One managed passenger support team</span></div></div></div></section>'''
    def ind_sec(sid, label, h2, sub, items, svc, band=False):
        st = ' band soft' if band else ''
        sty = ' style="padding:100px 0"' if band else ''
        return f'<section class="sec{st}" id="{sid}"{sty}><div class="wrap">{sec_head(label, h2, sub)}{fcards(items, 3, True)}<div class="ctas rv" style="justify-content:center;margin-top:30px"><a href="{PAGES["contact"]}?service={svc}#proposal" class="btn btn-gold mag">Request a proposal <span class="ar">→</span></a></div></div></section>'
    body += ind_sec('fintech', 'B · Fintech and financial technology', 'Reliable support for <span class="gold">financial services.</span>', 'Customer-facing support and administration for fintech teams.', FIN, 'CRM', True)
    body += ind_sec('saas', 'C · Technology and SaaS companies', 'Helpdesk and product support that <span class="gold">scales with you.</span>', 'Technical and customer support for technology and software businesses.', SAAS, 'Customer', False)
    body += ind_sec('ecommerce', 'D · E-commerce and online businesses', 'Keep customers happy <span class="gold">from order to delivery.</span>', 'Customer support and back-office operations for online retailers.', ECOM, 'Back-office', True)
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Questions about <span class=\"gold\">industry support.</span>")}' + faq([
        ('Do you support airlines and travel companies?', 'Yes. This is a priority area for us. We support passenger enquiries, booking and reservation assistance, ticketing enquiries, complaints handling and flight disruption communication across email, chat and telephone.'),
        ('Can you provide multilingual passenger support?', 'Our advertised languages are English, French, German and Spanish. Multilingual support is subject to verified staffing availability, and we confirm language coverage against assessed personnel before agreeing a service.'),
        ('Will your team work in our booking or CRM systems?', 'Yes. Our teams work in your systems under controlled access and follow your documented procedures.'),
        ('Can we start with a pilot?', 'Yes. We offer structured paid pilots starting with 20–30 personnel, then expand following successful delivery.')]) + '</div></section>'
    body += cta_band()
    return page('ind', body, 'ind')

# ================================================================ CONTACT
def build_contact():
    def opt(x, key=''):
        k = f' data-key="{key}"' if key else ''
        return f'<span class="opt" role="button" tabindex="0"{k}>{x}</span>'
    types = [('direct', 'Direct BPO outsourcing contract'), ('pilot', 'Paid pilot programme (20–30 personnel)'), ('intl', 'International BPO partnership'), ('sub', 'Subcontracting opportunity'),
             ('overflow', 'Overflow customer support'), ('managed', 'Managed customer service operations'), ('backoffice', 'Back-office outsourcing partnership'), ('longterm', 'Long-term business partnership')]
    t_html = ''.join(opt(t, k) for k, t in types)
    svcs = ['Inbound customer support', 'Outbound customer support', 'Call centre outsourcing', '24/7 operations', 'Email &amp; live chat support', 'Multilingual support', 'Airline &amp; travel support', 'Back-office &amp; admin',
            'Data entry &amp; processing', 'CRM &amp; case management', 'Quality assurance', 'Customer success support', 'Managed BPO team', 'Virtual assistance']
    s_html = ''.join(opt(x) for x in svcs)
    countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 'Netherlands', 'France', 'Spain', 'Other Europe', 'Middle East', 'Asia', 'Africa', 'Other']
    co = '<option value="">Select country</option>' + ''.join(f'<option>{c}</option>' for c in countries)
    body = page_hero('Contact', 'Contact us', 'Request a proposal, book a consultation or <em class="gold">start a partnership discussion.</em>',
        'Tell us about your business and what you want to outsource. We will review your request and come back to you with next steps.', ctas=False)
    body += f'''<section class="sec" style="padding-top:60px" id="start"><div class="wrap contact-grid">
<aside class="cside rv" aria-label="Contact details">
  <a class="cc" href="mailto:" data-email><span class="ic">{IC['mail']}</span><div><small>BUSINESS EMAIL</small><b data-email-text></b></div></a>
  <a class="cc wsp" id="whatsapp" href="#" data-wa><span class="ic">{IC['chat']}</span><div><small>WHATSAPP BUSINESS</small><b>Chat with our team</b></div></a>
  <a class="cc" href="#consultation" data-consult><span class="ic">{IC['calendar']}</span><div><small>BOOK A CONSULTATION</small><b>Discovery call</b></div></a>
  <div class="cc"><span class="ic">{IC['building']}</span><div><small>HEADQUARTERS</small><b>Abuja, Nigeria</b></div></div>
  <div class="cc"><span class="ic">{IC['globe']}</span><div><small>SERVING</small><b>Clients worldwide</b></div></div>
</aside>
<div class="formcard rv" id="lead" data-mode="proposal">
  <div class="mode" role="group" aria-label="Choose request type"><button type="button" class="on" data-mode="proposal" id="proposal">Request a Proposal</button><button type="button" data-mode="consult" id="consultation">Book a Consultation</button></div>
  <div class="wiz-top"><b id="wtitle">What do you need?</b><span id="wcount">Step 1 of 3</span></div>
  <div class="wbar"><i id="wbar"></i></div>
  <form id="leadform" novalidate autocomplete="on">
    <div class="step on" data-s="1"><p class="hint" id="hint">Choose your enquiry type, then select the services you are interested in.</p>
      <span class="lbl" style="margin-top:0">Enquiry type *</span><div class="opts" data-single data-name="enquiryType">{t_html}</div>
      <span class="lbl">Services *</span><div class="opts" data-multi data-name="services">{s_html}</div></div>
    <div class="step" data-s="2">
      <div class="mode-p">
        <span class="lbl" style="margin-top:0">Estimated team size</span><div class="opts" data-single data-name="teamSize">{opt('1–10')}{opt('20–30 (pilot)')}{opt('30–50')}{opt('50+')}{opt('Not sure')}</div>
        <span class="lbl">Operational coverage</span><div class="opts" data-single data-name="coverage">{opt('Business hours')}{opt('Extended hours')}{opt('24/7')}</div>
        <span class="lbl">Languages required</span><div class="opts" data-multi data-name="languages">{opt('English')}{opt('French')}{opt('German')}{opt('Spanish')}{opt('Other')}</div>
        <div class="fields" style="margin-top:16px">
          <div class="fld"><label for="f-start">Preferred start date</label><input id="f-start" type="date" name="startDate"></div>
          <div class="fld"><label for="f-hours">Preferred working hours</label><input id="f-hours" type="text" name="hours" maxlength="80" placeholder="e.g. 09:00–18:00 your time"></div>
        </div>
      </div>
      <div class="mode-c"><div class="fields">
        <div class="fld"><label for="f-date">Preferred date</label><input id="f-date" type="date" name="date"></div>
        <div class="fld"><label for="f-time">Preferred time</label><select id="f-time" name="time"><option value="">Any time</option><option>Morning (8am–12pm)</option><option>Afternoon (12pm–4pm)</option><option>Evening (4pm–8pm)</option></select></div>
      </div></div>
      <div class="fields" style="margin-top:12px"><div class="fld full"><label for="f-tz">Your time zone</label><input id="f-tz" type="text" name="timezone" maxlength="60" placeholder="e.g. Europe/London"></div></div>
    </div>
    <div class="step" data-s="3"><div class="fields">
      <div class="fld"><label for="f-name">Full name *</label><input id="f-name" name="name" maxlength="100" placeholder="Jane Smith" autocomplete="name" required></div>
      <div class="fld"><label for="f-job">Job title <span class="opt-l">(optional)</span></label><input id="f-job" name="jobTitle" maxlength="100" placeholder="Operations Director" autocomplete="organization-title"></div>
      <div class="fld"><label for="f-co">Company *</label><input id="f-co" name="company" maxlength="120" placeholder="Company Ltd" autocomplete="organization" required></div>
      <div class="fld"><label for="f-em">Business email *</label><input id="f-em" name="email" type="email" maxlength="120" inputmode="email" placeholder="jane@company.com" autocomplete="email" required></div>
      <div class="fld"><label for="f-ph">Contact number <span class="opt-l">(optional)</span></label><input id="f-ph" name="phone" type="tel" maxlength="30" inputmode="tel" placeholder="+1 555 000 0000" autocomplete="tel"></div>
      <div class="fld"><label for="f-cn">Country *</label><select id="f-cn" name="country" required>{co}</select></div>
      <div class="fld full"><label for="f-msg">Additional project information</label><textarea id="f-msg" name="message" maxlength="2000" placeholder="Volumes, systems, timelines, anything else we should know…"></textarea></div>
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    </div>
    <label class="consent"><input type="checkbox" name="consent" id="f-consent"><span>I agree to ELVORRA OPERATIONS using these details to respond to my enquiry, as described in the <a href="{PAGES['privacy']}" target="_blank" rel="noopener">Privacy Policy</a>. *</span></label></div>
    <div class="step done" data-s="4"><div class="chk">{svg('<path d="m5 12 5 5 9-10"/>')}</div><h4>Request received</h4><p id="donemsg">Thank you. Our team will be in touch shortly.</p>
      <div class="actions"><a class="btn btn-gold" href="{PAGES['home']}">Back to home <span class="ar">→</span></a><a class="btn btn-line" id="donewa" href="#" data-wa hidden>Message us on WhatsApp <span class="ar">→</span></a></div></div>
    <div class="errmsg" id="err" role="alert" aria-live="polite"></div>
    <div class="wiz-nav" id="wnav"><button type="button" class="back" id="wback" style="visibility:hidden">← Back</button><button type="button" class="btn btn-gold" id="wnext">Continue <span class="ar">→</span></button></div>
    <span id="submitlabel" hidden>Submit request </span>
  </form>
  <p class="legal-note">Your details are sent securely to our business inbox and used only to respond to your enquiry. See our <a href="{PAGES['privacy']}" style="text-decoration:underline">Privacy Policy</a>.</p>
</div></div></section>'''
    body += f'''<section class="sec band soft" style="padding:90px 0"><div class="wrap">{sec_head("What happens next", "Simple, <span class=\"gold\">no-pressure steps.</span>")}
<div class="mini-steps">{''.join(f'<div class="step-c rv"><h3>{t}</h3><p>{d}</p></div>' for t, d in [("We review", "A member of our team reads your request and any details you share."), ("We respond", "We come back to you with questions or a suggested call."), ("We propose", "You receive a tailored proposal covering team, coverage, SLAs and timelines.")])}</div></div></section>'''
    body += f'<section class="sec"><div class="wrap">{sec_head("FAQ", "Before you <span class=\"gold\">get in touch.</span>")}' + faq([
        ('Do I need to know exactly what I need?', 'No. Share what you know. We will help you shape the scope on a consultation call.'),
        ('Can I request a proposal for several services?', 'Yes. Select every service you are interested in and add detail in the message box.'),
        ('I represent a BPO company. Can we discuss a partnership?', 'Yes. Choose an enquiry type such as International BPO partnership, Subcontracting opportunity or Overflow customer support.'),
        ('Is my information kept confidential?', 'We use your details only to respond to your enquiry. See our Privacy Policy for details.')]) + '</div></section>'
    return page('contact', body, 'contact')

# ================================================================ PRIVACY
def build_privacy():
    body = f'''<section class="page-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{PAGES['home']}">Home</a><span aria-hidden="true">/</span><span aria-current="page">Privacy Policy</span></nav><h1>Privacy <em class="gold">Policy</em></h1><p class="lead">How ELVORRA OPERATIONS handles information submitted through this website.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap"><div class="prose">
<p class="upd">Last updated: November 2026</p>
<h2>Who we are</h2><p>ELVORRA OPERATIONS is an international business process outsourcing and managed operations company based in Abuja, Nigeria. You can contact us at <a href="mailto:" data-email data-email-text></a>.</p>
<h2>Information we collect</h2><p>When you submit our enquiry form we collect the information you provide:</p>
<ul><li>Contact details: full name, job title, company name, business email, country and contact number.</li><li>Enquiry details: services required, team size, preferred start date, languages, coverage, working hours, time zone and any additional project information.</li><li>Technical information needed to protect the form from spam, such as the time taken to complete it.</li></ul>
<p>We do not ask for sensitive personal information. Please do not include confidential customer data or personal data about third parties in your message.</p>
<h2>How we use it</h2><p>We use your information to respond to your enquiry, prepare proposals, arrange consultations, send you a confirmation and manage a potential business relationship. We do not sell your information.</p>
<h2>Legal basis</h2><p>We process your information based on your consent when you submit the form, and our legitimate interest in responding to business enquiries, in line with applicable data protection laws, including the Nigeria Data Protection Act 2023 and, where it applies to you, the GDPR or UK GDPR.</p>
<h2>Where information is stored and who sees it</h2><p>Submitted enquiries are delivered to our business email inbox and recorded in a spreadsheet, both held in Google Workspace services. Access is limited to authorised ELVORRA OPERATIONS personnel. Google acts as a service provider and may process data in countries outside your own. This website is hosted by a third-party hosting provider.</p>
<h2>Third-party content</h2><p>To display this website we load fonts from Google Fonts and photographs from Unsplash. Your browser may share your IP address with these providers when loading them. We do not currently use advertising or analytics cookies. Your light or dark display preference is stored in your own browser only.</p>
<h2>How long we keep it</h2><p>We keep enquiry records for as long as needed to respond to you and manage any resulting relationship, and then delete or anonymise them.</p>
<h2>Your rights</h2><p>Depending on where you live, you may have the right to access, correct or delete your information, to object to or restrict its use, and to withdraw consent at any time. To exercise these rights, email us at <a href="mailto:" data-email data-email-text></a>.</p>
<h2>Security</h2><p>Form submissions are sent over an encrypted (HTTPS) connection. We limit access to enquiry records and take reasonable steps to protect them, but no method of transmission over the internet is completely secure.</p>
<h2>Changes to this policy</h2><p>We may update this policy from time to time. The latest version will always be available on this page.</p>
<h2>Contact</h2><p>Questions about this policy? Email <a href="mailto:" data-email data-email-text></a>.</p>
</div></div></section>'''
    return page('privacy', body, 'none')

def build_404():
    t = '''<section class="error-page"><div class="wrap"><h1 class="gold">404</h1><h2 class="h2" style="margin:10px 0 18px">Page not found</h2><p class="sub" style="margin:0 auto 28px">The page you are looking for does not exist or has moved.</p><a href="index.html" class="btn btn-gold">Back to home <span class="ar">→</span></a></div></section>'''
    TITLES['404'] = 'Page not found | ELVORRA OPERATIONS'; DESCS['404'] = 'Page not found.'; PAGES['404'] = '404.html'
    return page('404', t, 'none').replace('content="index, follow, max-image-preview:large"', 'content="noindex"')

# ---------------------------------------------------------------- write
def finish(s):
    return re.sub(r'\{\{IMG:([\w-]+):(\d+)\}\}', lambda m: f'https://images.unsplash.com/{m.group(1)}?auto=format&fit=crop&w={m.group(2)}&q=75', s)

builders = {'home': build_home, 'about': build_about, 'cc': build_cc, 'ml': build_ml, 'bo': build_bo, 'crm': build_crm, 'mt': build_mt, 'ind': build_ind, 'contact': build_contact, 'privacy': build_privacy}
for k, fn in builders.items():
    open(os.path.join(OUT, PAGES[k]), 'w', encoding='utf-8').write(finish(fn()))
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(finish(build_404()))

# sitemap.xml + robots.txt
urls = ''.join(f'  <url><loc>{DOMAIN}/{"" if k == "home" else PAGES[k]}</loc></url>\n' for k in builders)
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
print('built', len(builders) + 1, 'pages')
