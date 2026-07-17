import json
import os
import re
from pathlib import Path
from collections import defaultdict

# Get the script directory and construct paths relative to it
SCRIPT_DIR = Path(__file__).parent
spec_file = SCRIPT_DIR / "docs" / "mlb_api_spec.json"

with open(spec_file, 'r', encoding='utf-8') as f:
    spec = json.load(f)

# Extract all GET endpoints by tag
endpoints_by_tag = defaultdict(list)

for path, methods in spec.get("paths", {}).items():
    if "get" in methods:
        get_op = methods["get"]
        tags = get_op.get("tags", ["Untagged"])
        for tag in tags:
            endpoints_by_tag[tag].append({
                "path": path,
                "operationId": get_op.get("operationId", "unknown")
            })

# Sort endpoints by tag
for tag in endpoints_by_tag:
    endpoints_by_tag[tag].sort(key=lambda x: x["path"])

print(f"Total tags in spec: {len(endpoints_by_tag)}")
print(f"Total GET endpoints: {sum(len(v) for v in endpoints_by_tag.values())}")
print()

# Now analyze router files
routers_dir = SCRIPT_DIR / "api-service" / "routers"
router_files = [f for f in os.listdir(routers_dir) if f.endswith(".py") and f != "__init__.py"]

# Map router filenames to their likely tags
router_to_tag_map = {
    "attendance.py": "Attendance",
    "awards.py": "Awards",
    "bat_tracking.py": "Bat Tracking",
    "biomechanics.py": "Biomechanics",
    "broadcast.py": "Broadcast",
    "conference.py": "Conference",
    "division.py": "Division",
    "draft.py": "Draft",
    "game_pace.py": "Game Pace",
    "games.py": "Game",
    "high_low.py": "High/Low",
    "job.py": "Job",
    "league.py": "League",
    "milestones.py": "Milestones",
    "misc.py": "Misc",
    "people.py": "Person",
    "reviews.py": "Reviews",
    "schedule.py": "Schedule",
    "season.py": "Season",
    "skeletal.py": "Skeletal",
    "sports.py": "Sports",
    "standings.py": "Standings",
    "stats.py": "Stats",
    "streaks.py": "Streaks",
    "teams.py": "Teams",
    "transactions.py": "Transactions",
    "uniforms.py": "Uniforms",
    "venues.py": "Venues",
    "weather.py": "Weather",
}

# Extract routes from router files
def extract_routes_from_router(router_file):
    """Extract API routes from a router file"""
    routes = []
    
    try:
        with open(os.path.join(routers_dir, router_file), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find @router.get patterns
        get_patterns = re.findall(r'@router\.get\(["\']([^"\']+)["\']\)', content)
        
        for route in get_patterns:
            routes.append(route)
    except Exception as e:
        print(f"Error reading {router_file}: {e}")
    
    return routes

# Store implemented routes
implemented_routes = {}
for router_file in sorted(router_files):
    routes = extract_routes_from_router(router_file)
    implemented_routes[router_file] = routes

# Create comparison report
print("=" * 100)
print("MLB API ENDPOINT VALIDATION REPORT")
print("=" * 100)
print()

validation_results = []

for router_file in sorted(router_files):
    tag_name = router_to_tag_map.get(router_file, "Unknown")
    expected_endpoints = endpoints_by_tag.get(tag_name, [])
    implemented = implemented_routes.get(router_file, [])
    
    # Normalize paths for comparison - remove /api/v1 prefix and convert to snake_case
    def normalize_path(path):
        # Remove /api/v1 prefix if present
        path = path.replace("/api/v1", "")
        # Remove path parameters by replacing {paramName} with placeholders
        path = re.sub(r'\{[^}]+\}', '{param}', path)
        return path.lower()
    
    expected_normalized = {normalize_path(e["path"]): e["path"] for e in expected_endpoints}
    implemented_normalized = {normalize_path(r) for r in implemented}
    
    # Find matches
    matched = implemented_normalized & set(expected_normalized.keys())
    missing = set(expected_normalized.keys()) - implemented_normalized
    extra = implemented_normalized - set(expected_normalized.keys())
    
    status = "✅ COMPLETE" if len(missing) == 0 and len(expected_endpoints) > 0 else "❌ MISSING"
    if len(expected_endpoints) == 0:
        status = "⚠️  NO SPEC"
    
    alignment = len(matched) / len(expected_endpoints) * 100 if expected_endpoints else 0
    
    validation_results.append({
        "router": router_file,
        "tag": tag_name,
        "expected_count": len(expected_endpoints),
        "implemented_count": len(implemented),
        "matched": len(matched),
        "missing": missing,
        "extra": extra,
        "status": status,
        "alignment": alignment,
        "expected_normalized": expected_normalized
    })

# Print detailed reports
for result in sorted(validation_results, key=lambda x: x["alignment"]):
    router = result["router"]
    tag = result["tag"]
    expected_count = result["expected_count"]
    implemented_count = result["implemented_count"]
    matched = result["matched"]
    missing = result["missing"]
    extra = result["extra"]
    status = result["status"]
    alignment = result["alignment"]
    
    print(f"\n{'='*100}")
    print(f"Router: {router}")
    print(f"Tag/Domain: {tag}")
    print(f"Expected endpoints (from spec): {expected_count}")
    print(f"Implemented endpoints: {implemented_count}")
    print(f"Matched: {matched}")
    print(f"Status: {status} ({alignment:.1f}% alignment)")
    
    if missing:
        print(f"\n⚠️  MISSING ENDPOINTS ({len(missing)}):")
        for path in sorted(missing):
            original_path = result["expected_normalized"].get(path)
            print(f"   - {original_path}")
    
    if extra and expected_count > 0:
        print(f"\n➕ EXTRA ENDPOINTS ({len(extra)}):")
        for normalized_path in sorted(extra):
            print(f"   - (normalized: {normalized_path})")

# Summary statistics
print(f"\n\n{'='*100}")
print("SUMMARY")
print(f"{'='*100}")
print(f"Total routers validated: {len(validation_results)}")
print(f"Routers with 100% alignment: {sum(1 for r in validation_results if r['alignment'] == 100 and r['expected_count'] > 0)}")
print(f"Routers with gaps: {sum(1 for r in validation_results if r['alignment'] < 100 and r['expected_count'] > 0)}")
print(f"Routers with no spec: {sum(1 for r in validation_results if r['expected_count'] == 0)}")

total_expected = sum(r["expected_count"] for r in validation_results)
total_implemented = sum(r["implemented_count"] for r in validation_results)
total_matched = sum(r["matched"] for r in validation_results)

overall_alignment = total_matched / total_expected * 100 if total_expected > 0 else 0

print(f"\nOverall statistics:")
print(f"  Total endpoints in spec: {total_expected}")
print(f"  Total endpoints implemented: {total_implemented}")
print(f"  Total matched: {total_matched}")
print(f"  Overall alignment: {overall_alignment:.1f}%")

# List routers with gaps
print(f"\n{'='*100}")
print("ROUTERS WITH GAPS (Sorted by alignment)")
print(f"{'='*100}")
gap_routers = [r for r in validation_results if r["alignment"] < 100 and r["expected_count"] > 0]
for result in sorted(gap_routers, key=lambda x: x["alignment"]):
    router = result["router"]
    tag = result["tag"]
    alignment = result["alignment"]
    matched = result["matched"]
    expected = result["expected_count"]
    missing_count = len(result["missing"])
    
    print(f"\n{router:25s} | {tag:20s} | {alignment:6.1f}% | {matched}/{expected} | {missing_count} missing")
