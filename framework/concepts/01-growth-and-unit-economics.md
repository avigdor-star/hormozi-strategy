# Concept 01 · Growth levers and unit economics (gross profit, LTV/LTGP, CAC, ratios, the 30-day cash test)

**Books:** Offers (definitions: Ch.3). Leads (CAC, LTGP, 3:1, client-financed acquisition, test budget). Money Models (the 30-day test and its nine wordings).
**Built from entries:** OF-006, OF-007, OF-008, OF-011, OF-012 · LD-001, LD-002, LD-044, LD-059, LD-060, LD-061, LD-070, LD-080, LD-090, LD-095 · MM-002, MM-004, MM-064, MM-066, MM-068. (other IDs cited in the body include: LD-013, LD-015, LD-045, LD-062)
**Tag key:** [stated] · [figure] · [derived] · [FLAG] · [claim] · [our note].
**This is the file a calculator should read first.** Every number below is tagged with how reliable it is. Where the books disagree, the disagreement is stated and a choice is left to the user.

## 1. Ways to grow
- Offers (OF-006): three ways: more customers, higher average purchase value, more purchases per customer. Author note: simplified to two: more customers, and more value per customer (profit per purchase, number of purchases). [stated]
- Leads (LD-001): two ways: get more customers, make them worth more (Leads covers the first). More customers = **more, better, cheaper, reliable** leads. [stated]
- Ceiling [derived; the book gives only the example]: new clients per month × lifetime value = maximum monthly revenue. Example [stated]: 10 clients/month × $1,000 lifetime value = $10,000/month "max revenue."
- [FLAG] The example calls the $1,000 "avg cart value × avg number of purchases" (revenue wording) while Offers defines LTV as **gross profit** (below). A tool must pick one and say so.
- Growth as a duty (OF-012) [claim]: "maintenance is a myth"; stock market ~9%/yr; 20–30%/yr may be needed. Unsourced; do not hard-code.
- Multiplier claim (MM-004): twice as valuable × twice as many × twice as fast = **8x** faster; triple = **27x**. [derived ✓] Holds only if the factors are independent; no evidence in the book.

## 2. Definitions (use these labels in any tool)
| Term | Definition | Source |
|---|---|---|
| Lead | "a person you can contact. That's all." | LD-002 |
| Engaged lead | a lead who **shows interest** (gives contact info, follows and is contactable, replies) | LD-002 |
| Qualified (second Leads definition) | a person who has a problem to solve and also the money to spend on it | LD-002 [FLAG: not reconciled] |
| Gross profit | revenue − **direct cost of servicing an additional customer**. $10 sale, $2 cost → $8 (80%). Net profit = after ALL expenses. | OF-007 |
| LTV (the author's) | gross profit per period × number of periods over the customer's lifetime; indirect costs (admin, software, rent) **excluded**. Example: $1,000/mo × 90% × 5 months = **$4,500**. | OF-008 [derived ✓] |
| LTGP | lifetime gross profit = all the money a customer spends over time, less everything it costs to deliver to them. Example: $15 sale, $5 delivery, ten purchases → **LTGP $100**. | LD-060 |
| CAC | cost to acquire a customer; includes **non-ad costs such as sales** | LD-060, LD-062 |
| Efficiency | LTGP ÷ CAC | LD-060 |
- Why gross profit, not revenue: gross profit is the real cash used to win customers, pay rent and cover payroll. The author notes other sources define LTV on revenue. [stated]
- [FLAG] Offers labels the $4,500 calculation "Revenue" (a slip); the number is gross profit. **Label every LTV as gross-profit-based and name the margin used.**
- [our note] Money Models never uses LTV or LTGP and gives no definition of either.
- Three lead counts: contactable · engaged · has problem and money. Store which one a number refers to.

## 3. The ratios and tests (all [stated] as patterns, not laws)
1. **LTGP > CAC** = profitable; < CAC = losing. (LD-060)
2. **LTGP ÷ CAC ≥ 3** target: businesses that struggle to scale had a ratio under 3:1 and "take off" above it. The author says this is something he saw himself and not a rule. (LD-060, LD-044, LD-080, LD-095, LD-090)
3. **CAC vs industry average (a different "3"):** CAC below **3x the industry average** → focus on the business model (LTGP); above → focus on advertising (CAC). (LD-060, LD-080) [FLAG] LD-060 says to focus on advertising (CAC); LD-080 says only that above 3x above 3x the issue lies in sales or in advertising. A heuristic; 2.9x is "good," 3.1x is "bad."
4. **Cold outreach success test:** profit ÷ cost ≥ 3 (LD-044). [FLAG] One paragraph states it in the opposite direction; use profit ÷ cost ≥ 3. Same inversion in LD-080 ("at least one-third of the profit"): the meaning is **CAC at most one-third of LTGP**.
5. **Affiliate targets:** at least 3:1 "for a decent business"; want 5:1, 10:1+ (LD-095).
6. [FLAG] **Payout-ratio definitional drift:** in LD-090 "3:1" treats LTGP as the business's share after paying the affiliate ($120 on $160 gross profit); by the stated LTGP definition it would be 4:1. In LD-095 "LTGP" is net of the payout. **A calculator must take gross profit per customer, acquisition cost, and payout as separate inputs and state which ratio it shows.**
7. [FLAG] LTGP:CAC says nothing about **payback time**; see section 4.

## 4. The 30-day cash test (the user must pick one definition)
**What the books agree on [stated]:** get cash back from a customer fast so you can recycle it. Reason given: a credit card gives any business a 30-day loan with no interest, and if the balance is cleared before the month ends it behaves like normal money. (MM-004; same rationale in LD-061.)
**What they do not give:** a formula. Nine mentions in Money Models (table from MM-068) plus the Leads wording:
| Where | Wording |
|---|---|
| MM outline (p.18) | earn so much within the first thirty days that paying to get more customers is never an issue again |
| MM box title (p.24) | Earn enough profit to recoup your costs inside 30 days or less |
| MM box body (p.24) | The author likes to recover the cost of acquiring a customer within 30 days. |
| MM attraction conclusion (p.75) | Ideally, we collect enough cash to pay for acquiring the customer and delivering what we sell, several times over. (no 30-day window) |
| MM upsell conclusion (p.110) | if the Attraction Offer has already paid for acquiring and serving customers, extra money is welcome (an "if" clause) |
| MM continuity bonus (p.148) | "we can still hit our 30-day profit goals" |
| MM Section VI Step 2 (p.175) | profits within 30 days that sit well above what it costs to acquire a new customer and deliver the offer to them |
| MM Section VI definition (p.172) | one customer brings in enough money to pay for winning and serving at least two more customers within less than 30 days (hedged with "Ideally") |
| MM recap (pp.180–181) | a customer yields more profit than it costs to acquire and serve them in their first 30 days (bare minimum); one customer yields more profit than the cost of acquiring and serving many customers ($100M model) |
| Leads (LD-061) | within 30 days the customer's spend exceeds what it cost to acquire and serve them |
**Differences the user must decide:**
- (a) **What "costs" include:** acquisition only, or acquisition + delivery.
- (b) **Revenue, cash or profit** on the left side. The recap says "profit… than it costs to get and service," which double counts delivery if profit is already net of it.
- (c) **The multiple:** cover one customer (1x), "multiple times over," "at least two more" (MM-064 [derived]: 30-day cash from one customer ≥ the cost to get and service two more customers; roughly 2x if the two are counted alone, roughly 3x if this customer's own cost is counted too; the entries do not say which the author meant), "many."
- [FLAG] The Leads test budget rule (concept 16) uses 2x of 30-day **cash** in its rule but "profit" in its example.
**Suggested neutral formula for a tool (ours, not the book's):** `30-day cash collected per customer ÷ (cost to acquire + cost to deliver for the same customer)`; the user chooses the pass mark (1x, 2x or other) and whether the numerator is revenue, cash or gross profit.
**Risks (our note):** the 30-day window is a credit-card float convenience; the books do not discuss card limits, interest after 30 days, refunds, or chargebacks (refunds cost $150,000 in the Leads origin story, LD-015). Live ad accounts and payments are a risk area.

## 5. Worked 30-day example from Leads (LD-061, with figure)
$15/month membership, $5 delivery → $10 gross profit/month; average stay 10 months → LTGP $100; CAC $30 → 3.3:1. Old way [figure]: month 0 cash −$20, break-even at month 2, +$40 by month 6. Fix: a **$100 upsell with 100% margin** that **one in five** new customers take → $20 average per customer → first-30-day gross profit = $10 + $20 = $30 = CAC. [derived ✓] [FLAG] 100% margin and 20% take rate are inputs; at 50% margin the upsell adds $10 and break-even fails.

## 6. Funnel math (Offers, OF-011) and the chain a tool should compute
Ad spend → impressions → response rate → appointments booked → show rate → showed → closing % → closed → price → cash up front → ROAS. [figure]
- Compute from **counts and rates**, never from the text's "2.5 × 2.5 × 4 = 22.4x" (that equals 25; the figure's 2.3x gives 23.0; 22.4x holds only from the counts). The $3,997 price is in the figure only.
- The payback narrative (commodity offer: 5 customers pay another $1,000 in 30 days → $10,000 = break-even) uses **cash**, not gross profit, and ignores delivery cost.
- Example values are "rounded for illustration," from an agency; not benchmarks. See concept 05 for the full chain.

## 7. Cost-per-engaged-lead formulas by channel (Leads)
- Lead magnet vs core offer (LD-013): compute cost per customer from explicit stage counts (see concept 11).
- Cold calling team (LD-045): $240/rep/day → $120 per show → ≈$360 per client → 10:1 on $3,600 profit (concept 15); [FLAG] "excluding commissions" mismatch.
- Employees (LD-080): total payroll ÷ total engaged leads; CAC = that × (1 ÷ conversion) (concept 18).
- Affiliates (LD-095): CAC per affiliate vs gross profit of all customers they send; **13.5:1** (the book says 12.5:1; arithmetic error) (concept 19).
- Referrals (LD-070): **% referred monthly − % churned monthly = % monthly compounding growth** (concept 17). [FLAG] The book's "referrals cost nothing" example conflicts with paying referrers.
- Test-budget rule for new ads (LD-059): 2x the first-30-day customer **cash** (not LTGP), shut off at 1x if no leads; Phase 3 budget = customers wanted × CAC padded 20% (concept 16).

## 8. Authors' track-record numbers (not usable as benchmarks)
Offers OF-013 (36:1 lifetime ad return; $100,117 first launch; $500k→$28M; "$1,200,000/mo profit"); Leads LD-015 ($250M+ annual revenue, 36:1, Acquisition.com averages 1.8x revenue / 3.01x profit in 12 months with no baseline); MM-002 ($680 per customer, 34:1; [FLAG] $680 mixes $600 revenue and $80 profit, so do not reuse 34:1 as either). Full list in flagged-claims.md.

## Do not
- Do not call any ratio "LTV:CAC" without saying revenue-based or gross-profit-based; the author uses gross profit.
- Do not present the 30-day test as one formula; offer the three choices.
- Do not use 3:1, 3x, 2x or 20% as universal rules; the author calls the 3:1 "a pattern… not a rule."
