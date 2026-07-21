#!/usr/bin/env bash
#
# manual_form_test.sh
#
# Safeguard against the "stale field name" class of bug (e.g. telephone vs phone).
# Fires real POST requests at both form endpoints and checks:
#   1. HTTP status is 200 or 302 (302 = correct redirect-on-success behavior)
#   2. Response body does NOT contain "Missing required fields"
#
# Usage:
#   ./manual_form_test.sh https://your-site.example.com
set -uo pipefail
BASE_URL="${1:-}"
if [ -z "$BASE_URL" ]; then
  echo "Usage: $0 <base_url>   (e.g. $0 https://staging.example.com)"
  exit 2
fi
BASE_URL="${BASE_URL%/}"
FAIL=0

test_endpoint() {
  local label="$1"
  local path="$2"
  local payload="$3"
  local expected_codes="$4"   # space-separated, e.g. "200 302"
  echo "--- Testing ${label} (${path}) ---"
  local response
  local http_code
  local body
  response=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "$payload" \
    "${BASE_URL}${path}")
  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | sed '$d')
  local ok=1
  local code_ok=0
  for c in $expected_codes; do
    if [ "$http_code" = "$c" ]; then
      code_ok=1
    fi
  done
  if [ "$code_ok" -eq 0 ]; then
    echo "  FAIL: expected HTTP [${expected_codes}], got ${http_code}"
    ok=0
  else
    echo "  OK: HTTP ${http_code}"
  fi
  if echo "$body" | grep -qi "Missing required fields"; then
    echo "  FAIL: response contains 'Missing required fields'"
    ok=0
  else
    echo "  OK: no 'Missing required fields' in response"
  fi
  if [ "$ok" -eq 0 ]; then
    echo "  --- response body (first 500 chars) ---"
    echo "$body" | head -c 500
    echo
    FAIL=1
  fi
  echo
}

test_endpoint "main contact form" "/send.php" \
  "name=Test+User&email=test%40example.com&phone=07123456789&message=Automated+form+test" \
  "200 302"
test_endpoint "popup contact form" "/send-popup.php" \
  "name=Test+User&phone=07123456789&postcode=AB1+2CD" \
  "200 302"

if [ "$FAIL" -eq 0 ]; then
  echo "=== ALL TESTS PASSED ==="
  exit 0
else
  echo "=== ONE OR MORE TESTS FAILED ==="
  exit 1
fi
