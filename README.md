# ospsd-team-07 Project

## Team Members
* **Somaditya Singh** (`ss20288`)
* **Saakshi Narayan** (`sn4230`)
* **Mingjian Li** (`ml8347`)
* **Joshua Leeman** (`jl17087`)
* **Riddhi Prasad** (`rrp4822`)

## Project Description
Welcome to the repository for Team 7! This project focuses on developing an interface and implementation for Trello. Our goal is to collaborate effectively to deliver a robust and scalable solution using the best software development practices.

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[your-username]/[repo-name].git
   ```

2. **Install dependencies with `uv` (recommended):**
   ```bash
   uv sync --all-extras
   ```

   Or with pip:
   ```bash
   pip install -e .
   pip install -e components/issue_tracker_client_api[dev]
   pip install -e components/trello_client_impl[dev]
   ```

## Testing

This project includes comprehensive unit tests, integration tests, and end-to-end tests.

### Quick Start
```bash
# Run all tests with coverage
pytest

# Run only unit tests (fast)
pytest -m unit

# Run integration tests
pytest -m integration

# Run e2e tests (requires Trello credentials)
pytest -m e2e
```

For detailed testing documentation, see [TESTING.md](TESTING.md).

**Coverage Requirements:**
- Minimum threshold: 85%
- Run `pytest --cov=components --cov-report=html` to generate detailed coverage reports

## Project Structure
```
ospsd-team-07/
├── components/
│   ├── issue_tracker_client_api/     # Abstract interface definitions
│   └── trello_client_impl/           # Concrete Trello implementation
├── tests/
│   ├── integration/                  # Integration tests
│   └── e2e/                          # End-to-end tests
├── docs/                             # Documentation
├── conftest.py                       # Pytest fixtures
└── pyproject.toml                    # Project configuration
```

## Development

### Code Quality
- Run `ruff` for linting and formatting
- Run `mypy` for type checking
- All code must pass 85%+ test coverage
- See `TESTING.md` for testing guidelines

### Documentation
Documentation is built with MkDocs. See `docs/` directory.

## LICENSE
[MIT LICENSE] - see the [LICENSE](LICENSE) file for details.
