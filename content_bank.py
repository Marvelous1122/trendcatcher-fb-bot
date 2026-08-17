"""
Static, pre-written content for days that don't need live news lookup.
These are used as-is (no LLM generation, no hallucination risk) — they
just rotate by ISO week number so they don't repeat back-to-back.
"""

# Tuesday — bug bounty tips (educational, evergreen)
BB_TIPS = [
    "IDOR bugs are some of the least glamorous and most consistently "
    "profitable findings in bug bounty. Quick checklist: test any "
    "numeric/sequential/guessable ID with a second low-privilege "
    "account's session, hit the underlying API directly (not just the "
    "UI), check the mobile app's API traffic separately from the web "
    "app's, and test every HTTP verb, not just GET. None of this "
    "replaces reading the program's scope first.",
    "SSRF hunting tip: look anywhere an app fetches a URL on your "
    "behalf — webhooks, PDF generators, image proxies, \"import from "
    "URL\" features, link unfurlers. Try internal IPs (127.0.0.1, "
    "169.254.169.254 for cloud metadata), alternate encodings of "
    "localhost, and DNS rebinding if the first attempts get filtered.",
    "Before you touch a target: read the program's scope AND its "
    "out-of-scope list twice. The fastest way to burn a relationship "
    "with a program is reporting something explicitly excluded. Scope "
    "discipline is part of the skill, not just the technical hunt.",
    "Recon checklist worth automating: subdomain enumeration, "
    "historical endpoints via archive.org/Wayback, JS file diffing for "
    "exposed endpoints/keys, and GitHub dorking for the target's org. "
    "Most high-value bugs live in forgotten corners, not the main app.",
    "Authorization bugs (broken access control) consistently outrank "
    "XSS in bounty payouts because they're direct data/account "
    "exposure. When testing any feature, always ask: what happens if I "
    "do this as a different user, a lower-privilege role, or logged "
    "out entirely?",
]

# Sunday — engagement / community posts (no external facts needed)
ENGAGEMENT_POSTS = [
    "What's the security story you think more people should be paying "
    "attention to right now? Drop it below.",
    "Genuinely curious — what got you into security or bug bounty in "
    "the first place? Tell us in the comments.",
    "If you could make one change to how bug bounty programs operate "
    "today, what would it be?",
    "What's a security tool or technique you think is underrated and "
    "more people should be using?",
    "AI is reshaping both offense and defense in security right now. "
    "Which side do you think it's helping more, right now, today?",
]


def pick(items, week_number):
    """Deterministically rotate through a list by ISO week number."""
    return items[week_number % len(items)]
