# SERP API and LLM Scraping API Benchmark

A daily benchmark of SERP APIs and LLM scraping APIs: the success rate and response time of [cloro](https://cloro.dev/), Bright Data, Oxylabs, DataForSEO, SerpApi and SearchApi on the same prompts, over the last 30 days. It covers ChatGPT, Gemini, Google AI Mode, Bing AI Mode and Google Search. Bing AI Mode and SearchApi joined in November 2026, so their cells fill in once a pair has 1,000 attempts in the window. The tables refresh every day from [`data/benchmark.json`](data/benchmark.json).

<!-- BEGIN window -->
Window: 2026-10-14 to 2026-11-12 (30 days). Generated 2026-11-13.
<!-- END window -->

## Which API is the most reliable on each engine?

<!-- BEGIN leaders -->
- **ChatGPT:** highest success rate SearchApi (100.0%), fastest DataForSEO (28.4 s).
- **Gemini:** highest success rate SearchApi (99.9%), fastest DataForSEO (27.0 s).
- **Google AI Mode:** highest success rate SerpApi (99.9%), fastest SerpApi (6.7 s).
- **Bing AI Mode:** highest success rate cloro (98.0%).
- **Google Search:** highest success rate SerpApi (99.9%), fastest SerpApi (3.9 s).
<!-- END leaders -->

## What success rate should you expect from an LLM scraping API?

Share of requests that returned a result, on the same full-sentence prompts for every API. A dash means the API was not measured on that engine.

<!-- BEGIN success -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| ChatGPT | 97.2% | 65.8% | 98.1% | 99.8% | – | 100.0% |
| Gemini | 99.6% | 97.7% | 97.7% | 97.1% | – | 99.9% |
| Google AI Mode | 99.4% | 64.0% | 97.2% | 93.7% | 99.9% | 96.4% |
| Bing AI Mode | 98.0% | – | – | – | – | 92.6% |
<!-- END success -->

## How do the APIs compare on latency?

Mean seconds from request to result, over the successful calls. "n/a" means the API succeeded on fewer than 7 days of the window, which is too few for a stable mean.

<!-- BEGIN latency -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| ChatGPT | 50.1 s | 133.6 s | 84.0 s | 28.4 s | – | n/a (5 days) |
| Gemini | 35.1 s | 71.5 s | 38.0 s | 27.0 s | – | n/a (5 days) |
| Google AI Mode | 15.8 s | 76.1 s | 28.5 s | 9.9 s | 6.7 s | n/a (5 days) |
| Bing AI Mode | n/a (5 days) | – | – | – | – | n/a (5 days) |
<!-- END latency -->

## What success rate should you expect from a Google scraping API?

Short keywords and a plain request, the same keywords for every API.

<!-- BEGIN search -->
| Google Search | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| Success rate | 99.3% | – | 91.2% | 99.8% | 99.9% | 99.8% |
| Mean latency | 6.7 s | – | 10.0 s | 6.3 s | 3.9 s | n/a (5 days) |
<!-- END search -->

## Which SERP API returns the most of the Google results page?

Share of full-sentence questions sent to Google Search on which each API returned the block. A failed request counts as not returned.

<!-- BEGIN features -->
| Block | cloro | SerpApi |
|---|---|---|
| Returned a result | 97.8% | 96.0% |
| Organic results | 97.8% | 96.0% |
| People Also Ask | 85.1% | 79.8% |
| AI Overview | 80.5% | 91.1% |
| AI Overview sources | 71.3% | 78.2% |
| AI Overview citation pills | 70.5% | 74.1% |
| Related searches | 71.9% | 56.1% |
| Local results | 8.2% | 9.3% |
| Shopping cards | 5.8% | 5.4% |
| Knowledge graph | 2.6% | 10.8% |

Share of 12,686 cloro and 12,686 SerpApi responses that contain each block.
<!-- END features -->

## How the benchmark works

1. **The same prompts go to every API.** About 420 full-sentence prompts a day go to each AI engine, and 100 short keywords a day go to Google Search. Each API gets the same prompt or keyword.
2. **A result counts only if it comes back.** A failed request counts as not returned.
3. **Latency is a stopwatch on one request.** It runs from the request to the parsed result. Oxylabs returns an AI answer through a job that is polled every 3 seconds, so its AI-engine latency includes up to one poll interval.
4. **The window is the last 30 days.** A pair with fewer than 1,000 attempts in the window, or 50 on Google Search, is left out.
5. **Some pairs are not measured.** A dash in a table means the pair is not in the benchmark. Pairs whose failures come from a plan's rate limit, and not from the API, are left out, because they measure the account.

## FAQ

### Which LLM scraping API is the most reliable for ChatGPT?

See the ChatGPT row in the success-rate table. It is the share of the same ChatGPT prompts that each API returned over the last 30 days.

### Is Oxylabs or Bright Data more reliable for scraping AI answers?

Compare their columns engine by engine. Both get the same prompts, so the difference is the API, not the prompt mix.

### How often is the data updated?

Every day. `data/benchmark.json` is replaced once a day, and a GitHub Action rewrites the tables in this README from it.

### Can I use the data?

Yes. The data and the script are MIT licensed. [`scripts/render.py`](scripts/render.py) builds every table in this README from the JSON file, so you can check each number.

## Data format

`data/benchmark.json` holds:

- `days`: the dates in the window, oldest first.
- `pairs`: one row per API and engine, with `attempts`, `successRatePct` and `latencyS`, cloro's figures on the same prompts (`cloroAttempts`, `cloroSuccessRatePct`, `cloroLatencyS`), and a `daily` series.
- `serpFeatures`: the share of Google Search responses that contain each block, for cloro and SerpApi.
