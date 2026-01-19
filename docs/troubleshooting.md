# Troubleshooting Guide

This guide covers common issues you might encounter while setting up or using ForgeAI.

## Connection Issues

### "No module named 'win32com'"
- **Cause**: The `pywin32` library is not installed or the post-installation script hasn't been run.
- **Solution**: 
  Ensure you are in your virtual environment and run:
  ```bash
  pip install pywin32
  python Scripts/pywin32_postinstall.py -install
  ```

### "SolidWorks not found" / COM connection fails
- **Cause**: SolidWorks is not installed, not activated, or its COM objects are not registered correctly in Windows.
- **Solutions**:
  - Ensure SolidWorks is installed and activated.
  - Try running SolidWorks manually first before starting ForgeAI.
  - Check Windows registry for COM registration.
  - Try running your terminal or Claude Desktop as Administrator.
  - Verify `FORGEAI_SOLIDWORKS_VERSION` in your `.env` matches your installed version (or leave it empty to use the latest).

### "Connection timeout"
- **Cause**: SolidWorks is taking too long to start or initialize.
- **Solution**:
  - Increase the timeout value in your `.env` file: `FORGEAI_SOLIDWORKS_TIMEOUT=60` (default is 30).
  - Start SolidWorks manually before using ForgeAI to bypass the launch time.

## MCP Issues

### Claude Desktop doesn't show ForgeAI tools
- **Check Configuration**: Verify `claude_desktop_config.json` syntax is valid JSON.
- **Verify Paths**: Ensure the `cwd` (current working directory) and the path to the Python executable are correct.
- **Restart**: Claude Desktop must be restarted after any configuration changes.
- **Environment**: Check that `PYTHONPATH` is set correctly if you are not using the `-m` module execution style or if your project structure requires it.

### Server fails to start
- **Python Version**: Ensure you are using Python 3.10 or higher.
- **Dependencies**: Run `pip install -r requirements.txt` to ensure all required packages are installed.
- **Logs**: Check for errors in the console output or the log file (if `FORGEAI_LOGGING_LOG_FILE` is configured).
- **Port Conflicts**: If using a transport other than stdio (though only stdio is currently supported), check for port conflicts.

## Runtime Issues

### "No document open"
- **Cause**: You are trying to perform an operation (like sketching or extruding) without an active part document.
- **Solution**: Always call the `create_new_part` tool or open an existing part before performing sketch or feature operations.

### Operations not visible in SolidWorks
- **Visibility Setting**: Ensure `FORGEAI_SOLIDWORKS_VISIBLE` is set to `true` in your `.env` (default is true).
- **Auto Launch**: Check that `FORGEAI_SOLIDWORKS_AUTO_LAUNCH` is true or start SolidWorks manually.
- **Refresh View**: Sometimes SolidWorks requires a manual click in the viewport to refresh the graphics, though ForgeAI attempts to handle this.

## Getting Help

If you continue to experience issues:
- **Review Logs**: Check `logs/forgeai.log` (if enabled) for detailed error messages and stack traces.
- **Check Connection**: Run `python scripts/test_connection.py` to verify the COM bridge is working.
- **Open an Issue**: Report bugs on GitHub with the following details:
  - Python version
  - SolidWorks version
  - The exact error message or behavior
  - Log snippets (with sensitive info removed)
