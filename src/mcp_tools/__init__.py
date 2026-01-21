"""MCP tool implementations for SolidWorks operations."""

from mcp_tools.document_tools import create_new_part, save_part
from mcp_tools.feature_tools import chamfer, extrude, fillet
from mcp_tools.sketch_tools import (
    close_sketch,
    create_sketch,
    draw_arc,
    draw_circle,
    draw_line,
    draw_polygon,
    draw_rectangle,
    draw_spline,
)

__all__ = [
    # Document tools
    "create_new_part",
    "save_part",
    # Sketch tools
    "create_sketch",
    "close_sketch",
    "draw_rectangle",
    "draw_circle",
    "draw_line",
    "draw_arc",
    "draw_polygon",
    "draw_spline",
    # Feature tools
    "extrude",
    "fillet",
    "chamfer",
]
