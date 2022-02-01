"""
Token module, handles everything relating to login tokens.

"""
from __future__ import annotations

SECRET_TOKEN: dict[str, dict[str | list[str]]] = {"installed": {
    "client_id": "364147813428-bkch7766kpe4ci474s9lni0ggb6gjqjg.apps.googleusercontent.com",
    "project_id": "testproject-339308",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}