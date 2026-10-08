# Framework index · start here

**Public edition:** long book quotations are replaced by paraphrase, and the entry ledger (`framework/entries/`, where each ID is verified against the book) is not published. IDs and page locators still identify each point.
**What this is:** a precise, calculator-grade knowledge base of three Hormozi books, built so tools for our business and clients map exactly onto the theory. Source books are in `source-material/` and are never edited.
**Books:** Offers (OF-001 to OF-081) · Leads (LD-001 to LD-104) · Money Models (MM-001 to MM-069). 254 entries in all.
**Rule:** always name the book and the entry ID. If the books do not cover something, say so; do not invent book advice.

## 1. Read in this order for a tool
1. `concepts/01-growth-and-unit-economics.md`: definitions, ratios, the 30-day cash test (open decision below).
2. `flagged-claims.md`: what NOT to use as a benchmark, default or forecast.
3. `cross-reference-map.md`: where the books agree, differ or clash.
4. The concept file for the topic (table below).
5. Only then the entry (for exact wording, source page and tags), and only then the book in `source-material/`.

## 2. Which file answers which question
| Question | Open |
|---|---|
| What is gross profit / LTV / LTGP / CAC? Which ratio is "good"? | concepts/01 |
| What is the 30-day cash test? | concepts/01 section 4, then cross-reference-map row 4 |
| Is this a good market? Should I niche down? | concepts/02 |
| How should I price? Why not copy competitors? | concepts/03 |
| How do I make an offer worth more? (Value Equation) | concepts/04 |
| How do I build the offer (problems, solutions, trim, stack)? | concepts/05 |
| Scarcity / urgency / bonuses / guarantees? | concepts/06, 07, 08, 09 |
| What do I call it? It stopped working. | concepts/10 |
| Free offer to get a lead | concepts/11 (Leads) and concepts/22 (Money Models attraction offers) |
| Which lead channel first? How do the four fit? | concepts/12 |
| Warm outreach / content / cold outreach / paid ads | concepts/13 / 14 / 15 / 16 |
| Referrals, employees, agencies, affiliates | concepts/17 / 18 / 19 |
| How much volume? How do I test? | concepts/20 |
| What do I sell after the first sale? | concepts/21 (framework), then 23 upsell, 24 downsell, 25 continuity |
| Can I use the author's number X? | flagged-claims.md |
| Do the books agree on Y? | cross-reference-map.md |
| I have a client situation (leads, cash, churn, plateau, price...) | situation-playbooks.md |
| What do the books say about closing a sale? | Nothing usable (cross-reference-map row 30) |

## 3. What is in each folder
- `concepts/` (25 files): one file per core idea across all three books. Definition, rules, tagged numbers, FLAGs, cross-book links, "Do not" list. Numbers are copied from the entries, not re-read from the books.
- `entries/` (25 files): the base layer. One entry per idea with source locator, type and tagged bullets.
  - Offers: ch00-03 (OF-001–013), ch04-05 (OF-014–024), ch06-08 (OF-025–033), ch09-10 (OF-034–043), ch11-12 (OF-044–053), ch13-14 (OF-054–064), ch15 (OF-065–073), ch16-end (OF-074–081).
  - Leads: sec1-2 (LD-001–015), sec3-intro-warm (LD-016–024), sec3-content1 (LD-025–032), sec3-content2 (LD-033–039), sec3-cold (LD-040–048), sec3-ads1 (LD-049–058), sec3-ads2-steroids (LD-059–068), sec4-referrals (LD-069–075), sec4-employees-agencies (LD-076–084), sec4-affiliates (LD-085–096), sec5-get-started (LD-097–104).
  - Money Models: sec0-1-intro-model (MM-001–008), sec2-attraction (MM-009–027), sec3-upsell (MM-028–041), sec4-downsell (MM-042–052), sec5-continuity (MM-053–062), sec6-make-model (MM-063–069).
- `cross-reference-map.md`: topic matrix across books, same-word-different-meaning table, tensions.
- `situation-playbooks.md`: 12 situations (not enough leads, leads don't buy, no offer yet, price competition, free offer, paid ads, tight cash, churn, plateau, scaling with people, can I use the author's number, building a tool): what to ask, which files to read in order, flags, what the books do not cover. Routing only; adds no advice.
- `skill-audit-offer-growth-coach.md`: report (nothing changed in the skill) comparing the `/offer-growth-coach` skill to this base: 5 high and 10 medium findings, coverage stated.
- `flagged-claims.md`: track-record numbers, case multiples, rule-like numbers with no data, unverified sources, absolute statements, ethics flags, numbers that do not tie.
- `local working file, not published`: extracted text and images used to build the entries. Working files, not for tool use.

## 4. Tag key (used everywhere)
- **[stated]** in the book text · **[figure]** only in an image · **[derived]** our arithmetic or logic · **[FLAG]** inconsistency, ambiguity or ethics concern · **[claim]** author's anecdote or assertion, not a usable threshold · **[our note]** our observation.
- Quotation marks surround exact book wording only.

## 5. How far to trust each layer
| Layer | Checked how |
|---|---|
| entries | Pass 1 (Claude read the text and viewed figures), then Pass 2 (independent fresh checkers; every checker claim verified against the book before editing). All three books done. |
| concepts, cross-reference map, flagged-claims, index | Written by us from the entries. ID coverage and number presence checked mechanically. Independently checked on 2026-10-07 (3 report-only checkers, then a smaller second check of the edits made after the first; every finding verified against the entries and fixed). Fixes made after the second check have not been re-checked. |
| situation-playbooks | Written by us from the concept files. Checked once on 2026-10-07 (second check); fixes since then not re-checked. |

## 6. Open decisions and known gaps
- **The 30-day cash test has no formula.** Nine mentions inside Money Models (MM-068), plus a differently worded version in Leads (LD-061). A calculator needs the user to choose (a) what "costs" include, (b) revenue vs cash vs profit, (c) the multiple. See concepts/01 section 4.
- **About 140 Leads image pages were not viewed (decision 2026-10-07: the owner chose to skip).** Text was read in full and the figures are taken to illustrate the same points. Known caveat: figures that were viewed earlier sometimes held a detail the text lacked (LD-048's "Count in 100s" box), so a number could still sit in an unviewed figure.
- **No closing method in any book.** Leads leaves sales out on purpose.
- **Not independently checked:** only the small fixes made after the second check (wording and citation corrections).
- **Risk areas for any live tool:** ad accounts, client data, payments. The books do not discuss platform terms, privacy law or card-network rules.
- **Skill audit done (report only):** see `skill-audit-offer-growth-coach.md`. Skill not yet changed; awaiting a decision on the fixes (the 30-day definition first).

## Do not
- Do not build a number into a tool unless it is [stated], [figure] or [derived] and is not on the flagged-claims list.
- Do not merge rows marked DIFFERENT or TENSION in the cross-reference map.
- Do not treat the concept files as the book. They are our summary of our entries.
