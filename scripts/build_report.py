"""
Yeh script gitleaks-report.json aur trivy-report.json ko parse karti hai
aur ek clean security-report.md file bana deti hai jo PR comment ban jaati hai.
"""

import json
import os

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        content = f.read().strip()
        if not content:
            return None
        return json.loads(content)


def build_secrets_section():
    data = load_json("gitleaks-report.json")
    lines = ["## 🔑 Hardcoded Secrets Scan (Gitleaks)\n"]

    if not data:
        lines.append("✅ No hardcoded secrets found.\n")
        return "\n".join(lines)

    lines.append(f"⚠️ **{len(data)} potential secret(s) found:**\n")
    lines.append("| File | Line | Rule |")
    lines.append("|------|------|------|")
    for item in data:
        file = item.get("File", "unknown")
        line = item.get("StartLine", "?")
        rule = item.get("RuleID", "unknown")
        lines.append(f"| `{file}` | {line} | {rule} |")

    return "\n".join(lines)


def build_dependency_section():
    data = load_json("trivy-report.json")
    lines = ["\n## 📦 Dependency Vulnerability Scan (Trivy)\n"]

    if not data or "Results" not in data:
        lines.append("✅ No vulnerable dependencies found.\n")
        return "\n".join(lines)

    total = 0
    rows = []
    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []) or []:
            total += 1
            rows.append(
                f"| {vuln.get('PkgName')} | {vuln.get('InstalledVersion')} "
                f"| {vuln.get('FixedVersion', 'N/A')} | {vuln.get('Severity')} "
                f"| {vuln.get('VulnerabilityID')} |"
            )

    if total == 0:
        lines.append("✅ No vulnerable dependencies found.\n")
        return "\n".join(lines)

    lines.append(f"⚠️ **{total} vulnerability(ies) found:**\n")
    lines.append("| Package | Installed | Fixed In | Severity | CVE |")
    lines.append("|---------|-----------|----------|----------|-----|")
    lines.extend(rows)

    return "\n".join(lines)


def main():
    report = "# 🛡️ Automated Security Audit Report\n"
    report += build_secrets_section()
    report += build_dependency_section()

    with open("security-report.md", "w") as f:
        f.write(report)

    print(report)


if __name__ == "__main__":
    main()
