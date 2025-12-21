# Auth Timing Analyzer

Small helper script to detect timing-based discrepancies in authentication workflows.

This tool is intended for security assessments and defensive audits, helping identify
potential username enumeration risks caused by inconsistent authentication execution paths.

python3 timing_analyzer.py \
  -u https://target/login \
  -U users.txt \
  -n 15 \
  --threshold 2.0

## Why this matters

Authentication endpoints should not leak information about user existence.
Even subtle response time differences can be abused to enumerate valid usernames
through timing analysis.

## Remediation Guidance

For a detailed explanation of the root cause and recommended fixes, see:
- [Authentication Timing Remediation](docs/remediation.md)

⚠️ This tool does not perform brute-force attacks.
It is designed to help identify timing inconsistencies during authorized security assessments.


Example:

python3 timing_analyzer.py \
  -u https://target/login \
  -U users.txt \
  -n 15 \
  --threshold 2.0
