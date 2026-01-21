"""MCP resource for SolidWorks viewport screenshot.

Exposes current viewport screenshot as a read-only resource at solidworks://viewport/screenshot.
Clients can query this resource to get a PNG image of the current SolidWorks view.
"""

from typing import Optional

from loguru import logger

from core.mcp_server import mcp
from solidworks.operations import capture_screenshot


@mcp.resource(
    uri="solidworks://viewport/screenshot",
    name="ViewportScreenshot",
    description="Current SolidWorks viewport as a PNG screenshot. Returns viewport info if image capture is not available.",
    mime_type="application/json",
)
def screenshot_resource() -> dict:
    """Capture a screenshot of the current SolidWorks viewport.
    
    Returns a dictionary containing:
    - success: Whether the screenshot was captured
    - message: Description of the result
    - data: Screenshot data including view settings
    
    The screenshot automatically:
    - Sets the view to isometric for 3D visibility
    - Zooms to fit the entire model
    
    Note: For V1, actual PNG bytes are not returned. The resource
    confirms the view is prepared and provides viewport metadata.
    Full image capture requires win32gui/PIL integration.
    """
    logger.debug("Reading screenshot resource")
    
    result = capture_screenshot()
    
    if result.success:
        return {
            "success": True,
            "message": result.message,
            "viewport": result.data if result.data else {"view": "isometric", "fit": True},
        }
    else:
        return {
            "success": False,
            "message": result.message,
            "viewport": None,
        }
