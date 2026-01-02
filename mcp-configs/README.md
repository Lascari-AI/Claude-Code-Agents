# MCP Configuration Files

Pre-configured MCP server configurations for use with Claude Code's `--mcp-config` flag.

## Quick Start

```bash
# Run Claude Code with a specific MCP config
claude --mcp-config ./mcp-configs/.mcp.json.firecrawl_7k

# Run with multiple configs
claude --mcp-config ./mcp-configs/.mcp.json.firecrawl_7k ./mcp-configs/another.mcp.json

# Use --strict-mcp-config to ONLY use the specified configs (ignores all other MCP servers)
claude --strict-mcp-config --mcp-config ./mcp-configs/.mcp.json.firecrawl_7k
```

## Available Configurations

### Firecrawl (7K credits plan)

- **Config:** [.mcp.json.firecrawl_7k](./.mcp.json.firecrawl_7k)
- **Description:** Firecrawl web scraping MCP server for crawling and converting web pages to markdown
- **Required Env Vars:** `FIRECRAWL_API_KEY`
- **Run:**
  ```bash
  claude --mcp-config ./mcp-configs/.mcp.json.firecrawl_7k
  ```

## Environment Variable Support

Claude Code supports environment variable interpolation in MCP configs, allowing you to:
- Keep secrets out of version control
- Share configs across teams
- Use machine-specific paths

### Supported Syntax

```bash
${VAR}              # Expands to the value of VAR
${VAR:-default}     # Uses VAR if set, otherwise uses "default"
```

### Where Variables Are Expanded

- `command` - Server executable path
- `args` - Command-line arguments
- `env` - Environment variables passed to the server
- `url` - For HTTP server types
- `headers` - For HTTP authentication

### Example: Using Environment Variables

**Config file (safe to commit):**
```json
{
  "mcpServers": {
    "firecrawl-mcp": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

**Before running Claude Code:**
```bash
# Option 1: Export in your shell
export FIRECRAWL_API_KEY="your-api-key-here"
claude --mcp-config ./mcp-configs/firecrawl.mcp.json

# Option 2: Set inline
FIRECRAWL_API_KEY="your-api-key-here" claude --mcp-config ./mcp-configs/firecrawl.mcp.json

# Option 3: Add to your shell profile (~/.zshrc, ~/.bashrc, etc.)
echo 'export FIRECRAWL_API_KEY="your-api-key-here"' >> ~/.zshrc
```

## Setting Up Your Own Configs

1. **Copy the sample file:**
   ```bash
   cp mcp-configs/firecrawl.mcp.json.sample mcp-configs/firecrawl.mcp.json
   ```

2. **Either:**
   - Set the required environment variables (recommended), OR
   - Replace `${VAR}` placeholders with actual values (not recommended for shared repos)

3. **Since configs use `${VAR}` interpolation:**
   - Configs are safe to commit (no hardcoded secrets)
   - Set required environment variables before running Claude Code

## Best Practices

### For Secrets

1. **Use environment variables** - Never hardcode API keys in config files
2. **Use `.sample` extension** - Keep templates in git, actual configs local
3. **Use `${VAR:-}` with empty default** - Fails clearly if var is not set
4. **Consider using a `.env` file** - Load via `source .env` or direnv

### For Teams

```json
{
  "mcpServers": {
    "team-api": {
      "type": "http",
      "url": "${TEAM_API_URL:-https://api.default.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${TEAM_API_KEY}"
      }
    }
  }
}
```

This allows:
- Different API URLs per environment (dev/staging/prod)
- Each team member uses their own API key
- Safe to commit to version control

## Scope Comparison

| Method | Location | Shared? | Use Case |
|--------|----------|---------|----------|
| `--mcp-config` | Command line | No | One-off sessions, CI/CD |
| Local scope | `~/.claude.json` | No | Personal dev servers |
| Project scope | `.mcp.json` | Yes | Team-shared servers |
| User scope | `~/.claude.json` | No | Cross-project personal tools |

## Additional CLI Options

```bash
# List all configured MCP servers
claude mcp list

# Get details for a specific server
claude mcp get firecrawl-mcp

# Add a server interactively
claude mcp add --transport stdio firecrawl -- npx -y firecrawl-mcp

# Remove a server
claude mcp remove firecrawl-mcp

# Check server status within Claude Code
/mcp
```

## References

- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp.md)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)
- [MCP Servers on GitHub](https://github.com/modelcontextprotocol/servers)
