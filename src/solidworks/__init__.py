"""SolidWorks COM API integration modules."""

from solidworks.connection import SolidWorksConnection, get_connection, reset_connection
from solidworks.models import (
    DocumentType,
    PlaneType,
    SketchEntityType,
    FeatureType,
    OperationResult,
    DocumentInfo,
    ModelState,
    mm_to_m,
    m_to_mm,
)
from solidworks.operations import (
    # Document operations
    create_new_document,
    save_document,
    # Sketch lifecycle
    select_plane,
    insert_sketch,
    create_sketch,
    exit_sketch,
    # Sketch entities
    draw_rectangle,
    draw_circle,
    draw_line,
    draw_arc,
    draw_polygon,
    draw_spline,
    # Features
    extrude,
    fillet,
    chamfer,
    # Utilities
    capture_screenshot,
    get_model_state,
)

__all__ = [
    # Connection
    "SolidWorksConnection",
    "get_connection",
    "reset_connection",
    # Models
    "DocumentType",
    "PlaneType",
    "SketchEntityType",
    "FeatureType",
    "OperationResult",
    "DocumentInfo",
    "ModelState",
    "mm_to_m",
    "m_to_mm",
    # Operations - Document
    "create_new_document",
    "save_document",
    # Operations - Sketch lifecycle
    "select_plane",
    "insert_sketch",
    "create_sketch",
    "exit_sketch",
    # Operations - Sketch entities
    "draw_rectangle",
    "draw_circle",
    "draw_line",
    "draw_arc",
    "draw_polygon",
    "draw_spline",
    # Operations - Features
    "extrude",
    "fillet",
    "chamfer",
    # Operations - Utilities
    "capture_screenshot",
    "get_model_state",
]
