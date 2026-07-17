# Implementation Guide: Missing Endpoint

## Missing Endpoint Summary
- **Path**: `/api/v1/leagues/allStarBallot`
- **Method**: GET
- **Router File**: `api-service/routers/league.py`
- **Status**: Not yet implemented
- **Estimated Effort**: 2 minutes

---

## Implementation Steps

### 1. Open league.py
File: `api-service/routers/league.py`

### 2. Add the Missing Endpoint

Insert the following code after the existing `/api/v1/league/allStarBallot` endpoint (around line 31):

```python
@router.get("/api/v1/leagues/allStarBallot")
async def get_leagues_all_star_ballot(
    request: Request,
    x_api_key: Optional[str] = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagues/allStarBallot", x_api_key)
```

### 3. Verify Implementation

After adding the endpoint:

1. Test the endpoint with curl or your API client:
   ```bash
   curl "http://localhost:8000/api/v1/leagues/allStarBallot" \
     -H "x-api-key: YOUR_API_KEY"
   ```

2. Run the validation script again to confirm 100% alignment:
   ```bash
   python validation_script.py
   ```

3. You should see:
   ```
   league.py                 | League               |  100.0% | 12/12 | 0 missing
   Overall alignment: 100.0%
   ```

---

## Code Context

### Current league.py Structure (approx. line 31):

```python
@router.get("/api/v1/league/allStarBallot")
async def get_league_all_star_ballot_general(
    request: Request,
    x_api_key: Optional[str] = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/league/allStarBallot", x_api_key)


# INSERT NEW ENDPOINT HERE ↓↓↓

@router.get("/api/v1/leagues")
async def get_leagues(
    request: Request,
    x_api_key: Optional[str] = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagues", x_api_key)
```

### After Addition:

```python
@router.get("/api/v1/league/allStarBallot")
async def get_league_all_star_ballot_general(
    request: Request,
    x_api_key: Optional[str] = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/league/allStarBallot", x_api_key)


@router.get("/api/v1/leagues/allStarBallot")
async def get_leagues_all_star_ballot(
    request: Request,
    x_api_key: Optional[str] = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagues/allStarBallot", x_api_key)


@router.get("/api/v1/leagues")
async def get_leagues(
    request: Request,
    x_api_key: Optional[str] = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagues", x_api_key)
```

---

## Endpoint Behavior

This endpoint:
- **Retrieves** All-Star ballot information for **all leagues** in a single request
- **Requires** valid MLB API authentication (X-API-Key header)
- **Returns** JSON response containing All-Star ballot data across all leagues
- **Complements** the existing `/api/v1/leagues/{leagueId}/allStarBallot` endpoint which gets data for a specific league

---

## Testing After Implementation

### Example Request:
```bash
GET /api/v1/leagues/allStarBallot HTTP/1.1
Host: localhost:8000
x-api-key: your-api-key-here
Accept: application/json
```

### Expected Response:
```json
{
  "leaguesResult": {
    "resultsSets": [
      {
        "resultsMetadata": {
          "timestamp": "2026-02-07T...",
          ...
        },
        "results": [
          {
            "leagueId": 103,
            "leagueName": "American League",
            "allStarBallot": [
              ...
            ]
          },
          {
            "leagueId": 104,
            "leagueName": "National League",
            "allStarBallot": [
              ...
            ]
          }
        ]
      }
    ]
  }
}
```

---

## Validation Checklist

- [ ] Added endpoint to league.py
- [ ] Method is GET
- [ ] Path is `/api/v1/leagues/allStarBallot`
- [ ] Function signature matches existing pattern
- [ ] X-API-Key header is properly forwarded
- [ ] Ran validation script to confirm 100% alignment
- [ ] Tested endpoint with API client
- [ ] Response data matches expected structure
- [ ] Deployment ready

---

## Related Endpoints (for context)

These similar endpoints already exist and work correctly:
- ✅ `/api/v1/league/allStarBallot` - Single league ballot
- ✅ `/api/v1/leagues/{leagueId}/allStarBallot` - Specific league ballot
- ✅ `/api/v1/leagues` - All leagues list
- NEW → `/api/v1/leagues/allStarBallot` - All leagues ballots (to implement)

---

## Support

If you need help or have questions about any implementation details, refer to:
1. [VALIDATION_REPORT.md](./VALIDATION_REPORT.md) - Complete validation results
2. [Existing router implementations](./api-service/routers/) - Code examples
3. [proxy.py](./api-service/proxy.py) - Forward_get function details
