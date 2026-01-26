# prisme-saas

Prisme Saas - Built with Prism

## Quick Start

```bash
# Install dependencies
uv sync

# Start database
docker-compose -f docker/docker-compose.yml up -d db

# Generate code from spec
prism generate

# Run the API
uvicorn prisme_saas.main:app --reload
```

## API Documentation

- OpenAPI docs: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql

## MCP (Model Context Protocol) Integration

This project includes an MCP server that allows AI assistants to interact with your data.

### Running the MCP Server

```bash
# SSE mode (HTTP server for development)
python -c "from prisme_saas.mcp_server.server import run_server; run_server(transport='sse')"

# stdio mode (for Claude Desktop)
python -c "from prisme_saas.mcp_server.server import run_server; run_server()"
```

### Cursor IDE

Add to your Cursor settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "prisme_saas": {
      "url": "http://localhost:8765/sse"
    }
  }
}
```

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "prisme_saas": {
      "command": "uv",
      "args": ["run", "python", "-c", "from prisme_saas.mcp_server.server import run_server; run_server()"],
      "cwd": "{{ absolute_path_to_project }}"
    }
  }
}
```

Replace `{{ absolute_path_to_project }}` with the actual path to your project.
