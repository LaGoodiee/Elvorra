/**
 * ELVORRA OPERATIONS — enquiry form receiver (Google Apps Script)
 *
 * What it does for every submission:
 *   1. Validates it and blocks spam (honeypot, too-fast submissions, rate limit, size limits, duplicate refs)
 *   2. Saves a backup row in a Google Sheet ("ELVORRA Enquiries", created automatically in the owner's Drive)
 *   3. Emails the complete enquiry to the business inbox (NOTIFY_EMAIL)
 *   4. Emails a confirmation to the prospective client
 *   5. Returns JSON {ok:true} so the website can show its confirmation, or {ok:false} so it can show an error
 *
 * SETUP (about 5 minutes) — sign in to the ELVORRA Google account that owns the business inbox:
 *   1. script.google.com > New project > paste this file in place of Code.gs
 *   2. Select the function  setup  and press Run. Approve the permissions when asked.
 *      (This creates the spreadsheet and sends you a test email.)
 *   3. Deploy > New deployment > type: Web app
 *        Execute as: Me        Who has access: Anyone
 *   4. Copy the Web app URL (ends in /exec) into  docs/assets/config.js  as  endpoint
 *   5. Open the /exec URL in a browser: you should see {"ok":true,"service":"ELVORRA enquiry endpoint"}
 *   6. IMPORTANT: after changing this code later, use Deploy > Manage deployments > Edit > New version.
 *
 * OPTIONAL: Triggers (clock icon) > Add trigger > retryUnsent > Time-driven > Every hour.
 *           It re-sends the notification for any enquiry saved while email was temporarily unavailable.
 */
var CONFIG = {
  NOTIFY_EMAIL: 'elvoraoperation@gmail.com',   // where enquiries are delivered
  BRAND: 'ELVORRA OPERATIONS',
  SHEET_NAME: 'ELVORRA Enquiries',
  SEND_AUTOREPLY: true,        // confirmation email to the enquirer
  MIN_FILL_MS: 4000,           // forms submitted faster than this are treated as bots
  MAX_PER_HOUR: 5,             // per email address
  MAX_BODY: 30000              // bytes
};

var HEADERS = ['Received', 'Reference', 'Type', 'Enquiry type', 'Services', 'Name', 'Job title', 'Company', 'Email', 'Phone', 'Country',
               'Team size', 'Coverage', 'Languages', 'Start date', 'Working hours', 'Preferred date', 'Preferred time', 'Time zone',
               'Message', 'Page', 'Notified'];

function doGet() { return json_({ ok: true, service: 'ELVORRA enquiry endpoint' }); }

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    var raw = (e && e.postData && e.postData.contents) || '';
    if (!raw || raw.length > CONFIG.MAX_BODY) return json_({ ok: false, error: 'size' });
    var d = JSON.parse(raw);

    // --- spam protection: pretend success so bots learn nothing
    if (d.website) return json_({ ok: true });
    if (Number(d.elapsed) < CONFIG.MIN_FILL_MS) return json_({ ok: true });

    var rec = clean_(d);
    if (!rec.name || !rec.company || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(rec.email) || !rec.enquiryType || !d.consent) {
      return json_({ ok: false, error: 'invalid' });
    }

    var cache = CacheService.getScriptCache();
    if (rec.ref && cache.get('ref_' + rec.ref)) return json_({ ok: true, duplicate: true, confirmed: true });  // retry of an earlier send
    var rlKey = 'rl_' + Utilities.base64EncodeWebSafe(rec.email.toLowerCase());
    var count = Number(cache.get(rlKey) || 0);
    if (count >= CONFIG.MAX_PER_HOUR) return json_({ ok: false, error: 'rate' });
    cache.put(rlKey, String(count + 1), 3600);

    // --- 1. backup record first, so nothing is lost even if email fails
    var sheet = getSheet_();
    var row = sheet.getLastRow() + 1;
    sheet.appendRow(rowFor_(rec, 'pending'));

    // --- 2. notify ELVORRA
    var notified = 'yes';
    try { notify_(rec); } catch (err) { notified = 'NO: ' + err; }
    sheet.getRange(row, HEADERS.length).setValue(notified);

    // --- 3. confirmation to the client
    var confirmed = false;
    if (CONFIG.SEND_AUTOREPLY) { try { autoreply_(rec); confirmed = true; } catch (err2) { confirmed = false; } }

    if (rec.ref) cache.put('ref_' + rec.ref, '1', 21600);
    return json_({ ok: true, confirmed: confirmed });
  } catch (err3) {
    return json_({ ok: false, error: 'server' });
  } finally {
    try { lock.releaseLock(); } catch (x) {}
  }
}

/* ---------------- helpers ---------------- */
function s_(v, max) { return String(v == null ? '' : v).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, ' ').trim().slice(0, max || 200); }
function list_(v, max) { return (Array.isArray(v) ? v : [v]).map(function (x) { return s_(x, 80); }).filter(String).slice(0, 20).join(', ').slice(0, max || 400); }

function clean_(d) {
  return {
    ref: s_(d.ref, 30), type: s_(d.type, 40), enquiryType: s_(d.enquiryType, 120), services: list_(d.services, 600),
    name: s_(d.name, 100), jobTitle: s_(d.jobTitle, 100), company: s_(d.company, 120), email: s_(d.email, 120), phone: s_(d.phone, 30), country: s_(d.country, 60),
    teamSize: s_(d.teamSize, 60), coverage: s_(d.coverage, 60), languages: list_(d.languages, 200), startDate: s_(d.startDate, 20), hours: s_(d.hours, 80),
    preferredDate: s_(d.preferredDate, 20), preferredTime: s_(d.preferredTime, 40), timezone: s_(d.timezone, 60),
    message: s_(d.message, 2000), page: s_(d.page, 300)
  };
}

function cell_(v) { v = String(v || ''); return /^[=+\-@]/.test(v) ? "'" + v : v; }   // block spreadsheet formula injection

function rowFor_(r, notified) {
  return [new Date(), r.ref, r.type, r.enquiryType, r.services, r.name, r.jobTitle, r.company, r.email, r.phone, r.country, r.teamSize, r.coverage, r.languages,
          r.startDate, r.hours, r.preferredDate, r.preferredTime, r.timezone, r.message, r.page, notified].map(cell_);
}

function getSheet_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID');
  var ss;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
  if (!ss) { ss = SpreadsheetApp.create(CONFIG.SHEET_NAME); props.setProperty('SHEET_ID', ss.getId()); }
  var sh = ss.getSheets()[0];
  if (sh.getLastRow() === 0) { sh.appendRow(HEADERS); sh.setFrozenRows(1); sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold'); }
  return sh;
}

function body_(r) {
  var L = [CONFIG.BRAND + ' website enquiry', '',
    'Reference: ' + r.ref, 'Type: ' + r.type, 'Enquiry type: ' + (r.enquiryType || '-'), 'Services: ' + (r.services || '-'), '',
    'CONTACT', 'Name: ' + r.name, 'Job title: ' + (r.jobTitle || '-'), 'Company: ' + r.company, 'Email: ' + r.email, 'Phone: ' + (r.phone || '-'), 'Country: ' + (r.country || '-'), ''];
  if (r.type === 'Consultation request') {
    L.push('CONSULTATION', 'Preferred date: ' + (r.preferredDate || '-'), 'Preferred time: ' + (r.preferredTime || '-'), 'Time zone: ' + (r.timezone || '-'));
  } else {
    L.push('OPERATIONAL REQUIREMENTS', 'Team size: ' + (r.teamSize || '-'), 'Coverage: ' + (r.coverage || '-'), 'Languages: ' + (r.languages || '-'),
           'Preferred start date: ' + (r.startDate || '-'), 'Preferred working hours: ' + (r.hours || '-'), 'Time zone: ' + (r.timezone || '-'));
  }
  L.push('', 'MESSAGE', r.message || '-', '', 'Submitted from: ' + (r.page || '-'), 'Time: ' + new Date());
  return L.join('\n');
}

function notify_(r) {
  MailApp.sendEmail({
    to: CONFIG.NOTIFY_EMAIL, replyTo: r.email, name: CONFIG.BRAND + ' Website',
    subject: '[' + r.type + '] ' + r.company + ' — ' + r.name + ' (' + r.ref + ')',
    body: body_(r)
  });
}

function autoreply_(r) {
  MailApp.sendEmail({
    to: r.email, replyTo: CONFIG.NOTIFY_EMAIL, name: CONFIG.BRAND,
    subject: 'We received your request (' + r.ref + ') — ' + CONFIG.BRAND,
    body: 'Hello ' + r.name + ',\n\nThank you for contacting ' + CONFIG.BRAND + '. We have received your ' + r.type.toLowerCase() +
          ' (reference ' + r.ref + ') and our team will review it and be in touch.\n\nA copy of what you sent:\n\n' + body_(r) +
          '\n\nGlobal Reach. Operational Excellence. Human-Centred Service.\n' + CONFIG.BRAND
  });
}

function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/* ---------------- run once from the editor ---------------- */
function setup() {
  var sh = getSheet_();
  MailApp.sendEmail(CONFIG.NOTIFY_EMAIL, CONFIG.BRAND + ' form setup test', 'The enquiry form backend is set up. Enquiries will be saved in the spreadsheet "' + CONFIG.SHEET_NAME + '": ' + sh.getParent().getUrl());
  Logger.log('Spreadsheet: ' + sh.getParent().getUrl());
}

/* ---------------- optional hourly trigger ---------------- */
function retryUnsent() {
  var sh = getSheet_(), last = sh.getLastRow();
  if (last < 2) return;
  var vals = sh.getRange(2, 1, last - 1, HEADERS.length).getValues();
  vals.forEach(function (v, i) {
    if (String(v[HEADERS.length - 1]).indexOf('NO') === 0) {
      var r = { ref: v[1], type: v[2], enquiryType: v[3], services: v[4], name: v[5], jobTitle: v[6], company: v[7], email: v[8], phone: v[9], country: v[10], teamSize: v[11], coverage: v[12],
                languages: v[13], startDate: v[14], hours: v[15], preferredDate: v[16], preferredTime: v[17], timezone: v[18], message: v[19], page: v[20] };
      try { notify_(r); sh.getRange(i + 2, HEADERS.length).setValue('yes (retried)'); } catch (e) {}
    }
  });
}
