#!/usr/bin/env bash
#
# deploy.sh
#
# Single command for the full build -> deploy -> verify cycle for site_BAT.
# Replaces the previous practice of manually running rsync with no automatic
# verification. Created 2026-07-21 as part of Phase 4 permanent fix following
# the send.php (2026-06-30) and homepage (2026-07-03) silent deploy failures.
#
# Exits non-zero at the FIRST failed stage. Does not proceed to deploy if the
# build fails verification. Does not report success unless the LIVE site has
# been checked and confirmed correct after deploy.
#
set -uo pipefail

DOMAIN="https://buildingsandtrust.co.uk"
SERVER="root@217.154.33.12"
SSH_KEY="$HOME/.ssh/github_actions_bat"
REMOTE_PATH="/var/www/vhosts/buildingsandtrust.co.uk/httpdocs/"

echo "=================================================="
echo "STAGE 1: BUILD"
echo "=================================================="
python3 build.py
BUILD_EXIT=$?
if [ "$BUILD_EXIT" -ne 0 ]; then
    echo ""
    echo "❌ BUILD FAILED — deploy aborted. Fix the build before deploying."
    exit 1
fi

echo ""
echo "=================================================="
echo "STAGE 2: DEPLOY (rsync)"
echo "=================================================="
rsync -avz --delete -e "ssh -i ${SSH_KEY}" build/ "${SERVER}:${REMOTE_PATH}"
RSYNC_EXIT=$?
if [ "$RSYNC_EXIT" -ne 0 ]; then
    echo ""
    echo "❌ RSYNC FAILED (exit ${RSYNC_EXIT}) — deploy incomplete."
    exit 1
fi
echo "✅ rsync completed (exit 0) — note: this only confirms transfer succeeded, not that the site is correct. Verifying live now."

echo ""
echo "=================================================="
echo "STAGE 3: POST-DEPLOY LIVE VERIFICATION"
echo "=================================================="
VERIFY_FAIL=0

echo "--- Homepage ---"
HOME_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${DOMAIN}/")
if [ "$HOME_CODE" == "200" ]; then
    echo "✅ Homepage: HTTP ${HOME_CODE}"
else
    echo "❌ Homepage: HTTP ${HOME_CODE} (expected 200)"
    VERIFY_FAIL=1
fi

echo ""
echo "--- robots.txt ---"
ROBOTS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${DOMAIN}/robots.txt")
if [ "$ROBOTS_CODE" == "200" ]; then
    echo "✅ robots.txt: HTTP ${ROBOTS_CODE}"
else
    echo "❌ robots.txt: HTTP ${ROBOTS_CODE} (expected 200)"
    VERIFY_FAIL=1
fi

echo ""
echo "--- sitemap.xml ---"
SITEMAP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${DOMAIN}/sitemap.xml")
if [ "$SITEMAP_CODE" == "200" ]; then
    echo "✅ sitemap.xml: HTTP ${SITEMAP_CODE}"
else
    echo "❌ sitemap.xml: HTTP ${SITEMAP_CODE} (expected 200)"
    VERIFY_FAIL=1
fi

echo ""
echo "--- Contact forms (send.php + send-popup.php) ---"
if [ -f "./manual_form_test.sh" ]; then
    ./manual_form_test.sh "${DOMAIN}"
    FORM_EXIT=$?
    if [ "$FORM_EXIT" -ne 0 ]; then
        VERIFY_FAIL=1
    fi
else
    echo "❌ manual_form_test.sh not found — cannot verify contact forms"
    VERIFY_FAIL=1
fi

echo ""
echo "=================================================="
if [ "$VERIFY_FAIL" -eq 0 ]; then
    echo "✅ DEPLOY COMPLETE AND VERIFIED — all live checks passed."
    exit 0
else
    echo "❌ DEPLOY COMPLETED BUT LIVE VERIFICATION FAILED."
    echo "The files were transferred (rsync succeeded) but the live site is NOT"
    echo "confirmed correct. Investigate immediately — do not assume this deploy is safe."
    exit 1
fi
