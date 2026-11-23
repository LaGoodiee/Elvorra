/**
 * ELVORRA OPERATIONS — form receiver (Google Apps Script)
 * Emails every enquiry to the business inbox and (optionally) logs it in a Google Sheet.
 * Deploy: Extensions > Apps Script > Deploy > New deployment > Web app
 *   Execute as: Me   |   Who has access: Anyone
 * Paste the /exec URL into site/assets/config.js as `endpoint`.
 */
var NOTIFY_EMAIL = 'elevoraoperation@gmail.com';   // where enquiries are sent
var SHEET_ID = '';                                  // optional: Google Sheet ID to log rows
var SEND_AUTOREPLY = true;                          // thank-you email to the enquirer

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    if (d.website) return out({ ok: true });         // honeypot: silently drop bots
    if (!d.name || !d.email) return out({ ok: false, error: 'missing fields' });

    var list = function (v) { return Array.isArray(v) ? v.join(', ') : (v || '-'); };
    var type = d.mode === 'consult' ? 'Consultation request' : 'Proposal request';
    var body = [
      'Type: ' + type,
      'Name: ' + d.name, 'Company: ' + (d.company || '-'), 'Email: ' + d.email, 'Country: ' + (d.country || '-'),
      'Services: ' + list(d.services),
      d.mode === 'consult'
        ? 'Preferred date: ' + (d.date || '-') + '\nPreferred time: ' + (d.time || '-') + '\nTime zone: ' + (d.timezone || '-')
        : 'Team size: ' + list(d.teamSize) + '\nCoverage: ' + list(d.coverage) + '\nLanguages: ' + list(d.languages),
      'Message: ' + (d.message || '-'),
      'Submitted: ' + new Date()
    ].join('\n');

    MailApp.sendEmail({ to: NOTIFY_EMAIL, replyTo: d.email, subject: '[ELVORRA website] ' + type + ' — ' + d.name + (d.company ? ' (' + d.company + ')' : ''), body: body });

    if (SHEET_ID) {
      var sh = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
      sh.appendRow([new Date(), type, d.name, d.company, d.email, d.country, list(d.services), list(d.teamSize), list(d.coverage), list(d.languages), d.date, d.time, d.timezone, d.message]);
    }
    if (SEND_AUTOREPLY) {
      MailApp.sendEmail({ to: d.email, replyTo: NOTIFY_EMAIL, name: 'ELVORRA OPERATIONS',
        subject: 'We received your request — ELVORRA OPERATIONS',
        body: 'Hello ' + d.name + ',\n\nThank you for contacting ELVORRA OPERATIONS. We have received your ' + type.toLowerCase() + ' and will respond within one business day.\n\nGlobal Reach. Operational Excellence. Human-Centred Service.\nELVORRA OPERATIONS' });
    }
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
