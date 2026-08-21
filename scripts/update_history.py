"""
Yeh script gitleaks-report.json aur trivy-report.json parh kar
docs/history.json mein ek naya record add karti hai (purana data safe rehta hai).
Dashboard (docs/index.html) isi history.json ko parh kar charts banata hai.
"""

import json
import os
from datetime import datetime, timezone


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else None


def count_secrets():
    data = load_json("gitleaks-report.json")
    return len(data) if data else 0


def count_vulnerabilities():
    data = load_json("trivy-report.json")
    if not data or "Results" not in data:
        return 0
    total = 0
    for result in data.get("Results", []):
        total += len(result.get("Vulnerabilities", []) or [])
    return total


def main():
    history_path = "docs/history.json"

    # Purani history load karo (agar hai to)
    history = []
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            content = f.read().strip()
            if content:
                history = json.loads(content)

    # Naya record banao
    record = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "commit": os.environ.get("GITHUB_SHA", "local")[:7],
        "secrets_found": count_secrets(),
        "vulnerabilities_found": count_vulnerabilities(),
    }

    history.append(record)

    # Sirf recent 100 records rakho (file zyada bari na ho)
    history = history[-100:]

    os.makedirs("docs", exist_ok=True)
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    print(f"Added record: {record}")


if __name__ == "__main__":
    main()
