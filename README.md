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
Claude Desktop ◄─MCP─► ForgeAI Server ◄─COM─► SolidWorks
```

- **MCP Server**: Python-based server exposing SolidWorks operations as tools
- **SolidWorks Integration**: COM API automation via pywin32
- **AI Client**: Claude Desktop (or custom UI later)

## Goals

- Natural language CAD modeling
- Real-time operation execution
- Intelligent validation and safety checks
- Visual feedback with screenshots
- Design pattern recognition

## Status

🚧 **Under Active Development** - Phase 1: Foundation

See [local_resources/plan.md](local_resources/plan.md) for detailed planning and [local_resources/checklist.md](local_resources/checklist.md) for progress tracking.

## Requirements

- Windows 10/11
- SolidWorks 2018+
- Python 3.10+
- Claude Desktop or Anthropic API key

## License

MIT

---

*Project started December 2025*
