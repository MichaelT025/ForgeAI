"""MCP tools for document operations.

Provides tools for creating and saving SolidWorks part documents.
These tools are registered with the MCP server and can be called
by Claude Desktop.
"""

from typing import Optional

from loguru import logger

from core.mcp_server import mcp
from solidworks.operations import (
    create_new_document,
    save_document,
    capture_screenshot,
)


@mcp.tool()
def create_new_part(template_path: Optional[str] = None) -> dict:
    """Create a new SolidWorks part document.
    
    Opens a new, empty part document in SolidWorks. This must be called
    before using any sketch or feature tools.
    
    Args:
        template_path: Optional path to a custom part template file (.prtdot).
                      If not provided, uses the default SolidWorks template.
    
    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - document: Document info (name, type, path)
        - screenshot: Base64-encoded PNG of the viewport (if available)
    
    Example:
        >>> create_new_part()
        {"success": True, "message": "Created new part: Part1", ...}
        
        >>> create_new_part(template_path="C:\\templates\\metric.prtdot")
        {"success": True, "message": "Created new part: Part1", ...}
    """
    logger.info(f"Creating new part (template: {template_path or 'default'})")
    
    # Create the document using operations layer
    result = create_new_document(template_path)
    
    response = {
        "success": result.success,
        "message": result.message,
    }
    
    if result.success and result.data:
        response["document"] = result.data.get("document")
        
        # Take screenshot of the new document
        screenshot_result = capture_screenshot()
        if screenshot_result.success and screenshot_result.data:
            response["screenshot"] = screenshot_result.data
    
    return response


@mcp.tool()
def save_part(file_path: str) -> dict:
    """Save the current part document to a file.
    
    Saves the active part document to the specified file path.
    The file extension .SLDPRT will be added automatically if not present.
    
    Args:
        file_path: Full path where to save the file.
                  Example: "C:\\parts\\mypart.SLDPRT" or "C:\\parts\\mypart"
    
    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - path: The full path where the file was saved
    
    Raises:
        Error if no document is open or path is not writable.
    
    Example:
        >>> save_part(file_path="C:\\parts\\bracket.SLDPRT")
        {"success": True, "message": "Saved to: C:\\parts\\bracket.SLDPRT", ...}
    """
    if not file_path:
        return {
            "success": False,
            "message": "file_path is required. Provide a full path like 'C:\\parts\\mypart.SLDPRT'"
        }
    
    logger.info(f"Saving part to: {file_path}")
    
    # Save the document using operations layer
    result = save_document(file_path)
    
    response = {
        "success": result.success,
        "message": result.message,
    }
    
    if result.success and result.data:
        response["path"] = result.data.get("path")
    
    return response
