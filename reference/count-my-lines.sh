#!/bin/bash

# Emails to search for (add more with additional --author flags)
EMAILS=(
  "ford@bubba.ai"
  "ford.lascari@gmail.com"
)

# Build author flags
AUTHOR_FLAGS=""
for email in "${EMAILS[@]}"; do
  AUTHOR_FLAGS="$AUTHOR_FLAGS --author=$email"
done

# Collect all data first
declare -a REPOS ADDS DELS NETS
TOTAL_ADD=0
TOTAL_DEL=0

while IFS= read -r gitdir; do
  dir="$(dirname "$gitdir")"
  repo="${dir#./}"

  stats=$(cd "$dir" && \
    git log $AUTHOR_FLAGS --since="30 days ago" --pretty=tformat: --numstat 2>/dev/null \
    | awk '($1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/) {add+=$1; del+=$2}
           END {printf "%d %d %d", add, del, add-del}')

  read add del net <<< "$stats"

  if [[ "$add" != "0" || "$del" != "0" ]]; then
    REPOS+=("$repo")
    ADDS+=("$add")
    DELS+=("$del")
    NETS+=("$net")
    TOTAL_ADD=$((TOTAL_ADD + add))
    TOTAL_DEL=$((TOTAL_DEL + del))
  fi
done < <(find . -maxdepth 4 -name ".git" -type d 2>/dev/null)

TOTAL_NET=$((TOTAL_ADD - TOTAL_DEL))

# Calculate column widths
COL1_WIDTH=4  # "REPO"
COL2_WIDTH=5  # "ADDED"
COL3_WIDTH=7  # "DELETED"
COL4_WIDTH=3  # "NET"

for i in "${!REPOS[@]}"; do
  (( ${#REPOS[$i]} > COL1_WIDTH )) && COL1_WIDTH=${#REPOS[$i]}
  (( ${#ADDS[$i]} > COL2_WIDTH )) && COL2_WIDTH=${#ADDS[$i]}
  (( ${#DELS[$i]} > COL3_WIDTH )) && COL3_WIDTH=${#DELS[$i]}
  len=${#NETS[$i]}
  (( NETS[$i] >= 0 )) && ((len++))  # account for + sign
  (( len > COL4_WIDTH )) && COL4_WIDTH=$len
done

# Check totals width
(( ${#TOTAL_ADD} > COL2_WIDTH )) && COL2_WIDTH=${#TOTAL_ADD}
(( ${#TOTAL_DEL} > COL3_WIDTH )) && COL3_WIDTH=${#TOTAL_DEL}
TOTAL_NET_LEN=${#TOTAL_NET}
(( TOTAL_NET >= 0 )) && ((TOTAL_NET_LEN++))
(( TOTAL_NET_LEN > COL4_WIDTH )) && COL4_WIDTH=$TOTAL_NET_LEN
(( 5 > COL1_WIDTH )) && COL1_WIDTH=5  # "TOTAL"

# Add padding
COL1_WIDTH=$((COL1_WIDTH + 2))
COL2_WIDTH=$((COL2_WIDTH + 2))
COL3_WIDTH=$((COL3_WIDTH + 2))
COL4_WIDTH=$((COL4_WIDTH + 2))

# Calculate total table width (columns + separators)
TABLE_WIDTH=$((COL1_WIDTH + COL2_WIDTH + COL3_WIDTH + COL4_WIDTH + 7))

# Function to print a line of characters
print_line() {
  printf '%*s\n' "$TABLE_WIDTH" '' | tr ' ' "$1"
}

# Colors (using tput for better compatibility)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NC=$(tput sgr0)

# Function to format net with +/- sign
format_net() {
  if (( $1 >= 0 )); then
    echo "+$1"
  else
    echo "$1"
  fi
}

# Function to format net with color
format_net_color() {
  if (( $1 >= 0 )); then
    printf "${GREEN}+%d${NC}" "$1"
  else
    printf "${RED}%d${NC}" "$1"
  fi
}

# Print header
print_line '-'
printf "| %-*s | %*s | %*s | %*s |\n" \
  $((COL1_WIDTH - 1)) "REPO" \
  $((COL2_WIDTH - 1)) "ADDED" \
  $((COL3_WIDTH - 1)) "DELETED" \
  $((COL4_WIDTH - 1)) "NET"
print_line '-'

# Print data rows
for i in "${!REPOS[@]}"; do
  printf "| %-*s | %*d | %*d | %*s |\n" \
    $((COL1_WIDTH - 1)) "${REPOS[$i]}" \
    $((COL2_WIDTH - 1)) "${ADDS[$i]}" \
    $((COL3_WIDTH - 1)) "${DELS[$i]}" \
    $((COL4_WIDTH - 1)) "$(format_net "${NETS[$i]}")"
done

# Print total with colors
print_line '='
printf "| %-*s | ${GREEN}%*d${NC} | ${RED}%*d${NC} | %*s |\n" \
  $((COL1_WIDTH - 1)) "TOTAL" \
  $((COL2_WIDTH - 1)) "$TOTAL_ADD" \
  $((COL3_WIDTH - 1)) "$TOTAL_DEL" \
  $((COL4_WIDTH - 1)) "$(format_net_color "$TOTAL_NET")"
print_line '='
