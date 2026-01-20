"""Unit tests for document tools.

These tests use mocked COM objects and don't require SolidWorks to be running.
"""

import pytest
from unittest.mock import MagicMock, patch

from solidworks.models import OperationResult


@pytest.mark.unit
class TestCreateNewPartTool:
    """Tests for create_new_part tool."""
    
    def test_create_new_part_success(self):
        """Test successful part creation."""
        mock_result = OperationResult(
            success=True,
            message="Created new part: Part1",
            data={"document": {"name": "Part1", "type": "part", "path": None}}
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"}
        )
        
        with patch('mcp_tools.document_tools.create_new_document', return_value=mock_result):
            with patch('mcp_tools.document_tools.capture_screenshot', return_value=mock_screenshot):
                from mcp_tools.document_tools import create_new_part
                
                result = create_new_part()
                
                assert result["success"] is True
                assert "Created" in result["message"]
                assert result["document"] is not None
    
    def test_create_new_part_with_template(self):
        """Test part creation with custom template."""
        mock_result = OperationResult(
            success=True,
            message="Created new part: Part1",
            data={"document": {"name": "Part1", "type": "part", "path": None}}
        )
        mock_screenshot = OperationResult(
            success=True,
            message="Screenshot captured",
            data={"view": "isometric"}
        )
        
        with patch('mcp_tools.document_tools.create_new_document', return_value=mock_result) as mock_create:
            with patch('mcp_tools.document_tools.capture_screenshot', return_value=mock_screenshot):
                from mcp_tools.document_tools import create_new_part
                
                result = create_new_part(template_path="C:\\templates\\custom.prtdot")
                
                assert result["success"] is True
                mock_create.assert_called_once_with("C:\\templates\\custom.prtdot")
    
    def test_create_new_part_failure(self):
        """Test part creation failure."""
        mock_result = OperationResult(
            success=False,
            message="Failed to connect to SolidWorks. Is it running?"
        )
        
        with patch('mcp_tools.document_tools.create_new_document', return_value=mock_result):
            from mcp_tools.document_tools import create_new_part
            
            result = create_new_part()
            
            assert result["success"] is False
            assert "Failed" in result["message"] or "connect" in result["message"].lower()


@pytest.mark.unit
class TestSavePartTool:
    """Tests for save_part tool."""
    
    def test_save_part_success(self):
        """Test successful part save."""
        mock_result = OperationResult(
            success=True,
            message="Saved to: C:\\parts\\test.SLDPRT",
            data={"path": "C:\\parts\\test.SLDPRT"}
        )
        
        with patch('mcp_tools.document_tools.save_document', return_value=mock_result):
            from mcp_tools.document_tools import save_part
            
            result = save_part(file_path="C:\\parts\\test.SLDPRT")
            
            assert result["success"] is True
            assert "Saved" in result["message"]
            assert result["path"] == "C:\\parts\\test.SLDPRT"
    
    def test_save_part_no_path(self):
        """Test save with empty path."""
        from mcp_tools.document_tools import save_part
        
        result = save_part(file_path="")
        
        assert result["success"] is False
        assert "required" in result["message"].lower()
    
    def test_save_part_no_document(self):
        """Test save when no document is open."""
        mock_result = OperationResult(
            success=False,
            message="No document is open. Use create_new_part() to create a new part first."
        )
        
        with patch('mcp_tools.document_tools.save_document', return_value=mock_result):
            from mcp_tools.document_tools import save_part
            
            result = save_part(file_path="C:\\parts\\test.SLDPRT")
            
            assert result["success"] is False
            assert "No document" in result["message"]
    
    def test_save_part_adds_extension(self):
        """Test that save accepts path without extension."""
        mock_result = OperationResult(
            success=True,
            message="Saved to: C:\\parts\\test.SLDPRT",
            data={"path": "C:\\parts\\test.SLDPRT"}
        )
        
        with patch('mcp_tools.document_tools.save_document', return_value=mock_result) as mock_save:
            from mcp_tools.document_tools import save_part
            
            result = save_part(file_path="C:\\parts\\test")
            
            assert result["success"] is True
            # Operations layer handles extension
            mock_save.assert_called_once_with("C:\\parts\\test")
