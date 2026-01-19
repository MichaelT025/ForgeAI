# Getting Started with ForgeAI

## Prerequisites

1. **Windows 10/11** - ForgeAI uses COM API which is Windows-only
2. **SolidWorks 2018+** - Installed and activated
3. **Python 3.10+** - [Download from python.org](https://www.python.org/downloads/)
4. **Claude Desktop** - [Download from Anthropic](https://claude.ai/download)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MichaelT025/ForgeAI.git
cd ForgeAI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -r requirements-dev.txt
```

### 4. Configure Environment (Optional)

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` to customize settings (most defaults work fine).

## Verify Installation

### Test Python Environment

```bash
python -c "import mcp; import win32com.client; print('Dependencies OK')"
```

### Test SolidWorks Connection

Run the connection test script:
```bash
python scripts/test_connection.py
```

## Configure Claude Desktop

ForgeAI uses the MCP stdio transport to communicate with Claude Desktop. You can configure it automatically or manually.

### Automatic Configuration (Recommended)

Run the included installation script:
```bash
python scripts/install_mcp.py
```

### Manual Configuration

If you prefer to configure it manually, edit your Claude Desktop configuration file:

- **Path**: `%AppData%\Roaming\Claude\claude_desktop_config.json`

Add the `forgeai` server to the `mcpServers` section:

```json
{
  "mcpServers": {
    "forgeai": {
      "command": "python",
      "args": ["-m", "core.mcp_server"],
      "cwd": "C:\\\\path\\\\to\\\\ForgeAI\\\\src"
    }
  }
}
```

*Note: Replace `C:\\\\path\\\\to\\\\ForgeAI\\\\src` with the actual absolute path to your cloned repository's `src` folder.*

## Next Steps

Once installation is complete:
1. Restart Claude Desktop
2. Start a new conversation and ask "Can you connect to SolidWorks?"
3. Try creating a simple part: "Create a new part and make a 100x50mm rectangle on the Front Plane"
4. See the [Architecture](./project-structure.md) for more technical details

## Troubleshooting

### Common Issues

**"No module named 'win32com'"**
- Install pywin32: `pip install pywin32`
- Run post-install: `python Scripts/pywin32_postinstall.py -install`

**"SolidWorks not found"**
- Ensure SolidWorks is installed
- Check Windows registry for COM registration
- Try running SolidWorks manually first

**MCP Connection Issues**
- Verify Claude Desktop configuration
- Check stdio transport is configured correctly
- Review logs in `logs/forgeai.log`

For more help, open an issue on GitHub.
