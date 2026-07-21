# Archived Full Changelog Entries (condensed 2026-07-21)

## Entry 0 — 2026-07-03
9 of the 26 service hub pages were found returning 410 Gone live (regression from Task 20, which only covered 12 of 26 hub slugs). Root cause: stale 410 nginx rules for building-site-waste, care-clearance, commercial-waste, guest-house-clearance, removals, scrap-motorbike, scrap-motorhome, caravan-disposal, waste-item-pickup left over from the original 47,283-page 404 cleanup, wrongly shadowing the live hub pages. Fixed by removing the 18 exact-match location blocks (with and without trailing slash) from vhost_nginx.conf, backed up as vhost_nginx.conf.bak.2026-07-03. Verified nginx -t clean, reloaded, all 9 slugs confirmed returning HTTP 200 live. Separately found 5 hub slugs (loft-insulation, black-bag, scrap-car, old-caravan, house-clean) returning 404 with no matching nginx rule at all -- different root cause, not yet diagnosed, logged as pending task 22.

## Entry 1 — 2026-07-03
Corrected task 22: the 5 remaining hub pages (old-caravan-collection, black-bag-collection, house-clean, loft-insulation-cleared, scrap-car-collection) were NOT missing from the build -- they had the exact same root cause as the first 9: stale 410 nginx rules left over from the original 47,283-page GSC cleanup, shadowing the correct live slugs (my earlier task-22 diagnosis tested the wrong URLs and produced a false conclusion). Removed 10 exact-match location blocks from vhost_nginx.conf, backed up as vhost_nginx.conf.bak.2026-07-03-b. nginx -t validated, reloaded, all 5 confirmed returning HTTP 200 live. All 26 of 26 service hub pages now confirmed live and correct.

## Entry 2 — 2026-07-03
Root-caused and fixed silent homepage deploy failure: deploy_command had --exclude=index.html left over from an earlier caution note; homepage had not been updated on the live server since 2026-06-30 despite many "successful" rsync deploys in between. Removed the exclude from deploy_command. Added ai_governance rule requiring direct server-side verification (not just rsync exit status) when a deploy is reported as not working.

## Entry 3 — 2026-07-20
Contact form fields verified directly from assets/send.php (identical copies confirmed in build/send.php and build/assets/send.php via diff): required POST fields name, email, message; optional field phone. Recipient darren@buildingsandtrust.co.uk (matches project_metadata.email). Success redirects to /thank-you/. No honeypot or CSRF field present. Verified as part of cross-site contact form audit (contact_form_audit.json at sites root) - not yet added to manual_form_test.sh, no live HTTP test run yet.

## Entry 9 — 2026-07-21
Fixed build.py non-deterministic template selection (hash(slug) randomization bug found during division migration testing) -- replaced with stable_idx() using hashlib.md5. Verified deterministic, deployed live, all deploy.sh checks passed.
