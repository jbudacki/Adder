# ADDER examples

The `gitlab/` directory contains an advisory CI example and a synthetic assessment input. The job publishes Markdown and GitLab Code Quality artifacts while remaining non-blocking. It does not call the GitLab API, post merge-request comments, or enforce a merge decision.

Examples use synthetic data and do not imply that advisory output is an enforced GitLab decision. See `docs/gitlab-integration.md` before adoption.
