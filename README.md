# Auth Timing Analyzer

A lightweight helper script to detect timing-based discrepancies in authentication endpoints.

This tool is intended for authorized security assessments and defensive audits, helping identify
potential username enumeration risks caused by inconsistent response times during login attempts.

---

## Why this matters

Authentication mechanisms should not leak information about user existence.
Even subtle response time differences can be abused by attackers to infer valid usernames
through timing analysis, without requiring valid credentials.

This type of issue is commonly introduced when authentication logic follows different execution
paths depending on whether a username exists or not.

---

## What this tool does

- Sends multiple authentication requests per username
- Measures response times with high-resolution timers
- Calculates:
  - average response time
  - standard deviation
- Compares results against a global baseline
- Flags usernames whose timing significantly deviates from the expected pattern

The goal is to **identify timing side channels**, not to perform brute-force or exploitation.

---

## How to use

### 1. Prepare a username wordlist
Create a file containing one username per line, for example:

admin
test
guest
support


### 2. Run the analyzer

```bash
python3 timing_analyzer.py \
  -u https://target/login \
  -U users.txt \
  -n 15 \
  --threshold 2.0
```

Arguments

| Parameter          | Description                                                |
| ------------------ | ---------------------------------------------------------- |
| `-u, --url`        | Login endpoint URL                                         |
| `-U, --users`      | File containing usernames                                  |
| `-p, --password`   | Password used for all attempts (default: invalid password) |
| `-n, --iterations` | Requests per username (default: 10)                        |
| `--threshold`      | Standard deviation multiplier to flag anomalies            |


### Example output

```bash
=== Timing Analysis Results ===

Global average: 0.1523s | Global std: 0.0214s

admin                avg=0.3124s std=0.0102s ⚠️ POSSIBLE VALID USER
test                 avg=0.1411s std=0.0081s
guest                avg=0.1398s std=0.0093s

```
Usernames flagged as anomalies may indicate different backend execution paths and should be reviewed manually.

### How it works (high-level)

For each username, the script:

Sends multiple authentication requests using the same invalid password

Measures request duration using a high-resolution monotonic clock

Computes statistical metrics

Compares per-user averages against the global distribution

Significant deviations may suggest timing-based information leakage.

### Limitations

Network jitter and latency can affect measurements

HTTPS overhead may reduce timing precision

Small timing differences may require higher iteration counts

Results should always be validated manually

This tool is intended to assist analysis, not replace expert judgment.

## Remediation guidance

Executing the same authentication logic regardless of user existence

Using dummy password hashes when a username is not found

Returning generic error messages for all authentication failures

Responsible usage

⚠️ This tool must only be used during authorized security assessments.

It does not perform brute-force attacks and is designed to help identify
authentication design weaknesses, not exploit them.


# Author

Javier Sopeña

Offensive Security / Pentesting