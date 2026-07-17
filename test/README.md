# MLB API Test Suite

Comprehensive test suite for the MLB API proxy service using the hybrid testing approach.

## 📁 Test Structure

```
test/
├── conftest.py              # Shared fixtures and pytest configuration
├── unit/                    # Unit tests (fast, mocked)
│   ├── routers/            # Parametrized tests for all 33 routers (190 endpoints)
│   │   ├── test_teams.py
│   │   ├── test_people.py
│   │   ├── test_games.py
│   │   └── ... (32 total files)
│   └── test_critical_flows.py  # Hand-written critical scenario tests
├── integration/             # Integration tests (end-to-end flows)
│   └── test_end_to_end.py
├── contract/                # Contract tests (API spec validation)
├── smoke/                   # Smoke tests (deployment validation)
│   └── test_deployment.py
└── fixtures/                # Test data fixtures
```

## 🎯 Test Categories

### Unit Tests (`pytest -m unit`)
- **32 parametrized router test files** covering all 190 endpoints
- **Critical flow tests** for core functionality
- Fast execution with mocked dependencies
- Tests individual components in isolation

### Integration Tests (`pytest -m integration`)
- End-to-end user workflows
- Multi-step scenarios (search → retrieve → process)
- Data consistency validation
- Concurrent request handling

### Smoke Tests (`pytest -m smoke`)
- Deployment validation tests
- Critical endpoint availability
- System health checks
- Run against live deployments

## 🚀 Quick Start

### Run All Tests
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run all tests
pytest

# Run with coverage report
pytest --cov --cov-report=html
```

### Run Specific Test Categories
```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests only
pytest -m integration

# Smoke tests (deployment validation)
pytest -m smoke --smoke

# Run tests for a specific router
pytest test/unit/routers/test_teams.py

# Run a specific test
pytest test/unit/test_critical_flows.py::TestCriticalFlows::test_teams_list_retrieval
```

### Run Tests with Different Verbosity
```bash
# Verbose output
pytest -v

# Very verbose (show individual test results)
pytest -vv

# Quiet (minimal output)
pytest -q

# Show print statements
pytest -s
```

## 📊 Test Coverage

### Coverage Goals
- **Unit Tests**: 90%+ code coverage
- **Integration Tests**: 80%+ workflow coverage
- **Smoke Tests**: 10-20 critical endpoints

### Generate Coverage Reports
```bash
# HTML report (opens in browser)
pytest --cov --cov-report=html
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
xdg-open htmlcov/index.html  # Linux

# Terminal report
pytest --cov --cov-report=term-missing

# XML report (for CI/CD)
pytest --cov --cov-report=xml
```

## 🔧 Test Configuration

### Environment Variables
Create a `.env.test` file for test-specific configuration:

```env
MLB_API_BASE_URL=https://statsapi.mlb.com
MLB_API_KEY=test_api_key
REQUIRE_KEY=false
STRIP_COPYRIGHT=true
LOG_LEVEL=INFO
ENABLE_CACHE=false
CACHE_TTL=300
REQUEST_TIMEOUT=30
```

### Pytest Configuration
Test behavior is configured in `pytest.ini`:
- Test discovery patterns
- Coverage settings
- Markers and categories
- Output formatting

## 🧪 Writing Tests

### Using Fixtures
```python
def test_example(client, mock_teams_response, respx_mock):
    """Example test using fixtures."""
    respx.get("https://statsapi.mlb.com/api/v1/teams").mock(
        return_value=Response(200, json=mock_teams_response)
    )
    
    response = client.get("/api/v1/teams")
    assert response.status_code == 200
```

### Available Fixtures
- `client`: FastAPI TestClient
- `async_client`: Async TestClient for concurrent tests
- `respx_mock`: HTTP request mocking
- `mock_teams_response`: Sample teams data
- `mock_people_response`: Sample people data
- `mock_game_response`: Sample game data
- `mock_lookup_values`: Sample lookup values
- `sample_team_ids`: List of real team IDs
- `sample_person_ids`: List of real person IDs
- `sample_game_pks`: List of real game PKs

### Test Markers
```python
@pytest.mark.unit
def test_unit_example():
    """Unit test - fast, mocked dependencies."""
    pass

@pytest.mark.integration
def test_integration_example():
    """Integration test - tests multiple components."""
    pass

@pytest.mark.smoke
def test_smoke_example():
    """Smoke test - deployment validation."""
    pass

@pytest.mark.slow
def test_slow_example():
    """Slow test - may take significant time."""
    pass
```

## 📈 Test Metrics

### Current Coverage
- **Total Endpoints**: 190
- **Parametrized Tests**: 32 router files
- **Critical Tests**: ~50 scenarios
- **Integration Tests**: ~15 workflows
- **Smoke Tests**: ~15 health checks

### Test Matrix
- 190 endpoints × 5 test cases = **950 test scenarios**
  - Endpoint exists ✓
  - Returns 200 ✓
  - Copyright stripped ✓
  - Query params forwarded ✓
  - Error handling ✓

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov respx
      
      - name: Run unit tests
        run: pytest -m unit --cov
      
      - name: Run integration tests
        run: pytest -m integration
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🐛 Debugging Tests

### Run Tests in Debug Mode
```bash
# Stop at first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Show local variables on failure
pytest -l

# Enter debugger on failure
pytest --pdb

# Trace test execution
pytest --trace
```

### Run Specific Failed Tests
```bash
# Re-run only failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff
```

## 📝 Test Data

### Static Test IDs
Use these known IDs for consistent testing:
- **Teams**: 147 (Yankees), 121 (Mets), 111 (Red Sox)
- **People**: 660271 (Aaron Judge), 545361 (Mike Trout)
- **Seasons**: 2024, 2023, 2022

### Mock Responses
Mock responses are defined in `conftest.py` and match the structure of real MLB API responses.

## 🔍 Test Maintenance

### Regenerate Router Tests
If endpoints change, regenerate parametrized tests:
```bash
python generate_unit_tests.py
```

### Update Fixtures
Edit `test/conftest.py` to add new fixtures or modify existing ones.

### Validate Spec Alignment
```bash
# Ensures all spec endpoints have tests
python validate_test_coverage.py
```

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [RESPX Documentation](https://lundberg.github.io/respx/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [MLB Stats API Documentation](docs/MLB_API_Documentation.md)

## 🤝 Contributing

### Adding New Tests
1. Identify the test category (unit/integration/smoke)
2. Use appropriate fixtures from `conftest.py`
3. Follow naming conventions: `test_*.py` and `test_*()` functions
4. Add appropriate markers: `@pytest.mark.unit`, etc.
5. Run tests to verify: `pytest path/to/test_file.py`

### Test Checklist
- [ ] Test has descriptive name
- [ ] Test has docstring explaining purpose
- [ ] Test uses appropriate fixtures
- [ ] Test has proper marker (@pytest.mark.unit, etc.)
- [ ] Test assertions are clear and specific
- [ ] Test is focused on one aspect
- [ ] Test passes consistently

## 📊 Performance

### Test Execution Times
- **Unit Tests**: ~30-60 seconds (mocked, fast)
- **Integration Tests**: ~2-5 minutes (multiple calls)
- **Smoke Tests**: ~1-2 minutes (live API calls)
- **Full Suite**: ~5-10 minutes

### Optimization Tips
- Run unit tests during development (fastest feedback)
- Run integration tests before committing
- Run smoke tests in CI/CD pipeline
- Use `pytest-xdist` for parallel execution: `pytest -n auto`

## 🎉 Test Summary

This test suite implements the **hybrid approach** combining:
1. ✅ **Automated parametrized tests** for broad coverage (190 endpoints)
2. ✅ **Hand-written critical tests** for complex scenarios
3. ✅ **Integration tests** for end-to-end workflows
4. ✅ **Smoke tests** for deployment validation

**Total Test Count**: ~300+ individual test cases covering all aspects of the MLB API proxy.
