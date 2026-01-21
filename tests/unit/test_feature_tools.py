"""Unit tests for feature tools.

These tests use mocked operations and don't require SolidWorks to be running.
"""

from unittest.mock import patch

import pytest

from solidworks.models import OperationResult


@pytest.mark.unit
class TestExtrudeTool:
    """Tests for extrude tool."""

    def test_extrude_boss_forward_success(self):
        """Test successful boss extrude in forward direction."""
        mock_result = OperationResult(
            success=True,
            message="Extruded 25mm (boss)",
            feature_name="Boss-Extrude1",
            data={"depth_mm": 25, "operation": "boss", "direction": "forward"},
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result) as mock_extrude:
            with patch("mcp_tools.feature_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.feature_tools import extrude

                result = extrude(depth=25, operation="boss", direction="forward")

                assert result["success"] is True
                assert result["feature"] == "Boss-Extrude1"
                assert result["data"]["depth_mm"] == 25
                assert "screenshot" in result
                mock_extrude.assert_called_once_with(25, "boss", "forward")

    def test_extrude_cut_backward_success(self):
        """Test successful cut extrude in backward direction."""
        mock_result = OperationResult(
            success=True,
            message="Extruded 10mm (cut)",
            feature_name="Cut-Extrude1",
            data={"depth_mm": 10, "operation": "cut", "direction": "backward"},
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result) as mock_extrude:
            with patch("mcp_tools.feature_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.feature_tools import extrude

                result = extrude(depth=10, operation="cut", direction="backward")

                assert result["success"] is True
                assert result["feature"] == "Cut-Extrude1"
                mock_extrude.assert_called_once_with(10, "cut", "backward")

    def test_extrude_both_direction(self):
        """Test extrude with midplane (both) direction."""
        mock_result = OperationResult(
            success=True,
            message="Extruded 20mm (boss)",
            feature_name="Boss-Extrude1",
            data={"depth_mm": 20, "operation": "boss", "direction": "both"},
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result) as mock_extrude:
            with patch("mcp_tools.feature_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.feature_tools import extrude

                result = extrude(depth=20, operation="boss", direction="both")

                assert result["success"] is True
                mock_extrude.assert_called_once_with(20, "boss", "both")

    def test_extrude_default_parameters(self):
        """Test extrude with default operation and direction."""
        mock_result = OperationResult(
            success=True,
            message="Extruded 15mm (boss)",
            feature_name="Boss-Extrude1",
            data={"depth_mm": 15, "operation": "boss", "direction": "forward"},
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result) as mock_extrude:
            with patch("mcp_tools.feature_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.feature_tools import extrude

                result = extrude(depth=15)

                assert result["success"] is True
                mock_extrude.assert_called_once_with(15, "boss", "forward")

    def test_extrude_invalid_operation(self):
        """Test error with invalid operation type."""
        from mcp_tools.feature_tools import extrude

        result = extrude(depth=25, operation="invalid")

        assert result["success"] is False
        assert "boss" in result["message"] and "cut" in result["message"]

    def test_extrude_invalid_direction(self):
        """Test error with invalid direction."""
        from mcp_tools.feature_tools import extrude

        result = extrude(depth=25, direction="invalid")

        assert result["success"] is False
        assert "forward" in result["message"]
        assert "backward" in result["message"]
        assert "both" in result["message"]

    def test_extrude_no_sketch(self):
        """Test error when no sketch to extrude."""
        mock_result = OperationResult(
            success=False,
            message="Failed to create extrusion. Make sure a closed sketch profile exists.",
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result):
            from mcp_tools.feature_tools import extrude

            result = extrude(depth=25)

            assert result["success"] is False
            assert "sketch" in result["message"].lower()

    def test_extrude_negative_depth(self):
        """Test error with negative depth (handled by operations layer)."""
        mock_result = OperationResult(
            success=False,
            message="Depth must be positive. Got depth=-10",
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result):
            from mcp_tools.feature_tools import extrude

            result = extrude(depth=-10)

            assert result["success"] is False
            assert "positive" in result["message"].lower()

    def test_extrude_no_screenshot_on_failure(self):
        """Test that no screenshot is returned on failure."""
        mock_result = OperationResult(
            success=False,
            message="No document is open.",
        )

        with patch("mcp_tools.feature_tools.extrude_operation", return_value=mock_result):
            from mcp_tools.feature_tools import extrude

            result = extrude(depth=25)

            assert result["success"] is False
            assert "screenshot" not in result


@pytest.mark.unit
class TestFilletTool:
    """Tests for fillet tool."""

    def test_fillet_success(self):
        """Test successful fillet creation."""
        mock_result = OperationResult(
            success=True,
            message="Applied 5mm fillet to 12 edges",
            feature_name="Fillet1",
            data={"radius_mm": 5, "edge_count": 12},
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.feature_tools.fillet_operation", return_value=mock_result) as mock_fillet:
            with patch("mcp_tools.feature_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.feature_tools import fillet

                result = fillet(radius=5)

                assert result["success"] is True
                assert result["feature"] == "Fillet1"
                assert result["data"]["radius_mm"] == 5
                assert result["data"]["edge_count"] == 12
                assert "screenshot" in result
                mock_fillet.assert_called_once_with(5)

    def test_fillet_negative_radius(self):
        """Test error with negative radius (handled by operations layer)."""
        mock_result = OperationResult(
            success=False,
            message="Radius must be positive. Got radius=-5",
        )

        with patch("mcp_tools.feature_tools.fillet_operation", return_value=mock_result):
            from mcp_tools.feature_tools import fillet

            result = fillet(radius=-5)

            assert result["success"] is False
            assert "positive" in result["message"].lower()

    def test_fillet_no_geometry(self):
        """Test error when no solid body exists."""
        mock_result = OperationResult(
            success=False,
            message="No solid bodies found. Create geometry first using extrude.",
        )

        with patch("mcp_tools.feature_tools.fillet_operation", return_value=mock_result):
            from mcp_tools.feature_tools import fillet

            result = fillet(radius=5)

            assert result["success"] is False
            assert "solid" in result["message"].lower() or "geometry" in result["message"].lower()

    def test_fillet_radius_too_large(self):
        """Test error when radius is too large for geometry."""
        mock_result = OperationResult(
            success=False,
            message="Failed to create fillet. Radius may be too large for edge geometry.",
        )

        with patch("mcp_tools.feature_tools.fillet_operation", return_value=mock_result):
            from mcp_tools.feature_tools import fillet

            result = fillet(radius=100)

            assert result["success"] is False
            assert "too large" in result["message"].lower()

    def test_fillet_no_screenshot_on_failure(self):
        """Test that no screenshot is returned on failure."""
        mock_result = OperationResult(
            success=False,
            message="No document is open.",
        )

        with patch("mcp_tools.feature_tools.fillet_operation", return_value=mock_result):
            from mcp_tools.feature_tools import fillet

            result = fillet(radius=5)

            assert result["success"] is False
            assert "screenshot" not in result


@pytest.mark.unit
class TestChamferTool:
    """Tests for chamfer tool."""

    def test_chamfer_success(self):
        """Test successful chamfer creation."""
        mock_result = OperationResult(
            success=True,
            message="Applied 2mm chamfer to 12 edges",
            feature_name="Chamfer1",
            data={"distance_mm": 2, "edge_count": 12},
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"},
        )

        with patch("mcp_tools.feature_tools.chamfer_operation", return_value=mock_result) as mock_chamfer:
            with patch("mcp_tools.feature_tools.capture_screenshot", return_value=mock_screenshot):
                from mcp_tools.feature_tools import chamfer

                result = chamfer(distance=2)

                assert result["success"] is True
                assert result["feature"] == "Chamfer1"
                assert result["data"]["distance_mm"] == 2
                assert result["data"]["edge_count"] == 12
                assert "screenshot" in result
                mock_chamfer.assert_called_once_with(2)

    def test_chamfer_negative_distance(self):
        """Test error with negative distance (handled by operations layer)."""
        mock_result = OperationResult(
            success=False,
            message="Distance must be positive. Got distance=-2",
        )

        with patch("mcp_tools.feature_tools.chamfer_operation", return_value=mock_result):
            from mcp_tools.feature_tools import chamfer

            result = chamfer(distance=-2)

            assert result["success"] is False
            assert "positive" in result["message"].lower()

    def test_chamfer_no_geometry(self):
        """Test error when no solid body exists."""
        mock_result = OperationResult(
            success=False,
            message="No solid bodies found. Create geometry first using extrude.",
        )

        with patch("mcp_tools.feature_tools.chamfer_operation", return_value=mock_result):
            from mcp_tools.feature_tools import chamfer

            result = chamfer(distance=2)

            assert result["success"] is False
            assert "solid" in result["message"].lower() or "geometry" in result["message"].lower()

    def test_chamfer_distance_too_large(self):
        """Test error when distance is too large for geometry."""
        mock_result = OperationResult(
            success=False,
            message="Failed to create chamfer. Distance may be too large for edge geometry.",
        )

        with patch("mcp_tools.feature_tools.chamfer_operation", return_value=mock_result):
            from mcp_tools.feature_tools import chamfer

            result = chamfer(distance=100)

            assert result["success"] is False
            assert "too large" in result["message"].lower()

    def test_chamfer_no_screenshot_on_failure(self):
        """Test that no screenshot is returned on failure."""
        mock_result = OperationResult(
            success=False,
            message="No document is open.",
        )

        with patch("mcp_tools.feature_tools.chamfer_operation", return_value=mock_result):
            from mcp_tools.feature_tools import chamfer

            result = chamfer(distance=2)

            assert result["success"] is False
            assert "screenshot" not in result
