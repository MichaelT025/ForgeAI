"""Utility script to install ForgeAI MCP server in Claude Desktop.

This script configures Claude Desktop to use ForgeAI as an MCP server.

Usage:
    python scripts/install_mcp.py
"""

import json
import sys
from pathlib import Path

# Claude Desktop config location
CLAUDE_CONFIG_DIR = Path.home() / "AppData" / "Roaming" / "Claude"
CLAUDE_CONFIG_FILE = CLAUDE_CONFIG_DIR / "claude_desktop_config.json"


def main():
    """Install ForgeAI MCP server configuration."""
    print("=" * 60)
    print("ForgeAI - Claude Desktop MCP Installation")
    print("=" * 60)
    print()
    
    # Get ForgeAI project path
    project_root = Path(__file__).parent.parent.resolve()
    venv_python = project_root / "venv" / "Scripts" / "python.exe"
    
    if not venv_python.exists():
        print("✗ Virtual environment not found!")
        print(f"  Expected: {venv_python}")
        print("\nPlease create a virtual environment first:")
        print("  python -m venv venv")
        print("  venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        return 1
    
    # MCP server configuration
    mcp_config = {
        "mcpServers": {
            "forgeai": {
                "command": str(venv_python),
                "args": [
                    "-m",
                    "core.mcp_server"
                ],
                "cwd": str(project_root / "src"),
                "env": {}
            }
        }
    }
    
    # Check if Claude config exists
    if not CLAUDE_CONFIG_DIR.exists():
        print("✗ Claude Desktop config directory not found!")
        print(f"  Expected: {CLAUDE_CONFIG_DIR}")
        print("\nPlease install Claude Desktop first:")
        print("  https://claude.ai/download")
        return 1
    
    # Load existing config or create new
    if CLAUDE_CONFIG_FILE.exists():
        print(f"Found existing config: {CLAUDE_CONFIG_FILE}")
        try:
            with open(CLAUDE_CONFIG_FILE, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("⚠ Warning: Existing config is invalid, creating new one")
            config = {}
    else:
        print("Creating new config file...")
        config = {}
    
    # Merge configurations
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["forgeai"] = mcp_config["mcpServers"]["forgeai"]
    
    # Write config
    try:
        with open(CLAUDE_CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        print(f"✓ Configuration written to: {CLAUDE_CONFIG_FILE}")
    except Exception as e:
        print(f"✗ Failed to write config: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("Installation Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Restart Claude Desktop")
    print("2. Look for 'forgeai' in the MCP servers list")
    print("3. Start a conversation and try: 'Can you connect to SolidWorks?'")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
