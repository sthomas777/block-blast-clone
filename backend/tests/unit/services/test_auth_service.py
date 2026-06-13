from datetime import datetime, timedelta, timezone

import jwt
import pytest

from src.services.auth_service import (
    ALGORITHM,
    create_access_token,
    hash_password,
    settings,
    verify_access_token,
    verify_password,
)

SECRET = settings.secret_key.get_secret_value()


def _encode(payload: dict, secret: str = SECRET, algorithm: str = ALGORITHM) -> str:
    return jwt.encode(payload, secret, algorithm=algorithm)


def test_hash_password_does_not_return_plaintext() -> None:
    hashed = hash_password("supersecret")

    assert hashed != "supersecret"
    assert hashed


def test_verify_password_accepts_correct_password() -> None:
    hashed = hash_password("supersecret")

    assert verify_password("supersecret", hashed) is True


def test_verify_password_rejects_wrong_password() -> None:
    hashed = hash_password("supersecret")

    assert verify_password("wrongpassword", hashed) is False


def test_hash_password_is_salted() -> None:
    first = hash_password("supersecret")
    second = hash_password("supersecret")

    assert first != second
    assert verify_password("supersecret", first)
    assert verify_password("supersecret", second)


def test_create_then_verify_returns_sub() -> None:
    token = create_access_token({"sub": "42"})

    assert verify_access_token(token) == "42"


def test_create_access_token_does_not_mutate_input() -> None:
    data = {"sub": "42"}

    create_access_token(data)

    assert data == {"sub": "42"}
    assert "exp" not in data


def test_create_access_token_uses_custom_expiry() -> None:
    token = create_access_token({"sub": "1"}, expires_delta=timedelta(minutes=30))

    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    expected = datetime.now(timezone.utc) + timedelta(minutes=30)

    assert abs((exp - expected).total_seconds()) < 5


def test_create_access_token_defaults_expiry_from_settings() -> None:
    token = create_access_token({"sub": "1"})

    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    expected = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes,
    )

    assert abs((exp - expected).total_seconds()) < 5


def test_verify_access_token_rejects_expired_token() -> None:
    token = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))

    assert verify_access_token(token) is None


def test_verify_access_token_rejects_garbage() -> None:
    assert verify_access_token("not-a-real-token") is None


def test_verify_access_token_rejects_wrong_secret() -> None:
    token = _encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        secret="a-different-secret-that-is-at-least-32-bytes-long",
    )

    assert verify_access_token(token) is None


def test_verify_access_token_rejects_missing_sub_claim() -> None:
    token = _encode({"exp": datetime.now(timezone.utc) + timedelta(minutes=5)})

    assert verify_access_token(token) is None


def test_verify_access_token_rejects_missing_exp_claim() -> None:
    token = _encode({"sub": "1"})

    assert verify_access_token(token) is None


def test_verify_access_token_rejects_alg_none() -> None:
    # Algorithm-confusion guard: an unsigned ("alg": "none") token must fail.
    token = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        key=None,
        algorithm="none",
    )

    assert verify_access_token(token) is None


@pytest.mark.parametrize("sub", ["1", "42", "9999999999"])
def test_verify_access_token_round_trips_various_subs(sub: str) -> None:
    token = create_access_token({"sub": sub})

    assert verify_access_token(token) == sub
