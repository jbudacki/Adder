# Package trust policy

**Version:** 0.1.0  
**Mode:** Advisory pilot  
**Owner:** Not yet assigned

This policy defines the initial ADDER evidence requirements for a newly introduced or materially changed third-party dependency. It does not approve registry access, authorize package installation, or configure a merge gate.

## Required evidence

For production, build, security-sensitive, or Tier 3 dependencies, record:

- Exact ecosystem, namespace, package, requested version, resolved version, and dependency scope
- Effective source and whether the registry or repository is approved
- Existence of the exact package and version in that source
- Publisher, namespace, or source relationship when the ecosystem exposes it
- Artifact integrity tied to an authoritative digest, signature, provenance statement, or approved lockfile record
- Lockfile consistency when the ecosystem uses a lockfile
- Dated results from approved vulnerability and malware sources
- Reputation or maintenance evidence required by repository policy
- Sources not queried, stale results, contradictions, and other limitations

A source must be attributable to the exact package coordinate and artifact. “No signal” is a result from a named source at a recorded time; it is not a claim that no vulnerability or malware exists.

## Advisory decisions

Recommend blocking when exact evidence establishes a core-policy condition, including a confirmed malicious or prohibited dependency, an unapproved source prohibited by policy, an exact package or version that cannot resolve, an integrity mismatch, or a failed mandatory trust check.

Require manual review when required access is unavailable, evidence is stale or contradictory, private and public resolution is ambiguous, or signals cannot be correlated to the exact package and artifact. Name similarity, popularity, package age, sparse metadata, or maintenance activity can justify review but cannot independently justify blocking.

Use `verified` only when every requirement applicable to the dependency’s scope and risk tier is complete. A package that exists is not necessarily trusted.

## Data and execution boundary

Do not send private package metadata to an external provider without approved data handling. Do not install, import, execute, build, or detonate an untrusted package as part of this policy. Dynamic analysis requires separate authorization and isolation.

Exceptions must satisfy `core-decision-policy.md`; they do not erase package findings.
