#!/bin/bash
# Fires after any .py file is edited.
# Scans the saved file for patterns that look like hardcoded secrets
# (Telegram token format or long hex/base64 strings assigned to known key names).

input=$(cat)
file_path=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('path',''))" 2>/dev/null)

if [ -z "$file_path" ]; then
  echo '{"additional_context": ""}'
  exit 0
fi

# Only inspect Python files
if [[ "$file_path" != *.py ]]; then
  echo '{"additional_context": ""}'
  exit 0
fi

# Pattern 1: Telegram bot token  (digits:alphanum, 35+ chars)
# Pattern 2: OWM API key assigned to a variable (32 hex chars)
if grep -qP '(BOT_TOKEN|OWM_API_KEY|token|api_key)\s*=\s*["\x27][0-9]{8,10}:[A-Za-z0-9_-]{35}["\x27]' "$file_path" 2>/dev/null || \
   grep -qP '(BOT_TOKEN|OWM_API_KEY|token|api_key)\s*=\s*["\x27][a-fA-F0-9]{32}["\x27]' "$file_path" 2>/dev/null; then

  echo '{
    "additional_context": "WARNING: A hardcoded secret was detected in '"$file_path"'. Move it to .env and load it with os.getenv() instead. See bot-conventions.mdc for the correct key names."
  }'
  exit 0
fi

echo '{"additional_context": ""}'
exit 0
