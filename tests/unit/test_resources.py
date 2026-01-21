"""Unit tests for MCP resources.

These tests verify the model_state and screenshot resources work correctly
with mocked SolidWorks connections.
"""

import pytest
from unittest.mock import MagicMock, patch


@pytest.mark.unit
class TestModelStateResource:
    """Tests for the model_state resource."""
    
    def test_model_state_returns_success_with_doc(self, mock_connection, mock_sw_doc):
        """Test that model_state returns success when document is open."""
        from mcp_resources.model_state import model_state_resource
        
        result = model_state_resource()
        
        assert result["success"] is True
        assert "model_state" in result
        assert result["model_state"] is not None
    
    def test_model_state_contains_document_info(self, mock_connection, mock_sw_doc):
        """Test that model_state includes document information."""
        from mcp_resources.model_state import model_state_resource
        
        result = model_state_resource()
        
        assert result["success"] is True
        model_state = result["model_state"]
        assert "document" in model_state
        assert model_state["document"]["name"] == "Part1"
    
    def test_model_state_returns_failure_no_doc(self, mock_connection_no_doc):
        """Test that model_state returns failure when no document is open."""
        from mcp_resources.model_state import model_state_resource
        
        result = model_state_resource()
        
        assert result["success"] is False
        assert result["model_state"] is None
        assert "message" in result
    
    def test_model_state_includes_features_list(self, mock_connection, mock_sw_doc):
        """Test that model_state includes features list."""
        from mcp_resources.model_state import model_state_resource
        
        result = model_state_resource()
        
        assert result["success"] is True
        model_state = result["model_state"]
        assert "features" in model_state
        assert isinstance(model_state["features"], list)
    
    def test_model_state_includes_sketches_list(self, mock_connection, mock_sw_doc):
        """Test that model_state includes sketches list."""
        from mcp_resources.model_state import model_state_resource
        
        result = model_state_resource()
        
        assert result["success"] is True
        model_state = result["model_state"]
        assert "sketches" in model_state
        assert isinstance(model_state["sketches"], list)
    
    def test_model_state_includes_active_sketch(self, mock_connection, mock_sw_doc, mock_active_sketch):
        """Test that model_state includes active sketch info."""
        mock_sw_doc.SketchManager.ActiveSketch = mock_active_sketch
        
        from mcp_resources.model_state import model_state_resource
        
        result = model_state_resource()
        
        assert result["success"] is True
        model_state = result["model_state"]
        assert "active_sketch" in model_state


@pytest.mark.unit
class TestScreenshotResource:
    """Tests for the screenshot resource."""
    
    def test_screenshot_returns_success_with_doc(self, mock_connection, mock_sw_doc):
        """Test that screenshot returns success when document is open."""
        from mcp_resources.screenshot import screenshot_resource
        
        result = screenshot_resource()
        
        assert result["success"] is True
        assert "viewport" in result
    
    def test_screenshot_returns_viewport_info(self, mock_connection, mock_sw_doc):
        """Test that screenshot returns viewport information."""
        from mcp_resources.screenshot import screenshot_resource
        
        result = screenshot_resource()
        
        assert result["success"] is True
        viewport = result["viewport"]
        assert viewport is not None
        # Check for view settings
        assert "view" in viewport or "note" in viewport
    
    def test_screenshot_returns_failure_no_doc(self, mock_connection_no_doc):
        """Test that screenshot returns failure when no document is open."""
        from mcp_resources.screenshot import screenshot_resource
        
        result = screenshot_resource()
        
        assert result["success"] is False
        assert result["viewport"] is None
        assert "message" in result
    
    def test_screenshot_message_on_success(self, mock_connection, mock_sw_doc):
        """Test that screenshot returns meaningful message on success."""
        from mcp_resources.screenshot import screenshot_resource
        
        result = screenshot_resource()
        
        assert result["success"] is True
        assert "message" in result
        # Should mention view or screenshot
        assert any(word in result["message"].lower() for word in ["view", "screenshot", "isometric", "fit"])


@pytest.mark.unit
class TestResourceImports:
    """Test that resources are properly importable and registered."""
    
    def test_model_state_importable(self):
        """Test that model_state_resource can be imported."""
        from mcp_resources.model_state import model_state_resource
        assert model_state_resource is not None
        assert callable(model_state_resource)
    
    def test_screenshot_importable(self):
        """Test that screenshot_resource can be imported."""
        from mcp_resources.screenshot import screenshot_resource
        assert screenshot_resource is not None
        assert callable(screenshot_resource)
    
    def test_package_exports(self):
        """Test that resources are exported from package."""
        from mcp_resources import model_state_resource, screenshot_resource
        assert model_state_resource is not None
        assert screenshot_resource is not None
