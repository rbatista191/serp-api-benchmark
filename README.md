# SERP API and LLM Scraping API Benchmark

A daily benchmark of SERP APIs and LLM scraping APIs: the success rate and response time of [cloro](https://cloro.dev/), Bright Data, Oxylabs, DataForSEO, SerpApi and SearchApi on the same prompts, over the last 30 days. It covers ChatGPT, Gemini, Google AI Mode, Bing AI Mode and Google Search. Bing AI Mode and SearchApi joined in November 2026, so their cells fill in once a pair has 1,000 attempts in the window. The tables refresh every day from [`data/benchmark.json`](data/benchmark.json).

<!-- BEGIN window -->
Window: 2026-10-27 to 2026-11-25 (30 days). Generated 2026-11-26.
<!-- END window -->

## Which API is the most reliable on each engine?

<!-- BEGIN leaders -->
- **ChatGPT:** highest success rate SearchApi (100.0%), fastest SearchApi (17.9 s).
- **Gemini:** highest success rate cloro (99.5%), fastest SearchApi (15.0 s).
- **Google AI Mode:** highest success rate cloro (99.8%), fastest SerpApi (6.8 s).
- **Bing AI Mode:** highest success rate cloro (98.6%), fastest SearchApi (23.9 s).
- **Google Search:** highest success rate DataForSEO (99.9%), fastest SerpApi (2.7 s).
<!-- END leaders -->

## What success rate should you expect from an LLM scraping API?

Share of requests that returned a result, on the same full-sentence prompts for every API. A dash means the API was not measured on that engine.

<!-- BEGIN success -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| ChatGPT | 99.4% | 77.7% | 99.0% | 99.8% | – | 100.0% |
| Gemini | 99.5% | 96.4% | 99.3% | 98.3% | – | 99.4% |
| Google AI Mode | 99.8% | 83.7% | 98.6% | 97.2% | 99.6% | 99.0% |
| Bing AI Mode | 98.6% | – | – | – | – | 95.3% |
<!-- END success -->

## How do the APIs compare on latency?

Mean seconds from request to result, over the successful calls. "n/a" means the API succeeded on fewer than 7 days of the window, which is too few for a stable mean.

<!-- BEGIN latency -->
| Engine | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| ChatGPT | 48.0 s | 111.8 s | 97.0 s | 26.1 s | – | 17.9 s |
| Gemini | 37.4 s | 80.6 s | 32.0 s | 26.8 s | – | 15.0 s |
| Google AI Mode | 14.9 s | 80.3 s | 28.7 s | 10.8 s | 6.8 s | 7.9 s |
| Bing AI Mode | 33.1 s | – | – | – | – | 23.9 s |
<!-- END latency -->

## What success rate should you expect from a Google scraping API?

Short keywords and a plain request, the same keywords for every API.

<!-- BEGIN search -->
| Google Search | cloro | Bright Data | Oxylabs | DataForSEO | SerpApi | SearchApi |
|---|---|---|---|---|---|---|
| Success rate | 99.1% | – | 91.3% | 99.9% | 99.8% | 99.9% |
| Mean latency | 6.4 s | – | 28.1 s | 7.0 s | 2.7 s | 3.9 s |
<!-- END search -->

## Which SERP API returns the most of the Google results page?

Share of full-sentence questions sent to Google Search on which each API returned the block. A failed request counts as not returned.

<!-- BEGIN features -->
| Block | cloro | SerpApi |
|---|---|---|
| Returned a result | 97.6% | 94.2% |
| Organic results | 97.6% | 94.2% |
| People Also Ask | 83.3% | 77.3% |
| AI Overview | 82.4% | 91.1% |
| AI Overview sources | 70.6% | 77.0% |
| AI Overview citation pills | 69.8% | 76.5% |
| Related searches | 63.7% | 47.2% |
| Local results | 8.3% | 9.5% |
| Shopping cards | 5.1% | 5.2% |
| Knowledge graph | 2.2% | 10.0% |

Share of 12,666 cloro and 12,666 SerpApi responses that contain each block.
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
