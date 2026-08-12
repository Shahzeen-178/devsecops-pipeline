# ⚠️ INTENTIONALLY INSECURE — for testing the Gitleaks scan only.
# Delete this file before using the pipeline on a real project.

DATABASE_PASSWORD = "SuperSecret123!"
AWS_ACCESS_KEY_ID = "AKIAFAKEKEYFORTESTONLY12"
STRIPE_API_KEY = "sk_live_fake_key_for_testing_purposes_only"

def connect_to_db():
    # Bad practice: credentials hardcoded directly in source code
    return f"Connecting with password={DATABASE_PASSWORD}"
