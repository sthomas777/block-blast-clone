import os

# Ensure the env vars read at import time by the app (database URL, JWT secret)
# exist before any test imports `backend.src.main`. `setdefault` keeps any value
# already provided by the developer's real environment / CI.
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
