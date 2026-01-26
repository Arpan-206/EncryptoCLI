# Getting Started

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Using uv (Recommended)

```bash
# Install using uv
uv pip install encryptocli

# Or clone the repository
git clone https://github.com/arpanpandey/EncryptoCLI.git
cd EncryptoCLI

# Install dependencies
uv sync
```

### Using pip

```bash
pip install encryptocli
```

## Running EncryptoCLI

EncryptoCLI supports two interfaces: **Interactive TUI** (prompts-based) and **CLI** (arguments-based).

### Interactive Mode (TUI)

Best for manual, interactive use:

**From PyPI:**
```bash
encryptocli
```

**From Source:**
```bash
cd EncryptoCLI
python -m encryptocli
```

### Command-Line Mode (CLI)

Best for scripting and automation:

**Hash text:**
```bash
encryptocli hash --text "hello world" --algorithm SHA256
```

**Encrypt text:**
```bash
encryptocli encrypt --text "secret message" --password "mypassword"
```

**Decrypt text:**
```bash
encryptocli decrypt --text "encrypted_text_here" --password "mypassword"
```

**Get help:**
```bash
encryptocli --help
encryptocli hash --help
```

## First Run

When you start EncryptoCLI in interactive mode, you'll see the welcome banner:

```
   ______                      _           _____ _      _____
  / ____/____   _____________ / /_ _____  / ____/  |    /  _/
 / __/ / __ \ / ___/ ___/ __ / __// ___/ / /    | |    / /
/ /__ / / / / (__  ) __/ ___/ /_ (__  ) / /___ | |   _/ /
\____/_/ /_/ /____/____/___/\__/____/  \____/ |____| /___/
                                     By Arpan Pandey

A tool to hash or encrypt your data easily using Fernet Encryption.
It is very easy and intuitive to use.
You can also use this on any type of file below 1GB.
```

### Menu Options (Interactive Mode)

1. **Hash** - Generate cryptographic hashes
2. **Encrypt** - Encrypt text or files
3. **Decrypt** - Decrypt encrypted data
4. **Exit** - Close the application

## System Requirements

- **Storage**: Minimum 100 MB for dependencies
- **RAM**: 512 MB minimum (1 GB recommended)
- **File Size Limit**: Maximum 1 GB per file
- **Supported Platforms**: macOS, Linux, Windows

## Troubleshooting

### Issue: "Command not found: encryptocli"

**Solution**: Make sure the package is installed:
```bash
uv pip list | grep encryptocli
```

If not installed, reinstall using:
```bash
uv pip install encryptocli
```

### Issue: "File too large" error

**Solution**: EncryptoCLI supports files up to 1 GB. Split larger files before encrypting.

### Issue: "Wrong password" during decryption

**Solution**: Ensure you're using the exact same password used during encryption. Passwords are case-sensitive.

## Next Steps

- Learn about [Hashing](hashing.md)
- Learn about [Encryption](encryption.md)
- Learn about [Decryption](decryption.md)
- Explore [Steganography](steganography.md)
