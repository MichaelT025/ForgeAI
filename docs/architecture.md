## ForgeAI Architecture

### Overview
ForgeAI is an MCP (Model Context Protocol) server that bridges Claude Desktop and SolidWorks, enabling natural language CAD modeling. It translates plain English descriptions into precise SolidWorks operations through a robust automation layer.

### System Diagram
```
┌─────────────────┐     stdio      ┌─────────────────┐     COM API     ┌─────────────────┐
│  Claude Desktop │◄──────────────►│  ForgeAI MCP    │◄───────────────►│   SolidWorks    │
│   (AI Client)   │                │    Server       │                 │                 │
└─────────────────┘                └─────────────────┘                 └─────────────────┘
```

### Technology Stack
| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| MCP Framework | `mcp` (FastMCP) |
| COM Automation | `pywin32` |
| Data Validation | `pydantic` |
| Logging | `loguru` |
| Testing | `pytest` |

### Layer Architecture
- **MCP Layer**: Handles the MCP protocol, tool definitions, and resource handlers. It manages the interface with Claude Desktop.
- **Operations Layer**: Contains business logic, manages state, and performs unit conversion (converting user-provided millimeters to SolidWorks internal meters).
- **COM Layer**: Directly interfaces with the SolidWorks API using the `pywin32` library to execute CAD commands.

### Key Design Decisions
1. **Unit Handling**: To ensure user-friendliness, all tool inputs accept millimeters. These are converted to meters (the SolidWorks internal unit system) within the operations layer.
2. **Screenshot Feedback**: To provide visual confirmation of actions, every modifying operation returns a text result accompanied by a viewport screenshot.
3. **Lifespan Management**: For performance and stability, the SolidWorks COM connection is established once at server startup and reused across all operations.
4. **Error Strategy**: Descriptive and actionable error messages are returned to Claude, allowing the AI to understand failures and decide on a recovery approach.

### Data Flow
1. **User**: Provides a natural language instruction (e.g., "Create a 100mm cube").
2. **Claude Desktop**: Parses the intent and calls the appropriate MCP tool.
3. **MCP Server**: Receives the tool call via stdio.
4. **Operations Layer**: Validates inputs, converts units, and prepares the operation.
5. **COM Layer**: Executes the low-level API calls in SolidWorks.
6. **SolidWorks**: Performs the CAD operation and updates the model.
7. **Feedback**: The server captures a screenshot and returns success/failure status back through the layers to Claude.
