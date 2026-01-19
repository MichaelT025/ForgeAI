"""Data models for SolidWorks entities."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """SolidWorks document types."""
    PART = "part"
    ASSEMBLY = "assembly"
    DRAWING = "drawing"
    UNKNOWN = "unknown"


class PlaneType(str, Enum):
    """Standard reference planes."""
    FRONT = "Front Plane"
    TOP = "Top Plane"
    RIGHT = "Right Plane"


class SketchEntityType(str, Enum):
    """Types of sketch entities."""
    LINE = "line"
    CIRCLE = "circle"
    ARC = "arc"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"
    SPLINE = "spline"
    POINT = "point"


class FeatureType(str, Enum):
    """Types of SolidWorks features."""
    EXTRUDE_BOSS = "extrude_boss"
    EXTRUDE_CUT = "extrude_cut"
    REVOLVE_BOSS = "revolve_boss"
    REVOLVE_CUT = "revolve_cut"
    FILLET = "fillet"
    CHAMFER = "chamfer"
    HOLE = "hole"
    PATTERN = "pattern"
    MIRROR = "mirror"


class Point3D(BaseModel):
    """3D point coordinates."""
    x: float = Field(description="X coordinate in meters")
    y: float = Field(description="Y coordinate in meters")
    z: float = Field(description="Z coordinate in meters")


class BoundingBox(BaseModel):
    """3D bounding box."""
    min_point: Point3D = Field(description="Minimum corner point")
    max_point: Point3D = Field(description="Maximum corner point")
    
    @property
    def width(self) -> float:
        """Width (X dimension) in meters."""
        return self.max_point.x - self.min_point.x
    
    @property
    def height(self) -> float:
        """Height (Y dimension) in meters."""
        return self.max_point.y - self.min_point.y
    
    @property
    def depth(self) -> float:
        """Depth (Z dimension) in meters."""
        return self.max_point.z - self.min_point.z


class MassProperties(BaseModel):
    """Mass properties of a model."""
    mass: float = Field(description="Mass in kilograms")
    volume: float = Field(description="Volume in cubic meters")
    surface_area: float = Field(description="Surface area in square meters")
    center_of_mass: Point3D = Field(description="Center of mass coordinates")


class SketchInfo(BaseModel):
    """Information about a sketch."""
    name: str = Field(description="Sketch name")
    plane: str = Field(description="Reference plane or face")
    entity_count: int = Field(description="Number of sketch entities")
    is_fully_defined: bool = Field(description="Whether sketch is fully defined")


class FeatureInfo(BaseModel):
    """Information about a feature."""
    name: str = Field(description="Feature name")
    type: str = Field(description="Feature type")
    is_suppressed: bool = Field(default=False, description="Whether feature is suppressed")


class DocumentInfo(BaseModel):
    """Information about a SolidWorks document."""
    name: str = Field(description="Document name")
    type: DocumentType = Field(description="Document type")
    path: Optional[str] = Field(default=None, description="File path if saved")
    is_modified: bool = Field(default=False, description="Whether document has unsaved changes")


class ModelState(BaseModel):
    """Current state of a SolidWorks model."""
    document: DocumentInfo = Field(description="Document information")
    bounding_box: Optional[BoundingBox] = Field(default=None, description="Model bounding box")
    mass_properties: Optional[MassProperties] = Field(default=None, description="Mass properties")
    features: List[FeatureInfo] = Field(default_factory=list, description="List of features")
    sketches: List[SketchInfo] = Field(default_factory=list, description="List of sketches")
    active_sketch: Optional[str] = Field(default=None, description="Name of active sketch")


class SketchRectangle(BaseModel):
    """Rectangle sketch entity parameters."""
    center_x: float = Field(description="Center X coordinate in mm")
    center_y: float = Field(description="Center Y coordinate in mm")
    width: float = Field(gt=0, description="Width in mm")
    height: float = Field(gt=0, description="Height in mm")


class SketchCircle(BaseModel):
    """Circle sketch entity parameters."""
    center_x: float = Field(description="Center X coordinate in mm")
    center_y: float = Field(description="Center Y coordinate in mm")
    radius: float = Field(gt=0, description="Radius in mm")


class ExtrudeParameters(BaseModel):
    """Parameters for extrude operation."""
    depth: float = Field(gt=0, description="Extrusion depth in mm")
    direction: str = Field(
        default="forward",
        description="Extrusion direction: forward, backward, or both"
    )
    operation: str = Field(
        default="boss",
        description="Operation type: boss (add material) or cut (remove material)"
    )


class FilletParameters(BaseModel):
    """Parameters for fillet operation."""
    radius: float = Field(gt=0, description="Fillet radius in mm")
    edges: Optional[List[int]] = Field(
        default=None,
        description="Edge IDs to fillet. If None, applies to all edges."
    )


class OperationResult(BaseModel):
    """Result of a SolidWorks operation."""
    success: bool = Field(description="Whether operation succeeded")
    message: str = Field(description="Result message")
    feature_name: Optional[str] = Field(default=None, description="Name of created feature")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional result data")


# Unit conversion helpers
MM_TO_M = 0.001
M_TO_MM = 1000.0


def mm_to_m(value: float) -> float:
    """Convert millimeters to meters."""
    return value * MM_TO_M


def m_to_mm(value: float) -> float:
    """Convert meters to millimeters."""
    return value * M_TO_MM
