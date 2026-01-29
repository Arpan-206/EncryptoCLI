# EncryptoCLI — Comprehensive Function Breakdown

This document explains every major function in EncryptoCLI and its role in the larger system. The project is organized in layers: interfaces, services, domain modules, and utilities. Each function is documented with its purpose, inputs, outputs, and how it fits into the overall data flow.

---

## 1. Entry Point Layer

### `main.py::main()`
**Purpose**: Routes between CLI and TUI based on command-line arguments.

**Parameters**:
- None (reads from `sys.argv`)

**Return**: None

**Logic**:
- If arguments are provided (`sys.argv > 1`), launch CLI via `cli_app()`
- Otherwise, instantiate `TUIHandler()` and call `run()`

**Role in System**: This is the gateway function. It decides which interface (CLI or TUI) the user sees based on how they invoke the program.

---

## 2. Interfaces Layer

### Interface Functions
The interfaces layer handles all user input/output. It parses arguments, validates them, calls services, and displays results.

---

#### CLI Handler (`cli_handler.py`)

**`app`** (Typer app instance)
- The Typer application that routes CLI commands
- Defines subcommands: `hash`, `encrypt`, `decrypt`, `pgp`
- All commands are invoked with flags (e.g., `--text`, `--password`)

---

##### Hash Command: `hash()`
**Purpose**: Hash text or files using various algorithms (SHA256, BLAKE3, etc.)

**Parameters**:
- `text`: Optional text to hash (via `--text` or `-t`)
- `file`: Optional file path to hash (via `--file` or `-f`)
- `algorithm`: Hashing algorithm name (default: SHA256)

**Return**: None (prints result to terminal)

**Logic**:
1. Validate that exactly one of `text` or `file` is provided
2. Check file exists (for file path)
3. Call `hashing_service.hash_text()` or `hashing_service.hash_file()`
4. Print result in green
5. Catch errors and delegate to `handle_error()`

**Role in System**: User-facing CLI command for hashing. Acts as a wrapper around the service.

---

##### Encrypt Command: `encrypt()`
**Purpose**: Encrypt text or files using AES or PGP, optionally into an image.

**Parameters**:
- `text`: Optional text to encrypt
- `file`: Optional file to encrypt
- `password`: Password for AES
- `recipient_email`: PGP recipient email
- `recipient_key`: PGP recipient public key (string)
- `recipient_key_file`: PGP recipient public key (file)
- `image`: Optional image for steganography
- `output_dir`: Output directory for encrypted image
- `steganography`: Stego method (lsb or dct)
- `method`: Encryption method (aes or pgp)

**Return**: None (prints result)

**Logic**:
1. Validate input (text XOR file, not both)
2. Validate encryption method parameters:
   - AES requires password
   - PGP requires one of: email, key, or key_file
3. Call appropriate service method (`encrypt_text()`, `encrypt_file()`, or `encrypt_text_to_image()`)
4. Print result
5. Handle errors

**Role in System**: CLI encryption command. Bridges user input to encryption service layer. Handles both simple and complex workflows (with steganography).

---

##### Decrypt Command: `decrypt()`
**Purpose**: Decrypt text, files, or images using AES or PGP.

**Parameters**:
- `text`: Encrypted text
- `file`: Encrypted file path
- `image`: Image with embedded encrypted text
- `password`: Password/passphrase
- `steganography`: Stego method (lsb or dct)
- `method`: Decryption method (aes or pgp)
- `output_dir`: Output directory for decrypted file

**Return**: None (prints result)

**Logic**:
1. Validate exactly one of text/file/image is provided
2. Call appropriate service method
3. Print decrypted result
4. Handle errors

**Role in System**: CLI decryption command. Mirrors the encrypt command but for decryption. Supports all three input types (text, file, image).

---

##### PGP Gen Key Command: `pgp_gen_key()`
**Purpose**: Generate a new PGP key pair (RSA 2048-bit).

**Parameters**:
- `name`: Full name for the key
- `email`: Email address for the key
- `passphrase`: Passphrase to protect the key

**Return**: None (prints fingerprint)

**Logic**:
1. Instantiate `PGPCipher()`
2. Call `generate_key_pair()`
3. Print success message and fingerprint
4. Handle errors

**Role in System**: CLI key generation for PGP. Sets up user's public/private key pair in GPG keyring.

---

##### PGP Export Key Command: `pgp_export_key()`
**Purpose**: Export a public key from the keyring to a file.

**Parameters**:
- `email`: Email of key to export
- `output`: Output file path for the public key

**Return**: None

**Logic**:
1. Instantiate `PGPCipher()`
2. Export public key by email
3. Write to file
4. Print success message

**Role in System**: CLI utility for sharing public keys. Enables other users to encrypt for you.

---

#### TUI Handler (`tui_handler.py`)

**`TUIHandler` class**

This class manages all TUI interactions. It prompts users with menus and delegates to services.

---

##### `__init__()`
**Purpose**: Initialize TUI handler with service instances.

**Parameters**: None

**Return**: None

**Logic**:
- Instantiate `EncryptionService()`, `DecryptionService()`, `HashingService()`
- Store as instance variables for reuse

**Role in System**: Constructor. Ensures services are available for all TUI methods.

---

##### `display_banner()`
**Purpose**: Render the welcome banner with application title and description.

**Parameters**: None

**Return**: None

**Logic**:
- Use Figlet library to generate ASCII art banner
- Display with colored output (green title, yellow credit, cyan description)

**Role in System**: UI cosmetic. Provides a friendly introduction when the TUI starts.

---

##### `get_operation()`
**Purpose**: Prompt user to select a top-level operation.

**Parameters**: None

**Return**: str (operation name: "Hash", "Encrypt", "Decrypt", "PGP", "Exit")

**Logic**:
- Use InquirerPy's `select()` to present a menu
- Return the user's choice

**Role in System**: Main dispatcher. Routes the user to the appropriate sub-operation.

---

##### `run()`
**Purpose**: Main TUI loop. Display banner, prompt for operation, delegate to handlers.

**Parameters**: None

**Return**: None

**Logic**:
1. Call `display_banner()`
2. Call `get_operation()` to get user's choice
3. Dispatch to appropriate handler (`_handle_hash()`, `_handle_encrypt()`, etc.)
4. Catch exceptions and delegate to `handle_error()`

**Role in System**: Main entry point for TUI. Orchestrates the entire TUI experience.

---

##### `_handle_hash()`
**Purpose**: TUI workflow for hashing.

**Parameters**: None

**Return**: None

**Logic**:
1. Prompt for algorithm (select from available algorithms)
2. Prompt for type (Text or File)
3. If file, prompt for file path and hash it
4. If text, prompt for text and hash it
5. Display result in green
6. Handle errors

**Role in System**: TUI handler for hashing. Provides guided prompts instead of CLI flags.

---

##### `_handle_encrypt()`
**Purpose**: TUI workflow for encryption. Routes to text or file encryption.

**Parameters**: None

**Return**: None

**Logic**:
1. Prompt for type (Text or File)
2. Delegate to `_encrypt_text_tui()` or `_encrypt_file_tui()`
3. Handle errors

**Role in System**: TUI dispatcher for encryption. Branches to more specific handlers.

---

##### `_encrypt_text_tui()`
**Purpose**: TUI workflow for encrypting text.

**Parameters**: None

**Return**: None

**Logic**:
1. Prompt for encryption method (AES or PGP)
2. If AES:
   - Prompt for password
   - Optionally prompt for image (for steganography)
   - Call `encryption_service.encrypt_text()` or `encrypt_text_to_image()`
3. If PGP:
   - Prompt for recipient email or key
   - Call `encryption_service.encrypt_text()`
4. Display result
5. Handle errors

**Role in System**: TUI handler for text encryption. Provides guided flow with conditional prompts.

---

##### `_encrypt_file_tui()`
**Purpose**: TUI workflow for encrypting files.

**Parameters**: None

**Return**: None

**Logic**:
1. Prompt for encryption method (AES or PGP)
2. Prompt for file path
3. Call appropriate service method (`encrypt_file()`)
4. Display success message
5. Handle errors

**Role in System**: TUI handler for file encryption. Simpler than text since files don't support steganography directly.

---

##### `_handle_decrypt()`
**Purpose**: TUI workflow for decryption. Routes to text, file, or image decryption.

**Parameters**: None

**Return**: None

**Logic**:
1. Prompt for type (Text, File, or Image)
2. Delegate to appropriate method (`_decrypt_text_tui()`, etc.)
3. Handle errors

**Role in System**: TUI dispatcher for decryption. Routes to specific handlers based on input type.

---

##### `_decrypt_text_tui()`, `_decrypt_file_tui()`, `_decrypt_image_tui()`
**Purpose**: TUI workflows for specific decryption scenarios.

**Parameters**: None

**Return**: None

**Logic**:
- Prompt for required parameters (password, method, etc.)
- Call appropriate service method
- Display result
- Handle errors

**Role in System**: TUI handlers for decryption variants. Each tailored to a specific input type.

---

##### `_handle_pgp_keys()`
**Purpose**: TUI workflow for PGP key management.

**Parameters**: None

**Return**: None

**Logic**:
1. Prompt for operation (Generate, Export, List, etc.)
2. Delegate to specific method
3. Handle errors

**Role in System**: TUI dispatcher for PGP operations. Centralizes key management UX.

---

### Error Handler (`error_handler.py`)

#### `handle_error()`
**Purpose**: Format and display errors with appropriate colors.

**Parameters**:
- `e`: Exception (FatalError, MildError, or generic Exception)

**Return**: None

**Logic**:
- If `FatalError`: print in red (critical error)
- If `MildError`: print in yellow (warning)
- Otherwise: print in default color

**Role in System**: Centralized error display. Ensures consistent, color-coded feedback to users.

---

## 3. Services Layer

Services act as orchestrators. They validate inputs, select algorithms, call domain modules, and return results. Services are **UI-agnostic**—both CLI and TUI use the same service methods.

---

### Encryption Service (`encryption_service.py`)

#### `__init__()`
**Purpose**: Initialize encryption service with cipher instances.

**Parameters**: None

**Return**: None

**Logic**:
- Instantiate `AESCipher()` immediately
- Lazy-initialize `_pgp_cipher` (only when needed, since it requires GPG)

**Role in System**: Constructor. Prepares ciphers for use. Lazy loading avoids GPG dependency if not needed.

---

#### `_get_pgp_cipher()`
**Purpose**: Get or create PGP cipher instance lazily.

**Parameters**: None

**Return**: PGPCipher instance

**Logic**:
- If `_pgp_cipher` is None, try to import and instantiate `PGPCipher()`
- If import fails (GPG not installed), raise a helpful error message
- Cache the instance for reuse

**Role in System**: Lazy loader for PGP. Avoids importing GPG (and requiring it) until actually used.

---

#### `encrypt_text()`
**Purpose**: Encrypt text using AES or PGP.

**Parameters**:
- `secret`: Text to encrypt
- `password`: Password for AES
- `method`: "aes" or "pgp" (default: "aes")
- `recipient_email`, `recipient_key`, `recipient_key_file`: PGP options

**Return**: str (encrypted text)

**Logic**:
- If method is "pgp", call `self._get_pgp_cipher().encrypt_text()`
- Otherwise, call `self.aes_cipher.encrypt_text()`

**Role in System**: High-level encryption orchestrator. Routes to the right cipher based on method.

---

#### `encrypt_file()`
**Purpose**: Encrypt a file using AES or PGP.

**Parameters**:
- `file_path`: Path to file
- `password`: Password for AES
- `method`: "aes" or "pgp"
- PGP recipient options

**Return**: str (success message)

**Logic**:
- Similar to `encrypt_text()` but delegates to file encryption methods
- Returns success message

**Role in System**: File encryption orchestrator.

---

#### `encrypt_text_to_image()`
**Purpose**: Encrypt text and embed it into an image using steganography.

**Parameters**:
- `image_path`: Path to input image
- `secret`: Text to encrypt
- `password`: Password for AES
- `output_dir`: Output directory
- `steganography`: "lsb" or "dct"
- `method`: "aes" or "pgp"
- PGP recipient options

**Return**: str (success message)

**Logic**:
1. Encrypt the text using `encrypt_text()` (returns ciphertext)
2. Get steganography handler via `get_steganography_handler()`
3. Call stego handler's `encrypt_text()` to embed ciphertext into image
4. Return success message

**Role in System**: High-level orchestrator for crypto + steganography workflow. Chains encryption and hiding.

---

#### `decrypt_text_from_image()`
**Purpose**: Extract and decrypt text from an image.

**Parameters**:
- `image_path`: Path to stego image
- `password`: Password
- `steganography`: Stego method
- `method`: Decryption method

**Return**: str (decrypted text)

**Logic**:
1. Get stego handler and extract encrypted text via `decrypt_image()`
2. Decrypt the extracted text using `decrypt_text()`
3. Return plaintext

**Role in System**: High-level orchestrator for extraction + decryption workflow. Reverses the encrypt-to-image process.

---

### Decryption Service (`decryption_service.py`)

Similar structure to `EncryptionService`.

#### `decrypt_text()`
**Purpose**: Decrypt text using AES or PGP.

**Parameters**:
- `data`: Encrypted text
- `password`: Password/passphrase
- `method`: "aes" or "pgp"

**Return**: str (plaintext)

**Logic**:
- Route to correct cipher based on method
- Return decrypted result

**Role in System**: High-level decryption orchestrator.

---

#### `decrypt_file()`
**Purpose**: Decrypt a file.

**Parameters**:
- `file_path`: Encrypted file
- `password`: Password
- `method`: Decryption method
- `output_dir`: Output directory (for PGP)

**Return**: str (success message)

**Logic**:
- Route to correct cipher
- Return success message

**Role in System**: File decryption orchestrator.

---

#### `decrypt_image()`
**Purpose**: Decrypt text hidden in an image.

**Parameters**:
- `image_path`: Stego image
- `password`: Password
- `steganography`: Stego method
- `method`: Decryption method

**Return**: str (plaintext)

**Logic**:
1. Get stego handler and extract encrypted text
2. Decrypt using correct cipher
3. Return plaintext

**Role in System**: Image extraction + decryption orchestrator.

---

### Hashing Service (`hashing_service.py`)

#### `ALGORITHMS` (class variable)
**Purpose**: Dictionary of available hashing algorithms mapped to hashlib functions.

**Value**:
```
{
  "MD5": hashlib.md5,
  "SHA1": hashlib.sha1,
  "SHA256": hashlib.sha256,
  "SHA512": hashlib.sha512,
  "BLAKE2B": hashlib.blake2b,
  "BLAKE3": blake3,
  ... (13 total)
}
```

**Role in System**: Algorithm registry. Enables dynamic selection at runtime.

---

#### `hash_text()`
**Purpose**: Hash text using a specified algorithm.

**Parameters**:
- `text`: Text to hash
- `algorithm`: Algorithm name (key in `ALGORITHMS` dict)

**Return**: str (hex digest)

**Logic**:
1. Validate algorithm is supported
2. Get hash function from `ALGORITHMS`
3. Update hash with encoded text
4. Return hex digest

**Role in System**: Text hashing orchestrator.

---

#### `hash_file()`
**Purpose**: Hash a file using a specified algorithm.

**Parameters**:
- `file_path`: Path to file
- `algorithm`: Algorithm name

**Return**: str (hex digest)

**Logic**:
1. Validate algorithm
2. Check file exists
3. Open file and read in chunks (4KB at a time)
4. Update hash with each chunk
5. Return hex digest

**Role in System**: File hashing orchestrator. Chunks are read to handle large files efficiently.

---

#### `get_available_algorithms()`
**Purpose**: Return list of available hashing algorithms.

**Parameters**: None

**Return**: list[str] (sorted algorithm names)

**Logic**:
- Return sorted list of `ALGORITHMS.keys()`

**Role in System**: Utility for TUI and help text. Dynamically lists supported algorithms.

---

## 4. Domain Modules (Cryptography and Steganography)

These modules implement the actual algorithms.

---

### AES Cipher (`encryption/aes/cipher.py`)

#### `AESCipher` class

#### `encrypt_text()`
**Purpose**: Encrypt text using Fernet (AES-128 in CBC mode).

**Parameters**:
- `secret`: Plaintext
- `password`: Password

**Return**: str (ciphertext)

**Logic**:
1. Validate password is not empty
2. Generate Fernet key from password via `key_gen()`
3. Create Fernet cipher
4. Encrypt secret and return as string

**Role in System**: Low-level AES encryption. Used by `EncryptionService`.

---

#### `decrypt_text()`
**Purpose**: Decrypt Fernet-encrypted text.

**Parameters**:
- `encrypted_secret`: Ciphertext
- `password`: Password

**Return**: str (plaintext)

**Logic**:
1. Validate password
2. Generate same key from password
3. Decrypt and decode
4. Catch decryption errors and raise FatalError

**Role in System**: Low-level AES decryption.

---

#### `encrypt_file()`
**Purpose**: Encrypt a file to `.encrypto` extension.

**Parameters**:
- `file_path`: File to encrypt
- `password`: Password

**Return**: str (success message)

**Logic**:
1. Validate password
2. Generate key
3. Read file via `get_file()` (validates size < 1GB)
4. Encrypt binary content
5. Write to `{filename}.encrypto`
6. Return success message

**Role in System**: File-level encryption. Produces `.encrypto` files.

---

#### `decrypt_file()`
**Purpose**: Decrypt a `.encrypto` file.

**Parameters**:
- `file_path`: Encrypted file
- `password`: Password

**Return**: None

**Logic**:
1. Validate password
2. Generate key
3. Read encrypted file
4. Decrypt
5. Write to original filename (without `.encrypto` extension)

**Role in System**: File-level decryption. Restores original filename.

---

#### `_cipher()`
**Purpose**: Create a Fernet cipher from a password.

**Parameters**:
- `password`: Password

**Return**: Fernet instance

**Logic**:
1. Derive key using `key_gen()`
2. Create Fernet cipher with key
3. Handle errors

**Role in System**: Internal utility. Abstracts key derivation and cipher creation.

---

### PGP Cipher (`encryption/pgp/cipher.py`)

#### `PGPCipher` class

#### `__init__()`
**Purpose**: Initialize PGP cipher with GPG instance.

**Parameters**:
- `gpg_home`: Optional custom GPG home directory (defaults to ~/.gnupg)

**Return**: None

**Logic**:
1. Expand home directory path or use system default
2. Create directory with secure permissions (0o700)
3. Instantiate `gnupg.GPG()` with home directory

**Role in System**: Constructor. Sets up GPG instance for all PGP operations.

---

#### `generate_key_pair()`
**Purpose**: Generate a PGP key pair (RSA 2048-bit).

**Parameters**:
- `name`: Full name for key
- `email`: Email for key
- `passphrase`: Passphrase to protect key

**Return**: str (key fingerprint)

**Logic**:
1. Validate all parameters provided
2. Build key input configuration with `gen_key_input()`
3. Generate key with `gen_key()`
4. Return fingerprint

**Role in System**: Key generation utility. Called via CLI/TUI.

---

#### `encrypt_text()`
**Purpose**: Encrypt text using recipient's public key.

**Parameters**:
- `secret`: Text to encrypt
- `recipient_email`: Recipient's email (from keyring)
- `recipient_key`: Public key as string
- `recipient_key_file`: Path to public key file
- `passphrase`: Optional passphrase for signing

**Return**: str (ciphertext)

**Logic**:
1. Validate secret is not empty
2. Determine recipient ID (priority: file > string > email)
3. If file or string, import key into keyring
4. Encrypt secret to recipient
5. Check encryption status
6. Return encrypted data

**Role in System**: PGP text encryption. Supports multiple ways to specify recipient.

---

#### `decrypt_text()`
**Purpose**: Decrypt PGP-encrypted text.

**Parameters**:
- `encrypted_secret`: Ciphertext
- `passphrase`: Passphrase for private key

**Return**: str (plaintext)

**Logic**:
1. Validate passphrase provided
2. Decrypt using passphrase
3. Check decryption status
4. Return plaintext

**Role in System**: PGP text decryption.

---

#### `encrypt_file()`
**Purpose**: Encrypt a file using public key.

**Parameters**:
- `file_path`: File to encrypt
- Recipient options (same as text)

**Return**: str (success message)

**Logic**:
1. Validate recipient specified
2. Determine recipient ID (import if needed)
3. Read file
4. Encrypt file content
5. Write to `.pgp` file
6. Return success message

**Role in System**: PGP file encryption.

---

#### `decrypt_file()`
**Purpose**: Decrypt a PGP-encrypted file.

**Parameters**:
- `file_path`: Encrypted file
- `passphrase`: Passphrase
- `output_dir`: Output directory

**Return**: str (success message)

**Logic**:
1. Validate passphrase
2. Read encrypted file
3. Decrypt
4. Write to output directory (original filename)
5. Return success message

**Role in System**: PGP file decryption.

---

### LSB Steganography (`steganography/lsb/handler.py`)

#### `LSBSteganography` class

Embeds data into the **least significant bits** of image pixels. Works with PNG (lossless).

#### `encrypt_text()`
**Purpose**: Hide text in an image's LSBs.

**Parameters**:
- `input_image_path`: Input image (PNG recommended)
- `secret`: Text to hide
- `output_dir`: Output directory

**Return**: None

**Logic**:
1. Open image and convert to RGB
2. Flatten pixel array
3. Encode secret:
   - First 32 bits: length of secret (as 4-byte big-endian integer)
   - Next N bits: secret bytes
   - Final 8 bits: end marker (11111111)
4. For each bit in encoded secret:
   - Clear LSB of pixel (`pixel & 0xFE`)
   - Set LSB to encoded bit (`| bit`)
5. Reshape array and save as PNG

**Role in System**: LSB embedding algorithm. Simple, fast, but visible to statistical analysis.

---

#### `decrypt_image()`
**Purpose**: Extract hidden text from image.

**Parameters**:
- `input_image_path`: Image with hidden text

**Return**: str (hidden text)

**Logic**:
1. Open image and flatten to array
2. Extract LSBs as bit string
3. Read first 32 bits as length
4. Read next (length * 8) bits as secret bytes
5. Decode and return text
6. Catch errors and return empty string

**Role in System**: LSB extraction algorithm. Reverses the embedding process.

---

### DCT Steganography (`steganography/dct/handler.py`)

#### `DCTSteganography` class

Conceptually similar to LSB (current implementation is simplified). Intended for frequency-domain embedding but simplified for compatibility.

#### `encrypt_text()`
**Purpose**: Hide text in image (currently uses LSB, not full DCT).

**Parameters**: Same as LSB

**Return**: None

**Logic**: Same as LSB (simplified implementation)

**Role in System**: Placeholder for DCT algorithm. Could be extended with true DCT in the future.

---

#### `decrypt_image()`
**Purpose**: Extract text from image (LSB-based).

**Parameters**: Same as LSB

**Return**: str (hidden text)

**Logic**: Same as LSB

**Role in System**: Placeholder extraction. Mirrors encryption.

---

## 5. Utilities Layer

### Key Generation (`util/key_gen.py`)

#### `key_gen()`
**Purpose**: Derive a cryptographic key from a password using scrypt.

**Parameters**:
- `passW`: Password (string)

**Return**: bytes (base64-encoded key)

**Logic**:
1. Use password as seed for random number generator
2. Generate salt from random number
3. Use scrypt with password and salt:
   - n=16384 (CPU/memory cost)
   - r=8 (block size)
   - p=1 (parallelization)
   - dklen=32 (32-byte output)
4. Base64-encode result
5. Return key

**Role in System**: Key derivation function. Used by AES cipher to convert passwords to Fernet keys. Ensures same password → same key (for decryption).

---

### File Handling (`util/file_handling.py`)

#### `get_file()`
**Purpose**: Open a file in binary mode with size validation.

**Parameters**:
- `filename`: Path to file

**Return**: BinaryIO (file object)

**Logic**:
1. Check file size using `os.path.getsize()`
2. Validate size < 1 GB (1073741824 bytes)
3. Open file in binary read mode (`"rb"`)
4. Return file object
5. Catch errors and raise FatalError

**Role in System**: Safe file opener. Prevents accidentally processing huge files and provides clear error messages.

---

### Exceptions (`util/exceptions.py`)

#### `FatalError` (class)
**Purpose**: Exception for critical errors that should terminate execution.

**Attributes**:
- `message`: Error description

**Role in System**: Signals unrecoverable errors. Caught by `handle_error()` and displayed in red.

#### `MildError` (class)
**Purpose**: Exception for non-fatal warnings.

**Attributes**:
- `message`: Error description

**Role in System**: Signals warnings or issues that don't stop execution. Displayed in yellow.

---

## 6. Steganography Factory

### `steganography/__init__.py`

#### `get_steganography_handler()`
**Purpose**: Factory function to get the right steganography handler by name.

**Parameters**:
- `name`: "lsb" or "dct"

**Return**: LSBSteganography or DCTSteganography instance

**Logic**:
- If "lsb": return `LSBSteganography()`
- If "dct": return `DCTSteganography()`
- Otherwise: raise error

**Role in System**: Factory pattern. Abstracts stego handler selection from services.

---

## 7. Data Flow Examples

### Example 1: CLI AES Encryption
```
user runs: encryptocli encrypt --text "hello" --password "secret"
  ↓
CLI handler `encrypt()` validates inputs
  ↓
Calls `EncryptionService.encrypt_text("hello", "secret")`
  ↓
Service calls `AESCipher.encrypt_text()`
  ↓
Cipher derives key via `key_gen()`, creates Fernet, encrypts
  ↓
Returns ciphertext to service
  ↓
Service returns to CLI
  ↓
CLI prints result in green
```

### Example 2: TUI Text → Image (LSB Steganography)
```
user selects: Encrypt → Text → AES + Image
  ↓
TUI `_encrypt_text_tui()` prompts for text, password, image, output dir
  ↓
Calls `EncryptionService.encrypt_text_to_image(...)`
  ↓
Service encrypts text via `AESCipher` → ciphertext
  ↓
Service gets LSB handler via `get_steganography_handler("lsb")`
  ↓
Handler's `encrypt_text()` embeds ciphertext into image LSBs
  ↓
Handler saves stego image as `encrypto.png`
  ↓
Service returns success message
  ↓
TUI displays result
```

### Example 3: CLI Hash
```
user runs: encryptocli hash --file "data.bin" --algorithm "SHA256"
  ↓
CLI handler `hash()` validates file exists
  ↓
Calls `HashingService.hash_file("data.bin", "SHA256")`
  ↓
Service validates algorithm is in `ALGORITHMS` dict
  ↓
Service opens file, reads in 4KB chunks, updates SHA256 hash
  ↓
Service returns hex digest
  ↓
CLI prints result in green
```

---

## 8. Key Design Patterns

### Layered Architecture
- **Interfaces** (CLI/TUI) handle user input/output
- **Services** validate and orchestrate
- **Domain modules** implement algorithms
- **Utilities** provide helpers

This separation keeps each layer independent and testable.

### Lazy Initialization
- `PGPCipher` is created only when needed (requires GPG)
- Avoids unnecessary dependencies

### Factory Pattern
- `get_steganography_handler()` abstracts handler selection
- Enables easy addition of new stego methods

### Error Mapping
- `FatalError` and `MildError` provide semantic error levels
- `handle_error()` displays them appropriately

### Service Abstraction
- Both CLI and TUI use the same service methods
- Ensures consistent behavior regardless of interface

---

## 9. Testing Implications

Each layer can be tested independently:

- **Utilities**: Test key generation and file handling in isolation
- **Domain modules**: Test encryption/decryption without UI
- **Services**: Test orchestration and error handling
- **Interfaces**: Test user flows and validation

This modular structure enables comprehensive testing without needing to mock UI elements.

---

## 10. Extension Points

To add a new feature:

1. **New algorithm**: Add to domain module, extend service routing
2. **New CLI command**: Add `@app.command()` in `cli_handler.py`
3. **New TUI flow**: Add method to `TUIHandler` class
4. **New steganography method**: Implement in new file, add to factory

The layered design makes these changes localized and low-risk.
