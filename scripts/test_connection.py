"""Test script for SolidWorks COM connection.

Run this script to verify SolidWorks connection is working properly.
Make sure SolidWorks is installed before running.

Usage:
    python scripts/test_connection.py
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    from core.logging_config import setup_logging
    from solidworks.connection import get_connection
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    print(f"Current directory: {Path.cwd()}")
    sys.exit(1)


def main():
    """Test SolidWorks connection."""
    # Setup logging
    setup_logging(level="DEBUG")
    
    print("=" * 60)
    print("ForgeAI - SolidWorks Connection Test")
    print("=" * 60)
    print()
    
    # Get connection instance
    conn = get_connection()
    
    # Test 1: Connect to SolidWorks
    print("Test 1: Connecting to SolidWorks...")
    try:
        if conn.connect():
            print("✓ Connected successfully!")
        else:
            print("✗ Connection failed")
            return 1
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return 1
    
    print()
    
    # Test 2: Get version
    print("Test 2: Getting SolidWorks version...")
    try:
        version = conn.get_version()
        if version:
            print(f"✓ SolidWorks version: {version}")
        else:
            print("✗ Could not get version")
    except Exception as e:
        print(f"✗ Error getting version: {e}")
    
    print()
    
    # Test 3: Check active document
    print("Test 3: Checking for active document...")
    try:
        doc = conn.get_active_doc()
        if doc:
            print(f"✓ Active document found: {doc.GetTitle()}")
        else:
            print("⚠ No active document (this is normal if no document is open)")
    except Exception as e:
        print(f"✗ Error checking document: {e}")
    
    print()
    
    # Test 4: Verify connection health
    print("Test 4: Verifying connection health...")
    try:
        if conn.check_connection():
            print("✓ Connection is healthy")
        else:
            print("✗ Connection check failed")
    except Exception as e:
        print(f"✗ Error checking connection: {e}")
    
    print()
    
    # Test 5: Test reconnection
    print("Test 5: Testing reconnection...")
    try:
        if conn.reconnect():
            print("✓ Reconnection successful")
        else:
            print("✗ Reconnection failed")
    except Exception as e:
        print(f"✗ Error during reconnection: {e}")
    
    print()
    
    # Cleanup
    print("Cleaning up...")
    conn.disconnect()
    print("✓ Disconnected")
    
    print()
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
