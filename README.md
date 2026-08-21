# Automated DevSecOps Vulnerability Scanner

A GitHub Actions pipeline that automatically scans code for security issues on every push and pull request. It runs three checks:

1. **Secret scanning** - checks for hardcoded API keys, passwords, and tokens using Gitleaks
2. **Dependency scanning** - checks project dependencies for known vulnerabilities using Trivy
3. **Automated reporting** - combines both results into a single report and posts it as a comment on the pull request

I built this project to learn how security scanning can be integrated directly into a CI/CD pipeline, instead of being a separate manual step.

---

## Project Structure

devsecops-pipeline/
├── .github/
│ └── workflows/
│ └── security-scan.yml # CI/CD pipeline definition
├── scripts/
│ └── build_report.py # Parses scan results into a readable report
├── .gitignore
└── README.md


---

## How It Works

1. On every push or pull request to main, GitHub Actions runs two jobs in parallel - one runs Gitleaks, the other runs Trivy.
2. Each job saves its results as a JSON file.
3. A third job downloads both results, runs build_report.py to turn them into a Markdown report, and posts it as a comment on the pull request using the GitHub API.

No manual setup is needed - GitHub provides the GITHUB_TOKEN automatically for the pipeline to comment on the PR.

---

## Setup

1. Copy the .github/ and scripts/ folders into the root of your repository.
2. Commit and push to a branch, then open a pull request into main.
3. Check the Actions tab - you will see DevSecOps Security Scan running.
4. Once it finishes, the bot comment with the report appears on your PR.

---

## Running It Locally

```bash
# Secret scan
docker run --rm -v "$PWD":/repo zricethezav/gitleaks:latest detect --source /repo --report-format json --report-path gitleaks-report.json --exit-code 0

# Dependency scan (requires Trivy)
trivy fs . --format json --output trivy-report.json --severity CRITICAL,HIGH,MEDIUM

# Build the report
python3 scripts/build_report.py
cat security-report.md
```

---

## Customization

| What | How |
|------|------|
| Change severity threshold | Edit the severity line in the Trivy job in security-scan.yml |
| Ignore false positives | Add a .gitleaksignore file, or .trivyignore for specific CVEs |
| Fail the build on findings | Change exit-code: 0 to exit-code: 1 in the relevant step |
