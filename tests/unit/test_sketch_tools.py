"""Unit tests for sketch tools.

These tests use mocked operations and don't require SolidWorks to be running.
"""

from unittest.mock import patch

import pytest

from solidworks.models import OperationResult, PlaneType


@pytest.mark.unit
class TestCreateSketchTool:
    """Tests for create_sketch tool."""

    def test_create_sketch_on_front_plane(self):
        """Test successful sketch creation on Front plane."""
        mock_result = OperationResult(
            success=True,
            message="Started sketch: Sketch1",
            feature_name="Sketch1",
        )

        with patch("mcp_tools.sketch_tools.create_sketch_operation", return_value=mock_result) as mock_create:
            from mcp_tools.sketch_tools import create_sketch

            result = create_sketch("Front")

            assert result["success"] is True
            assert "Sketch" in result["message"]
            assert result["sketch"] == "Sketch1"
            mock_create.assert_called_once_with(PlaneType.FRONT)

    def test_create_sketch_on_top_plane(self):
        """Test successful sketch creation on Top plane."""
        mock_result = OperationResult(
            success=True,
            message="Started sketch: Sketch1",
            feature_name="Sketch1",
        )

        with patch("mcp_tools.sketch_tools.create_sketch_operation", return_value=mock_result) as mock_create:
            from mcp_tools.sketch_tools import create_sketch

            result = create_sketch("Top")

            assert result["success"] is True
            mock_create.assert_called_once_with(PlaneType.TOP)

    def test_create_sketch_on_right_plane(self):
        """Test successful sketch creation on Right plane."""
        mock_result = OperationResult(
            success=True,
            message="Started sketch: Sketch1",
            feature_name="Sketch1",
        )

        with patch("mcp_tools.sketch_tools.create_sketch_operation", return_value=mock_result) as mock_create:
            from mcp_tools.sketch_tools import create_sketch

            result = create_sketch("Right")

            assert result["success"] is True
            mock_create.assert_called_once_with(PlaneType.RIGHT)

    def test_create_sketch_with_plane_suffix(self):
        """Test that 'Front Plane' works as well as 'Front'."""
        mock_result = OperationResult(
            success=True,
            message="Started sketch: Sketch1",
            feature_name="Sketch1",
        )

        with patch("mcp_tools.sketch_tools.create_sketch_operation", return_value=mock_result) as mock_create:
            from mcp_tools.sketch_tools import create_sketch

            result = create_sketch("Front Plane")

            assert result["success"] is True
            mock_create.assert_called_once_with(PlaneType.FRONT)

    def test_create_sketch_invalid_plane(self):
        """Test invalid plane name rejection."""
        from mcp_tools.sketch_tools import create_sketch

        result = create_sketch("Left")

        assert result["success"] is False
        assert "Invalid plane" in result["message"]

    def test_create_sketch_empty_plane(self):
        """Test empty plane name rejection."""
        from mcp_tools.sketch_tools import create_sketch

        result = create_sketch("")

        assert result["success"] is False
        assert "required" in result["message"].lower()

    def test_create_sketch_no_document_open(self):
        """Test error when no document is open."""
        mock_result = OperationResult(
            success=False,
            message="No document is open. Use create_new_part() to create a new part first.",
        )

        with patch("mcp_tools.sketch_tools.create_sketch_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import create_sketch

            result = create_sketch("Front")

            assert result["success"] is False
            assert "No document" in result["message"]


@pytest.mark.unit
class TestCloseSketchTool:
    """Tests for close_sketch tool."""

    def test_close_sketch_success_with_screenshot(self):
        """Test close_sketch returns screenshot when available."""
        mock_result = OperationResult(
            success=True,
            message="Closed sketch: Sketch1",
            feature_name="Sketch1",
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.sketch_tools.exit_sketch", return_value=mock_result):
            with patch("mcp_tools.sketch_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.sketch_tools import close_sketch

                result = close_sketch()

                assert result["success"] is True
                assert result["sketch"] == "Sketch1"
                assert result["screenshot"] == {"view": "isometric"}

    def test_close_sketch_no_active_sketch(self):
        """Test close_sketch when no sketch is active (should be no-op success)."""
        mock_result = OperationResult(
            success=True,
            message="Exited sketch mode",
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.sketch_tools.exit_sketch", return_value=mock_result):
            with patch("mcp_tools.sketch_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.sketch_tools import close_sketch

                result = close_sketch()

                assert result["success"] is True
                assert "sketch" not in result  # No feature_name when no sketch was active

    def test_close_sketch_failure(self):
        """Test close_sketch handles failure from operations layer."""
        mock_result = OperationResult(
            success=False,
            message="No document is open. Use create_new_part() to create a new part first.",
        )

        with patch("mcp_tools.sketch_tools.exit_sketch", return_value=mock_result):
            from mcp_tools.sketch_tools import close_sketch

            result = close_sketch()

            assert result["success"] is False
            assert "No document" in result["message"]
            assert "screenshot" not in result  # No screenshot on failure


@pytest.mark.unit
class TestDrawRectangleTool:
    """Tests for draw_rectangle tool."""

    def test_draw_rectangle_success(self):
        """Test drawing a rectangle successfully."""
        mock_result = OperationResult(
            success=True,
            message="Drew 100x50mm rectangle at (0, 0)",
            data={"width_mm": 100, "height_mm": 50},
        )

        with patch("mcp_tools.sketch_tools.draw_rectangle_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_rectangle

            result = draw_rectangle(center_x=0, center_y=0, width=100, height=50)

            assert result["success"] is True
            assert result["data"]["width_mm"] == 100
            assert result["data"]["height_mm"] == 50
            mock_draw.assert_called_once_with(0, 0, 100, 50)

    def test_draw_rectangle_no_active_sketch(self):
        """Test error when no sketch is active."""
        mock_result = OperationResult(
            success=False,
            message="No active sketch. Use create_sketch() to start a new sketch first.",
        )

        with patch("mcp_tools.sketch_tools.draw_rectangle_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_rectangle

            result = draw_rectangle(center_x=0, center_y=0, width=100, height=50)

            assert result["success"] is False
            assert "sketch" in result["message"].lower()

    def test_draw_rectangle_invalid_dimensions(self):
        """Test error with invalid dimensions (handled by operations layer)."""
        mock_result = OperationResult(
            success=False,
            message="Width and height must be positive. Got width=-100, height=50",
        )

        with patch("mcp_tools.sketch_tools.draw_rectangle_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_rectangle

            result = draw_rectangle(center_x=0, center_y=0, width=-100, height=50)

            assert result["success"] is False
            assert "positive" in result["message"].lower()


@pytest.mark.unit
class TestDrawCircleTool:
    """Tests for draw_circle tool."""

    def test_draw_circle_success(self):
        """Test drawing a circle successfully."""
        mock_result = OperationResult(
            success=True,
            message="Drew circle with radius 25mm at (0, 0)",
            data={"radius_mm": 25},
        )

        with patch("mcp_tools.sketch_tools.draw_circle_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_circle

            result = draw_circle(center_x=0, center_y=0, radius=25)

            assert result["success"] is True
            assert result["data"]["radius_mm"] == 25
            mock_draw.assert_called_once_with(0, 0, 25)

    def test_draw_circle_no_active_sketch(self):
        """Test error when no sketch is active."""
        mock_result = OperationResult(
            success=False,
            message="No active sketch. Use create_sketch() to start a new sketch first.",
        )

        with patch("mcp_tools.sketch_tools.draw_circle_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_circle

            result = draw_circle(center_x=0, center_y=0, radius=25)

            assert result["success"] is False
            assert "sketch" in result["message"].lower()


@pytest.mark.unit
class TestDrawLineTool:
    """Tests for draw_line tool."""

    def test_draw_line_success(self):
        """Test drawing a line successfully."""
        mock_result = OperationResult(
            success=True,
            message="Drew line from (0, 0) to (10, 0) mm",
            data={"length_mm": 10},
        )

        with patch("mcp_tools.sketch_tools.draw_line_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_line

            result = draw_line(x1=0, y1=0, x2=10, y2=0)

            assert result["success"] is True
            assert result["data"]["length_mm"] == 10
            mock_draw.assert_called_once_with(0, 0, 10, 0)

    def test_draw_line_no_active_sketch(self):
        """Test error when no sketch is active."""
        mock_result = OperationResult(
            success=False,
            message="No active sketch. Use create_sketch() to start a new sketch first.",
        )

        with patch("mcp_tools.sketch_tools.draw_line_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_line

            result = draw_line(x1=0, y1=0, x2=10, y2=0)

            assert result["success"] is False
            assert "sketch" in result["message"].lower()


@pytest.mark.unit
class TestDrawArcTool:
    """Tests for draw_arc tool."""

    def test_draw_arc_success(self):
        """Test drawing an arc successfully."""
        mock_result = OperationResult(
            success=True,
            message="Drew arc from (10, 0) to (0, 10) centered at (0, 0)",
            data={"center": {"x": 0, "y": 0}},
        )

        with patch("mcp_tools.sketch_tools.draw_arc_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_arc

            result = draw_arc(center_x=0, center_y=0, start_x=10, start_y=0, end_x=0, end_y=10)

            assert result["success"] is True
            assert result["data"]["center"]["x"] == 0
            mock_draw.assert_called_once_with(0, 0, 10, 0, 0, 10)

    def test_draw_arc_no_active_sketch(self):
        """Test error when no sketch is active."""
        mock_result = OperationResult(
            success=False,
            message="No active sketch. Use create_sketch() to start a new sketch first.",
        )

        with patch("mcp_tools.sketch_tools.draw_arc_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_arc

            result = draw_arc(center_x=0, center_y=0, start_x=10, start_y=0, end_x=0, end_y=10)

            assert result["success"] is False
            assert "sketch" in result["message"].lower()


@pytest.mark.unit
class TestDrawPolygonTool:
    """Tests for draw_polygon tool."""

    def test_draw_hexagon_success(self):
        """Test drawing a hexagon successfully."""
        mock_result = OperationResult(
            success=True,
            message="Drew 6-sided polygon with radius 50mm at (0, 0)",
            data={"sides": 6, "radius_mm": 50},
        )

        with patch("mcp_tools.sketch_tools.draw_polygon_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_polygon

            result = draw_polygon(center_x=0, center_y=0, radius=50, sides=6)

            assert result["success"] is True
            assert result["data"]["sides"] == 6
            mock_draw.assert_called_once_with(0, 0, 50, 6)

    def test_draw_polygon_too_few_sides(self):
        """Test error with fewer than 3 sides (handled by operations layer)."""
        mock_result = OperationResult(
            success=False,
            message="Polygon must have at least 3 sides. Got sides=2",
        )

        with patch("mcp_tools.sketch_tools.draw_polygon_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_polygon

            result = draw_polygon(center_x=0, center_y=0, radius=50, sides=2)

            assert result["success"] is False
            assert "3 sides" in result["message"]

    def test_draw_polygon_no_active_sketch(self):
        """Test error when no sketch is active."""
        mock_result = OperationResult(
            success=False,
            message="No active sketch. Use create_sketch() to start a new sketch first.",
        )

        with patch("mcp_tools.sketch_tools.draw_polygon_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_polygon

            result = draw_polygon(center_x=0, center_y=0, radius=50, sides=6)

            assert result["success"] is False
            assert "sketch" in result["message"].lower()


@pytest.mark.unit
class TestDrawSplineTool:
    """Tests for draw_spline tool."""

    def test_draw_spline_with_dict_points(self):
        """Test drawing a spline with dict-format points."""
        mock_result = OperationResult(
            success=True,
            message="Drew spline through 3 points",
            data={"point_count": 3},
        )

        with patch("mcp_tools.sketch_tools.draw_spline_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_spline

            points = [{"x": 0, "y": 0}, {"x": 10, "y": 0}, {"x": 20, "y": 5}]
            result = draw_spline(points)

            assert result["success"] is True
            assert result["data"]["point_count"] == 3
            mock_draw.assert_called_once_with([(0.0, 0.0), (10.0, 0.0), (20.0, 5.0)])

    def test_draw_spline_with_list_points(self):
        """Test drawing a spline with list-format points."""
        mock_result = OperationResult(
            success=True,
            message="Drew spline through 2 points",
            data={"point_count": 2},
        )

        with patch("mcp_tools.sketch_tools.draw_spline_operation", return_value=mock_result) as mock_draw:
            from mcp_tools.sketch_tools import draw_spline

            points = [[0, 0], [10, 5]]
            result = draw_spline(points)

            assert result["success"] is True
            mock_draw.assert_called_once_with([(0.0, 0.0), (10.0, 5.0)])

    def test_draw_spline_too_few_points(self):
        """Test error with fewer than 2 points."""
        from mcp_tools.sketch_tools import draw_spline

        result = draw_spline([{"x": 0, "y": 0}])

        assert result["success"] is False
        assert "at least 2 points" in result["message"].lower()

    def test_draw_spline_empty_points(self):
        """Test error with empty points list."""
        from mcp_tools.sketch_tools import draw_spline

        result = draw_spline([])

        assert result["success"] is False
        assert "required" in result["message"].lower()

    def test_draw_spline_invalid_point_format(self):
        """Test error with invalid point format."""
        from mcp_tools.sketch_tools import draw_spline

        result = draw_spline([{"a": 0, "b": 0}, {"x": 10, "y": 5}])

        assert result["success"] is False
        assert "dict with x/y" in result["message"].lower()

    def test_draw_spline_no_active_sketch(self):
        """Test error when no sketch is active."""
        mock_result = OperationResult(
            success=False,
            message="No active sketch. Use create_sketch() to start a new sketch first.",
        )

        with patch("mcp_tools.sketch_tools.draw_spline_operation", return_value=mock_result):
            from mcp_tools.sketch_tools import draw_spline

            result = draw_spline([{"x": 0, "y": 0}, {"x": 10, "y": 5}])

            assert result["success"] is False
            assert "sketch" in result["message"].lower()
