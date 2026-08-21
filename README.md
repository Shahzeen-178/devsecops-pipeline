# 🛡️ Automated DevSecOps Vulnerability Scanner

Ek GitHub Actions pipeline jo har `push` / `pull_request` par:
1. Hardcoded API keys / passwords scan karti hai (**Gitleaks**)
2. Vulnerable dependencies check karti hai (**Trivy**)
3. Combined **Security Audit Report** PR par comment kar deti hai

---

## 📁 Project Structure

```
devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── security-scan.yml     # Main CI/CD pipeline
├── scripts/
│   └── build_report.py           # Report generator (Python, no external deps)
├── sample-vulnerable-code/
│   └── config.py                 # Intentionally insecure file — for testing only
├── .gitignore
└── README.md
```

---

## ⚙️ Setup (5 minutes)

1. Copy the `.github/` and `scripts/` folders into the root of your repo.
2. Commit and push to a branch, then open a Pull Request into `main`.
3. Go to the **Actions** tab on GitHub — you'll see `DevSecOps Security Scan` running.
4. Once it finishes, check your PR — a bot comment with the full report will appear automatically.

No API keys or secrets need to be configured — `GITHUB_TOKEN` is provided automatically by GitHub Actions.

---

## 🧪 Testing it locally (before pushing)

```bash
# 1. Secret scan
docker run --rm -v "$PWD":/repo zricethezav/gitleaks:latest \
  detect --source /repo --report-format json \
  --report-path gitleaks-report.json --exit-code 0

# 2. Dependency scan (install trivy first: https://aquasecurity.github.io/trivy)
trivy fs . --format json --output trivy-report.json \
  --severity CRITICAL,HIGH,MEDIUM

# 3. Build the markdown report
python3 scripts/build_report.py
cat security-report.md
```

The `sample-vulnerable-code/config.py` file contains a fake hardcoded key on purpose —
run the scan against this repo once to confirm Gitleaks catches it, then delete that
folder before using the pipeline on real projects.

---

## 🔧 Customization

| What | How |
|------|-----|
| Change severity threshold | Edit `severity:` line in `security-scan.yml` (Trivy job) |
| Ignore false positives | Add a `.gitleaksignore` file, or `.trivyignore` for CVEs to skip |
| Add SAST (Semgrep/CodeQL) | Add a new job in `security-scan.yml` following the same pattern as `dependency-scan` |
| Fail the build on findings | Change `exit-code: 0` → `exit-code: 1` in the relevant step |

---
Testing pipeline trigger.

## 🗺️ Roadmap Ideas
- [ ] Add Semgrep / CodeQL as a real SAST job
- [ ] Add DAST scan (OWASP ZAP) against a staging deployment
- [ ] Slack/Teams notification on CRITICAL findings
- [ ] Auto-fail PR merge if CRITICAL secrets found
