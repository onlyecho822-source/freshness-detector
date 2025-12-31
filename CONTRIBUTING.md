# Contributing to Freshness Detector

Thank you for your interest in contributing! We welcome contributions from the community.

## Ways to Contribute

### 1. Report Bugs
- Use the [Bug Report](https://github.com/onlyecho822-source/freshness-detector/issues/new?template=bug_report.yml) template
- Include reproduction steps and expected vs. actual behavior
- Provide version information

### 2. Suggest Features
- Use the [Feature Request](https://github.com/onlyecho822-source/freshness-detector/issues/new?template=feature_request.yml) template
- Explain the problem you're trying to solve
- Describe your proposed solution

### 3. Share Your Use Case
- Use the [Use Case](https://github.com/onlyecho822-source/freshness-detector/issues/new?template=use_case.yml) template
- Help us understand real-world applications
- Share metrics and results if possible

### 4. Submit Code
- Fork the repository
- Create a feature branch
- Write tests for new functionality
- Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/onlyecho822-source/freshness-detector.git
cd freshness-detector

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
black freshness_detector/
flake8 freshness_detector/
```

## Pull Request Guidelines

1. **One feature per PR** - Keep changes focused
2. **Write tests** - Maintain or improve code coverage
3. **Update documentation** - Include README updates if needed
4. **Follow code style** - Use Black for formatting
5. **Write clear commit messages** - Explain what and why

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Write docstrings for public functions
- Add type hints where appropriate

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Test with Python 3.8, 3.9, 3.10, 3.11, 3.12

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include examples in docstrings
- Update CHANGELOG.md

## Questions?

- Open a [Discussion](https://github.com/onlyecho822-source/freshness-detector/discussions)
- Check existing issues and PRs
- Review the README and documentation

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow [GitHub Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Freshness Detector better!** 🙏
