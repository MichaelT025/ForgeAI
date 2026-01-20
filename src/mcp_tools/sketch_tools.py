"""MCP tools for sketch operations.

Provides tools for creating sketches and drawing sketch entities in SolidWorks.
"""

from typing import Any, List, Optional, Sequence, Tuple

from loguru import logger

from core.mcp_server import mcp
from solidworks.models import PlaneType
from solidworks.operations import (
    capture_screenshot,
    create_sketch as create_sketch_operation,
    draw_arc as draw_arc_operation,
    draw_circle as draw_circle_operation,
    draw_line as draw_line_operation,
    draw_polygon as draw_polygon_operation,
    draw_rectangle as draw_rectangle_operation,
    draw_spline as draw_spline_operation,
    exit_sketch,
)


def _parse_plane(plane: str) -> Tuple[Optional[PlaneType], Optional[str]]:
    if not plane:
        return None, "plane is required. Use Front, Top, or Right."

    normalized = plane.strip().lower()
    plane_map = {
        "front": PlaneType.FRONT,
        "front plane": PlaneType.FRONT,
        "top": PlaneType.TOP,
        "top plane": PlaneType.TOP,
        "right": PlaneType.RIGHT,
        "right plane": PlaneType.RIGHT,
    }
    if normalized not in plane_map:
        return None, "Invalid plane. Use Front, Top, or Right."

    return plane_map[normalized], None


def _coerce_point(point: Any) -> Optional[Tuple[float, float]]:
    if isinstance(point, dict):
        if "x" in point and "y" in point:
            return float(point["x"]), float(point["y"])
        return None

    if isinstance(point, (list, tuple)) and len(point) >= 2:
        return float(point[0]), float(point[1])

    return None


def _normalize_points(points: Sequence[Any]) -> Tuple[Optional[List[Tuple[float, float]]], Optional[str]]:
    if not points:
        return None, "points is required. Provide at least 2 points with x/y coordinates."

    parsed: List[Tuple[float, float]] = []
    for point in points:
        parsed_point = _coerce_point(point)
        if parsed_point is None:
            return None, "Each point must be a dict with x/y or a list/tuple of [x, y]."
        parsed.append(parsed_point)

    if len(parsed) < 2:
        return None, "Spline requires at least 2 points."

    return parsed, None


@mcp.tool()
def create_sketch(plane: str) -> dict:
    """Create a new sketch on a reference plane.

    Starts a new sketch on the specified reference plane. A part document
    must be open before calling this tool. Use close_sketch() when done
    adding sketch entities.

    Args:
        plane: Reference plane name. Valid values: "Front", "Top", or "Right".
               Also accepts "Front Plane", "Top Plane", "Right Plane".

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - sketch: Name of the created sketch (e.g., "Sketch1")

    Example:
        >>> create_sketch(plane="Front")
        {"success": True, "message": "Started sketch: Sketch1", "sketch": "Sketch1"}
    """
    plane_type, error = _parse_plane(plane)
    if error or plane_type is None:
        return {"success": False, "message": error or "Invalid plane."}

    logger.info(f"Creating sketch on plane: {plane_type.value}")
    result = create_sketch_operation(plane_type)

    response: dict = {"success": result.success, "message": result.message}
    if result.feature_name:
        response["sketch"] = result.feature_name

    return response


@mcp.tool()
def close_sketch() -> dict:
    """Exit the active sketch and rebuild the model.

    Closes the currently active sketch and rebuilds the model to apply
    any changes. If no sketch is active, this is a no-op that returns success.

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - sketch: Name of the closed sketch (if available)
        - screenshot: Viewport image data (if available)

    Example:
        >>> close_sketch()
        {"success": True, "message": "Closed sketch: Sketch1", "sketch": "Sketch1", ...}
    """
    logger.info("Closing active sketch")
    result = exit_sketch()

    response: dict = {"success": result.success, "message": result.message}
    if result.feature_name:
        response["sketch"] = result.feature_name

    if result.success:
        screenshot_result = capture_screenshot()
        if screenshot_result.success and screenshot_result.data:
            response["screenshot"] = screenshot_result.data

    return response


@mcp.tool()
def draw_rectangle(center_x: float, center_y: float, width: float, height: float) -> dict:
    """Draw a center rectangle in the active sketch.

    Draws a rectangle centered at the specified coordinates with the given
    dimensions. All measurements are in millimeters.

    Args:
        center_x: Center X coordinate in mm.
        center_y: Center Y coordinate in mm.
        width: Rectangle width in mm (must be positive).
        height: Rectangle height in mm (must be positive).

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - data: Additional info (width_mm, height_mm)

    Example:
        >>> draw_rectangle(center_x=0, center_y=0, width=100, height=50)
        {"success": True, "message": "Drew 100x50mm rectangle at (0, 0)", ...}
    """
    logger.info(f"Drawing rectangle {width}x{height} at ({center_x}, {center_y})")
    result = draw_rectangle_operation(center_x, center_y, width, height)
    response: dict = {"success": result.success, "message": result.message}
    if result.data:
        response["data"] = result.data
    return response


@mcp.tool()
def draw_circle(center_x: float, center_y: float, radius: float) -> dict:
    """Draw a circle in the active sketch.

    Draws a circle centered at the specified coordinates with the given radius.
    All measurements are in millimeters.

    Args:
        center_x: Center X coordinate in mm.
        center_y: Center Y coordinate in mm.
        radius: Circle radius in mm (must be positive).

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - data: Additional info (radius_mm)

    Example:
        >>> draw_circle(center_x=0, center_y=0, radius=25)
        {"success": True, "message": "Drew circle with radius 25mm at (0, 0)", ...}
    """
    logger.info(f"Drawing circle radius {radius} at ({center_x}, {center_y})")
    result = draw_circle_operation(center_x, center_y, radius)
    response: dict = {"success": result.success, "message": result.message}
    if result.data:
        response["data"] = result.data
    return response


@mcp.tool()
def draw_line(x1: float, y1: float, x2: float, y2: float) -> dict:
    """Draw a line between two points in the active sketch.

    Draws a straight line from point (x1, y1) to point (x2, y2).
    All measurements are in millimeters.

    Args:
        x1: Start X coordinate in mm.
        y1: Start Y coordinate in mm.
        x2: End X coordinate in mm.
        y2: End Y coordinate in mm.

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - data: Additional info (length_mm)

    Example:
        >>> draw_line(x1=0, y1=0, x2=100, y2=50)
        {"success": True, "message": "Drew line from (0, 0) to (100, 50) mm", ...}
    """
    logger.info(f"Drawing line from ({x1}, {y1}) to ({x2}, {y2})")
    result = draw_line_operation(x1, y1, x2, y2)
    response: dict = {"success": result.success, "message": result.message}
    if result.data:
        response["data"] = result.data
    return response


@mcp.tool()
def draw_arc(
    center_x: float,
    center_y: float,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
) -> dict:
    """Draw an arc in the active sketch.

    Draws an arc defined by a center point and start/end points.
    All measurements are in millimeters.

    Args:
        center_x: Center X coordinate in mm.
        center_y: Center Y coordinate in mm.
        start_x: Start point X coordinate in mm.
        start_y: Start point Y coordinate in mm.
        end_x: End point X coordinate in mm.
        end_y: End point Y coordinate in mm.

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - data: Additional info (center coordinates)

    Example:
        >>> draw_arc(center_x=0, center_y=0, start_x=10, start_y=0, end_x=0, end_y=10)
        {"success": True, "message": "Drew arc from (10, 0) to (0, 10) centered at (0, 0)", ...}
    """
    logger.info(f"Drawing arc with center ({center_x}, {center_y})")
    result = draw_arc_operation(center_x, center_y, start_x, start_y, end_x, end_y)
    response: dict = {"success": result.success, "message": result.message}
    if result.data:
        response["data"] = result.data
    return response


@mcp.tool()
def draw_polygon(center_x: float, center_y: float, radius: float, sides: int) -> dict:
    """Draw a regular polygon in the active sketch.

    Draws a regular polygon (equilateral, equiangular) inscribed in a circle
    with the specified radius. All measurements are in millimeters.

    Args:
        center_x: Center X coordinate in mm.
        center_y: Center Y coordinate in mm.
        radius: Circumscribed circle radius in mm (distance from center to vertices).
        sides: Number of sides (must be at least 3).

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - data: Additional info (sides, radius_mm)

    Example:
        >>> draw_polygon(center_x=0, center_y=0, radius=50, sides=6)
        {"success": True, "message": "Drew 6-sided polygon with radius 50mm at (0, 0)", ...}
    """
    logger.info(f"Drawing {sides}-sided polygon with radius {radius} at ({center_x}, {center_y})")
    result = draw_polygon_operation(center_x, center_y, radius, sides)
    response: dict = {"success": result.success, "message": result.message}
    if result.data:
        response["data"] = result.data
    return response


@mcp.tool()
def draw_spline(points: Sequence[Any]) -> dict:
    """Draw a spline through the provided points.

    Draws a smooth spline curve passing through the specified control points.
    All measurements are in millimeters.

    Args:
        points: List of points. Each point can be:
               - A dict with "x" and "y" keys: {"x": 0, "y": 0}
               - A list/tuple: [0, 0] or (0, 0)
               Minimum 2 points required.

    Returns:
        Dictionary with:
        - success: Whether the operation succeeded
        - message: Description of the result
        - data: Additional info (point_count)

    Example:
        >>> draw_spline(points=[{"x": 0, "y": 0}, {"x": 50, "y": 25}, {"x": 100, "y": 0}])
        {"success": True, "message": "Drew spline through 3 points", ...}
    """
    normalized_points, error = _normalize_points(points)
    if error or normalized_points is None:
        return {"success": False, "message": error or "Invalid points."}

    logger.info(f"Drawing spline through {len(normalized_points)} points")
    result = draw_spline_operation(normalized_points)
    response: dict = {"success": result.success, "message": result.message}
    if result.data:
        response["data"] = result.data
    return response
