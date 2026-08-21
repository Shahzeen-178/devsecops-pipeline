# Automated DevSecOps Vulnerability Scanner

A GitHub Actions pipeline that automatically scans code for security issues on every push and pull request. It runs three checks and tracks results over time on a live dashboard.

**Live Dashboard:** https://shahzeen-178.github.io/devsecops-pipeline/

1. **Secret scanning** - checks for hardcoded API keys, passwords, and tokens using Gitleaks
2. **Dependency scanning** - checks project dependencies for known vulnerabilities using Trivy
3. **Static code analysis (SAST)** - checks the project's own code logic for issues like injection flaws using CodeQL
4. **Automated reporting** - combines the results into a single report and posts it as a comment on the pull request
5. **History tracking** - each scan's results are logged to a dashboard, so trends are visible over time instead of only the latest scan

I built this project to learn how security scanning can be integrated directly into a CI/CD pipeline, instead of being a separate manual step.

---

## Project Structure

```
devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── security-scan.yml     # CI/CD pipeline definition
├── scripts/
│   ├── build_report.py           # Parses scan results into a readable report
│   └── update_history.py         # Appends this scan's results to the dashboard history
├── docs/
│   ├── index.html                # Dashboard page (served via GitHub Pages)
│   └── history.json              # Scan history data used by the dashboard
├── .gitignore
└── README.md
```

---

## How It Works

1. On every push or pull request to `main`, GitHub Actions runs three jobs in parallel: Gitleaks (secrets), Trivy (dependencies), and CodeQL (code analysis).
2. The Gitleaks and Trivy jobs save their results as JSON files.
3. A report job downloads both JSON results, runs `build_report.py` to turn them into a Markdown report, and posts it as a comment on the pull request using the GitHub API.
4. The same job runs `update_history.py`, which appends the scan's results (date, commit, counts) to `docs/history.json`, then commits that file back to the repository.
5. CodeQL results are posted separately to GitHub's built-in Security tab, since that's a native GitHub feature.
6. GitHub Pages serves `docs/index.html`, which reads `docs/history.json` and renders a chart and table of scan history.

No manual setup is needed - GitHub provides the `GITHUB_TOKEN` automatically for the pipeline to comment on PRs and commit back to the repo.

---

## Setup

1. Copy the `.github/`, `scripts/`, and `docs/` folders into the root of your repository.
2. Commit and push to a branch, then open a pull request into `main`.
3. Check the **Actions** tab - you will see `DevSecOps Security Scan` running.
4. Once it finishes, the bot comment with the report appears on your PR, and CodeQL findings appear under the **Security** tab.
5. To enable the live dashboard: go to **Settings > Pages**, set the source to the `main` branch and `/docs` folder, and save.

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
| Add more languages to CodeQL | Add them to the languages list in the codeql-scan job |

---

## What I Learned

- Deleting a file doesn't remove secrets that were previously committed - they remain in git history unless it's rewritten (e.g. with git filter-repo or BFG).
- Secret scanners are pattern-based, not just "looks random" - they match specific formats (like AWS key length, or Stripe token prefixes), which is why fake test secrets sometimes go undetected until formatted realistically.
- GitHub's own Push Protection can block a push before it even reaches the repo if it detects a matching secret pattern.
 <--demo test-- >