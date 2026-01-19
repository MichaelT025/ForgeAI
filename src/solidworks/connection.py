"""SolidWorks COM API connection manager."""

import time
from typing import Any, Optional

import win32com.client
from loguru import logger

from core.config import get_config


class SolidWorksConnection:
    """
    Manages connection to SolidWorks via COM API.
    
    Handles:
    - Connecting to running instance
    - Launching new instance if needed
    - Connection recovery
    - Graceful disconnection
    """

    def __init__(self):
        """Initialize connection manager."""
        self._app: Optional[Any] = None
        self._is_connected: bool = False
        self._config = get_config()

    @property
    def app(self) -> Any:
        """Get SolidWorks application object."""
        if not self._is_connected:
            raise RuntimeError("Not connected to SolidWorks. Call connect() first.")
        return self._app

    @property
    def is_connected(self) -> bool:
        """Check if connected to SolidWorks."""
        return self._is_connected and self._app is not None

    def connect(self, timeout: Optional[int] = None) -> bool:
        """
        Connect to SolidWorks.
        
        First attempts to connect to running instance. If that fails and
        auto_launch is enabled, launches a new instance.
        
        Args:
            timeout: Connection timeout in seconds. Uses config default if None.
            
        Returns:
            True if connection successful, False otherwise.
        """
        if self.is_connected:
            logger.info("Already connected to SolidWorks")
            return True

        timeout = timeout or self._config.solidworks.timeout
        logger.info("Attempting to connect to SolidWorks...")

        # Try to connect to running instance
        if self._connect_to_running():
            return True

        # If not running and auto_launch enabled, launch new instance
        if self._config.solidworks.auto_launch:
            logger.info("SolidWorks not running, launching new instance...")
            return self._launch_and_connect(timeout)

        logger.error("SolidWorks not running and auto_launch is disabled")
        return False

    def _connect_to_running(self) -> bool:
        """
        Connect to existing running SolidWorks instance.
        
        Returns:
            True if connection successful, False otherwise.
        """
        try:
            self._app = win32com.client.Dispatch("SldWorks.Application")
            
            # Test connection by accessing a property
            _ = self._app.RevisionNumber
            
            self._is_connected = True
            version = self._app.RevisionNumber
            logger.info(f"Connected to existing SolidWorks instance (version {version})")
            return True
            
        except Exception as e:
            logger.debug(f"Could not connect to running instance: {e}")
            self._app = None
            self._is_connected = False
            return False

    def _launch_and_connect(self, timeout: int) -> bool:
        """
        Launch new SolidWorks instance and connect.
        
        Args:
            timeout: Maximum time to wait for launch in seconds.
            
        Returns:
            True if launch and connection successful, False otherwise.
        """
        try:
            logger.info("Creating new SolidWorks instance...")
            # Create new instance
            self._app = win32com.client.Dispatch("SldWorks.Application")
            
            # Wait for SolidWorks to fully initialize
            logger.info("Waiting for SolidWorks to initialize...")
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # Try to get version to verify it's ready
                    version = self._app.RevisionNumber
                    
                    # Make visible if configured
                    if self._config.solidworks.visible:
                        self._app.Visible = True
                        logger.info("Made SolidWorks window visible")
                    
                    # Set frame state to normal (not minimized)
                    try:
                        self._app.FrameState = 0  # 0 = normal, 1 = minimized, 2 = maximized
                    except Exception as e:
                        logger.debug(f"Could not set frame state: {e}")
                    
                    self._is_connected = True
                    logger.info(f"Launched and connected to SolidWorks (version {version})")
                    return True
                except Exception as e:
                    logger.debug(f"Still initializing... ({e})")
                    time.sleep(1)
            
            logger.error(f"SolidWorks launch timed out after {timeout}s")
            self._app = None
            return False
            
        except Exception as e:
            logger.error(f"Failed to launch SolidWorks: {e}")
            self._app = None
            self._is_connected = False
            return False

    def disconnect(self) -> None:
        """
        Disconnect from SolidWorks.
        
        Does not close SolidWorks, just releases the COM connection.
        """
        if self._app is not None:
            try:
                # Release COM object
                del self._app
                self._app = None
                self._is_connected = False
                logger.info("Disconnected from SolidWorks")
            except Exception as e:
                logger.warning(f"Error during disconnect: {e}")

    def reconnect(self, timeout: Optional[int] = None) -> bool:
        """
        Reconnect to SolidWorks.
        
        Useful for recovering from connection loss.
        
        Args:
            timeout: Connection timeout in seconds.
            
        Returns:
            True if reconnection successful, False otherwise.
        """
        logger.info("Attempting to reconnect to SolidWorks...")
        self.disconnect()
        return self.connect(timeout)

    def check_connection(self) -> bool:
        """
        Verify connection is still alive.
        
        Returns:
            True if connection is active, False if broken.
        """
        if not self._is_connected or self._app is None:
            return False
        
        try:
            # Try to access a property to verify connection
            _ = self._app.RevisionNumber
            return True
        except Exception as e:
            logger.warning(f"Connection check failed: {e}")
            self._is_connected = False
            return False

    def get_active_doc(self) -> Optional[Any]:
        """
        Get currently active document in SolidWorks.
        
        Returns:
            Active document object or None if no document is active.
        """
        if not self.is_connected:
            return None
        
        try:
            doc = self._app.ActiveDoc
            return doc if doc is not None else None
        except Exception as e:
            logger.error(f"Failed to get active document: {e}")
            return None

    def get_version(self) -> Optional[str]:
        """
        Get SolidWorks version string.
        
        Returns:
            Version string or None if not connected.
        """
        if not self.is_connected:
            return None
        
        try:
            return self._app.RevisionNumber
        except Exception as e:
            logger.error(f"Failed to get version: {e}")
            return None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def __del__(self):
        """Cleanup on deletion."""
        self.disconnect()


# Global singleton instance
_connection: Optional[SolidWorksConnection] = None


def get_connection() -> SolidWorksConnection:
    """
    Get the global SolidWorks connection instance.
    
    Returns:
        Singleton SolidWorksConnection instance.
    """
    global _connection
    if _connection is None:
        _connection = SolidWorksConnection()
    return _connection


def reset_connection() -> None:
    """Reset the global connection instance."""
    global _connection
    if _connection is not None:
        _connection.disconnect()
    _connection = None
