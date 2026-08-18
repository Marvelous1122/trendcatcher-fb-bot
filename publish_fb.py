"""Minimal Facebook Page publisher via the Graph API."""

import os

import requests

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def post_text(message: str) -> dict:
    page_id = os.environ["FB_PAGE_ID"]
    access_token = os.environ["FB_PAGE_ACCESS_TOKEN"]
    url = f"{GRAPH_API_BASE}/{page_id}/feed"
    resp = requests.post(url, data={"message": message, "access_token": access_token}, timeout=30)
    if not resp.ok:
        # Print Facebook's actual error body before raising, so the Actions
        # log shows the real reason instead of a generic "403 Forbidden".
        print("Facebook API error response body:", resp.text)
    resp.raise_for_status()
    return resp.json()
