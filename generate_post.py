"""
Builds the next post's content: either a static bank item (roughly 1 in
every 6 runs) or a live item drafted from a real, freshly-fetched RSS/
YouTube entry, rotating through every requested topic category.

Design goal: minimize hallucination risk since nothing is human-reviewed
before publishing.
  - A rotating share of runs use 100% pre-written content, no LLM call.
  - News/video runs pass the LLM the actual title + summary + link and
    instruct it to use ONLY those facts, never invent numbers or names.
  - If no suitable fresh item is found, skip rather than risk a bad post.
  - If the model still produces meta-commentary instead of real content,
    a plain-text fallback template is used instead of publishing it.
"""

import datetime
import json
import os

import feedparser
from google import genai
from google.genai import types

from content_bank import BB_TIPS, ENGAGEMENT_POSTS, pick
from rss_sources import CATEGORIES, CATEGORY_ORDER

STATE_FILE = "posted_log.json"
MAX_LOG_ENTRIES = 500
MODEL = "gemini-3.5-flash"
BANK_EVERY_N_RUNS = 6  # roughly 1 in 6 posts is a static tip/engagement post

BRAND_SYSTEM_PROMPT = """You draft short Facebook posts for TrendCatcher, a \
cybersecurity/bug-bounty/AI-security news brand page (no personal name, no \
"I/my" voice - use a neutral brand voice, e.g. "TrendCatcher tracks..." or \
just state facts directly).

Some items you're given are articles, some are YouTube videos - either way,
treat the provided title/summary as the only source of truth.

Rules, no exceptions:
- Use ONLY the facts given to you in the title/summary below. Do not invent \
CVE numbers, statistics, company names, or details not present in the \
provided text.
- If the provided summary is thin, write a shorter post (as few as 2-3 \
sentences) rather than padding it with invented specifics. A short post is \
fine. Do NOT write about the fact that the summary is thin, do not mention \
"constraints," "instructions," or your own writing process anywhere.
- If this is a YouTube video, frame it as a video worth watching (e.g. "New \
from [creator]:") rather than as breaking news.
- End with the source/video link on its own line.
- No hashtags (Facebook doesn't reward them like Instagram does).
- Confident and practical tone, no hype, no fear-mongering.
- Your entire response must be ONLY the finished post text a reader would \
see, starting directly with the hook sentence. No preamble, no labels, no \
meta-commentary, no quotation marks around the whole thing.
"""


def _load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"posted_links": [], "run_index": 0}


def _save_state(state):
    state["posted_links"] = state["posted_links"][-MAX_LOG_ENTRIES:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def _fetch_candidate_entry(category_key, posted_links):
    category = CATEGORIES[category_key]
    keywords = category["keywords"]
    candidates = []

    for feed_url in category["feeds"]:
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

    candidates.sort(key=lambda c: c[0] or datetime.datetime.min.timetuple(), reverse=True)
    _, title, summary, link = candidates[0]
    return {"title": title, "summary": summary, "link": link}


_SUSPECT_PHRASES = (
    "constraint", "instruction", "as an ai", "i will", "let's expand",
    "the summary is", "system prompt", "my response", "i cannot", "i can't",
)


def _looks_degenerate(text: str) -> bool:
    """Catches cases where the model leaks meta-commentary instead of a
    real post, so we can fall back to a safe plain-text template."""
    if not text or len(text) < 30:
        return True
    lowered = text.lower()
    return any(phrase in lowered for phrase in _SUSPECT_PHRASES)


def _template_from_article(article):
    """Zero-AI fallback: just the item's own facts, no rewriting."""
    return f"{article['title']}\n\n{article['summary']}\n\n{article['link']}"


def _draft_from_article(article):
    client = genai.Client()  # reads GEMINI_API_KEY (or GOOGLE_API_KEY) from env
    user_prompt = (
        f"Title: {article['title']}\n"
        f"Summary: {article['summary']}\n"
        f"Link: {article['link']}\n\n"
        "Draft the TrendCatcher Facebook post now."
    )
    resp = client.models.generate_content(
        model=MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=BRAND_SYSTEM_PROMPT,
            max_output_tokens=600,
        ),
    )
    text = (resp.text or "").strip()

    if _looks_degenerate(text):
        return _template_from_article(article)

    return text


def build_next_post():
    """Returns the finished post text (string) for this run, or None if
    nothing safe could be produced (caller should skip posting)."""
    state = _load_state()
    run_index = state.get("run_index", 0)

    # Roughly 1 in every BANK_EVERY_N_RUNS posts is a static, zero-AI item
    # for variety and to keep overall hallucination risk low.
    if run_index % BANK_EVERY_N_RUNS == BANK_EVERY_N_RUNS - 1:
        bank = BB_TIPS if (run_index // BANK_EVERY_N_RUNS) % 2 == 0 else ENGAGEMENT_POSTS
        post = pick(bank, run_index)
        state["run_index"] = run_index + 1
        _save_state(state)
        return post

    category_key = CATEGORY_ORDER[run_index % len(CATEGORY_ORDER)]
    article = _fetch_candidate_entry(category_key, state["posted_links"])

    state["run_index"] = run_index + 1

    if article is None:
        # No fresh, unused item found in this category this run — skip
        # rather than risk a stale/low-quality auto-generated post.
        _save_state(state)
        return None

    post_text = _draft_from_article(article)
    state["posted_links"].append(article["link"])
    _save_state(state)

    return post_text
