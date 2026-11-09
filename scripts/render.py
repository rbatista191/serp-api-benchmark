"""Rewrite the generated sections of README.md from data/benchmark.json.

Each section sits between <!-- BEGIN name --> and <!-- END name --> markers.
Text outside the markers is not changed. Run: python3 scripts/render.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "benchmark.json"
README = ROOT / "README.md"

PROVIDERS = [
    ("cloro", "cloro"),
    ("brightdata", "Bright Data"),
    ("oxylabs", "Oxylabs"),
    ("dataforseo", "DataForSEO"),
    ("serpapi", "SerpApi"),
    ("searchapi", "SearchApi"),
]
AI_ENGINES = [
    ("CHATGPT", "ChatGPT"),
    ("GEMINI", "Gemini"),
    ("AIMODE", "Google AI Mode"),
    ("BING_AIMODE", "Bing AI Mode"),
]
# COPILOT and PERPLEXITY are not listed: cloro stopped serving both engines on
# 2026-11-05, and the data stops carrying them from 2026-11-10.
SEARCH = ("GOOGLE_KEYWORD", "Google Search")
FEATURES = [
    ("success_rate", "Returned a result"),
    ("has_organic_results", "Organic results"),
    ("has_people_also_ask", "People Also Ask"),
    ("has_aioverview", "AI Overview"),
    ("has_aioverview_sources", "AI Overview sources"),
    ("has_citation_pills", "AI Overview citation pills"),
    ("has_related_searches", "Related searches"),
    ("has_local_results", "Local results"),
    ("has_shopping_cards", "Shopping cards"),
    ("has_knowledge_graph", "Knowledge graph"),
]
# A mean latency from fewer days than this is not printed.
MIN_LATENCY_DAYS = 7


def cells(feed, engine):
    """Success rate and latency per provider on one engine, or None.

    Every pair carries cloro's figures on the same prompts. A provider that
    joined later has a shorter window, so cloro's cell comes from the pair
    with the most cloro attempts.
    """
    out = {}
    for p in feed["pairs"]:
        if p["engine"] != engine:
            continue
        days = sum(1 for d in p["daily"] if d and d.get("latencyS") is not None)
        cloro_days = sum(
            1 for d in p["daily"] if d and d.get("cloroLatencyS") is not None
        )
        out[p["provider"]] = (p["successRatePct"], p["latencyS"], days, p["attempts"])
        if "cloro" not in out or p["cloroAttempts"] > out["cloro"][3]:
            out["cloro"] = (
                p["cloroSuccessRatePct"],
                p["cloroLatencyS"],
                cloro_days,
                p["cloroAttempts"],
            )
    return out


def pct(cell):
    return "–" if cell is None else f"{cell[0]:.1f}%"


def secs(cell):
    if cell is None or cell[1] is None:
        return "–"
    if cell[2] < MIN_LATENCY_DAYS:
        return f"n/a ({cell[2]} days)"
    return f"{cell[1]:.1f} s"


def table(feed, engines, fmt):
    head = "| Engine | " + " | ".join(name for _, name in PROVIDERS) + " |"
    rule = "|---|" + "---|" * len(PROVIDERS)
    rows = [head, rule]
    for key, label in engines:
        c = cells(feed, key)
        rows.append(
            f"| {label} | " + " | ".join(fmt(c.get(p)) for p, _ in PROVIDERS) + " |"
        )
    return "\n".join(rows)


def search(feed):
    c = cells(feed, SEARCH[0])
    head = "| Google Search | " + " | ".join(name for _, name in PROVIDERS) + " |"
    rule = "|---|" + "---|" * len(PROVIDERS)
    return "\n".join(
        [
            head,
            rule,
            "| Success rate | " + " | ".join(pct(c.get(p)) for p, _ in PROVIDERS) + " |",
            "| Mean latency | " + " | ".join(secs(c.get(p)) for p, _ in PROVIDERS) + " |",
        ]
    )


def leaders(feed):
    lines = []
    for key, label in AI_ENGINES + [SEARCH]:
        c = cells(feed, key)
        if not c:
            continue
        name = dict(PROVIDERS)
        best = max(c, key=lambda p: c[p][0])
        timed = {p: v for p, v in c.items() if v[1] is not None and v[2] >= MIN_LATENCY_DAYS}
        line = f"- **{label}:** highest success rate {name.get(best, best)} ({c[best][0]:.1f}%)"
        if len(timed) > 1:
            fast = min(timed, key=lambda p: timed[p][1])
            line += f", fastest {name.get(fast, fast)} ({timed[fast][1]:.1f} s)"
        if all(v[0] < 50 for v in c.values()):
            line += ". Every API failed most requests in this window"
        lines.append(line + ".")
    return "\n".join(lines)


def features(feed):
    rows = {(f["metric"], f["provider"]): f for f in feed["serpFeatures"]}
    n = {p: f["n"] for (m, p), f in rows.items() if m == "success_rate"}
    out = [
        f"| Block | cloro | SerpApi |",
        "|---|---|---|",
    ]
    for metric, label in FEATURES:
        a, b = rows.get((metric, "cloro")), rows.get((metric, "serpapi"))
        if not a or not b:
            continue
        out.append(f"| {label} | {a['pct']:.1f}% | {b['pct']:.1f}% |")
    out.append("")
    out.append(
        f"Share of {n.get('cloro', 0):,} cloro and {n.get('serpapi', 0):,} SerpApi "
        "responses that contain each block."
    )
    return "\n".join(out)


def window(feed):
    days = feed["days"]
    return (
        f"Window: {days[0]} to {days[-1]} ({len(days)} days). "
        f"Generated {feed['generatedAt'][:10]}."
    )


def replace(text, name, body):
    pattern = re.compile(
        rf"(<!-- BEGIN {name} -->\n).*?(<!-- END {name} -->)", re.S
    )
    if not pattern.search(text):
        raise SystemExit(f"README.md has no {name} markers")
    return pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)


def main():
    feed = json.loads(DATA.read_text())
    text = README.read_text()
    text = replace(text, "window", window(feed))
    text = replace(text, "leaders", leaders(feed))
    text = replace(text, "success", table(feed, AI_ENGINES, pct))
    text = replace(text, "latency", table(feed, AI_ENGINES, secs))
    text = replace(text, "search", search(feed))
    text = replace(text, "features", features(feed))
    README.write_text(text)


if __name__ == "__main__":
    main()
