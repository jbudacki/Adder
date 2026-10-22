#!/usr/bin/env python3
"""Smoke-test the three embedded specialist scanners with synthetic inputs."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    secrets = load_module("adder_secrets_scan", ROOT / "skills" / "adder-secrets-analysis" / "scripts" / "secrets_scan.py")
    crypto = load_module("adder_crypto_scan", ROOT / "skills" / "adder-crypto-analysis" / "scripts" / "crypto_scan.py")
    llm = load_module("adder_llm_scan", ROOT / "skills" / "adder-llm-security" / "scripts" / "llm_scan.py")

    with tempfile.TemporaryDirectory(prefix="adder-specialist-fixtures-") as temporary:
        fixture_root = Path(temporary)
        synthetic_identifier = "AKIA" + "A" * 16
        (fixture_root / "secret.txt").write_text(f"credential = '{synthetic_identifier}'\n", encoding="utf-8")
        (fixture_root / "crypto.py").write_text("import hashlib\ndigest = hashlib.md5(data).hexdigest()\n", encoding="utf-8")
        (fixture_root / "agent.py").write_text("from openai import OpenAI\nresult = eval(response)\n", encoding="utf-8")

        secret_results = secrets.scan_directory(str(fixture_root), ["cloud"], set(), secrets.DEFAULT_MAX_FILE_BYTES)
        if len(secret_results) != 1 or synthetic_identifier in str(secret_results):
            raise ValueError("secret scanner failed detection or redaction invariant")
        if not str(secret_results[0].get("evidence", "")).startswith("<redacted"):
            raise ValueError("secret scanner did not return fingerprinted evidence")

        crypto_results = crypto.scan_directory(str(fixture_root), {"broken_algorithms"}, set(), crypto.DEFAULT_MAX_FILE_BYTES)
        if not any(result.get("type") == "MD5 in a cryptographic API" for result in crypto_results):
            raise ValueError("crypto scanner did not identify the synthetic MD5 review surface")

        discovery = llm.scan_directory(str(fixture_root), "discovery", llm.CATEGORY_SPECS["discovery"], set(), llm.DEFAULT_MAX_FILE_BYTES)
        output = llm.scan_directory(str(fixture_root), "output", llm.CATEGORY_SPECS["output"], set(), llm.DEFAULT_MAX_FILE_BYTES)
        if not discovery or not output:
            raise ValueError("LLM scanner did not identify synthetic discovery and output surfaces")
        if "from openai" in str(discovery) or "eval(response)" in str(output):
            raise ValueError("LLM scanner exposed raw matching source")
        if not all(str(item.get("evidence", "")).startswith("<redacted-line") for item in discovery + output):
            raise ValueError("LLM scanner did not return redacted-line evidence")

        validation_attempt = subprocess.run(
            [
                sys.executable,
                str(ROOT / "skills" / "adder-secrets-analysis" / "scripts" / "secrets_scan.py"),
                "--path",
                str(fixture_root),
                "--validate",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if validation_attempt.returncode == 0 or "not implemented" not in validation_attempt.stderr:
            raise ValueError("secret scanner did not fail closed for active validation")

    print("Validated secrets, cryptography, and LLM scanner smoke tests.")


if __name__ == "__main__":
    main()
