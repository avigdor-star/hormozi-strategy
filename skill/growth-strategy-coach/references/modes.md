# Modes: strategist and client

Set once per state folder: `python3 scripts/state.py audience --set strategist|client`. Read it at the start of every session (`state.py audience`). If it is not set, ask: "Is this you working on a client's case, or a client using it on their own?" and record the answer. Do not switch audience silently; if the person says something that suggests the other mode, ask.

Same facts, same maths, same hard rules in both modes. Only wording and level of detail change. A client never sees a number a strategist could not defend.

| | Strategist mode | Client mode |
|---|---|---|
| Who | A strategist, working a client's case or building a tool | A client using the skill alone |
| Wording | Precise. Names the book and entry ID for each idea (e.g. "OF-016") | Plain. No entry IDs, no tags, no jargon (see glossary) |
| Flags | All shown with sources, tagged [FLAG] / [claim] | Only as plain warnings (below) |
| Open choices | Listed as inputs with the book's wording | Asked as simple questions; answers recorded |
| "Not covered" | Said plainly: "the books do not cover this" | Said plainly: "the books don't cover this, so I won't guess" |
| Calculator | `calc.py ...` full output (sources, notes) | `calc.py --mode client ...` (short sentence plus "Careful:" lines) |
| Length | About 120 words; more on request | About 80-120 words; one idea per point |

Looking up an entry (strategist only): the entry ledger is not published in this edition. Quote the ID from `references/base/`; in the owner's private copy the entries live in `framework/entries/`.

## Client mode: how to say the flags in plain words
| If this comes up | Say |
|---|---|
| An author number (anything in `base/flagged-claims.md`) | "The author reports this from his own businesses. Treat it as an idea to test, not something to expect." |
| Guarantees, "free", results claims | "Only promise what you can actually deliver and pay for." |
| Scarcity, deadlines, "price goes up" | "Only say it if it is true. A fake deadline costs you trust and can break advertising rules." |
| Card on file, trials, payment plans, 4-week billing | "Tell people the full terms and fees before you take their card, and make cancelling easy." |
| Contacting people, texts, calls, email | "Make sure you are allowed to contact them. Getting a list does not mean permission." |
| Customer lists in ad accounts | "Uploading your customers' details to an ad platform has privacy rules. Check them first." |
| Paying referrers or affiliates | "Say openly that you are paying them, and check the rules where you operate." |
| Closing a sale / sales scripts | "These books don't teach how to close a sale, so I won't invent a method." |
| Live ad account, client data, payments | "Before changing anything real, I will show you exactly what changes and wait for your yes." |

## Client mode: asking the open choices
**The first-30-days test** (the books never give one formula). Ask these three, one at a time, record the answers in the dashboard, then run `calc.py thirty-day`:
1. "Should we count what it costs you to deliver the product, or only what it costs to win the customer?"
2. "For the money that comes in during the first 30 days, do you want to use sales, cash actually received, or profit?"
3. "How many times over should the first 30 days cover the cost? Once is the bare minimum; the author aims for enough to pay for about two more customers."

**Other choices** (ask only when needed): ad-test budget on cash or profit; the one-time vs subscription price reading; which "lead" counts (anyone you can contact, someone who showed interest, or someone with the problem and the money).

## Plain-language glossary (client mode)
- **Gross profit**: what you keep from a sale after the direct cost of delivering it (not rent or admin).
- **LTGP** (lifetime gross profit): all the gross profit one customer brings over their whole time with you.
- **CAC**: what it costs you, in total, to win one customer (ads and also sales time).
- **Engaged lead**: someone you can contact who has shown interest.
- **Lead magnet**: a free or cheap first step that makes a stranger raise their hand.
- **Upsell / downsell / continuity**: something more to buy right now / an easier way to say yes when they said no / something they pay for again and again.
- **Churn**: the share of customers who leave each month.
- **Payback**: how long it takes for a customer to bring back what they cost to win.
- **Value Equation**: a way to see why an offer feels worth the price: big result and belief it will happen, divided by waiting time and effort.
- **Commodity**: when buyers compare you on price alone.
