import os

_SECRETS_DIR = "/run/secrets"


def read_secret(name: str) -> str:
    """Read a secret value.

    In Docker Compose the secret is a file mounted at ``/run/secrets/<name>``.
    Outside Docker (local dev, CI) the value falls back to an env var with the
    same uppercased name (e.g. ``name="secret_key"`` → ``SECRET_KEY``).

    Raises ``RuntimeError`` if neither source provides a value.
    """
    path = os.path.join(_SECRETS_DIR, name)
    if os.path.isfile(path):
        with open(path) as f:
            return f.read().strip()

    env_var = name.upper()
    value = os.environ.get(env_var)
    if value is not None:
        return value

    raise RuntimeError(
        f"Secret '{name}' not found: expected file {path!r} or env var {env_var!r}",
    )
