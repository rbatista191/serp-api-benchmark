# SERP API and LLM Scraping API Benchmark

A daily benchmark of SERP APIs and LLM scraping APIs: the success rate and response time of [cloro](https://cloro.dev/), Bright Data, Oxylabs, DataForSEO and SerpApi on the same prompts, over the last 30 days. It covers ChatGPT, Gemini, Google AI Mode, Microsoft Copilot, Perplexity and Google Search. The tables refresh every day from [`data/benchmark.json`](data/benchmark.json).

<!-- BEGIN window -->
Window: 2026-10-04 to 2026-11-02 (30 days). Generated 2026-11-03.
<!-- END window -->

## Which API is the most reliable on each engine?

<!-- BEGIN leaders -->
- **ChatGPT:** highest success rate DataForSEO (97.5%), fastest DataForSEO (28.7 s).
- **Gemini:** highest success rate cloro (99.5%), fastest DataForSEO (26.4 s).
- **Google AI Mode:** highest success rate SerpApi (100.0%), fastest SerpApi (6.6 s).
- **Microsoft Copilot:** highest success rate cloro (99.8%).
- **Perplexity:** highest success rate Oxylabs (18.9%), fastest Oxylabs (77.8 s). Every API failed most requests in this window.
- **Google Search:** highest success rate SerpApi (99.9%), fastest SerpApi (4.5 s).
<!-- END leaders -->

## What success rate should you expect from an LLM scraping API?

Share of requests that returned a result, on the same full-sentence prompts for every API. A dash means the API was not measured on that engine.

<!-- BEGIN success -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi |
|---|---|---|---|---|---|
| ChatGPT | 96.6% | 52.9% | 96.7% | 97.5% | – |
| Gemini | 99.5% | 97.1% | 97.3% | 95.8% | – |
| Google AI Mode | 98.8% | 50.1% | 96.7% | 90.5% | 100.0% |
| Microsoft Copilot | 99.8% | 4.8% | – | – | – |
| Perplexity | 6.3% | 1.3% | 18.9% | – | – |
<!-- END success -->

## How do the APIs compare on latency?

Mean seconds from request to result, over the successful calls. "n/a" means the API succeeded on fewer than 7 days of the window, which is too few for a stable mean.

<!-- BEGIN latency -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi |
|---|---|---|---|---|---|
| ChatGPT | 53.3 s | 124.0 s | 71.9 s | 28.7 s | – |
| Gemini | 42.4 s | 64.5 s | 44.9 s | 26.4 s | – |
| Google AI Mode | 17.6 s | 84.7 s | 28.5 s | 11.1 s | 6.6 s |
| Microsoft Copilot | 50.7 s | n/a (3 days) | – | – | – |
| Perplexity | 160.4 s | 249.5 s | 77.8 s | – | – |
<!-- END latency -->

## What success rate should you expect from a Google scraping API?

Short keywords and a plain request, the same keywords for every API.

<!-- BEGIN search -->
| Google Search | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi |
|---|---|---|---|---|---|
| Success rate | 99.2% | – | 94.4% | 99.3% | 99.9% |
| Mean latency | 7.3 s | – | 6.2 s | 6.4 s | 4.5 s |
<!-- END search -->

## Which SERP API returns the most of the Google results page?

Share of full-sentence questions sent to Google Search on which each API returned the block. A failed request counts as not returned.

<!-- BEGIN features -->
| Block | cloro | SerpApi |
|---|---|---|
| Returned a result | 97.5% | 93.8% |
| Organic results | 97.3% | 93.8% |
| People Also Ask | 85.3% | 80.0% |
| AI Overview | 79.4% | 87.7% |
| AI Overview sources | 69.9% | 75.0% |
| AI Overview citation pills | 69.1% | 70.2% |
| Related searches | 63.2% | 55.7% |
| Local results | 8.5% | 8.7% |
| Shopping cards | 5.4% | 5.3% |
| Knowledge graph | 2.6% | 10.7% |

Share of 12,698 cloro and 12,695 SerpApi responses that contain each block.
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
