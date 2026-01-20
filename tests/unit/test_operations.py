"""Unit tests for SolidWorks operations layer.

These tests use mocked COM objects and don't require SolidWorks to be running.
"""

import pytest
from unittest.mock import MagicMock, patch

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
from solidworks.models import PlaneType


# =============================================================================
# Document Operations Tests
# =============================================================================

@pytest.mark.unit
class TestCreateNewDocument:
    """Tests for create_new_document operation."""
    
    def test_create_new_document_success(self, mock_connection, mock_sw_doc):
        """Test successful document creation."""
        result = create_new_document()
        
        assert result.success is True
        assert "Created new part" in result.message
        assert result.data is not None
        assert "document" in result.data
    
    def test_create_new_document_with_template(self, mock_connection, mock_sw_doc):
        """Test document creation with custom template."""
        result = create_new_document(template_path="C:\\custom\\template.prtdot")
        
        assert result.success is True
    
    def test_create_new_document_not_connected(self, mock_connection_disconnected):
        """Test document creation when not connected to SolidWorks."""
        result = create_new_document()
        
        assert result.success is False
        assert "connect" in result.message.lower() or "running" in result.message.lower()


@pytest.mark.unit
class TestSaveDocument:
    """Tests for save_document operation."""
    
    def test_save_document_success(self, mock_connection, mock_sw_doc):
        """Test successful document save."""
        result = save_document("C:\\parts\\test.SLDPRT")
        
        assert result.success is True
        assert "Saved" in result.message
        assert result.data is not None
        assert result.data["path"] == "C:\\parts\\test.SLDPRT"
    
    def test_save_document_adds_extension(self, mock_connection, mock_sw_doc):
        """Test that extension is added if missing."""
        result = save_document("C:\\parts\\test")
        
        assert result.success is True
        assert result.data["path"].endswith(".SLDPRT")
    
    def test_save_document_no_doc_open(self, mock_connection_no_doc):
        """Test save when no document is open."""
        result = save_document("C:\\parts\\test.SLDPRT")
        
        assert result.success is False
        assert "No document" in result.message


# =============================================================================
# Sketch Lifecycle Tests
# =============================================================================

@pytest.mark.unit
class TestSelectPlane:
    """Tests for select_plane operation."""
    
    def test_select_front_plane(self, mock_connection, mock_sw_doc):
        """Test selecting Front Plane."""
        result = select_plane(PlaneType.FRONT)
        
        assert result.success is True
        assert "Front Plane" in result.message
    
    def test_select_top_plane(self, mock_connection, mock_sw_doc):
        """Test selecting Top Plane."""
        result = select_plane(PlaneType.TOP)
        
        assert result.success is True
        assert "Top Plane" in result.message
    
    def test_select_right_plane(self, mock_connection, mock_sw_doc):
        """Test selecting Right Plane."""
        result = select_plane(PlaneType.RIGHT)
        
        assert result.success is True
        assert "Right Plane" in result.message
    
    def test_select_plane_no_doc(self, mock_connection_no_doc):
        """Test selecting plane when no document is open."""
        result = select_plane(PlaneType.FRONT)
        
        assert result.success is False


@pytest.mark.unit
class TestInsertSketch:
    """Tests for insert_sketch operation."""
    
    def test_insert_sketch_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test successful sketch insertion."""
        # Set up mock to return active sketch after insert
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = insert_sketch()
        
        assert result.success is True
        assert "Sketch" in result.message or "sketch" in result.message


@pytest.mark.unit
class TestCreateSketch:
    """Tests for create_sketch operation."""
    
    def test_create_sketch_on_front_plane(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test creating sketch on front plane."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = create_sketch(PlaneType.FRONT)
        
        assert result.success is True


@pytest.mark.unit
class TestExitSketch:
    """Tests for exit_sketch operation."""
    
    def test_exit_sketch_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test exiting sketch successfully."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = exit_sketch()
        
        assert result.success is True


# =============================================================================
# Sketch Entity Tests
# =============================================================================

@pytest.mark.unit
class TestDrawRectangle:
    """Tests for draw_rectangle operation."""
    
    def test_draw_rectangle_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test drawing a rectangle."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_rectangle(center_x=0, center_y=0, width=100, height=50)
        
        assert result.success is True
        assert "100" in result.message and "50" in result.message
    
    def test_draw_rectangle_negative_width(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test that negative width is rejected."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_rectangle(center_x=0, center_y=0, width=-100, height=50)
        
        assert result.success is False
        assert "positive" in result.message.lower()
    
    def test_draw_rectangle_zero_height(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test that zero height is rejected."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_rectangle(center_x=0, center_y=0, width=100, height=0)
        
        assert result.success is False
    
    def test_draw_rectangle_no_active_sketch(self, mock_connection, mock_sw_doc):
        """Test drawing when no sketch is active."""
        mock_sw_doc.SketchManager.ActiveSketch = None
        
        result = draw_rectangle(center_x=0, center_y=0, width=100, height=50)
        
        assert result.success is False
        assert "sketch" in result.message.lower()


@pytest.mark.unit
class TestDrawCircle:
    """Tests for draw_circle operation."""
    
    def test_draw_circle_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test drawing a circle."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_circle(center_x=0, center_y=0, radius=25)
        
        assert result.success is True
        assert "25" in result.message
    
    def test_draw_circle_negative_radius(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test that negative radius is rejected."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_circle(center_x=0, center_y=0, radius=-25)
        
        assert result.success is False
        assert "positive" in result.message.lower()


@pytest.mark.unit
class TestDrawLine:
    """Tests for draw_line operation."""
    
    def test_draw_line_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test drawing a line."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_line(x1=0, y1=0, x2=100, y2=50)
        
        assert result.success is True
        assert "line" in result.message.lower()


@pytest.mark.unit
class TestDrawArc:
    """Tests for draw_arc operation."""
    
    def test_draw_arc_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test drawing an arc."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_arc(
            center_x=0, center_y=0,
            start_x=50, start_y=0,
            end_x=0, end_y=50
        )
        
        assert result.success is True
        assert "arc" in result.message.lower()


@pytest.mark.unit
class TestDrawPolygon:
    """Tests for draw_polygon operation."""
    
    def test_draw_hexagon_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test drawing a hexagon."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_polygon(center_x=0, center_y=0, radius=50, sides=6)
        
        assert result.success is True
        assert "6" in result.message
    
    def test_draw_polygon_too_few_sides(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test that polygons with < 3 sides are rejected."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_polygon(center_x=0, center_y=0, radius=50, sides=2)
        
        assert result.success is False
        assert "3" in result.message


@pytest.mark.unit
class TestDrawSpline:
    """Tests for draw_spline operation."""
    
    def test_draw_spline_success(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test drawing a spline."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        points = [(0, 0), (25, 50), (50, 25), (100, 100)]
        result = draw_spline(points)
        
        assert result.success is True
        assert "4" in result.message  # 4 points
    
    def test_draw_spline_too_few_points(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test that splines with < 2 points are rejected."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        result = draw_spline([(0, 0)])
        
        assert result.success is False
        assert "2" in result.message


# =============================================================================
# Feature Operations Tests
# =============================================================================

@pytest.mark.unit
class TestExtrude:
    """Tests for extrude operation."""
    
    def test_extrude_boss_success(self, mock_connection, mock_sw_doc):
        """Test boss extrusion."""
        result = extrude(depth=25, operation="boss")
        
        assert result.success is True
        assert "25" in result.message
        assert result.feature_name is not None
    
    def test_extrude_cut_success(self, mock_connection, mock_sw_doc):
        """Test cut extrusion."""
        result = extrude(depth=10, operation="cut")
        
        assert result.success is True
        assert "cut" in result.message.lower() or result.data["operation"] == "cut"
    
    def test_extrude_negative_depth(self, mock_connection, mock_sw_doc):
        """Test that negative depth is rejected."""
        result = extrude(depth=-25, operation="boss")
        
        assert result.success is False
        assert "positive" in result.message.lower()
    
    def test_extrude_invalid_operation(self, mock_connection, mock_sw_doc):
        """Test that invalid operation is rejected."""
        result = extrude(depth=25, operation="invalid")
        
        assert result.success is False
        assert "boss" in result.message.lower() or "cut" in result.message.lower()
    
    def test_extrude_invalid_direction(self, mock_connection, mock_sw_doc):
        """Test that invalid direction is rejected."""
        result = extrude(depth=25, direction="invalid")
        
        assert result.success is False


@pytest.mark.unit
class TestFillet:
    """Tests for fillet operation."""
    
    def test_fillet_success(self, mock_connection, mock_sw_doc):
        """Test applying fillet."""
        result = fillet(radius=5)
        
        assert result.success is True
        assert "5" in result.message
    
    def test_fillet_negative_radius(self, mock_connection, mock_sw_doc):
        """Test that negative radius is rejected."""
        result = fillet(radius=-5)
        
        assert result.success is False
        assert "positive" in result.message.lower()
    
    def test_fillet_no_bodies(self, mock_connection, mock_sw_doc):
        """Test fillet when no solid bodies exist."""
        mock_sw_doc.GetBodies2.return_value = None
        
        result = fillet(radius=5)
        
        assert result.success is False
        assert "bodies" in result.message.lower() or "geometry" in result.message.lower()


@pytest.mark.unit
class TestChamfer:
    """Tests for chamfer operation."""
    
    def test_chamfer_success(self, mock_connection, mock_sw_doc):
        """Test applying chamfer."""
        result = chamfer(distance=2)
        
        assert result.success is True
        assert "2" in result.message
    
    def test_chamfer_negative_distance(self, mock_connection, mock_sw_doc):
        """Test that negative distance is rejected."""
        result = chamfer(distance=-2)
        
        assert result.success is False
        assert "positive" in result.message.lower()


# =============================================================================
# Utility Operations Tests
# =============================================================================

@pytest.mark.unit
class TestCaptureScreenshot:
    """Tests for capture_screenshot operation."""
    
    def test_capture_screenshot_success(self, mock_connection, mock_sw_doc):
        """Test capturing screenshot."""
        result = capture_screenshot()
        
        assert result.success is True
    
    def test_capture_screenshot_no_doc(self, mock_connection_no_doc):
        """Test screenshot when no document is open."""
        result = capture_screenshot()
        
        assert result.success is False


@pytest.mark.unit
class TestGetModelState:
    """Tests for get_model_state operation."""
    
    def test_get_model_state_success(self, mock_connection, mock_sw_doc):
        """Test getting model state."""
        result = get_model_state()
        
        assert result.success is True
        assert result.data is not None
        assert "model_state" in result.data
    
    def test_get_model_state_no_doc(self, mock_connection_no_doc):
        """Test model state when no document is open."""
        result = get_model_state()
        
        assert result.success is False
        assert result.data is not None
        assert result.data.get("model_state") is None
