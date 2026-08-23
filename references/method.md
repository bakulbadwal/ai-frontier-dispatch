# Dispatch method

Use this reference for candidate gathering, scoring, source discipline, and final synthesis.

## 1. Establish the window

1. Read the latest completed run from the state ledger when enabled.
2. Otherwise read the most recent `digests/YYYY-MM-DD.md` filename.
3. Use the configured cadence only when neither exists.
4. Date-check every candidate against the resulting window.

## 2. Gather independent streams

Gather these streams independently before ranking:

- Official model-lab, product, and company announcements.
- AI-native builder and researcher activity.
- Hacker News front page, `/show`, and recent high-signal results.
- Personalized GitHub and Hugging Face releases/trending candidates.
- Model routers, coding-harness usage leaderboards, and independent benchmarks.
- Reputable AI funding, partnership, policy, and regulation coverage.
- Consulting, macro, capital-markets, M&A/VC, career, and established-stack sources.
- Optional live-X pass through Grok.

### Hacker News

A single query has poor recall. Fan out across `AI`, `LLM`, `agents`, major lab names, and one rotating reader-domain term, then merge, deduplicate by canonical URL, sort by points, and inspect only the strongest candidates.

The Algolia endpoint takes a date floor and a points floor directly:

```
https://hn.algolia.com/api/v1/search_by_date?tags=story&query=<term>&numericFilters=created_at_i><unix-ts>,points><threshold>
```

Compute `<unix-ts>` from the window start rather than hardcoding it, and pair the per-term queries with `?tags=front_page` for what is live right now. Raise the points threshold for busy windows and lower it for quiet ones; a threshold that returns nothing is a signal about the threshold, not about the window.

### GitHub and Hugging Face

Treat stars, likes, downloads, and trending placement as discovery signals—not proof of quality. These are the most gameable numbers in the ecosystem and they are actively gamed. Prefer release notes, documentation, commits, issue threads, model cards, and direct project evidence.

**Prefer sustained engagement over novelty spikes.** Verify candidates through the API rather than the rendered page, and check `stargazers_count` against `open_issues_count`, `created_at`, and `pushed_at` together. The star-farming signature is consistent:

- A vertical star curve against near-zero open issues. Real adoption generates questions; stars without issues means nobody is using it.
- Commits clustered into a single day or a few minutes, then no pushes while stars keep accruing.
- A high star count on a repo whose last push is weeks old — trending in search, dead in practice.

Report what was excluded and why rather than dropping it silently, and note when a filter could not be applied at all: a repository with issues disabled cannot be scored on engagement, which is a caveat rather than a pass.

For model hubs, report new frontier-scale open releases, large movers against the previous run's baseline, and entries that tell a story — a community distill or quantization of a frontier model, a lab's weights landing after an API-only launch, a licensing change. Carry `createdAt` so a stale-but-charting model is not written up as new. Watch the **download-to-like ratio**: an extreme skew toward downloads indicates automated or pipeline pulling rather than community interest, and the two mean different things. Skip perennial small-model and OCR filler unless it signals a trend.

### The distribution layer: catching unannounced releases

Most streams above are announcement-shaped—newsrooms, front pages, press, social. A growing share of consequential model releases have **no announcement at all**. They appear on a router under a codename, often free, and are discovered through usage rather than publicity. A sweep built only on announcements is structurally blind to them, and will report a quiet week while a frontier-class model is being used at scale.

Sweep each run and report only what changed:

- **Router new-and-trending listings.** The newest-models list is where stealth or cloaked models surface first. Router rankings by **token share** show what people actually route production work to—a materially better signal than stars, likes, or benchmark claims.
- **Coding-harness usage leaderboards.** Public usage and stats pages for agent harnesses and routers show what builders actually run, in numbers rather than sentiment.
- **Independent benchmark aggregators.** Their primary job is as the antidote to vendor self-claims. When a lab asserts a leaderboard position, verify it independently before repeating it; if it is not independently confirmed, label it self-reported and uncorroborated.
- **Human-preference arenas.** Slow-moving. Report only a genuine leadership change, not routine churn.
- **Agentic-coding benchmarks.** Report real state-of-the-art changes; ignore ordinary movement.

Discipline for this stream: it is a **discovery channel, not an authority**. Token share and leaderboard placement tell you what is being used and what scores well. Neither is evidence that a model is good, safe, or of known provenance. When surfacing an unclaimed or codenamed model, state plainly that its origin is unverified, and note the fingerprinting theories rather than asserting one. **Free frontier inference is generally paid for in training data**—whenever a zero-cost model is surfaced, make the data-retention implication explicit alongside the capability, so a reader does not route sensitive work to it on the strength of the write-up. Keep this section to a few items; zero is a valid result.

## 3. Normalize and deduplicate

Represent every candidate with:

- canonical URL
- title and event date
- source stream
- one-sentence factual claim
- reader relevance
- source type: primary, established press, aggregator, or social

Merge candidates that describe the same underlying event. Preserve all independent source URLs on the merged record.

## 4. Score before writing

| Axis | Range | Test |
|---|---:|---|
| Recency | 0–2 | New inside the current window |
| Reader relevance | 0–2 | Specifically matches the configured profile |
| Substance | 0–1 | Launch, decision, number, filing, benchmark, or real debate |

Write a full item only at 3/5 or above. Add one ranking point when the story arrived independently through two or more streams. Subtract one when only aggregator/content-farm sources support it. Apply configured exclusions as a hard filter after scoring.

## 5. Enforce claim discipline

Classify material statements before synthesis:

- `fact`: an event, measurement, quotation, product capability, or other checkable statement.
- `thesis`: an interpretation, causal view, forecast, or strategic implication.
- `deal-status`: financing, acquisition, partnership, IPO, or transaction state that can change.

Use these confidence labels:

- `verified`: directly supported by a suitable primary source.
- `corroborated`: supported by at least two independent sources.
- `single-source`: attributable, but not independently confirmed.
- `unverified`: lead or rumor that should usually be omitted.

Deal-status claims must include an as-of date. Never promote a thesis to fact through repetition. If sources conflict, describe the conflict or omit the claim.

## 6. Track source health

Record material source checks when persistence is enabled:

- `ok`: source was reachable and useful.
- `degraded`: reachable but incomplete, stale, or structurally changed.
- `blocked`: access denied, paywalled, robots-blocked, or authentication-gated.
- `failed`: request or parsing failed.

Repeated failure is a routing signal. It does not make the source unreliable; it means the acquisition path needs replacement or repair.

## 7. Synthesize two separate halves

### Part A — Frontier & Builders

- Model releases and major updates.
- What AI-native builders are shipping or debating.
- Personalized GitHub and Hugging Face signal.
- Router, leaderboard, and unannounced-release signal.
- AI funding, partnerships, policy, and regulation.
- Two or three cross-cutting patterns.

### Part B — Markets, Deals & Careers

- Consulting and strategy.
- Macro and investment trends.
- Compact market pulse only when something moved.
- Capital markets, M&A, private equity, venture, and IPO activity.
- Career-track developments.
- The established AI stack.
- Optional thesis watch.
- Two or three cross-cutting patterns.

Keep a hard visual divider between the halves.

## 8. Run a thesis watch that can lose

A thesis watch is the optional Part B section where the reader tracks a standing hypothesis across runs. Configure it only when the reader has one. Its value comes entirely from being falsifiable, so structure it as instrumentation rather than as a recurring argument.

Define each watch with three parts:

- **A primary tell.** The single observable the reader believes moves first, with a numeric baseline and a stated threshold. Without a threshold there is no way to be wrong.
- **Secondary conditions.** Supporting observables that would corroborate the thesis but are not decisive alone.
- **A concealed channel.** Where the same risk would accumulate if the primary tell stayed quiet — off-balance-sheet structures, privately marked assets, lagged or discretionary valuations, adjacent leverage. Most theses fail here rather than being wrong, because the visible instrument is the one everyone else is also watching, and pressure routes around it.

Report only what moved since the last run. Zero lines is a valid result.

Three rules keep the section honest:

1. **Lead with disconfirming movement.** When the primary tell moves against the thesis, say so first and plainly. A watch that surfaces only confirming evidence has stopped being a monitor.
2. **Name divergence as its own state.** A quiet primary tell alongside a deteriorating concealed channel is a specific, reportable condition — risk relocating rather than resolving. It is more informative than either reading alone.
3. **Never silently drop a tell.** Omitting an indicator in the run where it disagrees is the failure mode this structure exists to prevent. If an indicator could not be checked, record it as `blocked` or `failed` rather than leaving it out.

Distinguish a dated measurement from an undated reference figure. Pricing-guide numbers, vendor marketing tables, and stale baselines are not evidence that something moved; label them as background or omit them.

## 9. Output and close

- Use one-line takeaways with direct links.
- Include an insight only when it is distinct from the factual takeaway.
- Label single-source or changing claims inline.
- Say “nothing new in this window” when a section is genuinely quiet.
- Never add filler to reach a target item count.
- Save the digest to `digests/YYYY-MM-DD.md` only when the user has authorized repository writes.
- Finish the state run as `completed`, `partial`, or `failed` and attach the digest path when one was written.
