"""
RSS feed sources per content pillar, with optional keyword filters to
narrow results (e.g. only AI-related stories on AI-focused days).
Multiple feeds per pillar give fallback options if one is empty/down.
"""

PILLARS = {
    "monday": {
        "label": "Cybersecurity news",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.bleepingcomputer.com/feed/",
        ],
        "keywords": None,  # no filter — general cyber news
    },
    "wednesday": {
        "label": "AI security",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.bleepingcomputer.com/feed/",
        ],
        "keywords": ["AI", "LLM", "GPT", "artificial intelligence", "machine learning"],
    },
    "thursday": {
        "label": "Bug bounty / industry news",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.securityweek.com/feed/",
        ],
        "keywords": ["bug bounty", "vulnerability", "disclosure", "CVE"],
    },
    "friday": {
        "label": "Cyber + AI crossover news",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.bleepingcomputer.com/feed/",
        ],
        "keywords": ["AI", "LLM", "copilot", "code editor", "developer tool"],
    },
    "saturday": {
        "label": "AI progress (security angle)",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.securityweek.com/feed/",
        ],
        "keywords": ["AI", "LLM", "model", "agent"],
    },
}

# Days handled by content_bank.py instead of live RSS + LLM generation:
# tuesday -> BB_TIPS, sunday -> ENGAGEMENT_POSTS
