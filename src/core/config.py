"""Configuration management for ForgeAI."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SolidWorksConfig(BaseSettings):
    """SolidWorks connection configuration."""

    version: Optional[str] = Field(
        default=None,
        description="SolidWorks version (e.g., '2024'). If None, uses latest installed.",
    )
    timeout: int = Field(
        default=30,
        description="Connection timeout in seconds",
    )
    auto_launch: bool = Field(
        default=True,
        description="Automatically launch SolidWorks if not running",
    )
    visible: bool = Field(
        default=True,
        description="Make SolidWorks window visible",
    )


class MCPConfig(BaseSettings):
    """MCP server configuration."""

    server_name: str = Field(
        default="forgeai",
        description="MCP server name",
    )
    server_version: str = Field(
        default="0.1.0",
        description="MCP server version",
    )
    transport: str = Field(
        default="stdio",
        description="Transport protocol (stdio only for now)",
    )


class LoggingConfig(BaseSettings):
    """Logging configuration."""

    level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_file: Optional[Path] = Field(
        default=None,
        description="Path to log file. If None, logs only to console.",
    )
    rotation: str = Field(
        default="10 MB",
        description="Log rotation size",
    )
    retention: str = Field(
        default="1 week",
        description="Log retention period",
    )


class ForgeAIConfig(BaseSettings):
    """Main ForgeAI configuration."""

    model_config = SettingsConfigDict(
        env_prefix="FORGEAI_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Sub-configurations
    solidworks: SolidWorksConfig = Field(default_factory=SolidWorksConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    # General settings
    workspace_dir: Path = Field(
        default=Path.cwd(),
        description="Working directory for temporary files",
    )
    screenshot_dir: Path = Field(
        default=Path.cwd() / "data" / "screenshots",
        description="Directory for model screenshots",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)


# Global config instance
_config: Optional[ForgeAIConfig] = None


def get_config() -> ForgeAIConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = ForgeAIConfig()
    return _config


def reload_config() -> ForgeAIConfig:
    """Reload configuration from environment/files."""
    global _config
    _config = ForgeAIConfig()
    return _config
