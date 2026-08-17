# TrendCatcher Auto-Poster — Setup

Fully automated: every day this pulls a real, current article from cybersecurity
RSS feeds (Mon/Wed/Thu/Fri/Sat), drafts a fact-grounded post from it, and
publishes straight to the TrendCatcher Facebook Page. Tuesday and Sunday use
pre-written content (bug bounty tips / engagement prompts) with no live
generation at all — zero moving parts, zero hallucination risk on those two
days. No manual step, ever, once this is running.

**Read this first — the honest tradeoff:** nothing reviews these posts before
they go live. The prompt is written to only use facts from the fetched
article and to skip posting rather than guess when nothing solid is found,
but an LLM can still misread a source occasionally. If a post is ever wrong,
you can delete it from the Page afterward — but it will already be live for
some period of time. Worth spot-checking the first couple of weeks.

## 1. Create the GitHub repo

1. Go to [github.com/new](https://github.com/new). Name it whatever you like
   (e.g. `trendcatcher-fb-bot`). **Private** is recommended — no reason for
   this to be public.
2. Upload all the files in this folder to the repo, keeping the folder
   structure intact — the `.github/workflows/daily-post.yml` file **must**
   stay at that exact path for GitHub to recognize it as a workflow. Easiest
   way: on the repo page, click "Add file" → "Upload files," drag in
   everything (including the `.github` folder — GitHub preserves the path).

## 2. Add your secrets

Repo → **Settings** → **Secrets and variables** → **Actions** → **New
repository secret**. Add three:

| Name | Value |
|---|---|
| `FB_PAGE_ID` | Your TrendCatcher InfoSec Page ID |
| `FB_PAGE_ACCESS_TOKEN` | The long-lived Page Access Token you generated earlier |
| `ANTHROPIC_API_KEY` | An API key from [console.anthropic.com](https://console.anthropic.com) |

**On the Anthropic key:** this is separate from your regular Claude app —
it's a pay-as-you-go API key from the Anthropic Console, which needs its own
billing set up. Cost here is tiny (a handful of short posts a day, cents per
month at most), but it is a real, separate account and a real, if small, cost.

## 3. Allow the workflow to push back to the repo

Repo → **Settings** → **Actions** → **General** → scroll to **Workflow
permissions** → select **"Read and write permissions"** → Save. (This is
what lets the bot remember which articles it's already posted, so it doesn't
repeat itself.)

## 4. Test it manually before trusting the schedule

Repo → **Actions** tab → select **"Daily TrendCatcher post"** on the left →
**"Run workflow"** button → Run. Watch the log — it'll show you exactly what
it drafted and whether the Facebook post succeeded. Check the actual Page to
confirm the post landed and reads the way you want.

## 5. Let it run

Once a manual test works, the schedule (`cron: "30 3 * * *"`, 8:30 AM
Asia/Karachi daily) takes over — no further action needed. You can watch
past runs anytime in the **Actions** tab.

## Turning it off / pausing

- **Pause without deleting anything:** Actions tab → "Daily TrendCatcher
  post" → "..." menu → Disable workflow.
- **Kill it completely:** revoke the Page Access Token from Facebook
  Settings → Business Integrations, or just delete the repo.
