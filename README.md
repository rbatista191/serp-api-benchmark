# SERP API and LLM Scraping API Benchmark

A daily benchmark of SERP APIs and LLM scraping APIs: the success rate and response time of [cloro](https://cloro.dev/), Bright Data, Oxylabs, DataForSEO, SerpApi and SearchApi on the same prompts, over the last 30 days. It covers ChatGPT, Gemini, Google AI Mode, Bing AI Mode and Google Search. Bing AI Mode and SearchApi joined in November 2026, so their cells fill in once a pair has 1,000 attempts in the window. The tables refresh every day from [`data/benchmark.json`](data/benchmark.json).

<!-- BEGIN window -->
Window: 2026-10-19 to 2026-11-17 (30 days). Generated 2026-11-18.
<!-- END window -->

## Which API is the most reliable on each engine?

<!-- BEGIN leaders -->
- **ChatGPT:** highest success rate SearchApi (100.0%), fastest SearchApi (18.0 s).
- **Gemini:** highest success rate SearchApi (99.9%), fastest SearchApi (16.0 s).
- **Google AI Mode:** highest success rate cloro (99.8%), fastest SerpApi (6.7 s).
- **Bing AI Mode:** highest success rate cloro (98.0%), fastest SearchApi (25.1 s).
- **Google Search:** highest success rate DataForSEO (99.9%), fastest SerpApi (2.8 s).
<!-- END leaders -->

## What success rate should you expect from an LLM scraping API?

Share of requests that returned a result, on the same full-sentence prompts for every API. A dash means the API was not measured on that engine.

<!-- BEGIN success -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| ChatGPT | 97.3% | 72.1% | 98.9% | 99.8% | – | 100.0% |
| Gemini | 99.8% | 97.8% | 98.7% | 98.2% | – | 99.9% |
| Google AI Mode | 99.8% | 74.4% | 98.2% | 95.2% | 99.8% | 98.2% |
| Bing AI Mode | 98.0% | – | – | – | – | 93.5% |
<!-- END success -->

## How do the APIs compare on latency?

Mean seconds from request to result, over the successful calls. "n/a" means the API succeeded on fewer than 7 days of the window, which is too few for a stable mean.

<!-- BEGIN latency -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| ChatGPT | 50.1 s | 123.0 s | 89.3 s | 27.5 s | – | 18.0 s |
| Gemini | 33.6 s | 72.5 s | 33.8 s | 27.5 s | – | 16.0 s |
| Google AI Mode | 15.4 s | 75.3 s | 29.0 s | 10.3 s | 6.7 s | 7.9 s |
| Bing AI Mode | 34.1 s | – | – | – | – | 25.1 s |
<!-- END latency -->

## What success rate should you expect from a Google scraping API?

Short keywords and a plain request, the same keywords for every API.

<!-- BEGIN search -->
| Google Search | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| Success rate | 99.0% | – | 91.6% | 99.9% | 99.8% | 99.9% |
| Mean latency | 6.8 s | – | 15.7 s | 6.7 s | 2.8 s | 3.9 s |
<!-- END search -->

## Which SERP API returns the most of the Google results page?

Share of full-sentence questions sent to Google Search on which each API returned the block. A failed request counts as not returned.

<!-- BEGIN features -->
| Block | cloro | SerpApi |
|---|---|---|
| Returned a result | 97.9% | 95.9% |
| Organic results | 97.9% | 95.9% |
| People Also Ask | 84.5% | 78.8% |
| AI Overview | 81.1% | 91.9% |
| AI Overview sources | 70.8% | 78.1% |
| AI Overview citation pills | 69.9% | 76.9% |
| Related searches | 69.2% | 50.5% |
| Local results | 8.2% | 9.3% |
| Shopping cards | 5.5% | 5.5% |
| Knowledge graph | 2.7% | 10.6% |

Share of 12,657 cloro and 12,657 SerpApi responses that contain each block.
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
