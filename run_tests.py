"""Test runner script for MLB API test suite.

This script provides convenient commands to run different test suites.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Main test runner."""
    if len(sys.argv) < 2:
        print("MLB API Test Runner")
        print("\nUsage: python run_tests.py <command>")
        print("\nAvailable commands:")
        print("  all          - Run all tests")
        print("  unit         - Run unit tests only (fast)")
        print("  integration  - Run integration tests")
        print("  smoke        - Run smoke tests")
        print("  critical     - Run critical flow tests")
        print("  coverage     - Run tests with coverage report")
        print("  quick        - Run unit tests with minimal output")
        print("  router NAME - Run tests for specific router (e.g., teams)")
        print("\nExamples:")
        print("  python run_tests.py unit")
        print("  python run_tests.py router teams")
        print("  python run_tests.py coverage")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Base pytest command
    pytest_cmd = [sys.executable, "-m", "pytest"]
    
    if command == "all":
        return run_command(pytest_cmd, "All Tests")
    
    elif command == "unit":
        return run_command(
            pytest_cmd + ["-m", "unit", "test/unit/"],
            "Unit Tests"
        )
    
    elif command == "integration":
        return run_command(
            pytest_cmd + ["-m", "integration", "test/integration/"],
            "Integration Tests"
        )
    
    elif command == "smoke":
        return run_command(
            pytest_cmd + ["-m", "smoke", "--smoke", "test/smoke/"],
            "Smoke Tests"
        )
    
    elif command == "critical":
        return run_command(
            pytest_cmd + ["test/unit/test_critical_flows.py"],
            "Critical Flow Tests"
        )
    
    elif command == "coverage":
        return run_command(
            pytest_cmd + ["--cov", "--cov-report=html", "--cov-report=term"],
            "All Tests with Coverage"
        )
    
    elif command == "quick":
        return run_command(
            pytest_cmd + ["-m", "unit", "-q", "--tb=line"],
            "Quick Unit Tests"
        )
    
    elif command == "router":
        if len(sys.argv) < 3:
            print("Error: Please specify a router name")
            print("Example: python run_tests.py router teams")
            return 1
        router_name = sys.argv[2]
        return run_command(
            pytest_cmd + [f"test/unit/routers/test_{router_name}.py"],
            f"Tests for {router_name} router"
        )
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Run 'python run_tests.py' to see available commands")
        return 1


if __name__ == "__main__":
    sys.exit(main())
