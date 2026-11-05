# SERP API and LLM Scraping API Benchmark

A daily benchmark of SERP APIs and LLM scraping APIs: the success rate and response time of [cloro](https://cloro.dev/), Bright Data, Oxylabs, DataForSEO and SerpApi on the same prompts, over the last 30 days. It covers ChatGPT, Gemini, Google AI Mode, Microsoft Copilot, Perplexity and Google Search. The tables refresh every day from [`data/benchmark.json`](data/benchmark.json).

<!-- BEGIN window -->
Window: 2026-10-06 to 2026-11-04 (30 days). Generated 2026-11-05.
<!-- END window -->

## Which API is the most reliable on each engine?

<!-- BEGIN leaders -->
- **ChatGPT:** highest success rate DataForSEO (97.4%), fastest DataForSEO (29.0 s).
- **Gemini:** highest success rate cloro (99.6%), fastest DataForSEO (26.8 s).
- **Google AI Mode:** highest success rate SerpApi (100.0%), fastest SerpApi (6.6 s).
- **Microsoft Copilot:** highest success rate cloro (94.9%).
- **Perplexity:** highest success rate Oxylabs (12.9%), fastest Oxylabs (83.0 s). Every API failed most requests in this window.
- **Google Search:** highest success rate SerpApi (99.9%), fastest SerpApi (4.4 s).
<!-- END leaders -->

## What success rate should you expect from an LLM scraping API?

Share of requests that returned a result, on the same full-sentence prompts for every API. A dash means the API was not measured on that engine.

<!-- BEGIN success -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi |
|---|---|---|---|---|---|
| ChatGPT | 96.9% | 51.8% | 96.8% | 97.4% | – |
| Gemini | 99.6% | 97.2% | 97.3% | 95.6% | – |
| Google AI Mode | 98.9% | 50.5% | 96.8% | 90.4% | 100.0% |
| Microsoft Copilot | 94.9% | 0.3% | – | – | – |
| Perplexity | 3.0% | 1.2% | 12.9% | – | – |
<!-- END success -->

## How do the APIs compare on latency?

Mean seconds from request to result, over the successful calls. "n/a" means the API succeeded on fewer than 7 days of the window, which is too few for a stable mean.

<!-- BEGIN latency -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi |
|---|---|---|---|---|---|
| ChatGPT | 53.7 s | 130.6 s | 74.3 s | 29.0 s | – |
| Gemini | 41.8 s | 66.6 s | 43.1 s | 26.8 s | – |
| Google AI Mode | 17.5 s | 84.8 s | 28.6 s | 10.7 s | 6.6 s |
| Microsoft Copilot | 50.4 s | n/a (1 days) | – | – | – |
| Perplexity | 156.6 s | 245.8 s | 83.0 s | – | – |
<!-- END latency -->

## What success rate should you expect from a Google scraping API?

Short keywords and a plain request, the same keywords for every API.

<!-- BEGIN search -->
| Google Search | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi |
|---|---|---|---|---|---|
| Success rate | 99.3% | – | 94.7% | 99.4% | 99.9% |
| Mean latency | 7.2 s | – | 6.2 s | 6.5 s | 4.4 s |
<!-- END search -->

## Which SERP API returns the most of the Google results page?

Share of full-sentence questions sent to Google Search on which each API returned the block. A failed request counts as not returned.

<!-- BEGIN features -->
| Block | cloro | SerpApi |
|---|---|---|
| Returned a result | 97.6% | 94.0% |
| Organic results | 97.5% | 93.9% |
| People Also Ask | 85.4% | 79.7% |
| AI Overview | 80.0% | 88.2% |
| AI Overview sources | 71.0% | 75.4% |
| AI Overview citation pills | 70.2% | 70.6% |
| Related searches | 65.5% | 56.0% |
| Local results | 8.4% | 8.7% |
| Shopping cards | 5.5% | 5.4% |
| Knowledge graph | 2.7% | 10.7% |

Share of 12,686 cloro and 12,683 SerpApi responses that contain each block.
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
