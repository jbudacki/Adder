# Install ADDER in Codex

This package is the ADDER `0.1.0-pre-pilot.1` build. It contains 18 repository-local skills and their shared policies, schemas, scripts, and evaluation fixtures. Keep the directory intact: ADDER skills use paths relative to the plugin root.

## Prerequisites

- A Codex client that supports local plugins and skills.
- Python 3.9 or later for the dependency-free ADDER validation scripts.
- Permission to install a local plugin or use an approved team marketplace.

ADDER has no bundled MCP server, external service, hook, or package-install step.

## Validate the archive

After extracting the ZIP, enter the `adder-ai-code-assurance` directory and run:

```sh
python3 scripts/validate_skills.py
python3 scripts/validate_core_fixtures.py
python3 scripts/validate_specialist_fixtures.py
python3 scripts/validate_specialist_scanners.py
python3 scripts/validate_phase3_completion.py
python3 scripts/validate_agent_recovery_fixtures.py
python3 scripts/validate_phase5.py
python3 scripts/validate_phase6.py
python3 scripts/validate_distribution.py
```

## Personal local installation

1. Copy the complete extracted directory to `~/.codex/plugins/adder-ai-code-assurance`.
2. Add an `adder-ai-code-assurance` entry to the personal marketplace at `~/.agents/plugins/marketplace.json`. Its local source path should be `./.codex/plugins/adder-ai-code-assurance` because marketplace paths resolve from the user home directory.
3. Keep `policy.installation` set to `AVAILABLE`, `policy.authentication` set to `ON_INSTALL`, and use the `Developer Tools` category.
4. Restart the Codex desktop app, open the Plugins Directory, and install or enable ADDER.
5. Start a new task and confirm that `$adder-code-assurance` is discoverable.

Do not copy only the individual skill directories. Doing so removes the shared schemas and policies referenced by those skills.

## GitLab repository installation

Extract the contents of the top-level `adder-ai-code-assurance` directory into the root of a new GitLab repository. Preserve dot-directories, including `.codex-plugin` and `.gitlab`. Do not commit an enclosing ZIP file, `.DS_Store`, or a source `.git` directory.

Clone the GitLab repository into the local plugin directory and register it through an approved personal or team marketplace. Pin pilot installations to the `0.1.0-pre-pilot.1` tag or its exact commit once the tag is created.

## Operating status

This is a pre-pilot build intended for controlled work next month. Its release-readiness decision remains `pilot_only`:

- Use read-only or advisory operation with human review.
- Do not enable mandatory merge, build, deployment, or release enforcement.
- Do not treat results as complete provenance or vulnerability coverage.
- Do not redistribute until licensing and release ownership are approved.

See `release/PRE-PILOT-NOTES.md` and `docs/release-readiness.md` before use.
