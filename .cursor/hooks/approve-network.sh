#!/bin/bash
# Fires before shell commands that involve network activity.
# Asks the user to confirm before proceeding.

input=$(cat)
command=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null)

echo "{
  \"permission\": \"ask\",
  \"user_message\": \"The agent wants to run a network command: $command\nPlease review it before allowing.\",
  \"agent_message\": \"Hook: network command requires user approval before execution.\"
}"
exit 0
