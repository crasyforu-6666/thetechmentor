/**
 * YourOneMentor — lead & sale receiver (Google Apps Script)
 *
 * Saves every website application and payment into this Google Sheet and
 * emails you instantly. Setup steps: see integrations/README.md.
 */

var NOTIFY_EMAIL = "info@youronementor.com"; // where alerts are sent

var COLUMNS = [
  "received_at", "type", "name", "email", "phone", "role", "timeline", "budget",
  "status", "program", "amount", "payment_id",
  "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid", "page"
];

function doPost(e) {
  var data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return ContentService.createTextOutput("bad request");
  }

  var type = data.type === "sale" ? "sale" : "lead";
  var sheetName = type === "sale" ? "Sales" : "Leads";
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(sheetName) || ss.insertSheet(sheetName);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS);
    sheet.setFrozenRows(1);
  }

  data.received_at = new Date();
  data.type = type;
  sheet.appendRow(COLUMNS.map(function (c) {
    var v = data[c] === undefined ? "" : data[c];
    // Stop spreadsheet formula injection from form input.
    if (typeof v === "string" && /^[=+\-@]/.test(v)) v = "'" + v;
    return v;
  }));

  var subject = type === "sale"
    ? "💰 New payment: ₹" + (data.amount || "?") + " — " + (data.program || "") + " — " + (data.name || "")
    : (data.budget === "Yes" ? "🔥 Qualified lead: " : "New lead: ") + (data.name || "") + " (" + (data.phone || "") + ")";

  var lines = COLUMNS.filter(function (c) { return data[c]; })
    .map(function (c) { return c + ": " + data[c]; });
  if (data.phone) {
    var digits = String(data.phone).replace(/\D/g, "");
    if (digits.length === 10) digits = "91" + digits;
    lines.push("", "WhatsApp them: https://wa.me/" + digits);
  }
  MailApp.sendEmail(NOTIFY_EMAIL, subject, lines.join("\n"));

  return ContentService.createTextOutput("ok");
}
