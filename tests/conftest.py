import os

# Must run before any test module imports app.config (which reads this at import time).
os.environ.setdefault("SQUAD_API_SHARED_SECRET", "test-secret-0123456789abcdef0123456789")
