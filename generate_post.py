"""
Builds today's post content: either a static bank item (Tue/Sun) or a
live-news item drafted from a real RSS article (Mon/Wed/Thu/Fri/Sat).

Design goal: minimize hallucination risk since nothing is human-reviewed
before publishing.
  - Tue/Sun use 100% pre-written content, no LLM call at all.
  - News days pass the LLM the actual article title + summary + link and
    instruct it to use ONLY those facts, never invent numbers or names.
  - If no suitable fresh article is found, fall back to a generic,
    fact-free evergreen line rather than risk a bad post.
"""

import datetime
import json
import os

import feedparser
from google import genai
from google.genai import types

from content_bank import BB_TIPS, ENGAGEMENT_POSTS, pick
from rss_sources import PILLARS

STATE_FILE = "posted_log.json"
MAX_LOG_ENTRIES = 300
MODEL = "claude-sonnet-5"

BRAND_SYSTEM_PROMPT = """You draft short Facebook posts for TrendCatcher, a \
cybersecurity/bug-bounty/AI-security news brand page (no personal name, no \
"I/my" voice - use a neutral brand voice, e.g. "TrendCatcher tracks..." or \
just state facts directly).

Rules, no exceptions:
- Use ONLY the facts given to you in the article title/summary below. Do not \
invent CVE numbers, statistics, company names, or details not present in the \
provided text.
- If the provided summary is thin, write a shorter post rather than padding \
it with invented specifics.
- End with the source link on its own line.
- No hashtags (Facebook doesn't reward them like Instagram does).
- 80-160 words, confident and practical tone, no hype, no fear-mongering.
- Output ONLY the finished post text, nothing else (no preamble, no labels).
"""


def _load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"posted_links": []}


def _save_state(state):
    state["posted_links"] = state["posted_links"][-MAX_LOG_ENTRIES:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def _fetch_candidate_entry(pillar_key, posted_links):
    pillar = PILLARS[pillar_key]
    keywords = pillar["keywords"]
    candidates = []

    for feed_url in pillar["feeds"]:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception:
            continue
        for entry in parsed.entries:
            link = entry.get("link", "")
            if not link or link in posted_links:
                continue
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            haystack = f"{title} {summary}".lower()
            if keywords and not any(kw.lower() in haystack for kw in keywords):
                continue
            published = entry.get("published_parsed")
            candidates.append((published, title, summary, link))

    if not candidates:
        return None

    # Most recent first (entries without a parsed date sort last).
    candidates.sort(key=lambda c: c[0] or datetime.datetime.min.timetuple(), reverse=True)
    _, title, summary, link = candidates[0]
    return {"title": title, "summary": summary, "link": link}


def _draft_from_article(article):
    client = Anthropic()  # reads ANTHROPIC_API_KEY from env
    user_prompt = (
        f"Article title: {article['title']}\n"
        f"Article summary: {article['summary']}\n"
        f"Source link: {article['link']}\n\n"
        "Draft the TrendCatcher Facebook post now."
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=BRAND_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return resp.content[0].text.strip()


def build_todays_post():
    """Returns the finished post text (string) for today, or None if
    nothing safe could be produced (caller should skip posting)."""
    today = datetime.datetime.utcnow()
    weekday = today.strftime("%A").lower()  # 'monday', 'tuesday', ...
    week_number = today.isocalendar()[1]

    if weekday == "tuesday":
        return pick(BB_TIPS, week_number)
    if weekday == "sunday":
        return pick(ENGAGEMENT_POSTS, week_number)

    if weekday not in PILLARS:
        # Shouldn't happen (all 7 days are covered), but fail safe.
        return None

    state = _load_state()
    article = _fetch_candidate_entry(weekday, state["posted_links"])
    if article is None:
        # No fresh, unused, on-topic article found today — skip rather
        # than risk a stale/low-quality auto-generated post.
        return None

    post_text = _draft_from_article(article)

    state["posted_links"].append(article["link"])
    _save_state(state)

    return post_text
