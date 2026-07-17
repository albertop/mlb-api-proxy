"""
Comprehensive API Response Collection Script

This script collects actual API responses from all endpoints and organizes them
into a documented structure with:
- Individual response JSON files organized by router
- Machine-readable index (response-examples-index.json)
- Human-readable catalog (API_RESPONSE_CATALOG.md)
- Router-specific README files

Usage:
    python utils/collect_api_responses.py [--base-url http://localhost:8000]
"""

import sys
import os
import re
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import httpx
from collections import defaultdict

# Set environment variables before importing app
os.environ.setdefault("MLB_API_BASE_URL", "https://statsapi.mlb.com")
os.environ.setdefault("PROXY_API_KEY", "local-3f2f6c8b0f4e4df3a6a1d2c9b4c7e8f1")
os.environ.setdefault("MLB_API_KEY", "test_api_key")

# Sample test data from conftest.py
SAMPLE_TEAM_IDS = [147, 121, 111, 110, 108]
SAMPLE_PERSON_IDS = [608070, 665742, 677594, 691406, 664285]
SAMPLE_PITCHERS_IDS = [664285, 608032]
SAMPLE_GAME_PKS = [776135, 776136, 776137]
SAMPLE_CONFERENCE_IDS = [301,302]
SAMPLE_SEASONS = [2024, 2023, 2022]
SAMPLE_DATES = ["2024-04-01", "2024-05-15", "2024-09-01"]
SAMPLE_VENUE_IDS = [5380]
SAMPLE_LEAGUE_IDS = [103, 104]

# Default API Base URL
DEFAULT_BASE_URL = "http://10.0.0.39:3002"

# API Key for authentication
DEFAULT_API_KEY = "local-3f2f6c8b0f4e4df3a6a1d2c9b4c7e8f1"

# Output directory structure
ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
RESPONSE_EXAMPLES_DIR = DOCS_DIR / "response-examples"


class APIResponseCollector:
    """Collects and organizes API responses."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            headers={"x-api-key": DEFAULT_API_KEY},
            timeout=10.0,
            follow_redirects=True
        )
        self.responses: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.endpoints: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def parse_router_files(self) -> Dict[str, List[Dict[str, Any]]]:
        """Parse all router files to extract endpoints."""
        routers_dir = ROOT_DIR / "api-service" / "routers"
        endpoints_by_router = defaultdict(list)

        for router_file in routers_dir.glob("*.py"):
            if router_file.name.startswith("__"):
                continue

            router_name = router_file.stem
            with open(router_file, "r") as f:
                content = f.read()

            # Extract route definitions
            route_pattern = r'@router\.(?:get|post|put|delete|patch)\(["\']([^"\']+)["\']'
            methods_pattern = r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'

            for match in re.finditer(methods_pattern, content):
                method, path = match.group(1), match.group(2)
                endpoints_by_router[router_name].append({
                    "method": method.upper(),
                    "path": path,
                    "router": router_name
                })

        return endpoints_by_router

    def build_test_url(self, endpoint: Dict[str, Any]) -> Optional[str]:
        """Build a testable URL with sample parameters."""
        path = endpoint["path"]

        # Replace path parameters with sample values
        replacements = {
            "{teamId}": str(SAMPLE_TEAM_IDS[0]),
            "{team_id}": str(SAMPLE_TEAM_IDS[0]),
            "{personId}": str(SAMPLE_PERSON_IDS[0]),
            "{person_id}": str(SAMPLE_PERSON_IDS[0]),
            "{game_pk}": str(SAMPLE_GAME_PKS[0]),
            "{playerId}": str(SAMPLE_PERSON_IDS[0]),
            "{venueId}": "5380",
            "{venue_id}": "5380",
            "{sportId}": "1",
            "{sport_id}": "1",
            "{leagueId}": str(SAMPLE_LEAGUE_IDS[0]),
            "{league_id}": str(SAMPLE_LEAGUE_IDS[0]),
            "{divisionId}": "200",
            "{division_id}": "200",
            "{conference_id}": str(SAMPLE_CONFERENCE_IDS[0]),
            "{award_id}": "MLBHOF",
            "{guid}": "1a2b3c4d",
            "{season}": str(SAMPLE_SEASONS[0]),
            "{season_id}": str(SAMPLE_SEASONS[0]),
            "{year}": str(SAMPLE_SEASONS[0]),
            "{date}": SAMPLE_DATES[0],
            "{roster_type}": "active",
            "{standings_type}": "regularSeason",
            "{schedule_type}": "regularSeason",
            "{high_low_type}": "player",
            "{umpire_id}": "596809",
        }

        # Replace all found parameters
        for param, value in replacements.items():
            if param in path:
                path = path.replace(param, value)

        # If path still has unmatched parameters, skip it
        if "{" in path:
            return None

        return f"{self.base_url}{path}"

    def build_query_params(self, endpoint: Dict[str, Any]) -> Dict[str, str]:
        """Build sensible query parameters based on endpoint."""
        path = endpoint["path"].lower()
        params = {}

        # Intelligent parameter building based on endpoint patterns
        if path.startswith("/api/v1/seasons"):
            params["sportId"] = "1"
        elif "/people/freeagents" in path:
            params["season"] = str(SAMPLE_SEASONS[0])
        elif "season" in path:
            params["season"] = str(SAMPLE_SEASONS[0])
        
        if "/people/changes" in path:
            params["updatedSince"] = "2025-01-01"
        
        if "broadcast" in path:
            params["broadcasterIds"] = "6245,6246"

        # Jobs requires jobType
        if path == "/api/v1/jobs":
            params["jobType"] = "UMPR"

        # Schedule requires sportId or gamePk
        if path == "/api/v1/schedule":
            params["sportId"] = "1"
        elif path == "/api/v1/venues":
            params["sportId"] = "1"
        elif path == "/api/v1/schedule/games/tied":
            params["season"] = str(SAMPLE_SEASONS[0])
        elif "schedule" in path and path != "/api/v1/schedule":
            params["startDate"] = SAMPLE_DATES[0]
            params["endDate"] = SAMPLE_DATES[1]
        
        # Uniforms requires gamePks or teamIds as lists
        if path == "/api/v1/uniforms/game":
            params["gamePks"] = str(SAMPLE_GAME_PKS[0])
        elif path == "/api/v1/uniforms/team":
            params["teamIds"] = str(SAMPLE_TEAM_IDS[0])
        
        # Game Pace requires season and sportId
        if path == "/api/v1/gamepace":
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportId"] = "1"
        
        # AllStarBallot endpoints require season
        if "allstarballot" in path:
            params["season"] = str(SAMPLE_SEASONS[0])
            if path == "/api/v1/leagues/allstarballot":
                params["leagueIds"] = "103,104"
            if path == "/api/v1/sports/{sport_id}/allsportballot":
                params["sportId"] = "1"

        if path == "/api/v1/sports/{sport_id}/allsportballot":
            params["season"] = "2025"
        
        # Milestones requires season
        if path == "/api/v1/milestones":
            params["season"] = str(SAMPLE_SEASONS[0])
        
        # MilestoneStatistics requires season
        if path == "/api/v1/milestonestatistics":
            params["season"] = str(SAMPLE_SEASONS[0])

        if path == "/api/v1/highlow/{high_low_type}":
            params["season"] = "2025"
            params["sportId"] = "1"
            params["statGroup"] = "hitting"
            params["sortStat"] = "atBats"

        # AchievementStatuses requires sportId
        if path == "/api/v1/achievementstatuses":
            params["sportId"] = "1"

        # MilestoneDurations requires sportId
        if path == "/api/v1/milestonedurations":
            params["sportId"] = "1"
        
        # Review requires sportId and season
        if path == "/api/v1/review":
            params["sportId"] = "1"
            params["season"] = str(SAMPLE_SEASONS[0])
        
        # Seasons/all requires sportId
        if path == "/api/v1/seasons/all":
            params["sportId"] = "1"
        
        # Standings requires leagueId, season, and standingsTypes
        if path == "/api/v1/standings":
            params["leagueId"] = "103,104"
            params["season"] = str(SAMPLE_SEASONS[0])
            params["standingsTypes"] = "regularSeason"
        
        if "team" in path and "{teamId}" not in path and "{team_id}" not in path and path not in ["/api/v1/uniforms/team", "/api/v1/teams/affiliates", "/api/v1/teams/history", "/api/v1/teams/stats", "/api/v1/teams/stats/leaders"]:
            params["teamId"] = str(SAMPLE_TEAM_IDS[0])

        if path == "/api/v1/teams/{team_id}/alumni":
            params["season"] = "2025"

        if path == "/api/v1/teams/{team_id}/leaders":
            params["season"] = "2025"
            params["sportId"] = "1"
            params["leaderCategories"] = "homeRuns"
            params["statGroup"] = "hitting"

        if path == "/api/v1/teams/{team_id}/stats":
            params["season"] = "2025"
            params["stats"] = "season"
            params["group"] = "hitting"
            params["sportId"] = "1"
        
        if "/people/" in path and "/stats" in path:
            params["stats"] = "season"
            params["group"] = "hitting"
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportId"] = "1"

        if "/people/" in path and "/stats/game/" in path:
            params["stats"] = "gameLog"
            params["group"] = "hitting"
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportId"] = "1"

        if "person" in path and "{personId}" not in path:
            params["personId"] = str(SAMPLE_PERSON_IDS[0])
        
        if path == "/api/v1/people":
            params["personId"] = str(SAMPLE_PERSON_IDS[0])
        
        if "game" in path:
            params["gamePk"] = str(SAMPLE_GAME_PKS[0])
        
        # Stats endpoints with specific parameters
        if path == "/api/v1/stats":
            params["stats"] = "season"
            params["group"] = "hitting"
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportId"] = "1"
            params["playerPool"] = "ALL"
        elif path == "/api/v1/stats/grouped":
            params["group"] = "hitting"
            params["stats"] = "season"
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportIds"] = "1"
        elif "stat" in path or "stats" in path:
            params["type"] = "hitting"
        
        if "group" in path:
            params["group"] = "hitting"
        
        if "homerunballpark" in path:
            params["isHomeRunParks"] = "true"
        
        # Teams/affiliates requires teamIds and season
        if path == "/api/v1/teams/affiliates":
            params["teamIds"] = str(SAMPLE_TEAM_IDS[0])
            params["season"] = str(SAMPLE_SEASONS[0])
        
        # Teams/history requires teamIds and season
        if path == "/api/v1/teams/history":
            params["teamIds"] = str(SAMPLE_TEAM_IDS[0])
            params["season"] = str(SAMPLE_SEASONS[0])
        
        # Teams/stats requires season, sportIds, stats, group, and teamIds
        if path == "/api/v1/teams/stats":
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportIds"] = "1"
            params["stats"] = "season"
            params["group"] = "hitting"
            params["teamIds"] = str(SAMPLE_TEAM_IDS[0])
        
        # Teams/stats/leaders requires season, sportId, leaderCategories, and statGroup
        if path == "/api/v1/teams/stats/leaders":
            params["season"] = str(SAMPLE_SEASONS[0])
            params["sportId"] = "1"
            params["leaderCategories"] = "homeRuns"
            params["statGroup"] = "hitting"

        return params

    async def collect_response(
        self,
        endpoint: Dict[str, Any],
        test_url: Optional[str] = None,
        query_params: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Collect a single API response."""
        if not test_url:
            test_url = self.build_test_url(endpoint)

        if not test_url:
            return None

        if not query_params:
            query_params = self.build_query_params(endpoint)

        try:
            method = endpoint["method"].lower()
            if endpoint["path"] == "/api/v1/attendance":
                attendance_param_sets = [
                    {"season": "2025", "sportId": "1", "leagueId": "103"},
                    {"teamId": "106"},
                ]
                response = None
                for param_set in attendance_param_sets:
                    response = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda params=param_set: getattr(self.client, method)(
                            test_url,
                            params=params,
                        )
                    )
                    if 200 <= response.status_code < 300:
                        break
            elif endpoint["path"] == "/api/v1/transactions":
                transaction_param_sets = [
                    {"playerId": str(SAMPLE_PERSON_IDS[0])},
                    {"teamId": "106"},
                    {"date": "07/31/2025"},
                    {"startDate": "07/31/2025", "endDate": "07/31/2025"},
                ]
                response = None
                for param_set in transaction_param_sets:
                    response = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda params=param_set: getattr(self.client, method)(
                            test_url,
                            params=params,
                        )
                    )
                    if 200 <= response.status_code < 300:
                        break
            elif endpoint["path"] == "/api/v1/people/{person_id}":
                # Player stats with different hydrate parameters (hitting, pitching, fielding)
                # Collect ALL variations separately, not just first success
                player_stats_param_sets = [
                    # Hitting stats with different types
                    {"sportId": "1", "hydrate": "stats(group=[hitting],gameType=[R],type=[season],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    {"sportId": "1", "hydrate": "stats(group=[hitting],gameType=[R],type=[seasonAdvanced],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    {"sportId": "1", "hydrate": "stats(group=[hitting],gameType=[R],type=[sabermetrics],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    # Pitching stats with different types
                    {"sportId": "1", "hydrate": "stats(group=[pitching],gameType=[R],type=[season],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    {"sportId": "1", "hydrate": "stats(group=[pitching],gameType=[R],type=[seasonAdvanced],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    {"sportId": "1", "hydrate": "stats(group=[pitching],gameType=[R],type=[sabermetrics],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    # Fielding stats with different types
                    {"sportId": "1", "hydrate": "stats(group=[fielding],gameType=[R],type=[season],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                    {"sportId": "1", "hydrate": "stats(group=[fielding],gameType=[R],type=[sabermetrics],startDate=01/01/2025,endDate=12/31/2025,season=2025)"},
                ]
                response = None
                for param_set in player_stats_param_sets:
                    response = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda params=param_set: getattr(self.client, method)(
                            test_url,
                            params=params,
                        )
                    )
                    # Always return first response (we'll collect all in collect_all_responses)
                    if 200 <= response.status_code < 300:
                        break
            else:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: getattr(self.client, method)(test_url, params=query_params)
                )

            return {
                "endpoint": endpoint["path"],
                "method": endpoint["method"],
                "url": str(response.url),
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "response": response.json() if response.status_code < 400 else None,
                "error": response.text if response.status_code >= 400 else None,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "endpoint": endpoint["path"],
                "method": endpoint["method"],
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def collect_all_responses(self, endpoints_by_router: Dict[str, List[Dict]]):
        """Collect responses from all endpoints."""
        print("[*] Starting API response collection...")
        total_endpoints = sum(len(eps) for eps in endpoints_by_router.values())
        collected = 0

        for router_name, endpoints in endpoints_by_router.items():
            router_responses = []
            print(f"\n[{router_name.upper()}] ({len(endpoints)} endpoints)")

            for idx, endpoint in enumerate(endpoints, 1):
                if endpoint["path"] == "/api/v1/schedule/{schedule_type}":
                    print(f"  [SKIP] [{idx}/{len(endpoints)}] {endpoint['method']} {endpoint['path']}")
                    continue
                
                # Special handling for player stats endpoint with multiple hydrate variations
                if endpoint["path"] == "/api/v1/people/{person_id}":
                    # Define all player stats variations
                    player_stats_param_sets = [
                        # Hitting stats with different types (use hitter)
                        ("hitting", SAMPLE_PERSON_IDS[0], {"sportId": "1", "hydrate": "stats(group=[hitting],gameType=[R],type=[season],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        ("hitting", SAMPLE_PERSON_IDS[0], {"sportId": "1", "hydrate": "stats(group=[hitting],gameType=[R],type=[seasonAdvanced],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        ("hitting", SAMPLE_PERSON_IDS[0], {"sportId": "1", "hydrate": "stats(group=[hitting],gameType=[R],type=[sabermetrics],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        # Pitching stats with different types (use pitcher)
                        ("pitching", SAMPLE_PITCHERS_IDS[0], {"sportId": "1", "hydrate": "stats(group=[pitching],gameType=[R],type=[season],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        ("pitching", SAMPLE_PITCHERS_IDS[0], {"sportId": "1", "hydrate": "stats(group=[pitching],gameType=[R],type=[seasonAdvanced],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        ("pitching", SAMPLE_PITCHERS_IDS[0], {"sportId": "1", "hydrate": "stats(group=[pitching],gameType=[R],type=[sabermetrics],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        # Fielding stats with different types (use hitter)
                        ("fielding", SAMPLE_PERSON_IDS[0], {"sportId": "1", "hydrate": "stats(group=[fielding],gameType=[R],type=[season],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                        ("fielding", SAMPLE_PERSON_IDS[0], {"sportId": "1", "hydrate": "stats(group=[fielding],gameType=[R],type=[sabermetrics],startDate=01/01/2025,endDate=12/31/2025,season=2025)"}),
                    ]
                    
                    # Collect each variation with appropriate person ID
                    for stat_group_name, person_id, param_set in player_stats_param_sets:
                        test_endpoint = endpoint.copy()
                        test_endpoint["path"] = endpoint["path"].replace("{person_id}", str(person_id))
                        test_url = self.build_test_url(test_endpoint)
                        
                        if test_url:
                            response_data = await self.collect_response(test_endpoint, test_url, param_set)
                            if response_data:
                                # Add variation metadata to response
                                stat_type = param_set.get("hydrate", "").split("type=[")[1].split("]")[0] if "type=[" in param_set.get("hydrate", "") else "unknown"
                                response_data["variation"] = f"{stat_group_name}_{stat_type}"
                                # Ensure endpoint is the resolved path (with person_id replaced)
                                response_data["endpoint"] = test_endpoint["path"]
                                
                                print(f"    [VARIATION] {stat_group_name}_{stat_type} -> variation set: {response_data.get('variation')}")
                                
                                router_responses.append(response_data)
                                status_code = response_data.get("status_code", 0)
                                status = "[OK]" if (200 <= status_code < 300) else "[FAIL]"
                                print(f"  {status} [{idx}/{len(endpoints)}] {endpoint['method']} {endpoint['path']} (person_id={person_id}, {stat_group_name}/{stat_type}, HTTP {status_code})")
                                collected += 1
                        else:
                            print(f"    [ERROR] Could not build URL for {stat_group_name}_{stat_type}")
                
                # Handle endpoints with person_id - use a single sample person ID
                elif "{person_id}" in endpoint["path"]:
                    person_id = SAMPLE_PERSON_IDS[0]
                    # Replace person_id, then resolve remaining path params (e.g., game_pk)
                    test_endpoint = endpoint.copy()
                    test_endpoint["path"] = endpoint["path"].replace("{person_id}", str(person_id))
                    test_url = self.build_test_url(test_endpoint)
                    if not test_url:
                        response_data = {
                            "endpoint": endpoint["path"],
                            "method": endpoint["method"],
                            "error": "Unresolved path parameters",
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        query_params = self.build_query_params(test_endpoint)
                        response_data = await self.collect_response(test_endpoint, test_url, query_params)

                    if response_data:
                        router_responses.append(response_data)
                        status_code = response_data.get("status_code", 0)
                        status = "[OK]" if (200 <= status_code < 300) else "[FAIL]"
                        print(f"  {status} [{idx}/{len(endpoints)}] {endpoint['method']} {endpoint['path']} (person_id={person_id}, HTTP {status_code})")
                        collected += 1
                else:
                    test_url = self.build_test_url(endpoint)
                    if not test_url:
                        response_data = {
                            "endpoint": endpoint["path"],
                            "method": endpoint["method"],
                            "error": "Unresolved path parameters",
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        response_data = await self.collect_response(endpoint, test_url)

                    if response_data:
                        router_responses.append(response_data)
                        status_code = response_data.get("status_code", 0)
                        status = "[OK]" if (200 <= status_code < 300) else "[FAIL]"
                        print(f"  {status} [{idx}/{len(endpoints)}] {endpoint['method']} {endpoint['path']} (HTTP {status_code})")
                        collected += 1

            self.responses[router_name] = router_responses

        print(f"\n[DONE] Collected {collected}/{total_endpoints} responses")
        return self.responses

    def save_responses(self):
        """Save responses to organized directory structure.
        
        Structure by resource type (3rd path element):
        - response-examples/awards/
          - GET_awards_award_id_recipients.json (each 200 response)
          - error.json (all non-200 responses)
        - response-examples/attendance/
          - GET_attendance.json
          - error.json
        """
        print("\n[SAVE] Saving responses...")
        (RESPONSE_EXAMPLES_DIR).mkdir(parents=True, exist_ok=True)

        # Group all responses by resource type (3rd path element)
        resources_dict = defaultdict(list)
        
        for router_name, responses in self.responses.items():
            if not responses:
                continue
                
            for resp_data in responses:
                endpoint = resp_data["endpoint"]
                
                # Extract resource type (3rd element from path)
                # /api/v1/awards/... → "awards"
                path_parts = endpoint.split("/")
                resource_type = path_parts[3] if len(path_parts) > 3 else "unknown"
                
                resources_dict[resource_type].append(resp_data)

        # Process each resource type
        for resource_type, resource_responses in resources_dict.items():
            resource_dir = RESPONSE_EXAMPLES_DIR / resource_type
            resource_dir.mkdir(parents=True, exist_ok=True)

            # Clean existing files
            print(f"  [CLEAN] Removing old files from {resource_type}/")
            for old_file in resource_dir.glob("*.json"):
                old_file.unlink()

            # Group by endpoint within each resource type
            endpoints_dict = defaultdict(list)
            for resp_data in resource_responses:
                endpoint = resp_data["endpoint"]
                method = resp_data["method"]
                endpoint_key = f"{method}_{endpoint}".lower()
                endpoints_dict[endpoint_key].append(resp_data)

            # Process each endpoint
            for endpoint_key, endpoint_responses in endpoints_dict.items():
                # Build filename without path separators
                filename_base = (
                    endpoint_key.replace("/api/v1/", "")
                    .replace("/api/v1.1/", "")
                    .replace("/", "_")
                    .replace("{", "")
                    .replace("}", "")
                )
                
                # Separate successful (200) from errors (non-200)
                successful = []
                errors = []

                for resp_data in endpoint_responses:
                    status_code = resp_data.get("status_code", 0)
                    if isinstance(status_code, int) and 200 <= status_code < 300:
                        successful.append(resp_data)
                    else:
                        errors.append(resp_data)

                # Debug: Show what we have
                if endpoint_responses:
                    print(f"    [DEBUG] {filename_base}: {len(endpoint_responses)} total, {len(successful)} successful, {len(errors)} errors")
                    for resp in endpoint_responses:
                        variation = resp.get("variation", "N/A")
                        status = resp.get("status_code", "N/A")
                        print(f"      - variation={variation}, status={status}")

                # Save each successful response as its own file
                for idx, resp_data in enumerate(successful, 1):
                    variation = resp_data.get("variation", "")
                    
                    # Always include variation in filename if present
                    if variation:
                        filename = f"{filename_base}_{variation}.json"
                    else:
                        # Fallback: use index if no variation
                        filename = f"{filename_base}_{idx}.json" if len(successful) > 1 else f"{filename_base}.json"
                    
                    response_file = resource_dir / filename
                    with open(response_file, "w") as f:
                        json.dump(resp_data, f, indent=2)
                    print(f"    [OK] {resource_type}/{filename}")

                # Save all errors to single error.json
                if errors:
                    error_file = resource_dir / "error.json"
                    error_data = {
                        "endpoint": endpoint_responses[0]["endpoint"],
                        "method": endpoint_responses[0]["method"],
                        "errors": [
                            {
                                "status_code": e.get("status_code"),
                                "error": e.get("error", "No error message"),
                                "timestamp": e.get("timestamp"),
                            }
                            for e in errors
                        ]
                    }
                    with open(error_file, "w") as f:
                        json.dump(error_data, f, indent=2)
                    print(f"    [ERR] {resource_type}/error.json ({len(errors)} errors)")

        print(f"\n[OK] All responses saved to {RESPONSE_EXAMPLES_DIR}")

    def print_summary(self):
        """Print collection summary."""
        print("\n" + "=" * 60)
        print("RESPONSE COLLECTION SUMMARY")
        print("=" * 60)

        total_responses = sum(len(resps) for resps in self.responses.values())
        successful = sum(
            1 for resps in self.responses.values() 
            for r in resps if r.get("status_code", 500) < 300
        )
        failed = total_responses - successful

        print(f"\nTotal Responses Collected: {total_responses}")
        print(f"  ✓ Successful (200-299): {successful}")
        print(f"  ✗ Failed (non-200): {failed}")
        print(f"\nSaved to: {RESPONSE_EXAMPLES_DIR}")
        print("\n" + "=" * 60)


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Collect API responses and generate documentation"
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Base URL for API proxy (default: {DEFAULT_BASE_URL})"
    )

    args = parser.parse_args()

    with APIResponseCollector(args.base_url) as collector:
        # Parse routers
        endpoints_by_router = collector.parse_router_files()
        print(f"[INFO] Found {len(endpoints_by_router)} routers")

        # Collect responses
        await collector.collect_all_responses(endpoints_by_router)

        # Save organized responses
        collector.save_responses()

        # Print summary
        collector.print_summary()

        print("\n[DONE] Response collection complete.")


if __name__ == "__main__":
    asyncio.run(main())
