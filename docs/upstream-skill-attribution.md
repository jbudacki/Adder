# Upstream skill attribution

The Phase 3 embedded specialist skills were adapted on 2026-09-25 from locally available Blue Osprey skill sources in the development environment.

| ADDER skill | Adapted source |
| --- | --- |
| `adder-security-review` | `security-review` |
| `adder-secure-code-review` | `secure-code-review` |
| `adder-secrets-analysis` | `secrets-analysis` |
| `adder-iam-security` | `iam-security` |
| `adder-network-exposure` | `network-exposure` |
| `adder-crypto-analysis` | `crypto-analysis` |
| `adder-llm-security` | `llm-security` |
| `adder-3pp-dependency-hygiene` | `3pp-dependency-hygiene` |
| `adder-threat-model` | `threat-model`, `threat-model-generator-stride`, and `threat-model-generator-maestro` |

The source IAM skill declares author metadata `golden-gate`. The source security-review router describes the collection as Blue Osprey. No standalone license file was present in the inspected source skill directories. ADDER therefore retains its internal-evaluation license status and does not represent these adaptations as licensed for external redistribution.

The adaptations preserve the source capabilities while changing names, local routing, output contracts, uncertainty handling, and operational boundaries for a standalone ADDER repository. Scanner matches remain candidates, live or active validation requires separate authorization, and no ADDER skill receives merge or deployment authority.
