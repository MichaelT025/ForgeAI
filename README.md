# ForgeAI

AI-powered conversational assistant for SolidWorks CAD automation using the Model Context Protocol (MCP).

## What is ForgeAI?

ForgeAI lets you design SolidWorks parts through natural language conversation. Instead of clicking through menus and remembering commands, you describe what you want to build and ForgeAI executes the CAD operations.

**Example:**
```
You: "Create a 100x50x25mm box on the front plane"
ForgeAI: ✓ Created sketch on Front plane
         ✓ Added 100x50mm rectangle
         ✓ Extruded 25mm

You: "Add 5mm fillets to all edges"
ForgeAI: ✓ Applied 5mm fillets to 12 edges
```

## Architecture

```
┌─────────────────┐     stdio      ┌─────────────────┐     COM API     ┌─────────────────┐
│  Claude Desktop │◄──────────────►│  ForgeAI MCP    │◄───────────────►│   SolidWorks    │
│   (AI Client)   │                │    Server       │                 │                 │
└─────────────────┘                └─────────────────┘                 └─────────────────┘
                                           │
                                           ▼
                                    ┌─────────────────┐
                                    │   Screenshots   │
                                    │   (feedback)    │
                                    └─────────────────┘
```

- **MCP Server**: Python-based server exposing SolidWorks operations as tools
- **SolidWorks Integration**: COM API automation via pywin32
- **AI Client**: Claude Desktop

## Status

Phase 1: Foundation

The project is currently implementing the core part modeling capabilities defined in the V1 roadmap.

## V1 Features

### Document Operations
- `create_new_part`: Create a new blank part document
- `save_part`: Save current document to specified path

### Sketch Operations
- `create_sketch`: Start a new sketch on a plane (Front/Top/Right)
- `close_sketch`: Exit sketch mode
- `draw_rectangle`: Draw a center rectangle
- `draw_circle`: Draw a circle
- `draw_line`: Draw a line between two points
- `draw_arc`: Draw a three-point arc
- `draw_polygon`: Draw a regular polygon
- `draw_spline`: Draw a spline through specified points

### Feature Operations
- `extrude`: Extrude sketch (boss or cut)
- `fillet`: Apply fillet to edges
- `chamfer`: Apply chamfer to edges

### Resources (Read-Only)
- `model_state`: Current features, sketches, and active sketch info
- `screenshot`: Current viewport as PNG image

## Claude Desktop Setup

ForgeAI operates as an MCP server using the standard input/output (stdio) transport. To use it with Claude Desktop, add the server configuration to your `claude_desktop_config.json` file.

```json
{
  "mcpServers": {
    "forgeai": {
      "command": "python",
      "args": ["-m", "core.mcp_server"],
      "cwd": "C:\\path\\to\\ForgeAI\\src"
    }
  }
}
```

See [Getting Started](docs/getting-started.md) for detailed setup instructions, or run `python scripts/install_mcp.py` for automatic configuration.

## Requirements

- Windows 10/11
- SolidWorks 2018+
- Python 3.10+
- Claude Desktop

## License

MIT

---

*Project started January 2026*

