# Compatibility statement

This statement describes environments actually exercised for the Phase 6 decision. Expected compatibility is not reported as verified compatibility.

## Verified locally

| Surface | Verified state | Evidence |
|---|---|---|
| Operating system | macOS local execution | Phase validators and pilot runner completed locally |
| Python | Python 3.9 standard library | Repository validators and pilot scripts completed without project dependencies |
| Skill packaging | Repository-local ADDER skill structure | `scripts/validate_skills.py` validates required files and metadata |
| JSON contracts | Draft 2020-12 JSON Schema syntax and repository-specific checks | Schema parsing plus phase validators |
| GitLab output | Advisory artifact format generated locally | Pilot produced GitLab-oriented artifacts; no live pipeline execution |
| Pilot target | One JavaScript/TypeScript AI/RAG repository snapshot | Operational pilot evidence under `evaluations/pilot/runs/` |

## Not yet verified

- Linux GitLab runners and GitLab SaaS or self-managed pipeline execution.
- Windows execution.
- Multiple Python runtime versions.
- GitHub, Bitbucket, Azure DevOps, or other CI platforms.
- Authoritative vulnerability, malware-reputation, package-registry, or provenance providers.
- Every language or framework described by the specialist skills.
- A specific Codex product release or hosted-agent configuration.

## Known dependency limitation

The repository validators use the Python standard library. The upstream skill quick-validation helper additionally requires PyYAML, which was unavailable in the Phase 6 environment. ADDER therefore records its own deterministic validation result and does not claim that the upstream helper ran successfully.

Compatibility expansion requires an explicit test matrix, versioned fixtures, and evidence from the target runner rather than an assumption based on local success.
