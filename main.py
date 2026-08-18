"""Entry point run daily by the GitHub Actions workflow."""

import sys

from generate_post import build_next_post
from publish_fb import post_text


def main():
    post = build_next_post()

    if not post:
        print("No suitable content found for today — skipping post (safe fallback).")
        return 0

    print("Publishing post:\n" + "-" * 40)
    print(post)
    print("-" * 40)

    result = post_text(post)
    print("Published. Facebook response:", result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
