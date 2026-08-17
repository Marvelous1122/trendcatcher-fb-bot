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
    resp.raise_for_status()
    return resp.json()
