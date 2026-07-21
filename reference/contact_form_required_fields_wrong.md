# contact_form_required_fields_wrong

IN PROGRESS 2026-07-21 — contact-us popup form (data/pages.json body_content)
has wrong required fields: Email and message textarea wrongly require input,
Service dropdown wrongly does not.

Target: only First Name, Telephone, Postcode, Service Required should be mandatory.

assets/send.php server-side validation also needs updating to match:
currently requires name+email+message, should require name+phone+postcode.

Two automated patch attempts on send.php failed on anchor-text mismatch.
Confirmed NOT a CRLF/line-ending issue (file is pure LF, 1160 bytes).
Likely cause: quote character mismatch or other invisible char diff.
NOT YET FIXED. Switching to regex-based line patch method next.
