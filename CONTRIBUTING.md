# Contributing to Nonstop Agent

Thank you for your interest in contributing to Nonstop Agent!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nonstop-agent.git
cd nonstop-agent
```

2. Install development dependencies with uv:
```bash
uv sync --all-extras
```

3. Run tests:
```bash
uv run pytest
```

4. Run linting:
```bash
uv run ruff check .
uv run mypy .
```

## Code Style

- We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Type hints are required for all public functions
- Follow PEP 8 naming conventions

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Commit Message Format

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat: add support for custom MCP servers

- Allow passing mcp_servers config to create_client
- Update documentation with examples
```

## Reporting Issues

When reporting issues, please include:

1. Python version
2. Operating system
3. Steps to reproduce
4. Expected vs actual behavior
5. Relevant log output

## Questions?

Feel free to open an issue for any questions!
