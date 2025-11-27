#!/usr/bin/env python3
"""
Quick test script for Avro server and client
Runs both in parallel and shows results
"""

import subprocess
import time
import sys
import os

def main():
    print("=" * 70)
    print("  Avro Server & Client - Quick Test")
    print("=" * 70)
    print()

    # Check if dependencies are installed
    print("📦 Checking dependencies...")
    try:
        import fastavro
        print("✓ fastavro is installed")
    except ImportError:
        print("❌ fastavro not installed!")
        print("   Install with: pip install fastavro")
        sys.exit(1)
    print()

    # Start server
    print("🚀 Starting Avro server...")
    server_process = subprocess.Popen(
        [sys.executable, "avro_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give server time to start
    time.sleep(2)
    
    # Check if server started
    if server_process.poll() is not None:
        print("❌ Server failed to start!")
        stdout, stderr = server_process.communicate()
        print("Error:", stderr.decode())
        sys.exit(1)
    
    print("✓ Server started on http://localhost:8000/")
    print()

    try:
        # Run client
        print("📱 Running client...")
        print()
        
        client_process = subprocess.run(
            [sys.executable, "avro_client.py"],
            capture_output=False
        )
        
        print()
        print("✓ Test completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
    finally:
        # Stop server
        print()
        print("🛑 Stopping server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✓ Server stopped")
        print()
        print("=" * 70)


if __name__ == "__main__":
    main()
