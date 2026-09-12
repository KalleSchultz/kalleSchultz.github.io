#!/usr/bin/env python3
"""One-time, LOCAL authorization helper for the Polar AccessLink API.

Run this yourself, once, on your own machine (never in CI). It walks you
through the OAuth2 authorization-code flow against your Polar account and
prints the long-lived access token + Polar user id you then store as
GitHub Actions secrets (POLAR_ACCESS_TOKEN, POLAR_USER_ID) — see
health/README.md for the full setup guide.

Requires:
    pip install requests

Usage:
    export POLAR_CLIENT_ID=your-client-id
    export POLAR_CLIENT_SECRET=your-client-secret
    python3 setup_polar_auth.py
"""

import base64
import os
import sys
import urllib.parse

import requests

AUTHORIZATION_URL = "https://flow.polar.com/oauth2/authorization"
TOKEN_URL = "https://polarremote.com/v2/oauth2/token"
USERS_URL = "https://www.polaraccesslink.com/v3/users"
REDIRECT_URI = "http://localhost/callback"


def extract_code(user_input: str) -> str:
    user_input = user_input.strip()
    if user_input.startswith("http"):
        query = urllib.parse.urlparse(user_input).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            return params["code"][0]
        sys.exit("Could not find a 'code' parameter in that URL.")
    return user_input


def main() -> None:
    client_id = os.environ.get("POLAR_CLIENT_ID")
    client_secret = os.environ.get("POLAR_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit(
            "Set POLAR_CLIENT_ID and POLAR_CLIENT_SECRET environment "
            "variables first (from admin.polaraccesslink.com). See "
            "health/README.md."
        )

    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
    }
    auth_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(auth_params)}"

    print("1. Open this URL in your browser and log in / approve access:\n")
    print(f"   {auth_url}\n")
    print(
        "2. Your browser will be redirected to a localhost URL that won't "
        "load (that's expected). Copy the full URL from the address bar "
        "(or just the 'code=' value) and paste it below.\n"
    )
    user_input = input("Paste the redirect URL or code here: ")
    code = extract_code(user_input)

    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    token_resp = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        timeout=30,
    )
    if not token_resp.ok:
        sys.exit(f"Token exchange failed ({token_resp.status_code}): {token_resp.text}")

    token_data = token_resp.json()
    access_token = token_data["access_token"]

    # Registering the user is required before the API will serve any data
    # for this token. If already registered, Polar returns 409 — that's fine.
    register_resp = requests.post(
        USERS_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"member-id": f"health-sync-{token_data.get('x_user_id', 'user')}"},
        timeout=30,
    )

    if register_resp.status_code == 409:
        user_id = token_data.get("x_user_id")
        if not user_id:
            sys.exit(
                "User already registered and no x_user_id was returned by "
                "the token endpoint. Re-run after revoking access in Polar "
                "Flow (Settings -> Data sharing) to get a clean token."
            )
    elif register_resp.ok:
        user_id = register_resp.json().get("polar-user-id", token_data.get("x_user_id"))
    else:
        sys.exit(f"User registration failed ({register_resp.status_code}): {register_resp.text}")

    print("\nSuccess! Add these as GitHub repository secrets")
    print("(Settings -> Secrets and variables -> Actions -> New repository secret):\n")
    print(f"  POLAR_ACCESS_TOKEN = {access_token}")
    print(f"  POLAR_USER_ID      = {user_id}")


if __name__ == "__main__":
    main()
