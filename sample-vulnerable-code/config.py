# ⚠️ INTENTIONALLY INSECURE — for testing the Gitleaks scan only.
# Delete this file before using the pipeline on a real project.
DATABASE_PASSWORD = "Xk9mQ2vLp8ZnR4wT6yB1"
AWS_ACCESS_KEY_ID = "AKIAT7EXAMPLE2FAKE12"
STRIPE_API_KEY = "sk_live_51H8anpFakeKeyForTesting123456"

def connect_to_db():
    # Bad practice: credentials hardcoded directly in source code
    return f"Connecting with password={DATABASE_PASSWORD}"
