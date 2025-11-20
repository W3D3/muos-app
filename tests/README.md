# Tests

This directory contains tests for the muos-app.

## Running Tests

To run all tests:

```bash
python3 -m unittest discover tests
```

To run a specific test file:

```bash
python3 -m unittest tests.test_artwork_integration
```

To run with verbose output:

```bash
python3 -m unittest tests.test_artwork_integration -v
```

## Test Coverage

- `test_artwork_integration.py`: Integration tests for artwork downloading functionality, including:
  - Artwork extraction from ss_metadata in API responses
  - URL construction with various path formats (with/without leading slashes)
  - Handling of missing or empty ss_metadata
