"""Pytest configuration and shared fixtures for ForgeAI tests."""

import sys
from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


# =============================================================================
# Mock Fixtures for SolidWorks COM API
# =============================================================================

@pytest.fixture
def mock_sw_app() -> MagicMock:
    """Create a mock SolidWorks application object."""
    app = MagicMock()
    app.RevisionNumber = "32.0.0"  # SW 2024
    app.Visible = True
    app.GetUserPreferenceStringValue.return_value = "C:\\templates\\part.prtdot"
    return app


@pytest.fixture
def mock_sw_doc() -> MagicMock:
    """Create a mock SolidWorks document object."""
    doc = MagicMock()
    doc.GetTitle.return_value = "Part1"
    doc.GetPathName.return_value = ""
    doc.GetType.return_value = 1  # swDocPART
    doc.GetSaveFlag.return_value = False
    doc.SaveAs3.return_value = True
    doc.EditRebuild3.return_value = True
    
    # Mock Extension for selection
    extension = MagicMock()
    extension.SelectByID2.return_value = True
    doc.Extension = extension
    
    # Mock SketchManager
    sketch_mgr = MagicMock()
    sketch_mgr.ActiveSketch = None
    sketch_mgr.InsertSketch.return_value = True
    sketch_mgr.CreateCenterRectangle.return_value = [MagicMock()]
    sketch_mgr.CreateCornerRectangle.return_value = [MagicMock()]
    sketch_mgr.CreateCircleByRadius.return_value = MagicMock()
    sketch_mgr.CreateLine.return_value = MagicMock()
    sketch_mgr.CreateArc.return_value = MagicMock()
    sketch_mgr.CreatePolygon.return_value = [MagicMock()]
    sketch_mgr.CreateSpline2.return_value = MagicMock()
    doc.SketchManager = sketch_mgr
    
    # Mock FeatureManager
    feature_mgr = MagicMock()
    feature = MagicMock()
    feature.Name = "Boss-Extrude1"
    feature_mgr.FeatureExtrusion2.return_value = feature
    feature_mgr.FeatureCut3.return_value = feature
    feature_mgr.FeatureFillet3.return_value = feature
    feature_mgr.InsertFeatureChamfer.return_value = feature
    doc.FeatureManager = feature_mgr
    
    # Mock body/edges for fillet/chamfer
    edge = MagicMock()
    edge.Select4.return_value = True
    body = MagicMock()
    body.GetEdges.return_value = [edge, edge, edge]
    doc.GetBodies2.return_value = [body]
    
    # Mock ActiveView for screenshots
    doc.ActiveView = MagicMock()
    doc.ShowNamedView2.return_value = True
    doc.ViewZoomtofit2.return_value = True
    
    # Mock feature traversal
    doc.FirstFeature.return_value = None
    
    return doc


@pytest.fixture
def mock_active_sketch() -> MagicMock:
    """Create a mock active sketch."""
    sketch = MagicMock()
    sketch.Name = "Sketch1"
    return sketch


@pytest.fixture
def mock_connection(mock_sw_app: MagicMock, mock_sw_doc: MagicMock) -> Generator[MagicMock, None, None]:
    """Create a mock SolidWorks connection that returns mock app and doc."""
    with patch("solidworks.operations.get_connection") as mock_get_conn:
        conn = MagicMock()
        conn.is_connected = True
        conn.app = mock_sw_app
        conn.connect.return_value = True
        conn.get_active_doc.return_value = mock_sw_doc
        
        # App creates new documents
        mock_sw_app.NewDocument.return_value = mock_sw_doc
        
        mock_get_conn.return_value = conn
        yield conn


@pytest.fixture
def mock_connection_no_doc(mock_sw_app: MagicMock) -> Generator[MagicMock, None, None]:
    """Create a mock connection with no active document."""
    with patch("solidworks.operations.get_connection") as mock_get_conn:
        conn = MagicMock()
        conn.is_connected = True
        conn.app = mock_sw_app
        conn.connect.return_value = True
        conn.get_active_doc.return_value = None
        
        mock_get_conn.return_value = conn
        yield conn


@pytest.fixture
def mock_connection_disconnected() -> Generator[MagicMock, None, None]:
    """Create a mock connection that is not connected."""
    with patch("solidworks.operations.get_connection") as mock_get_conn:
        conn = MagicMock()
        conn.is_connected = False
        conn.connect.return_value = False
        conn.get_active_doc.return_value = None
        
        mock_get_conn.return_value = conn
        yield conn


# =============================================================================
# Pytest Markers
# =============================================================================

def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: mark test as unit test (no SolidWorks needed)")
    config.addinivalue_line("markers", "integration: mark test as integration test (requires SolidWorks)")
