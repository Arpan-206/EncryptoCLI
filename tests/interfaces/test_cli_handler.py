"""Tests for CLI interface using Typer's testing utilities."""

import pytest
from typer.testing import CliRunner

from encryptocli.interfaces.cli_handler import app


class TestCLIHandler:
    """Test CLI commands using CliRunner."""

    @pytest.fixture
    def runner(self):
        """Provide CliRunner instance."""
        return CliRunner()

    def test_hash_text(self, runner):
        """Test hashing text via CLI."""
        result = runner.invoke(
            app, ["hash", "--text", "hello", "--algorithm", "SHA256"]
        )
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_hash_file(self, runner, sample_file):
        """Test hashing file via CLI."""
        result = runner.invoke(
            app, ["hash", "--file", str(sample_file), "--algorithm", "MD5"]
        )
        assert result.exit_code == 0
        assert len(result.stdout) > 0

    def test_hash_missing_input(self, runner):
        """Test hash command without text or file."""
        result = runner.invoke(app, ["hash", "--algorithm", "SHA256"])
        assert result.exit_code != 0

    def test_encrypt_text_aes(self, runner):
        """Test encrypting text via CLI."""
        result = runner.invoke(
            app,
            ["encrypt", "--text", "secret", "--password", "pass123", "--method", "aes"],
        )
        assert result.exit_code == 0

    def test_encrypt_file_aes(self, runner, sample_file):
        """Test encrypting file via CLI."""
        result = runner.invoke(
            app,
            [
                "encrypt",
                "--file",
                str(sample_file),
                "--password",
                "pass123",
                "--method",
                "aes",
            ],
        )
        assert result.exit_code == 0

    def test_decrypt_text_aes(self, runner, sample_text, sample_password):
        """Test decrypting text via CLI."""
        from encryptocli.services import EncryptionService

        # First encrypt
        service = EncryptionService()
        encrypted = service.encrypt_text(sample_text, sample_password)

        # Then decrypt via CLI
        result = runner.invoke(
            app,
            [
                "decrypt",
                "--text",
                encrypted,
                "--password",
                sample_password,
                "--method",
                "aes",
            ],
        )
        assert result.exit_code == 0
        assert sample_text in result.stdout

    def test_decrypt_file_aes(self, runner, sample_file, sample_password, temp_dir):
        """Test decrypting file via CLI."""
        from encryptocli.services import EncryptionService

        # First encrypt
        service = EncryptionService()
        service.encrypt_file(str(sample_file), sample_password)
        encrypted_file = temp_dir / f"{sample_file.name}.encrypto"

        # Then decrypt via CLI
        result = runner.invoke(
            app,
            [
                "decrypt",
                "--file",
                str(encrypted_file),
                "--password",
                sample_password,
                "--method",
                "aes",
            ],
        )
        assert result.exit_code == 0

    def test_encrypt_missing_password(self, runner):
        """Test encrypt command without password."""
        result = runner.invoke(app, ["encrypt", "--text", "secret", "--method", "aes"])
        assert result.exit_code != 0

    def test_decrypt_missing_password(self, runner):
        """Test decrypt command without password."""
        result = runner.invoke(
            app, ["decrypt", "--text", "encrypted", "--method", "aes"]
        )
        assert result.exit_code != 0

    @pytest.mark.skipif(True, reason="Requires GPG installation")
    def test_pgp_gen_key(self, runner):
        """Test PGP key generation via CLI."""
        result = runner.invoke(
            app,
            ["pgp", "gen-key", "--email", "test@test.com", "--passphrase", "pass123"],
        )
        # May fail if GPG not installed
        if result.exit_code == 0:
            assert "successfully" in result.stdout.lower()

    @pytest.mark.skipif(True, reason="Requires GPG installation")
    def test_pgp_list_keys(self, runner):
        """Test PGP list keys via CLI."""
        result = runner.invoke(app, ["pgp", "list-keys"])
        # May fail if GPG not installed, but should not crash
        assert result.exit_code in [0, 1]

    def test_help_command(self, runner):
        """Test help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "EncryptoCLI" in result.stdout

    def test_hash_help_command(self, runner):
        """Test hash command help."""
        result = runner.invoke(app, ["hash", "--help"])
        assert result.exit_code == 0
        assert "algorithm" in result.stdout.lower()

    def test_encrypt_help_command(self, runner):
        """Test encrypt command help."""
        result = runner.invoke(app, ["encrypt", "--help"])
        assert result.exit_code == 0
        assert "password" in result.stdout.lower()

    def test_decrypt_help_command(self, runner):
        """Test decrypt command help."""
        result = runner.invoke(app, ["decrypt", "--help"])
        assert result.exit_code == 0
        assert "password" in result.stdout.lower()
