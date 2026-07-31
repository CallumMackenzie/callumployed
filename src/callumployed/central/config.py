import os

import keyring
import turso

from callumployed.data.repositories import get_config_value, set_config_value

CENTRAL_API_URL_CONFIG_KEY = "central_api_url"
CENTRAL_PASSKEY_ENV = "CALLUMPLOYED_CENTRAL_PASSKEY"
CENTRAL_API_URL_ENV = "CALLUMPLOYED_CENTRAL_API_URL"
CENTRAL_KEYRING_SERVICE = "callumployed-central"
CENTRAL_KEYRING_USERNAME = "passkey"


def get_central_api_url(connection: turso.Connection) -> str | None:
    value = os.environ.get(CENTRAL_API_URL_ENV) or get_config_value(
        connection,
        CENTRAL_API_URL_CONFIG_KEY,
    )
    if value is None:
        return None
    stripped = value.strip().rstrip("/")
    return stripped or None


def set_central_api_url(connection: turso.Connection, api_url: str) -> None:
    cleaned_url = api_url.strip().rstrip("/")
    if not cleaned_url:
        raise ValueError("central API URL cannot be empty")
    set_config_value(connection, CENTRAL_API_URL_CONFIG_KEY, cleaned_url)


def get_central_passkey() -> str | None:
    value = os.environ.get(CENTRAL_PASSKEY_ENV)
    if value is not None and value.strip():
        return value.strip()
    try:
        saved = keyring.get_password(CENTRAL_KEYRING_SERVICE, CENTRAL_KEYRING_USERNAME)
    except keyring.errors.KeyringError:
        return None
    if saved is None:
        return None
    stripped = saved.strip()
    return stripped or None


def set_central_passkey(passkey: str) -> None:
    cleaned_passkey = passkey.strip()
    if not cleaned_passkey:
        raise ValueError("central passkey cannot be empty")
    keyring.set_password(
        CENTRAL_KEYRING_SERVICE,
        CENTRAL_KEYRING_USERNAME,
        cleaned_passkey,
    )

