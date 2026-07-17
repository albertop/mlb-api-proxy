#!/usr/bin/env python
"""
Convenience script to run response collection with common presets.

Usage:
    python run_response_collection.py              # Default: localhost:8000
    python run_response_collection.py prod         # Production URL (if configured)
    python run_response_collection.py staging      # Staging URL (if configured)
"""

import subprocess
import sys
from pathlib import Path

# Environment presets
PRESETS = {
    "local": "http://localhost:8000",
    "dev": "http://localhost:8000",
    "staging": "https://api-staging.example.com",
    "prod": "https://api.example.com",
}

# These will be replaced with your actual URLs
ACTIVE_PRESETS = {
    "local": "http://localhost:8000",
    "dev": "http://localhost:8000",
}


def run_collection(preset: str = "local"):
    """Run the response collection script."""
    if preset not in ACTIVE_PRESETS:
        print(f"❌ Unknown preset: {preset}")
        print(f"Available presets: {', '.join(ACTIVE_PRESETS.keys())}")
        sys.exit(1)

    url = ACTIVE_PRESETS[preset]
    print(f"🚀 Starting response collection for: {preset}")
    print(f"📍 Target: {url}\n")

    try:
        result = subprocess.run(
            [sys.executable, "utils/collect_api_responses.py", "--base-url", url],
            check=True
        )
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Collection failed with exit code {e.returncode}")
        print("\nTroubleshooting:")
        print("1. Check that the API proxy is running:")
        print("   cd api-service && uvicorn main:app --host 0.0.0.0 --port 8000")
        print("2. Check network connectivity")
        print("3. View the script output above for specific error")
        sys.exit(1)


def main():
    """Main entry point."""
    preset = sys.argv[1] if len(sys.argv) > 1 else "local"

    # Show available presets
    if preset == "--help" or preset == "-h":
        print("Response Collection Presets\n")
        print("Usage: python run_response_collection.py [PRESET]\n")
        print("Available presets:")
        for name, url in ACTIVE_PRESETS.items():
            print(f"  • {name}: {url}")
        print("\nExamples:")
        print("  python run_response_collection.py          # Uses 'local' preset")
        print("  python run_response_collection.py local    # Explicit local preset")
        print("\nOutput:")
        print("  • docs/response-examples/      - Organized response files")
        print("  • docs/API_RESPONSE_CATALOG.md - Navigation hub")
        print("  • docs/response-examples-index.json - Machine-readable index")
        sys.exit(0)

    run_collection(preset)


if __name__ == "__main__":
    main()
