---
description: Add a shell alias or shortcut to your profile
argument-hint: "<alias_name> <command>"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
model: haiku
---

# Add Shell Alias

Add a shell alias or shortcut to the user's shell profile, automatically detecting the shell type and appropriate configuration file.

## Variables

- `$ARGUMENTS` - Optional: alias name and command (e.g., "ll ls -la")

## Workflow

<phase name="detect-shell">
### Phase 1: Detect Shell Environment

1. Determine the user's current shell:
   ```bash
   echo $SHELL
   ```

2. Map shell to configuration file:
   - **bash**: Check in order: `~/.bashrc`, `~/.bash_profile`, `~/.profile`
   - **zsh**: `~/.zshrc`
   - **fish**: `~/.config/fish/config.fish`
   - **other**: Ask user for their config file path

3. Verify the config file exists. If not, ask user if they want to create it.
</phase>

<phase name="get-alias-details">
### Phase 2: Get Alias Details

If `$ARGUMENTS` is provided, parse it:
- First word = alias name
- Remaining words = command

If `$ARGUMENTS` is empty or incomplete, ask the user:
1. What should the alias/shortcut be called? (e.g., "ll", "gs", "myapp")
2. What command should it run? (e.g., "ls -la", "git status", "cd ~/projects && code .")

Validate:
- Alias name should be a single word with no spaces
- Command should not be empty
</phase>

<phase name="add-alias">
### Phase 3: Add Alias to Profile

1. Read the current profile file content

2. Check if an alias with the same name already exists:
   - For bash/zsh: Look for `alias <name>=`
   - For fish: Look for `alias <name> ` or `function <name>`

3. If alias exists, ask user:
   - Overwrite the existing alias?
   - Choose a different name?
   - Cancel?

4. Format the alias based on shell type:
   - **bash/zsh**: `alias <name>='<command>'`
   - **fish**: `alias <name> '<command>'`

5. Add a comment header and the alias to the end of the file:
   ```
   # Added by Claude Code
   alias <name>='<command>'
   ```

6. Show the user what was added
</phase>

<phase name="activate">
### Phase 4: Activate the Alias

1. Inform the user they can activate the alias by either:
   - Opening a new terminal window
   - Running `source <profile_file>` (or `source ~/.config/fish/config.fish` for fish)

2. Offer to show them the source command they can copy

3. Do NOT automatically source the profile (it won't persist to their actual shell)
</phase>

## Output Format

```yaml
result:
  shell: "<detected shell>"
  profile: "<path to profile file>"
  alias:
    name: "<alias name>"
    command: "<command>"
  status: "success" | "cancelled" | "error"
  next_steps:
    - "Open a new terminal, or run: source <profile>"
```

## Error Handling

- If shell detection fails, ask user to specify their shell
- If profile file is not writable, explain the permission issue
- If command contains special characters, ensure proper escaping
