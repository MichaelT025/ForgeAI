# ForgeAI Project Structure

```
ForgeAI/
├── src/                        # Source code
│   ├── __init__.py
│   ├── core/                   # Core infrastructure
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logging_config.py  # Logging setup
│   │   └── mcp_server.py      # Planned: MCP server implementation
│   ├── solidworks/            # SolidWorks integration
│   │   ├── __init__.py
│   │   ├── connection.py      # COM API connection
│   │   ├── models.py          # Data models
│   │   └── operations.py      # Planned: SolidWorks operations
│   ├── mcp_tools/             # MCP tool implementations
│   │   ├── __init__.py        # Stub
│   │   ├── base.py            # Planned: Base tool class
│   │   ├── document_tools.py  # Planned: Document operations
│   │   ├── sketch_tools.py    # Planned: Sketch operations
│   │   └── feature_tools.py   # Planned: Feature operations
│   └── mcp_resources/         # MCP resource implementations
│       ├── __init__.py        # Stub
│       ├── base.py            # Planned: Base resource class
│       ├── model_state.py     # Planned: Model state resource
│       └── screenshot.py      # Planned: Screenshot resource
├── tests/                     # Planned: Test suite
│   ├── __init__.py
│   ├── unit/                  # Planned: Mocked tests
│   └── integration/           # Planned: Real SolidWorks tests
├── scripts/                   # Utility scripts
│   ├── test_connection.py     # Test SolidWorks connection
│   └── install_mcp.py         # Claude Desktop setup
├── docs/                      # Documentation
│   ├── getting-started.md     # Existing
│   ├── project-structure.md   # Existing
│   ├── architecture.md        # Planned
│   └── api-reference.md       # Planned
├── data/                      # Planned: Runtime data
│   └── screenshots/           # Planned: Generated screenshots
├── config/                    # Planned: Configuration files
│   └── settings.toml          # Planned: Default settings
├── local_resources/           # Planning (not in git)
│   ├── plan.md
│   └── checklist.md
├── .env.example               # Environment template
├── .gitignore
├── pyproject.toml            # Project configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── README.md
```

## Key Modules

### `src/core/`
Core infrastructure shared across the project.

- **config.py** - Configuration management using Pydantic (Implemented)
- **logging_config.py** - Logging setup with loguru (Implemented)
- **mcp_server.py** - Main MCP server implementation (Planned)

### `src/solidworks/`
SolidWorks COM API integration layer.

- **connection.py** - Manages connection to SolidWorks via COM (Implemented)
- **models.py** - Pydantic models for SolidWorks entities (Implemented)
- **operations.py** - Low-level SolidWorks operations (Planned)

### `src/mcp_tools/`
MCP tool implementations (AI-callable functions).

- **base.py** - Base tool class with common functionality (Planned)
- **document_tools.py** - Tools for document operations (Planned)
- **sketch_tools.py** - Tools for sketch operations (Planned)
- **feature_tools.py** - Tools for features (Planned)

### `src/mcp_resources/`
MCP resource implementations (AI-readable state).

- **base.py** - Base resource class (Planned)
- **model_state.py** - Exposes current SolidWorks model state (Planned)
- **screenshot.py** - Viewport capture as PNG (Planned)

## Adding New Features


### New Tool
1. Create tool class in appropriate file under `mcp_tools/`
2. Inherit from base tool class
3. Define input schema with Pydantic
4. Implement `execute()` method
5. Register tool in MCP server
6. Add tests in `tests/`

### New Resource
1. Create resource class in `mcp_resources/`
2. Inherit from base resource class
3. Define resource URI and schema
4. Implement state extraction logic
5. Register resource in MCP server

## Development Workflow

1. **Feature Branch** - Create branch for new feature
2. **Implementation** - Write code following structure
3. **Testing** - Add tests, ensure they pass
4. **Documentation** - Update relevant docs
5. **PR** - Submit pull request for review
