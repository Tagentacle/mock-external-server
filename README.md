# mock-external-server

Mock MCP Server for testing `mcp-gateway` relay and directory functionality.

## Tools

| Tool | Description |
|------|-------------|
| `echo(text)` | Return input text unchanged |
| `get_time()` | Return current UTC time (ISO 8601) |
| `add(a, b)` | Add two numbers |

## Usage

**stdio** (for gateway relay testing):
```bash
python mock_server.py
```

**HTTP** (for gateway remote directory testing):
```bash
python mock_server.py --http 8400
```

## License

MIT
