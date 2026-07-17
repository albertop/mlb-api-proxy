# API Response Collection Guide

## Overview

The `utils/collect_api_responses.py` script automatically collects response examples from all API endpoints and organizes them into a structured documentation system.

## What It Does

✅ Scans all 33 API routers (`api-service/routers/*.py`)
✅ Extracts ~190 endpoints from each router
✅ Makes intelligent test calls to each endpoint
✅ Captures actual HTTP responses (success and errors)
✅ Organizes responses by router domain
✅ Generates machine-readable index (`response-examples-index.json`)
✅ Generates human-readable catalog (`API_RESPONSE_CATALOG.md`)
✅ Creates router-specific README files

## Prerequisites

1. **API Proxy Running**: The script calls your local proxy, so start it first:
   ```bash
   cd api-service
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Dependencies**: Already installed via requirements.txt
   - `httpx` - Making HTTP requests
   - `pathlib`, `json` - File handling

## Running the Script

### Quick Start (Default)
```bash
python utils/collect_api_responses.py
```
This connects to `http://localhost:8000` (default)

### Custom Base URL
```bash
python utils/collect_api_responses.py --base-url http://your-api:8080
```

### Expected Output
```
🔍 Starting API response collection...

📁 TEAMS (15 endpoints)
  ✓ [1/15] GET /api/v1/teams
  ✓ [2/15] GET /api/v1/teams/{teamId}
  ✓ [3/15] GET /api/v1/teams/{teamId}/roster
  ...
  ⊘ [15/15] DELETE /api/v1/teams/{teamId} (skipped)

✅ Collected 189/190 responses

💾 Saving responses...
✅ Responses saved to docs/response-examples
📋 Index: docs/response-examples-index.json
📑 Catalog: docs/API_RESPONSE_CATALOG.md

============================================================
API RESPONSE COLLECTION SUMMARY
============================================================

Total Routers: 33
Total Responses: 189

Responses by Router:
  • analytics: 8 responses (8 successful)
  • teams: 15 responses (14 successful)
  • people: 9 responses (8 successful)
  ...

✨ Done! Documentation is ready for client development.
```

## Output Structure

```
docs/
├── API_RESPONSE_CATALOG.md              # Navigation hub
├── response-examples-index.json         # Machine-readable index
└── response-examples/
    ├── teams/
    │   ├── README.md
    │   ├── get_teams.json
    │   ├── get_team_by_id.json
    │   ├── get_team_roster.json
    │   └── errors.json
    ├── people/
    │   ├── README.md
    │   ├── get_person.json
    │   └── errors.json
    ├── games/
    │   ├── README.md
    │   ├── get_game.json
    │   └── errors.json
    └── ... (other routers)
```

## Using the Collected Responses

### 1. **As Client Documentation**
Open `docs/API_RESPONSE_CATALOG.md` in your browser/IDE:
- Navigate to endpoint you're interested in
- Click response file link
- View actual JSON structure

### 2. **For Client Code Generation**
Use `docs/response-examples-index.json` to programmatically access metadata:
```python
import json

with open("docs/response-examples-index.json") as f:
    catalog = json.load(f)

for router in catalog["routers"]:
    print(f"Router: {router['name']}")
    for endpoint in router["endpoints"]:
        print(f"  {endpoint['method']} {endpoint['path']}")
        print(f"  Response: {endpoint['file']}")
```

### 3. **For Integration Testing**
Load response examples in tests:
```python
import json

def test_teams_response_format():
    with open("docs/response-examples/teams/get_teams.json") as f:
        response = json.load(f)
        
    assert response["status_code"] == 200
    assert "response" in response
    assert "teams" in response["response"]
```

### 4. **For API Client Libraries**
Reference response files as schema examples:
```typescript
// teams.ts - Client library
import teamResponse from "../../../docs/response-examples/teams/get_teams.json";

export interface Team extends typeof teamResponse.response.teams[0] {}

export class TeamsClient {
  async getTeams(): Promise<Team[]> { ... }
}
```

## Response File Format

Each response file contains:
```json
{
  "endpoint": "/api/v1/teams",
  "method": "GET",
  "url": "http://localhost:8000/api/v1/teams?sportId=1",
  "status_code": 200,
  "headers": {
    "content-type": "application/json",
    "content-length": "5243"
  },
  "response": {
    "copyright": "...",
    "teams": [...]
  },
  "error": null,
  "timestamp": "2026-02-07T14:32:45.123456"
}
```

## Troubleshooting

### Issue: `Connection refused` or timeout
**Solution**: Make sure the API proxy is running:
```bash
cd api-service
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Issue: Some endpoints return 404 or 422
**Solution**: This is normal and expected. The script captures error responses too:
- Check `docs/response-examples/{router}/errors.json` for error examples
- These show validation requirements

### Issue: Script takes too long
**Solution**: 
- 190 endpoints × ~2-3 seconds each = ~10-15 minutes total
- This is a one-time operation
- Run it once and commit responses to git

### Issue: Some path parameters not recognized
**Solution**: The script has a fixed set of sample parameters. If endpoints use custom parameters not in the system, they'll be skipped. Add more parameter mappings to `build_test_url()` method if needed.

## Customization

### Add Custom Test Parameters
Edit `utils/collect_api_responses.py` and modify the replacements dictionary:
```python
def build_test_url(self, endpoint: Dict[str, Any]) -> Optional[str]:
    replacements = {
        "{teamId}": str(SAMPLE_TEAM_IDS[0]),
        "{customId}": "123",  # NEW
        # ... other params
    }
```

### Filter Specific Routers
Modify `collect_all_responses()` to skip certain routers:
```python
for router_name, endpoints in endpoints_by_router.items():
    if router_name in ["internal", "debug"]:  # Skip these
        continue
    # ... collect responses
```

### Change Output Directory
Edit at top of script:
```python
RESPONSE_EXAMPLES_DIR = Path("docs/response-examples")  # Change this
```

## Integration with CI/CD

Add to your CI pipeline to auto-generate docs:
```yaml
# .github/workflows/update-docs.yml
- name: Collect API Responses
  run: |
    pip install -r requirements.txt
    python utils/collect_api_responses.py
    
- name: Commit changes
  run: |
    git add docs/response-examples* docs/API_RESPONSE_CATALOG.md
    git commit -m "docs: update API response examples"
    git push
```

## Next Steps

1. **Run the script** once to collect all responses
2. **Commit results** to git:
   ```bash
   git add docs/response-examples/ docs/API_RESPONSE_CATALOG.md docs/response-examples-index.json
   git commit -m "docs: collect and organize API response examples"
   ```
3. **Share with clients** - Point them to `docs/API_RESPONSE_CATALOG.md`
4. **Use for code generation** - Reference responses when building client libraries
5. **Regenerate periodically** - If API responses change significantly

## FAQ

**Q: How long does collection take?**
A: ~10-15 minutes depending on network speed and API response times.

**Q: Can I run this while API is in production?**
A: Only if you use a staging/test instance with `--base-url`. Live production calls are read-only by design.

**Q: What about POST/PUT/DELETE endpoints?**
A: The script handles them, but most will return 400+ errors (no valid data in request bodies). The script captures these errors to show validation requirements.

**Q: Can I extend this for other APIs?**
A: Yes! The script is generic and can work with any FastAPI project. Just adjust sample parameters and router directory.

**Q: How do I use this for OpenAPI schema generation?**
A: The responses can feed into tools like `quicktype` or `jsonschema2typescript` to generate TypeScript/Python models.
