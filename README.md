# Hormozi strategy knowledge base + growth-strategy-coach skill (public edition)

A structured, checked set of notes on three business books by Alex Hormozi, plus a Claude skill that coaches with them and a calculator that never hides a choice the books leave open.

- **Books:** *$100M Offers*, *$100M Leads*, *$100M Money Models*.
- **Not affiliated with or endorsed by the author or his companies.** The books are not included and must be bought separately. Names and titles belong to their owners.
- **Quotes:** long book passages have been removed on purpose. Short terms and labels stay. Page and chapter locators stay, so you can check any point in your own copy.
- **Entry IDs** (OF-###, LD-###, MM-###) refer to a private verification ledger that is not published, for copyright reasons. The conclusions, flags and maths are published.

## What is here
| Folder | What |
|---|---|
| `framework/concepts/` | 25 concept files: what each idea is, the numbers, and what the books leave open |
| `framework/flagged-claims.md` | Claims and numbers that must never be used as benchmarks, and why |
| `framework/cross-reference-map.md`, `situation-playbooks.md`, `00-index.md` | How ideas connect; what to do in common situations; where to start |
| `skill/growth-strategy-coach/` | The coaching skill: diagnosis, playbooks, calculator (`scripts/calc.py`), state tracker |

## Use the skill
Copy `skill/growth-strategy-coach/` into `~/.claude/skills/`, then in Claude Code run `/growth-strategy-coach <your question>`. It works in two modes: a strategist working a client's case, or a client on their own.

Run the calculator tests: `python3 skill/growth-strategy-coach/tests/test_calc.py`

## Maintainers
`scripts/sync_base.py` refreshes the skill's bundled copy from a framework folder and defaults to the `framework/` folder of this repo. Pass `--framework PATH` to use another folder.

The ideas here are summaries and analysis. They are not legal advice, financial advice or a promise of results: the authors' numbers are treated as hypotheses.
