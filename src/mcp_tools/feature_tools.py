"""MCP tools for feature operations.

Provides tools for creating 3D features from sketches in SolidWorks.
"""

from loguru import logger

from core.mcp_server import mcp
from solidworks.operations import (
    capture_screenshot,
    chamfer as chamfer_operation,
    extrude as extrude_operation,
    fillet as fillet_operation,
)


@mcp.tool()
def extrude(depth: float, operation: str = "boss", direction: str = "forward") -> dict:
    """Extrude the last sketch to create 3D geometry.

    Creates a 3D feature by extruding the most recent closed sketch profile.
    The sketch is automatically selected. Close the sketch with close_sketch()
    before calling this tool.

    Args:
        depth: Extrusion depth in mm (must be positive).
        operation: Type of extrusion:
                  - "boss": Add material (default)
                  - "cut": Remove material
        direction: Extrusion direction:
                  - "forward": Extrude in positive normal direction (default)
                  - "backward": Extrude in negative normal direction
                  - "both": Extrude symmetrically (midplane)

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - feature: Name of the created feature (e.g., "Boss-Extrude1")
        - data: Additional info (depth_mm, operation, direction)
        - screenshot: Viewport image data (if available)

    Example:
        >>> extrude(depth=25, operation="boss", direction="forward")
        {"success": True, "message": "Extruded 25mm (boss)", "feature": "Boss-Extrude1", ...}

        >>> extrude(depth=10, operation="cut")
        {"success": True, "message": "Extruded 10mm (cut)", "feature": "Cut-Extrude1", ...}
    """
    # Validate operation
    if operation not in ("boss", "cut"):
        return {
            "success": False,
            "message": f"operation must be 'boss' or 'cut'. Got: {operation}",
        }

    # Validate direction
    if direction not in ("forward", "backward", "both"):
        return {
            "success": False,
            "message": f"direction must be 'forward', 'backward', or 'both'. Got: {direction}",
        }

    logger.info(f"Extruding {depth}mm ({operation}, {direction})")
    result = extrude_operation(depth, operation, direction)

    response: dict = {"success": result.success, "message": result.message}

    if result.feature_name:
        response["feature"] = result.feature_name
    if result.data:
        response["data"] = result.data

    # Take screenshot on success
    if result.success:
        screenshot_result = capture_screenshot()
        if screenshot_result.success and screenshot_result.data:
            response["screenshot"] = screenshot_result.data

    return response


@mcp.tool()
def fillet(radius: float) -> dict:
    """Apply fillet to all edges of the model.

    Creates rounded edges on all edges of the solid body. For V1, edge
    selection is not supported - the fillet is applied to all edges.

    Args:
        radius: Fillet radius in mm (must be positive).
               The radius should be smaller than the smallest edge length.

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - feature: Name of the created feature (e.g., "Fillet1")
        - data: Additional info (radius_mm, edge_count)
        - screenshot: Viewport image data (if available)

    Example:
        >>> fillet(radius=5)
        {"success": True, "message": "Applied 5mm fillet to 12 edges", "feature": "Fillet1", ...}
    """
    logger.info(f"Applying {radius}mm fillet to all edges")
    result = fillet_operation(radius)

    response: dict = {"success": result.success, "message": result.message}

    if result.feature_name:
        response["feature"] = result.feature_name
    if result.data:
        response["data"] = result.data

    # Take screenshot on success
    if result.success:
        screenshot_result = capture_screenshot()
        if screenshot_result.success and screenshot_result.data:
            response["screenshot"] = screenshot_result.data

    return response


@mcp.tool()
def chamfer(distance: float) -> dict:
    """Apply chamfer to all edges of the model.

    Creates beveled edges on all edges of the solid body. For V1, edge
    selection is not supported - the chamfer is applied to all edges.
    Uses equal distance chamfer (45-degree angle).

    Args:
        distance: Chamfer distance in mm (must be positive).
                 The distance should be smaller than the smallest edge length.

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - feature: Name of the created feature (e.g., "Chamfer1")
        - data: Additional info (distance_mm, edge_count)
        - screenshot: Viewport image data (if available)

    Example:
        >>> chamfer(distance=2)
        {"success": True, "message": "Applied 2mm chamfer to 12 edges", "feature": "Chamfer1", ...}
    """
    logger.info(f"Applying {distance}mm chamfer to all edges")
    result = chamfer_operation(distance)

    response: dict = {"success": result.success, "message": result.message}

    if result.feature_name:
        response["feature"] = result.feature_name
    if result.data:
        response["data"] = result.data

    # Take screenshot on success
    if result.success:
        screenshot_result = capture_screenshot()
        if screenshot_result.success and screenshot_result.data:
            response["screenshot"] = screenshot_result.data

    return response
