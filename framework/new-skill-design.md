# New skill · one-page design (for approval)

**Working name:** `growth-strategy-coach` (a new folder next to the old `offer-growth-coach`, which stays untouched until the new one passes its checks).
**Status:** draft for approval. Nothing built yet.

## 1. Purpose
Help a strategist and the strategist's clients find the real bottleneck in a business and fix it in the right order, using the three books through our checked knowledge base, with calculators that never hide a choice the books leave open.

## 2. Two modes (set once at the start of a session, saved in the state folder)
| | Strategist mode | Client mode |
|---|---|---|
| Who | A strategist, working a client's case or building a tool | A client using it on their own |
| Language | Precise. Entry IDs, tags, flags, "the books don't cover this" | Plain. No IDs or jargon; every term explained in a few words |
| Flags | All shown, with sources | Shown only as plain warnings ("don't promise results you can't control"; "tell people the fees before taking the card") |
| Open choices (e.g. the 30-day test) | Shown as inputs to pick | Asked as a simple question with the options explained; the choice is recorded |
| Numbers | Calculator output with source and tag | Same calculator, shorter wording |
Same facts and same maths in both modes. A client never sees a number the strategist could not defend.

## 3. What it does
1. Diagnoses the bottleneck in the order market → offer → leads → money model (OF-016), one question at a time, and writes it down before advising.
2. Routes to the right playbook (the 12 in `situation-playbooks.md`).
3. Helps build or improve an offer, plan lead generation, and design the money model, using the concept files.
4. Runs the numbers with a calculator script, never in its head.
5. Records decisions, experiments and commitments in a state folder owned by the user (or the client), and reviews them next session.
6. Keeps ethics above tactics.

## 4. Hard rules (carried over from the base)
- Never use anything on `flagged-claims.md` as a benchmark, default or forecast.
- Never choose the 30-day definition silently; the user picks (costs, revenue/cash/profit, multiple).
- No 1–10 scale or "max 100" presented as the book's. Any scale is labelled "coach scale."
- Say "not covered by the books" for closing a sale and for the missing cold scripts. Never invent them.
- Coach-method numbers (sample sizes, kill-criteria examples) are labelled "coach rule, not from the books."
- Risk areas (live ad accounts, client data, payments): look first, show the exact change, wait for a yes, note how to undo it.
- Replies short; one question per turn; "Heard:" list for several topics; end with one next step.

## 5. The calculator (`scripts/calc.py`, rebuilt)
- **Keep as is (re-checked):** funnel, stack, continuity (with churn), billing (4-week), plan-check, ad-budget (2x/1x caps), outreach, rollover (4x rule).
- **Change:**
  - `thirty-day`: the three choices are required inputs; prints which formula it used.
  - `efficiency`: also prints payback time, because LTGP:CAC does not show it.
  - `value-equation`: becomes a relative comparison of two offers on a labelled coach scale; no "max 100."
  - `affiliate-payout`: takes gross profit per customer; payout = gross profit ÷ (ratio + 1); prints the book's $160 → $40 example as a check.
  - `standalone`: the 1.0 vs 1.5 basis is required; says table values between rows are interpolated.
  - `guarantee`: optional delivery-cost input.
  - `referral`: adds the book's growth equation (% referred − % churned); the simple model is labelled "coach model."
- **Every output** carries the source ID and tag; `--mode client` gives the short plain wording.
- **Tests:** each command checked against the worked examples in the entries (e.g. $160 → $40, 19 × $299, 13 ÷ 12 = +8.3%).

## 6. Files
```
SKILL.md                  short: modes, hard rules, router, session routine
references/base/          bundled copy of concepts, map, claims list, playbooks, index (date-stamped)
references/modes.md       how each mode words things; plain-language glossary
references/coaching.md    reused from the old coaching protocol and decision practices, trimmed, numbers labelled
scripts/calc.py           the calculator
scripts/state.py          reused state tracker (decisions, experiments, commitments)
scripts/sync_base.py      refreshes references/base from the framework folder
assets/templates/         reused where good
tests/                    calculator checks
```
Entries (254) are not bundled; they are cited by ID and read from the framework folder when present.

## 7. Reuse from the old skill
Keep: the state folder idea, decision records, experiments, commitments, `guardrails.md` (most of it), the department lenses (to be read at step 3). Replace: every reference file on the books (rebuilt from the concept files) and the calculator.

## 8. Build order and checks
1. This design (approval).
2. Skeleton and router.
3. Reference files from the base; the mode wording; trim the reused coaching files.
4. Calculator and tests (needs your 30-day choice).
5. Three test scenarios: a strategist case, a client case, and a "tight cash" case.
6. One independent check (cost note and a yes first).
7. Swap: rename the old skill to `-old`; keep it for a month.
No subagents before step 6.

## 9. Decisions for you
1. Name: `growth-strategy-coach`, or keep `offer-growth-coach`?
2. Bundle a copy of the base inside the skill (works anywhere, needs a sync step), or read it from the project folder (always current, works only on this machine)? Recommended: bundle, so clients can use it.
3. The 30-day test choice, needed at step 4 (we can decide then).
