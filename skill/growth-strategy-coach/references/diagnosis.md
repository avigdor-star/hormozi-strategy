# Diagnosis: find the bottleneck before advising

Rule: **diagnose, confirm, then recommend.** No offer, channel or money-model play until the bottleneck is written down and the user agrees with it.

## Order (OF-016: Market > Offer > Persuasion; fix the earliest broken link first)
1. **Market**: pain, purchasing power, easy to target, growing. User judgment; the books give no scores or cut-offs (`base/concepts/02-market-selection.md`).
2. **Offer**: is it an obvious yes, priced for value, not a commodity? (`03`, `04`, `05`, enhancers `06`-`10`).
3. **Leads**: a steady daily flow of engaged leads at a cost the business can pay (`11`-`20`).
4. **Money model**: does what a new customer pays in the first 30 days cover what it costs to get and serve them? The user chooses the definition (`01` s.4, `21`-`25`).
5. **Delivery and capacity**: can the business absorb more?
[our note] Treating "persuasion" as "leads" is our step, not the author's (concept 02).

## Intake: one question per turn, in this order (stop as soon as a clear bottleneck appears)
**A. Business and goal:** 1. What do you sell, to whom, what problem? 2. What outcome, by when (number + date)?
**B. Market:** 3. Who exactly, and how bad is the problem (would they pay to solve it now)? 4. Can they afford it, can you reach them, is the group growing?
**C. Offer:** 5. What do you promise, how fast, what must the customer do? What proof? 6. Price vs alternatives; how do you differ besides price? 7. Of people who hear the full offer, what share buy? Refunds? 8. What guarantee, bonus or deadline exists today, and are they real?
**D. Leads:** 9. Where do engaged leads come from today? 10. How many actions a day, for how many weeks? Did you stop early? 11. What does a lead cost, what does a customer cost to acquire: measured or guessed? 12. What share come from referrals? What happens to leads after they come in?
**E. Money model:** 13. What do customers pay in the first 30 days, in total? What does delivery cost? 14. What do they buy next, and what % do? What happens on a "no"? 15. Do any pay repeatedly? How long do they stay, why do they leave?
**F. Capacity:** 16. Cash and runway; what can you risk this quarter? 17. How many more customers can you serve next month? 18. Legal or industry limits, team, hours per week.

## Data tags (every number written to state)
`[measured]` from records · `[estimated]` the user's best guess · `[assumed]` coach placeholder to test · `[unknown]` not yet gathered. A recommendation built mostly on estimated or unknown numbers must say so; the first action is usually to measure.

## Signals to look at (not tests). Numbers from the books are the author's patterns, not rules.
| Area | Look at | What the books say | Caution |
|---|---|---|---|
| Market | Four indicators | A bad market stops the equation (OF-016) | No scores, weights or "any missing = disqualified" |
| Offer | Price vs alternatives; the four Value Equation drivers | Raise value before price (OF-020); [coach heuristic, not the book's] improve the weakest driver first | Any 1-10 rating is the coach scale, relative only |
| Offer | Refund rate | MM-011: "below 5%" to use Win Your Money Back; also "about 10%" will ask | The two figures are not reconciled; base unstated |
| Leads | Actions per day vs volume | Not enough leads = not enough skill or volume (LD-016) | No numeric test; ask the Rule-of-100 unit (count, minutes, dollars) |
| Leads | LTGP : CAC | Struggling businesses sat below 3:1 (LD-060) | "A pattern, not a rule"; says nothing about payback time |
| Leads | CAC vs industry average | Above 3x: advertising (LD-060) / sales or advertising (LD-080) | A heuristic; a different 3 |
| Leads | Referral share | Level 4 "shoot for 25% or more"; machine "a third" (LD-101) | Targets, unsourced; not revenue bands |
| Money model | 30-day amount vs cost | Nine wordings, no formula (MM-068) | Use `calc.py thirty-day` with the user's chosen definition |
| Money model | Pay-later cancels | Above 10%: the author says one of three things is off: over-promising, an easy-to-meet guarantee, or too high a price (MM-025) | Author's figure |
| Money model | Early cancels under commitment | Above 5%: look into the product (MM-061) | Base not stated |
| Money model | Share paying in full after adding plans | Should hold (MM-045) | `calc.py plan-check` |

## Constraint finder (ask in order; stop at the first "no")
```
1. Clear market with pain + money + reachable + growing?        no -> market / niche       (playbook 3)
2. Offer is a clear yes and priced for value, not a commodity?   no -> offer                (playbooks 3, 4)
3. Engaged leads arriving daily from a method run at volume?     no -> leads                (playbooks 1, 5, 6)
4. First-30-day result passes the user's chosen definition?      no -> money model          (playbook 7)
5. Customers buy more than once / next offers exist?             no -> upsell/downsell/continuity (7, 8)
6. Leads come but do not buy?                                    yes -> sales step, offer   (playbook 2; the books give no closing method)
7. Method works but the owner is the limit?                      yes -> people and partners (playbook 10)
8. Everything works, growth slow?                                -> more / better / new     (playbook 9)
9. Not enough data?                                              -> cheapest measurement first
```
Playbooks are in `references/base/situation-playbooks.md`.

## Output (write to state, then give a 5-line summary)
- Current offer ladder, lead sources and money-model map, with numbers and tags
- Bottleneck, stage and constraint, with evidence and data tags
- Up to 3 candidate moves (ICE-scored on the coach scale) and the recommended one, with confidence and what would change it
- Missing data (each becomes a commitment or experiment)
- Top 3 risks and ethics/legal flags
