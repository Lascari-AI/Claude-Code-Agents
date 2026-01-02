#!/usr/bin/env python3
"""
Lascari AI Default Statusline
=============================

A custom statusline for Claude Code that displays key session information.

Output Format:
    {model} | {git_status} {branch} ({files}) | 📁 {directory} | {lines} | Ctx: {percent} ({tokens})

Sections:
---------
1. MODEL
   - Displays the current Claude model in lowercase (opus, sonnet, haiku)
   - Falls back to full model name in lowercase for unknown models

2. GIT STATUS
   - Shows current branch name with status indicator:
     ✅ = Clean working directory (no changes)
     🟡 = Has staged changes ready to commit
     🔴 = Has unstaged/untracked changes
   - Displays count of changed files in parentheses when dirty

3. DIRECTORY
   - Shows the current working directory basename with 📁 icon

4. LINES CHANGED (UNCOMMITTED)
   - Shows lines added (green) and removed (red) that are NOT YET COMMITTED
   - Combines staged and unstaged changes from git diff
   - Format: +{added}/-{removed}
   - Resets automatically when you commit
   - Only displayed when there are uncommitted changes

5. CONTEXT WINDOW
   - Shows percentage of context window used with color coding:
     Green  = <25% used
     Yellow = 25-50% used
     Orange = 50-75% used
     Red    = >75% used
   - Displays token count in thousands (e.g., 24.0k)

Example Output:
    opus | 🔴 main (4) | 📁 my-project | +42/-15 | Ctx: 12% (24.0k)
"""

import json
import os
import subprocess
import sys

# =============================================================================
# CONFIGURATION: ANSI Color Codes
# =============================================================================
GREEN = "\033[32m"
YELLOW = "\033[33m"
ORANGE = "\033[38;5;208m"
RED = "\033[31m"
RESET = "\033[0m"


# =============================================================================
# INPUT: Read JSON data from Claude Code via stdin
# =============================================================================
data = json.load(sys.stdin)


# =============================================================================
# SECTION 1: MODEL NAME
# Simplify the full model name (e.g., "Claude Opus 4") to just the variant
# in lowercase (e.g., "opus")
# =============================================================================
model = data["model"]["display_name"]

MODEL_NAMES = ["Opus", "Sonnet", "Haiku"]
for name in MODEL_NAMES:
    if name in model:
        model = name.lower()
        break
else:
    model = model.lower()  # fallback to full name in lowercase


# =============================================================================
# SECTION 2: GIT STATUS
# Check if we're in a git repo, get branch name, and determine status:
# - ✅ Clean (no changes)
# - 🟡 Staged (has changes ready to commit)
# - 🔴 Dirty (has unstaged or untracked changes)
# Also counts total changed files (staged + unstaged + untracked)
# =============================================================================
git_info = ""
try:
    # Verify we're in a git repository
    subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        capture_output=True,
        check=True,
    )

    # Get current branch name (or "detached" if in detached HEAD state)
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip() or "detached"

    # Quick check: is the working directory clean?
    diff_result = subprocess.run(
        ["git", "diff", "--quiet"],
        capture_output=True,
    )
    cached_result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True,
    )

    # Count staged files (changes in index, ready to commit)
    staged_result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    staged_count = len([l for l in staged_result.stdout.strip().split("\n") if l])

    # Count unstaged files (modified but not added)
    unstaged_result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
    )
    unstaged_count = len([l for l in unstaged_result.stdout.strip().split("\n") if l])

    # Count untracked files (new files not yet added to git)
    untracked_result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
    )
    untracked_count = len([l for l in untracked_result.stdout.strip().split("\n") if l])

    total_changed = staged_count + unstaged_count + untracked_count

    # Determine status icon and file count display
    if diff_result.returncode == 0 and cached_result.returncode == 0:
        git_status = "✅"
        file_count = ""
    else:
        if staged_count > 0:
            git_status = "🟡"  # Has staged changes
        else:
            git_status = "🔴"  # Has unstaged changes
        file_count = f" ({total_changed})"

    git_info = f" | {git_status} {branch}{file_count}"

except (subprocess.CalledProcessError, FileNotFoundError):
    # Not a git repo or git not installed - skip git info
    pass


# =============================================================================
# SECTION 3: DIRECTORY
# Extract just the directory basename for display
# =============================================================================
current_dir = os.path.basename(data["workspace"]["current_dir"])


# =============================================================================
# SECTION 4: LINES CHANGED (UNCOMMITTED)
# Show lines added/removed that are NOT YET COMMITTED with color coding:
# - Green for additions (+)
# - Red for removals (-)
# Combines both staged and unstaged changes
# Resets automatically when you commit
# =============================================================================
lines_info = ""
try:
    # Get unstaged changes (working directory vs index)
    unstaged_diff = subprocess.run(
        ["git", "diff", "--numstat"],
        capture_output=True,
        text=True,
    )

    # Get staged changes (index vs HEAD)
    staged_diff = subprocess.run(
        ["git", "diff", "--cached", "--numstat"],
        capture_output=True,
        text=True,
    )

    lines_added = 0
    lines_removed = 0

    # Parse numstat output: "added\tremoved\tfilename" per line
    for output in [unstaged_diff.stdout, staged_diff.stdout]:
        for line in output.strip().split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    # Binary files show "-" for added/removed
                    if parts[0] != "-":
                        lines_added += int(parts[0])
                    if parts[1] != "-":
                        lines_removed += int(parts[1])

    if lines_added > 0 or lines_removed > 0:
        lines_info = f" | {GREEN}+{lines_added}{RESET}/{RED}-{lines_removed}{RESET}"

except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
    # Not a git repo or git not installed - skip lines info
    pass


# =============================================================================
# SECTION 5: CONTEXT WINDOW USAGE
# Calculate and display what percentage of the context window is used.
# Color coded by usage level:
# - Green:  <25% (plenty of room)
# - Yellow: 25-50% (getting used)
# - Orange: 50-75% (consider compacting)
# - Red:    >75% (running low)
# =============================================================================
context_info = ""
context_window = data.get("context_window", {})
context_size = context_window.get("context_window_size", 0)
current_usage = context_window.get("current_usage")

if current_usage and context_size > 0:
    # Sum all token types for total usage
    current_tokens = (
        current_usage.get("input_tokens", 0)
        + current_usage.get("cache_creation_input_tokens", 0)
        + current_usage.get("cache_read_input_tokens", 0)
    )
    percent_used = (current_tokens * 100) // context_size

    # Color based on usage threshold
    if percent_used < 25:
        color = GREEN
    elif percent_used < 50:
        color = YELLOW
    elif percent_used < 75:
        color = ORANGE
    else:
        color = RED

    # Round to nearest hundred and format as thousands for readability
    rounded_tokens = round(current_tokens / 100) * 100
    tokens_k = rounded_tokens / 1000

    context_info = f" | Ctx: {color}{percent_used}%{RESET} ({tokens_k:.1f}k)"
else:
    context_info = f" | Ctx: {GREEN}0%{RESET} (0.0k)"


# =============================================================================
# OUTPUT: Compose and print the final statusline
# =============================================================================
print(f"{model}{git_info} | 📁 {current_dir}{lines_info}{context_info}")
