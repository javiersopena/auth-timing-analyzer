# Demo Authentication Server

This is a small, intentionally vulnerable Node.js authentication server used to demonstrate
timing-based username enumeration issues and their remediation.

It is designed to be used together with the **Auth Timing Analyzer** tool as a reproducible
local lab for security testing and education.

---

## 🎯 Purpose

The goal of this demo server is to illustrate how differences in authentication execution paths
can introduce timing side channels that allow attackers to infer whether a username exists.

The server provides:
- A vulnerable authentication endpoint
- A timing-safe (fixed) authentication endpoint
- A realistic simulation using bcrypt password hashing

---

## 🧪 Endpoints

### `POST /login` — Vulnerable

This endpoint is **intentionally vulnerable** to timing-based username enumeration.

Behavior:
- Returns early if the username does not exist
- Performs a bcrypt password comparison only for existing users
- Introduces measurable response time differences

This endpoint exists **for demonstration and testing purposes only**.

---

### `POST /login-fixed` — Timing-safe

This endpoint implements a **timing-safe authentication flow**.

Behavior:
- Always performs a password hash comparison
- Uses a constant dummy hash when the username does not exist
- Returns a generic authentication error in all cases

This endpoint demonstrates the correct mitigation strategy.

---

## ▶️ How to run

### 1. Install dependencies

```bash
cd demo-server
npm install
```

2. Start the server
``` bash
npm start

# Listening on http://localhost:3000

```

Example request

The login endpoints expect form-encoded or JSON requests with the following fields:
```bash

{
  "username": "admin",
  "password": "invalid-password"
}
```

🔬 Testing with Auth Timing Analyzer

Example command:
```bash

python3 timing_analyzer.py \
  -u http://localhost:3000/login \
  -U users.txt \
  -n 20
```

To validate the fix:
```bash

python3 timing_analyzer.py \
  -u http://localhost:3000/login-fixed \
  -U users.txt \
  -n 20
```
⚠️ Security Notice

This server is intentionally insecure and must never be deployed in production.

It is provided solely for:

Educational purposes

Authorized security testing

Demonstration of timing side-channel vulnerabilities and mitigations

📚 Related Documentation

Authentication timing remediation: ../docs/remediation.md
