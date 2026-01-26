# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/EncryptoCLI.git
   cd EncryptoCLI
   ```
3. **Install development dependencies** using uv:
   ```bash
   uv sync
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Install with Development Dependencies

```bash
uv pip install -e ".[dev]"
```

### Running Tests

```bash
pytest encryption/aes/tests.py
pytest steganography/lsb/tests.py
```

### Code Formatting

We use `black` for code formatting:

```bash
black *.py util/ encryption/ steganography/
```

### Code Quality

Ensure your code follows PEP 8 and has proper type hints:

```bash
# Check for style issues
flake8 *.py util/ encryption/ steganography/

# Type checking
mypy *.py util/ encryption/ steganography/
```

## Pull Request Process

1. **Update tests** - Add tests for new functionality
2. **Format code** - Run `black` to ensure consistent formatting
3. **Add type hints** - Use strict type hints for all new code
4. **Update documentation** - Update relevant documentation in `/docs`
5. **Update CHANGELOG** - Document your changes
6. **Create Pull Request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to related issues
   - Test results

## Commit Messages

Follow conventional commit format:

```
type(scope): description

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(encryption): add AES-256 support`
- `fix(steganography): correct LSB capacity calculation`
- `docs(hashing): update algorithm recommendations`

## Reporting Issues

When reporting issues, include:

- **Description**: Clear explanation of the problem
- **Steps to reproduce**: How to recreate the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, EncryptoCLI version
- **Screenshots**: If applicable

## Feature Requests

When requesting features:

1. **Check existing issues** - Avoid duplicates
2. **Clear title** - Summarize the feature
3. **Use case** - Explain why this feature is needed
4. **Implementation ideas** - Suggest how it could be implemented
5. **Examples** - Provide usage examples

## Code Style Guidelines

### Python Style

- Follow PEP 8 standards
- Use 4 spaces for indentation
- Maximum line length: 88 characters (black default)
- Use f-strings for string formatting
- Add docstrings to all functions and classes

### Type Hints

All code must have strict type hints:

```python
from typing import Optional, List, Dict

def encrypt_file(self, file_path: str, password: str) -> None:
    """Encrypt a file and save as .encrypto.
    
    Args:
        file_path: Path to the file to encrypt.
        password: Password for encryption.
        
    Raises:
        FatalError: If file is too large or encryption fails.
    """
    # Implementation
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def function(param1: str, param2: int) -> Dict[str, Any]:
    """Brief description of the function.
    
    Longer description can go here, explaining the function
    in more detail if needed.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of the return value.
        
    Raises:
        ValueError: When invalid parameters are provided.
        RuntimeError: When the operation fails.
    """
    pass
```

## Testing

### Write Tests For

- New features
- Bug fixes
- Edge cases
- Error conditions

### Test Structure

```python
import pytest
from encryption.aes import AESCipher

class TestAESCipher:
    def test_encrypt_decrypt_text(self):
        """Test encrypting and decrypting text."""
        cipher = AESCipher()
        secret = "test message"
        password = "secure_password"
        
        encrypted = cipher.encrypt_text(secret, password)
        decrypted = cipher.decrypt_text(encrypted, password)
        
        assert decrypted == secret
```

## Documentation

When adding features:

1. **Update docstrings** - Clear, detailed docstrings
2. **Update user guide** - Add relevant user documentation
3. **Update API docs** - Auto-generated from docstrings
4. **Add examples** - Include usage examples
5. **Update README** - If it affects the main project

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

## Questions?

Feel free to open an issue or discussion for questions about contributing!

---

Thank you for contributing to EncryptoCLI! 🎉
