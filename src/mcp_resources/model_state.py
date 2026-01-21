"""MCP resource for SolidWorks model state.

Exposes current model state as a read-only resource at solidworks://model/state.
Clients can query this resource to get information about the current document,
features, sketches, and active sketch.
"""

from typing import Optional

from loguru import logger

from core.mcp_server import mcp
from solidworks.operations import get_model_state


@mcp.resource(
    uri="solidworks://model/state",
    name="ModelState",
    description="Current state of the SolidWorks model including document info, features, sketches, and active sketch.",
    mime_type="application/json",
)
def model_state_resource() -> dict:
    """Get the current state of the SolidWorks model.
    
    Returns a dictionary containing:
    - document: Document info (name, type, path, is_modified)
    - features: List of features in the model
    - sketches: List of sketches in the model
    - active_sketch: Name of the currently active sketch (if any)
    - bounding_box: Model bounding box (if computed)
    - mass_properties: Mass properties (if computed)
    
    If no document is open, returns an error state with null model_state.
    """
    logger.debug("Reading model state resource")
    
    result = get_model_state()
    
    if result.success and result.data:
        return {
            "success": True,
            "model_state": result.data.get("model_state"),
        }
    else:
        return {
            "success": False,
            "message": result.message,
            "model_state": None,
        }
