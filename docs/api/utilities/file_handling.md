# File Handling

File I/O and path validation utilities.

## Functions

### read_file(file_path)

Read file contents.

**Parameters:**
- `file_path` (str): Path to file to read

**Returns:** str or bytes - File contents

**Raises:**
- `FileOperationError` - If file cannot be read

**Example:**
```python
from encryptocli.util.file_handling import read_file

content = read_file("document.txt")
print(content)
```

### write_file(file_path, content)

Write content to file.

**Parameters:**
- `file_path` (str): Path to write to
- `content` (str or bytes): Content to write

**Returns:** None

**Raises:**
- `FileOperationError` - If file cannot be written

**Example:**
```python
from encryptocli.util.file_handling import write_file

write_file("output.txt", "encrypted data")
```

### validate_path(file_path)

Validate file path exists and is readable.

**Parameters:**
- `file_path` (str): Path to validate

**Returns:** bool - True if valid

**Raises:**
- `FileOperationError` - If path is invalid

**Example:**
```python
from encryptocli.util.file_handling import validate_path

if validate_path("document.txt"):
    print("File is valid and readable")
```

### get_file_size(file_path)

Get file size in bytes.

**Parameters:**
- `file_path` (str): Path to file

**Returns:** int - File size in bytes

**Raises:**
- `FileOperationError` - If file cannot be accessed

**Example:**
```python
from encryptocli.util.file_handling import get_file_size

size = get_file_size("data.bin")
print(f"File size: {size} bytes")
```

### file_exists(file_path)

Check if file exists.

**Parameters:**
- `file_path` (str): Path to check

**Returns:** bool - True if file exists

**Example:**
```python
from encryptocli.util.file_handling import file_exists

if file_exists("backup.enc"):
    print("Backup exists")
```

### is_readable(file_path)

Check if file is readable.

**Parameters:**
- `file_path` (str): Path to check

**Returns:** bool - True if readable

**Example:**
```python
from encryptocli.util.file_handling import is_readable

if is_readable("encrypted.enc"):
    print("Can read encrypted file")
```

### is_writable(directory_path)

Check if directory is writable.

**Parameters:**
- `directory_path` (str): Directory path to check

**Returns:** bool - True if writable

**Example:**
```python
from encryptocli.util.file_handling import is_writable

if is_writable("/tmp"):
    print("Can write to /tmp")
```

## Usage Examples

### Read and Encrypt File

```python
from encryptocli.util.file_handling import read_file, write_file
from encryptocli.services import EncryptionService

# Read file
content = read_file("document.txt")

# Encrypt
service = EncryptionService()
encrypted = service.encrypt_text(content, "password")

# Write encrypted
write_file("document.enc", encrypted)
```

### Validate Before Processing

```python
from encryptocli.util.file_handling import validate_path, get_file_size
from encryptocli.util.exceptions import FileOperationError

try:
    # Validate file exists
    validate_path("large_file.bin")
    
    # Check size
    size = get_file_size("large_file.bin")
    if size > 1000000000:  # 1GB
        print("File too large")
    else:
        print("File size OK")
except FileOperationError as e:
    print(f"File error: {e}")
```

### Safe File Writing

```python
from encryptocli.util.file_handling import write_file, is_writable
from encryptocli.util.exceptions import FileOperationError
import os

output_dir = "/path/to/output"

try:
    # Check directory writable
    if not is_writable(output_dir):
        raise FileOperationError(f"{output_dir} is not writable")
    
    # Write file
    output_path = os.path.join(output_dir, "encrypted.enc")
    write_file(output_path, encrypted_data)
    print(f"Saved to {output_path}")
except FileOperationError as e:
    print(f"Cannot save file: {e}")
```

### Batch File Processing

```python
from encryptocli.util.file_handling import read_file, write_file
from encryptocli.services import EncryptionService
import os

service = EncryptionService()
input_dir = "/path/to/files"
output_dir = "/path/to/encrypted"
password = "secure_password"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Process each file
for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)
    
    try:
        # Read
        content = read_file(input_path)
        
        # Encrypt
        encrypted = service.encrypt_text(content, password)
        
        # Write
        output_path = os.path.join(output_dir, f"{filename}.enc")
        write_file(output_path, encrypted)
        print(f"Encrypted: {filename}")
    except Exception as e:
        print(f"Failed to encrypt {filename}: {e}")
```

## File Operations Best Practices

### 1. Validate Before Operations

```python
from encryptocli.util.file_handling import validate_path

try:
    validate_path("document.txt")
    # Proceed with file operations
except FileOperationError:
    print("File does not exist")
```

### 2. Check Permissions

```python
from encryptocli.util.file_handling import is_readable, is_writable

if not is_readable("input.txt"):
    print("Cannot read input file")

if not is_writable("/output/"):
    print("Cannot write to output directory")
```

### 3. Handle Large Files

```python
from encryptocli.util.file_handling import get_file_size

MAX_SIZE = 1000000  # 1MB

size = get_file_size("file.txt")
if size > MAX_SIZE:
    print(f"File too large ({size} > {MAX_SIZE})")
```

### 4. Error Handling

```python
from encryptocli.util.file_handling import read_file, write_file
from encryptocli.util.exceptions import FileOperationError

try:
    content = read_file("missing.txt")
except FileOperationError as e:
    print(f"Read error: {e}")

try:
    write_file("/readonly/file.txt", "data")
except FileOperationError as e:
    print(f"Write error: {e}")
```

### 5. Cleanup on Error

```python
import os
from encryptocli.util.file_handling import write_file

output_file = "temporary.txt"

try:
    write_file(output_file, "data")
    # Process file
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)
```

## Security Considerations

### File Permissions

- Ensure output directories are secure
- Restrict file permissions after encryption
- Use secure temporary directories

### Data Integrity

- Validate file contents after read
- Verify file write success
- Use checksums for verification

### Path Handling

- Validate user-provided paths
- Use absolute paths when possible
- Avoid path traversal vulnerabilities

## See Also

- [Exceptions](exceptions.md)
- [Key Generation](key_gen.md)
- [Services](../services.md)
