"""Unit tests for ForgeAI MCP server.

These tests use mocked COM objects and don't require SolidWorks to be running.
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock


@pytest.mark.unit
class TestServerCreation:
    """Tests for MCP server creation."""
    
    def test_create_server_returns_fastmcp(self):
        """Test that create_server returns a FastMCP instance."""
        from core.mcp_server import create_server
        
        server = create_server()
        
        # Check it's a FastMCP instance
        assert server is not None
        assert hasattr(server, 'run')
        assert hasattr(server, 'tool')
    
    def test_server_has_correct_name(self):
        """Test that server has the configured name."""
        from core.mcp_server import create_server
        from core.config import get_config
        
        config = get_config()
        server = create_server()
        
        assert server.name == config.mcp.server_name


@pytest.mark.unit
class TestServerLifespan:
    """Tests for server lifespan management."""
    
    @pytest.mark.asyncio
    async def test_lifespan_creates_connection(self):
        """Test that lifespan initializes SolidWorks connection."""
        from core.mcp_server import forgeai_lifespan, ForgeAIContext
        
        mock_server = MagicMock()
        mock_connection = MagicMock()
        mock_connection.connect.return_value = True
        
        with patch('core.mcp_server.get_connection', return_value=mock_connection):
            async with forgeai_lifespan(mock_server) as ctx:
                # Verify context is correct type
                assert isinstance(ctx, ForgeAIContext)
                
                # Verify connection was attempted
                mock_connection.connect.assert_called_once()
                
                # Verify connection is accessible
                assert ctx.connection == mock_connection
    
    @pytest.mark.asyncio
    async def test_lifespan_disconnects_on_shutdown(self):
        """Test that lifespan disconnects on shutdown."""
        from core.mcp_server import forgeai_lifespan
        
        mock_server = MagicMock()
        mock_connection = MagicMock()
        mock_connection.connect.return_value = True
        
        with patch('core.mcp_server.get_connection', return_value=mock_connection):
            async with forgeai_lifespan(mock_server) as ctx:
                pass  # Context exits here
            
            # Verify disconnect was called
            mock_connection.disconnect.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_handles_connection_failure(self):
        """Test that lifespan handles connection failure gracefully."""
        from core.mcp_server import forgeai_lifespan
        
        mock_server = MagicMock()
        mock_connection = MagicMock()
        mock_connection.connect.return_value = False  # Connection fails
        
        with patch('core.mcp_server.get_connection', return_value=mock_connection):
            # Should not raise, just log warning
            async with forgeai_lifespan(mock_server) as ctx:
                # Context should still be created
                assert ctx.connection == mock_connection


@pytest.mark.unit
class TestSignalHandlers:
    """Tests for signal handler setup."""
    
    def test_setup_signal_handlers(self):
        """Test that signal handlers are set up without error."""
        from core.mcp_server import setup_signal_handlers
        
        # Should not raise
        setup_signal_handlers()


@pytest.mark.unit
class TestMainFunction:
    """Tests for the main entry point."""
    
    def test_main_configures_logging(self):
        """Test that main sets up logging correctly."""
        from core.mcp_server import main
        
        # Mock the server run to avoid actually starting
        with patch('core.mcp_server.mcp') as mock_mcp:
            mock_mcp.run = MagicMock()
            
            # Call main - it will exit when run is called
            try:
                main()
            except SystemExit:
                pass  # Expected if run calls exit
            
            # Verify run was called
            mock_mcp.run.assert_called_once()
