"""
Real, curated sources across every topic requested, grouped into
categories that rotate throughout the day. Keyword filters narrow a
general feed to a specific angle; dedicated topic feeds/blogs don't need
one. Feed failures are handled gracefully by generate_post.py (a dead
feed is skipped, not fatal), so it's safe to list feeds generously.
"""

CATEGORIES = {
    "cyber_news": {
        "label": "Cybersecurity news",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.bleepingcomputer.com/feed/",
            "https://www.securityweek.com/feed/",
            "https://krebsonsecurity.com/feed/",
            "https://www.darkreading.com/rss.xml",
        ],
        "keywords": None,
    },
    "bug_bounty": {
        "label": "Bug bounty",
        "feeds": [
            "https://infosecwriteups.com/feed",
            "https://portswigger.net/blog/rss",
        ],
        "keywords": None,
    },
    "vulnerabilities": {
        "label": "Vulnerabilities & CVEs",
        "feeds": [
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.bleepingcomputer.com/feed/",
            "https://www.securityweek.com/feed/",
        ],
        "keywords": ["CVE", "vulnerability", "patch", "exploit", "zero-day", "flaw"],
    },
    "scams_phishing": {
        "label": "Scams & phishing",
        "feeds": [
            "https://krebsonsecurity.com/feed/",
            "https://www.malwarebytes.com/blog/feed/index.xml",
            "https://www.bleepingcomputer.com/feed/",
        ],
        "keywords": ["phishing", "scam", "fraud", "social engineering"],
    },
    "data_breaches": {
        "label": "Data breaches & exposure",
        "feeds": [
            "https://www.troyhunt.com/rss/",
            "https://www.bleepingcomputer.com/feed/",
            "https://feeds.feedburner.com/TheHackersNews",
        ],
        "keywords": ["breach", "leaked", "exposed", "data leak", "database"],
    },
    "ai_news": {
        "label": "AI development, competition & performance",
        "feeds": [
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://venturebeat.com/category/ai/feed/",
            "https://www.technologyreview.com/feed/",
        ],
        "keywords": None,
    },
    "youtube": {
        "label": "Video (bug bounty / security YouTubers)",
        "feeds": [
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCCZDt7MuC3Hzs6IH4xODLBw",  # NahamSec
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCQN2DsjnYH60SFBIA6IkNwg",  # STOK
            "https://www.youtube.com/feeds/videos.xml?channel_id=UClcE-kVhqyiHCcjYwcpfj9w",  # LiveOverflow
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCVeW9qkBjo3zosnqUbG7CFw",  # John Hammond
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCPiN9NPjIer8Do9gUFxKv7A",  # InsiderPhD
        ],
        "keywords": None,
    },
}

# Rotation order — one category picked per run, cycling through the list
# so consecutive posts (every 3 hours) don't repeat the same topic.
CATEGORY_ORDER = list(CATEGORIES.keys())
