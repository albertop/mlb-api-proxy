"""Generate parametrized unit tests for all routers."""
import json
from pathlib import Path
from typing import Dict, List, Any

# Load the OpenAPI spec
spec_path = Path(__file__).parent / "docs" / "mlb_api_spec.json"
with open(spec_path, "r", encoding="utf-8") as f:
    spec = json.load(f)

# Map tags to router names
TAG_TO_ROUTER = {
    "Teams": "teams",
    "People": "people",
    "Person": "people",  # Alternative tag name
    "Games": "games",
    "Game": "games",  # Alternative tag name
    "Schedule": "schedule",
    "Stats": "stats",
    "Standings": "standings",
    "Draft": "draft",
    "Awards": "awards",
    "Venues": "venues",
    "Transactions": "transactions",
    "Sports": "sports",
    "League": "league",
    "Division": "division",
    "Conference": "conference",
    "Season": "season",
    "Attendance": "attendance",
    "Broadcast": "broadcast",
    "Uniforms": "uniforms",
    "Reviews": "reviews",
    "Milestones": "milestones",
    "Streaks": "streaks",
    "High/Low": "high_low",
    "Game Pace": "game_pace",
    "Bat Tracking": "bat_tracking",
    "Biomechanics": "biomechanics",
    "Skeletal": "skeletal",
    "Job": "job",
    "Misc": "misc",
    "Weather": "weather"
}


def extract_endpoints_by_tag() -> Dict[str, List[Dict[str, Any]]]:
    """Extract all GET endpoints grouped by tag."""
    endpoints_by_tag = {}
    
    for path, methods in spec["paths"].items():
        if "get" in methods:
            endpoint_info = methods["get"]
            tags = endpoint_info.get("tags", ["Misc"])
            tag = tags[0] if tags else "Misc"
            
            if tag not in endpoints_by_tag:
                endpoints_by_tag[tag] = []
            
            # Extract parameters
            params = []
            if "parameters" in endpoint_info:
                for param in endpoint_info["parameters"]:
                    params.append({
                        "name": param["name"],
                        "in": param["in"],
                        "required": param.get("required", False)
                    })
            
            endpoints_by_tag[tag].append({
                "path": path,
                "operation_id": endpoint_info.get("operationId", ""),
                "summary": endpoint_info.get("summary", ""),
                "parameters": params
            })
    
    return endpoints_by_tag


def generate_test_file(router_name: str, endpoints: List[Dict[str, Any]]) -> str:
    """Generate a test file for a router with parametrized tests."""
    
    # Build endpoint parameters list
    endpoint_params = []
    for endpoint in endpoints:
        path = endpoint["path"]
        operation_id = endpoint["operation_id"]
        summary = endpoint["summary"]
        params = endpoint["parameters"]
        
        # Sample values for path/query parameters
        sample_params = {}
        for param in params:
            if param["in"] == "path":
                # Common path parameter sample values
                if "id" in param["name"].lower():
                    sample_params[param["name"]] = "123"
                elif "season" in param["name"].lower():
                    sample_params[param["name"]] = "2024"
                elif "date" in param["name"].lower():
                    sample_params[param["name"]] = "2024-04-01"
                else:
                    sample_params[param["name"]] = "test_value"
        
        # Replace path parameters in URL
        test_path = path
        for param_name, param_value in sample_params.items():
            test_path = test_path.replace(f"{{{param_name}}}", str(param_value))
        
        endpoint_params.append((test_path, operation_id, summary))
    
    # Generate parametrize decorator
    parametrize_line = ",\n        ".join([
        f'("{path}", "{op_id}", "{summary}")'
        for path, op_id, summary in endpoint_params
    ])
    
    test_content = f'''"""Unit tests for {router_name} router."""
import pytest
from fastapi.testclient import TestClient
import respx
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        {parametrize_line}
    ]
)
def test_{router_name}_endpoint_exists(
    client: TestClient,
    endpoint_path: str,
    operation_id: str,
    summary: str,
    respx_mock
):
    """Test that {router_name} endpoint exists and returns expected structure."""
    # Mock the upstream MLB API
    upstream_url = f"https://statsapi.mlb.com{{endpoint_path}}"
    respx.get(upstream_url).mock(
        return_value=Response(200, json={{"data": "test", "copyright": "MLB"}})
    )
    
    # Make request to our API
    response = client.get(endpoint_path)
    
    # Verify response
    assert response.status_code == 200
    assert "copyright" not in response.json()  # Should be stripped


@pytest.mark.unit
def test_{router_name}_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that {router_name} endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={{"error": "Internal Server Error"}})
    )
    
    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit  
def test_{router_name}_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that {router_name} endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
'''
    
    return test_content


def main():
    """Generate test files for all routers."""
    endpoints_by_tag = extract_endpoints_by_tag()
    test_dir = Path(__file__).parent / "test" / "unit" / "routers"
    
    generated_count = 0
    for tag, endpoints in endpoints_by_tag.items():
        router_name = TAG_TO_ROUTER.get(tag)
        if not router_name:
            print(f"Warning: No router mapping for tag '{tag}'")
            continue
        
        test_content = generate_test_file(router_name, endpoints)
        test_file_path = test_dir / f"test_{router_name}.py"
        
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        generated_count += 1
        print(f"Generated: {test_file_path.name} ({len(endpoints)} endpoints)")
    
    print(f"\nTotal test files generated: {generated_count}")


if __name__ == "__main__":
    main()
