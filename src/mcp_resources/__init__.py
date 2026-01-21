"""MCP resource implementations for SolidWorks state.

This module exposes SolidWorks data as MCP resources:
- model_state: Current model state (document, features, sketches)
- screenshot: Viewport screenshot/metadata
"""

from mcp_resources.model_state import model_state_resource
from mcp_resources.screenshot import screenshot_resource

__all__ = ["model_state_resource", "screenshot_resource"]
