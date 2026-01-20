"""ForgeAI MCP Server for SolidWorks automation.

This module provides the FastMCP server that exposes SolidWorks operations
to Claude Desktop via the Model Context Protocol.

Usage:
    python -m core.mcp_server
"""

import signal
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional

from loguru import logger

from core.config import get_config
from solidworks.connection import SolidWorksConnection, get_connection

# Import FastMCP from the MCP SDK
from mcp.server.fastmcp import FastMCP


# =============================================================================
# Lifespan Context
# =============================================================================

@dataclass
class ForgeAIContext:
    """Application context with initialized resources."""
    
    connection: SolidWorksConnection
    """SolidWorks COM connection instance."""


@asynccontextmanager
async def forgeai_lifespan(server: FastMCP) -> AsyncIterator[ForgeAIContext]:
    """Manage ForgeAI server lifecycle.
    
    Initializes the SolidWorks COM connection on startup and
    ensures proper cleanup on shutdown.
    
    Yields:
        ForgeAIContext with initialized connection.
    """
    config = get_config()
    logger.info(f"Starting ForgeAI MCP Server v{config.mcp.server_version}")
    
    # Initialize SolidWorks connection
    connection = get_connection()
    
    try:
        # Attempt to connect to SolidWorks
        if connection.connect():
            logger.info("Connected to SolidWorks")
        else:
            logger.warning(
                "Could not connect to SolidWorks. "
                "Make sure SolidWorks is running or will be started when needed."
            )
        
        # Yield context for tools to access
        yield ForgeAIContext(connection=connection)
        
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down ForgeAI MCP Server")
        connection.disconnect()
        logger.info("Disconnected from SolidWorks")


# =============================================================================
# Server Initialization
# =============================================================================

def create_server() -> FastMCP:
    """Create and configure the ForgeAI MCP server.
    
    Returns:
        Configured FastMCP server instance.
    """
    config = get_config()
    
    # Create FastMCP server with lifespan
    mcp = FastMCP(
        name=config.mcp.server_name,
        lifespan=forgeai_lifespan,
    )
    
    logger.debug(f"Created MCP server: {config.mcp.server_name}")
    
    return mcp


# Create the global server instance
mcp = create_server()


# =============================================================================
# Import Tools (registers them with the server via @mcp.tool decorator)
# =============================================================================

# Import tool modules to register them with the MCP server
# Each module uses @mcp.tool() decorator which registers tools at import time
import mcp_tools.document_tools  # noqa: F401, E402 - registers create_new_part, save_part


# =============================================================================
# Signal Handlers
# =============================================================================

def setup_signal_handlers() -> None:
    """Set up graceful shutdown signal handlers."""
    
    def handle_signal(signum: int, frame: Optional[object]) -> None:
        """Handle shutdown signals gracefully."""
        sig_name = signal.Signals(signum).name
        logger.info(f"Received {sig_name}, initiating graceful shutdown...")
        sys.exit(0)
    
    # Handle SIGINT (Ctrl+C) and SIGTERM
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # On Windows, also handle SIGBREAK
    if sys.platform == "win32":
        signal.signal(signal.SIGBREAK, handle_signal)


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Main entry point for the ForgeAI MCP server.
    
    Starts the server using stdio transport for Claude Desktop integration.
    """
    # Configure logging
    config = get_config()
    logger.remove()  # Remove default handler
    
    # Log to stderr to avoid interfering with stdio transport
    logger.add(
        sys.stderr,
        level=config.logging.level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    
    # Add file logging if configured
    if config.logging.log_file:
        logger.add(
            config.logging.log_file,
            level=config.logging.level,
            rotation=config.logging.rotation,
            retention=config.logging.retention,
        )
    
    # Set up signal handlers for graceful shutdown
    setup_signal_handlers()
    
    logger.info(f"ForgeAI MCP Server starting (transport: {config.mcp.transport})")
    
    # Run the server with stdio transport (default for Claude Desktop)
    mcp.run()


if __name__ == "__main__":
    main()
