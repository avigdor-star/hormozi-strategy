#!/usr/bin/env python3
"""Calculator for the growth-strategy-coach skill. No dependencies. Run, don't derive.

Every command prints its result, its sources (entry ID + tag) and the flags that apply.
Add --mode client for short plain wording, --json for machine-readable output (both flags work before or after the command name;
--mode client --json leaves out entry IDs and notes).
Choices the books leave open (the 30-day test, the continuity price basis) are REQUIRED inputs: the tool never picks.
Rates are percentages (0-100). Exit code 2 on invalid input.

  thirty-day     --acquisition-cost X --collected X --collected-as revenue|cash|gross-profit
                 --costs acquisition|acquisition+delivery [--delivery-cost X] --pass-mark N
  efficiency     --ltgp X --cac X [--industry-cac X] [--monthly-gross-profit X] [--pattern-ratio 3] [--industry-multiple 3]
  lifetime-gross-profit  (--revenue-per-period X --margin-pct P --periods N) | (--price X --delivery-cost X --purchases N)
  growth-ceiling --new-per-month N --ltgp X
  funnel         --lead-cost X --book-pct P --show-pct P --close-pct P [--price X]
  stack          --offer "name:price:take_pct" [--offer ...]
  continuity     --price X --margin-pct P --churn-pct P [--horizon-months N]
  standalone     --continuity-monthly X --share-pct P --reading text|examples
  rollover       --next-price X --credit X [--months N]
  billing        --price X --margin-pct P [--fee-pct 3]
  plan-check     --leads N --sold-before N --paid-full-before N --sold-after N --paid-full-after N
  ad-budget      [--first-30d-amount X --basis cash|gross-profit] [--customers-wanted N --cac X]
  outreach       --actions-per-week N --reply-pct P --accept-pct P --convert-pct P [--price X]
  value-compare  --a d,l,t,e [--b d,l,t,e]      (coach scale 1-10, NOT from the books)
  guarantee      --sales-before N --refund-before-pct P --sales-after N --refund-after-pct P [--price X --delivery-cost-per-sale X]
  affiliate-payout --gross-profit X --ratio R [--mix 20,20,60]
  affiliate-return --affiliate-cac X --monthly-sales X --months N --margin-pct P --payout-pct-of-gp P
  referral-growth --referred-pct P --churn-pct P
"""
import argparse
import json
import math
import sys

STANDALONE_TABLE = [(50, 1.33), (60, 1.66), (70, 2.00), (80, 2.33), (90, 2.66)]  # MM-056 text values
ROLLOVER_MIN_MULTIPLE = 4.0          # MM-039: next offer at least 4x the credit (25% discount at most)
CYCLES_4WEEK = 52 / 4                # MM-059: 13 four-week cycles vs 12 months
AD_TEST_CAP_MULTIPLE = 2.0           # LD-059: test spend per ad up to 2x first-30-day amount
AD_SCALE_BUFFER = 1.2                # LD-059: scale budget = customers wanted x CAC, plus 20%
LTGP_CAC_PATTERN = 3.0               # LD-060: "a pattern I personally observed, not a rule"
CAC_INDUSTRY_PATTERN = 3.0           # LD-060 / LD-080
AFFILIATE_TIER_SHARES = (0.25, 0.50, 1.00)   # LD-090


class InputError(ValueError):
    pass


def nonneg(name, value):
    if value is None or not math.isfinite(value) or value < 0:
        raise InputError(f"{name} must be >= 0")
    return float(value)


def positive(name, value):
    value = nonneg(name, value)
    if value == 0:
        raise InputError(f"{name} must be > 0")
    return value


def pct(name, value, allow_zero=True):
    value = nonneg(name, value)
    if value > 100 or (value == 0 and not allow_zero):
        raise InputError(f"{name} must be a percentage between {'0' if allow_zero else '>0'} and 100")
    return value


def result(values, plain, sources, notes=(), warnings=()):
    return {"values": values, "plain": plain, "sources": list(sources), "notes": list(notes), "client_warnings": list(warnings)}


# ---------------------------------------------------------------- the 30-day test
def cmd_thirty_day(a):
    acq = nonneg("acquisition-cost", a.acquisition_cost)
    collected = nonneg("collected", a.collected)
    pass_mark = positive("pass-mark", a.pass_mark)
    if a.costs == "acquisition+delivery":
        if a.delivery_cost is None:
            raise InputError("--delivery-cost is required when --costs acquisition+delivery")
        basis = acq + nonneg("delivery-cost", a.delivery_cost)
    else:
        basis = acq
    if a.collected_as == "gross-profit" and a.costs == "acquisition+delivery":
        raise InputError("gross profit is already after delivery cost; counting delivery again double counts it. "
                         "Use --costs acquisition with --collected-as gross-profit")
    if basis == 0:
        raise InputError("cost basis must be > 0")
    ratio = collected / basis
    notes = [
        "The books give NO single formula: MM-068 lists nine wordings; LD-061 says 'get and fulfill'. You chose: costs="
        f"{a.costs}, collected={a.collected_as}, pass mark={pass_mark:g}x.",
        "Readings of the pass mark: 1x covers this customer (MM-068 'bare minimum'); MM-064 'get and service at least two more customers' "
        "[derived] is about 2x if the two are counted alone, about 3x if this customer's own cost is counted too (the entries do not say which); "
        "MM-068's '$100M' wording is 'many' (no number).",
    ]
    warnings = []
    if a.collected_as in ("revenue", "cash") and a.costs == "acquisition":
        notes.append("[FLAG] Delivery cost is ignored in this setting: revenue or cash collected is compared with acquisition cost only.")
        warnings.append("This leaves out what it costs you to deliver, so it flatters the result.")
    passes = ratio >= pass_mark
    plain = (f"In the first 30 days each customer brings in {a.collected:g} against {basis:g} of costs "
             f"({ratio:.2f} times). That {'meets' if passes else 'does not meet'} the pass mark you chose ({pass_mark:g} times).")
    return result({"cost_basis": round(basis, 2), "ratio": round(ratio, 2), "pass_mark": pass_mark, "meets_pass_mark": passes,
                   "surplus_covers_more_customers_like_this": round(max(collected - basis, 0) / basis, 2),
                   "definition_used": f"{a.collected_as} / {a.costs}"},
                  plain, ["MM-004 [stated]", "MM-064 [stated, derived]", "MM-068 [stated]", "LD-061 [stated]", "concept 01 s.4"], notes, warnings)


def cmd_efficiency(a):
    ltgp, cac = nonneg("ltgp", a.ltgp), positive("cac", a.cac)
    ratio = ltgp / cac
    pattern = positive("pattern-ratio", a.pattern_ratio)
    vals = {"ltgp_to_cac": round(ratio, 2), "pattern_ratio_used": pattern, "max_cac_at_pattern_ratio": round(ltgp / pattern, 2),
            "vs_pattern": f"below {pattern:g}:1" if ratio < pattern else f"at or above {pattern:g}:1"}
    notes = ["LD-060: the 3:1 is 'a pattern I personally observed, not a rule' [stated]; businesses that struggled to scale sat below it. The pattern ratio and the industry multiple are inputs here (defaults 3 and 3), not rules.",
             "[FLAG] LTGP:CAC says nothing about how fast cash comes back; check the 30-day test too."]
    if a.industry_cac is not None:
        industry = positive("industry-cac", a.industry_cac)
        mult = cac / industry
        limit = positive("industry-multiple", a.industry_multiple)
        vals["cac_vs_industry_multiple"] = round(mult, 2)
        vals["industry_multiple_used"] = limit
        vals["where_to_look"] = (f"above {limit:g}x industry average: LD-060 says focus on advertising (CAC); LD-080 says a sales problem or an advertising problem"
                                 if mult > limit else
                                 f"within {limit:g}x industry average: LD-060 says focus on the business model (LTGP)")
        notes.append("[FLAG] This 'industry average' 3x is a different 3 from the LTGP:CAC 3; a heuristic (2.9x good, 3.1x bad).")
    if a.monthly_gross_profit is not None:
        mgp = positive("monthly-gross-profit", a.monthly_gross_profit)
        vals["monthly_payments_to_recover_cac"] = round(cac / mgp, 1)
        notes.append("Coach calculation (not in the books): CAC divided by monthly gross profit = number of monthly payments needed. LD-061's figure counts the first payment at month 0, so its break-even month is one less (CAC $30, $10 a month: 3 payments, 'break even at month 2').")
    plain = (f"Each customer is worth {ltgp:g} in lifetime gross profit and costs {cac:g} to win: {ratio:.1f} to 1. "
             f"The author saw businesses struggle to grow below 3 to 1, but calls it a pattern, not a rule (you are comparing against {pattern:g} to 1).")
    return result(vals, plain, ["LD-060 [stated]", "LD-080 [stated]", "concept 01 s.3"], notes,
                  ["This ratio does not show how long it takes to get your money back."])


def cmd_lifetime_gross_profit(a):
    if a.revenue_per_period is not None and a.price is not None:
        raise InputError("give only one form: --revenue-per-period --margin-pct --periods, OR --price --delivery-cost --purchases")
    if a.revenue_per_period is not None:
        rev, margin, periods = nonneg("revenue-per-period", a.revenue_per_period), pct("margin-pct", a.margin_pct), nonneg("periods", a.periods)
        gp_period = rev * margin / 100
    elif a.price is not None:
        price, cost, periods = nonneg("price", a.price), nonneg("delivery-cost", a.delivery_cost), nonneg("purchases", a.purchases)
        gp_period = price - cost
    else:
        raise InputError("give either --revenue-per-period --margin-pct --periods, or --price --delivery-cost --purchases")
    ltgp = gp_period * periods
    return result({"gross_profit_per_period": round(gp_period, 2), "lifetime_gross_profit": round(ltgp, 2)},
                  f"Each customer is worth about {ltgp:g} in gross profit over their lifetime (after delivery cost, before overheads).",
                  ["OF-007 [stated]", "OF-008 [stated, derived]", "LD-060 [stated]"],
                  ["Gross profit = revenue minus the direct cost of serving one more customer (OF-007). Indirect costs (rent, admin) are excluded (OF-008).",
                   "[FLAG] Offers labels its $4,500 example 'revenue'; the number is gross profit. Always say which."])


def cmd_growth_ceiling(a):
    n, ltgp = nonneg("new-per-month", a.new_per_month), nonneg("ltgp", a.ltgp)
    return result({"ceiling_gross_profit_per_month": round(n * ltgp, 2)},
                  f"If you win {n:g} customers a month and each is worth {ltgp:g}, that is the most the pace can add: {n * ltgp:g} a month.",
                  ["OF-006 [stated example, derived]"],
                  ["[FLAG] The book's own example calls the $1,000 'avg cart value x avg number of purchases' (revenue wording) while OF-008 defines LTV as gross profit. This tool uses gross profit."])


# ---------------------------------------------------------------- funnels and offers
def cmd_funnel(a):
    lead_cost = nonneg("lead-cost", a.lead_cost)
    book, show, close = pct("book-pct", a.book_pct, False), pct("show-pct", a.show_pct, False), pct("close-pct", a.close_pct, False)
    rate = book / 100 * show / 100 * close / 100
    vals = {"lead_to_sale_pct": round(rate * 100, 2), "leads_per_sale": round(1 / rate, 2), "cost_per_sale": round(lead_cost / rate, 2)}
    if a.price is not None:
        price = nonneg("price", a.price)
        vals["revenue_per_lead"] = round(rate * price, 2)
        vals["revenue_per_dollar_of_lead_cost"] = round(rate * price / lead_cost, 2) if lead_cost else None
    return result(vals, f"You need about {vals['leads_per_sale']:.1f} leads for each sale, which costs about {vals['cost_per_sale']:.2f} per sale.",
                  ["OF-011 [figure]", "MM-002 [stated, derived]", "concept 01 s.6"],
                  ["Compute from counts and rates, never from the text's '22.4x' shorthand (OF-011: 2.5 x 2.5 x 4 = 25)."])


def parse_offer(text):
    parts = text.split(":")
    if len(parts) != 3:
        raise InputError(f'offer "{text}" must be name:price:take_pct')
    try:
        return parts[0].strip(), nonneg("price", float(parts[1])), pct("take_pct", float(parts[2]))
    except ValueError as exc:
        raise InputError(f'offer "{text}": {exc}')


def cmd_stack(a):
    if not a.offer:
        raise InputError("provide at least one --offer name:price:take_pct")
    lines, total = [], 0.0
    for text in a.offer:
        name, price, take = parse_offer(text)
        exp = price * take / 100
        total += exp
        lines.append({"offer": name, "price": price, "take_pct": take, "expected_amount_per_front_customer": round(exp, 2)})
    for line in lines:
        line["share_of_total_pct"] = round(100 * line["expected_amount_per_front_customer"] / total, 1) if total else 0.0
    return result({"offers": lines, "expected_amount_per_front_customer": round(total, 2)},
                  f"On average each new customer spends about {total:g} across these offers.",
                  ["LD-061 [stated example: $100 upsell, 1 in 5 take it]", "MM-053 [stated example: 40 of 100 buy]", "coach calculation: price x take rate"],
                  ["This is expected REVENUE per front-end customer. To judge it, run thirty-day with your chosen definition."])


def cmd_continuity(a):
    price, margin, churn = nonneg("price", a.price), pct("margin-pct", a.margin_pct), pct("churn-pct", a.churn_pct, False)
    surv = 1 - churn / 100
    vals = {"avg_months_retained": round(100 / churn, 1), "lifetime_revenue": round(price * 100 / churn, 2),
            "lifetime_gross_profit": round(price * margin / 100 * 100 / churn, 2)}
    if a.horizon_months is not None:
        if a.horizon_months <= 0:
            raise InputError("horizon-months must be > 0")
        n = int(a.horizon_months)
        vals[f"expected_revenue_{n}m"] = round(sum(price * surv ** m for m in range(n)), 2)
    return result(vals, f"Customers stay about {vals['avg_months_retained']:g} months on average at this churn.",
                  ["MM-053 [stated example]", "MM-045 [claim: third-party churn data]", "coach model: constant monthly churn"],
                  ["Coach model (not from the books): constant monthly churn. MM-053's 20-month example assumes nobody leaves; at the 10.7% monthly cancellation "
                   "the book itself cites for monthly billing only about 10% would remain after 20 months. Use YOUR churn."])


def cmd_standalone(a):
    cm, share = positive("continuity-monthly", a.continuity_monthly), pct("share-pct", a.share_pct)
    lo, hi = STANDALONE_TABLE[0][0], STANDALONE_TABLE[-1][0]
    if not lo <= share <= hi:
        raise InputError(f"share-pct must be within the book's tested range {lo}-{hi}")
    ratio = STANDALONE_TABLE[-1][1]
    for (x0, r0), (x1, r1) in zip(STANDALONE_TABLE, STANDALONE_TABLE[1:]):
        if x0 <= share <= x1:
            ratio = r0 + (r1 - r0) * (share - x0) / (x1 - x0)
            break
    text_price = cm * ratio
    examples_price = cm * 1.5 * ratio
    chosen = text_price if a.reading == "text" else examples_price
    other = examples_price if a.reading == "text" else text_price
    return result({"ratio": round(ratio, 2), "reading": a.reading, "standalone_price": round(chosen, 2),
                   "other_reading_would_give": round(other, 2)},
                  f"To have about {share:g}% of buyers choose the subscription, price the one-time option around {chosen:.0f} (the other way of reading the book gives {other:.0f}).",
                  ["MM-056 [stated table, FLAG high impact]"],
                  ["[FLAG high impact] The table's multiple applies to the '/mo' figure, which is the standalone price / 1.5 in every row. 'text' = multiple x first month (what the text and summary say); "
                   "'examples' = multiple x 1.5 x first month (what the book's worked prices show: $199 membership, $399 standalone at 50%).",
                   "Values between table rows are linear interpolation (ours). The line comes from the author's own testing; no sample size or source."],
                  ["This is the author's rule of thumb from his own tests. Test it in your market."])


def cmd_rollover(a):
    nxt, credit = positive("next-price", a.next_price), nonneg("credit", a.credit)
    if credit > nxt:
        raise InputError("credit cannot be larger than the next price")
    if a.months is not None and a.months <= 0:
        raise InputError("months must be > 0")
    vals = {"discount_pct": round(100 * credit / nxt, 1), "next_price_multiple_of_credit": round(nxt / credit, 2) if credit else None,
            "meets_4x_rule": credit == 0 or nxt >= ROLLOVER_MIN_MULTIPLE * credit}
    if a.months:
        months = int(a.months)
        vals["monthly_credit"] = round(credit / months, 2)
        vals["effective_monthly_price"] = round((nxt - credit) / months, 2)
    return result(vals, f"The credit takes {vals['discount_pct']:g}% off the next offer; the author asks for 25% at most.",
                  ["MM-039 [stated]"], ["MM-039: price the next offer at least 4x the credit so a profit is left after the credit."])


def cmd_billing(a):
    price, margin, fee = positive("price", a.price), pct("margin-pct", a.margin_pct, False), nonneg("fee-pct", a.fee_pct)
    monthly_annual, four_week_annual = price * 12, price * CYCLES_4WEEK
    lift = (four_week_annual / monthly_annual - 1) * 100
    return result({"annual_revenue_monthly_billing": round(monthly_annual, 2), "annual_revenue_every_4_weeks": round(four_week_annual, 2),
                   "four_week_revenue_lift_pct": round(lift, 2), "four_week_profit_lift_pct": round(lift / margin * 100, 1),
                   "fee_pct_used": fee, "fee_profit_lift_pct": round(fee / margin * 100, 1)},
                  f"Billing every 4 weeks instead of monthly collects {lift:.1f}% more per year, so customers must be told the real yearly cost.",
                  ["MM-059 [stated, derived]"],
                  ["Profit lift assumes the extra revenue carries no extra cost and customers accept the cadence or fee. The 3% fee is the book's example (MM-059); --fee-pct is your input.",
                   "[FLAG] Payments area: disclose the billing cadence and any fee BEFORE taking the card; surcharge and negative-option rules vary by place and card network."],
                  ["Tell customers the billing rhythm and any fee before taking their card."])


def cmd_plan_check(a):
    leads = positive("leads", a.leads)
    leads_after = positive("leads-after", a.leads_after) if a.leads_after is not None else leads
    sb, pb, sa, pa = (nonneg("sold-before", a.sold_before), nonneg("paid-full-before", a.paid_full_before),
                      nonneg("sold-after", a.sold_after), nonneg("paid-full-after", a.paid_full_after))
    if pb > sb or pa > sa or sb > leads or sa > leads_after:
        raise InputError("paid-in-full cannot exceed sold, and sold cannot exceed leads")
    cann = (pa / leads_after) < (pb / leads)
    if cann:
        verdict = "Plans are cannibalizing pay-in-full."
    elif sa / leads_after > sb / leads:
        verdict = "The close rate rose and the share paying in full held."
    elif sa / leads_after < sb / leads:
        verdict = "The close rate fell."
    else:
        verdict = "No change in the close rate."
    cb, ca = round(100 * sb / leads, 1), round(100 * sa / leads_after, 1)
    fb, fa = round(100 * pb / leads, 1), round(100 * pa / leads_after, 1)
    return result({"close_rate_before_pct": cb, "close_rate_after_pct": ca,
                   "paid_in_full_per_100_leads_before": fb, "paid_in_full_per_100_leads_after": fa,
                   "cannibalized": cann, "verdict": verdict},
                  f"{verdict} Close rate {cb:g}% before, {ca:g}% after; paying in full per 100 leads {fb:g} before, {fa:g} after.", ["MM-045 [stated safety test]"], ["MM-045: after adding payment plans, total close rate should rise AND the share paying in full should hold."])


def cmd_ad_budget(a):
    vals = {}
    buffer = nonneg("buffer-pct", a.buffer_pct)
    notes = [f"LD-059 [stated]: cap test spend per ad near 2x the first-30-day amount per customer; stop at 1x if there are no leads; scale budget = customers wanted x CAC padded {buffer:g}% because ads get less efficient as they scale (the book's example pads 20%)."]
    if a.first_30d_amount is not None:
        if a.basis is None:
            raise InputError("--basis cash|gross-profit is required with --first-30d-amount")
        amt = nonneg("first-30d-amount", a.first_30d_amount)
        vals["test_spend_cap_per_ad"] = round(AD_TEST_CAP_MULTIPLE * amt, 2)
        vals["stop_line_with_zero_leads"] = round(amt, 2)
        vals["basis"] = a.basis
        notes.append("[FLAG] LD-059's rule says 30-day CASH but its example uses PROFIT; you chose " + a.basis + ".")
    if a.customers_wanted is not None or a.cac is not None:
        if a.customers_wanted is None or a.cac is None:
            raise InputError("provide both --customers-wanted and --cac")
        monthly = nonneg("customers-wanted", a.customers_wanted) * nonneg("cac", a.cac) * (1 + buffer / 100)
        vals["buffer_pct_used"] = buffer
        vals["scale_budget_per_30_days"] = round(monthly, 2)
        vals["scale_budget_per_day"] = round(monthly / 30, 2)
    if not vals:
        raise InputError("provide --first-30d-amount (with --basis) and/or --customers-wanted with --cac")
    bits = []
    if "test_spend_cap_per_ad" in vals:
        bits.append(f"test spend per ad up to about {vals['test_spend_cap_per_ad']:g}, and stop at {vals['stop_line_with_zero_leads']:g} if no leads come")
    if "scale_budget_per_30_days" in vals:
        bits.append(f"a scaling budget of about {vals['scale_budget_per_30_days']:g} per 30 days ({vals['scale_budget_per_day']:g} per day)")
    return result(vals, "The author's rough limits: " + "; ".join(bits) + ". Set your own risk limit first.",
                  ["LD-059 [stated]"], notes, ["Treat ad spend as a risk area: agree the limit with the account owner before any change."])


def cmd_outreach(a):
    actions = nonneg("actions-per-week", a.actions_per_week)
    reply, accept, convert = pct("reply-pct", a.reply_pct), pct("accept-pct", a.accept_pct), pct("convert-pct", a.convert_pct)
    rate = reply / 100 * accept / 100 * convert / 100
    vals = {"outreach_to_customer_pct": round(rate * 100, 3), "customers_per_week": round(actions * rate, 2),
            "actions_per_customer": round(1 / rate, 1) if rate else None}
    if a.price is not None:
        vals["revenue_per_year_if_repeated_weekly"] = round(actions * rate * nonneg("price", a.price) * 52, 2)
    return result(vals, f"At these rates {vals['customers_per_week']:g} customers come from {actions:g} messages a week.",
                  ["coach model: product of stage rates"],
                  ["Coach model (not from the books). Use your measured rates; the books' rates (e.g. 1 in 5) are 'about' values that vary (LD-024)."])


# ---------------------------------------------------------------- value, guarantees, partners
def parse_ratings(name, text):
    try:
        vals = [float(x) for x in text.split(",")]
    except ValueError:
        raise InputError(f"{name} must be four numbers: dream,likelihood,delay,effort")
    if len(vals) != 4 or not all(1 <= v <= 10 for v in vals):
        raise InputError(f"{name} must be four numbers from 1 to 10: dream,likelihood,delay,effort")
    return vals


def value_score(r):
    d, l, t, e = r
    gaps = {"dream outcome": (10 - d) / 9, "perceived likelihood": (10 - l) / 9, "time delay": (t - 1) / 9, "effort and sacrifice": (e - 1) / 9}
    return d * l / (t * e), max(gaps, key=gaps.get)


def cmd_value_compare(a):
    sa, wa = value_score(parse_ratings("--a", a.a))
    vals = {"offer_a_relative_score": round(sa, 2), "offer_a_weakest_lever": wa}
    plain = f"Offer A's weakest point is {wa}."
    if a.b:
        sb, wb = value_score(parse_ratings("--b", a.b))
        vals.update({"offer_b_relative_score": round(sb, 2), "offer_b_weakest_lever": wb, "a_vs_b": round(sa / sb, 2)})
        plain = f"Offer A scores {sa / sb:.2f} times offer B on your ratings. A's weakest point: {wa}. B's: {wb}."
    return result(vals, plain, ["OF-025 [figure: formula]", "OF-030 [FLAG]"],
                  ["COACH SCALE, not from the books: the book has no 1-10 scale, no weights, no maximum, no pass mark (concept 04). "
                   "Ratings are your judgment of the CUSTOMER's view; delay and effort: 1 = fast/easy, 10 = slow/hard. Use only to compare offers or pick the weakest lever.",
                   "The book's own example (OF-030) scores each driver 0 or 1 and ADDS them; that is a different operation from this multiply/divide."])


def cmd_guarantee(a):
    sb, rb = positive("sales-before", a.sales_before), pct("refund-before-pct", a.refund_before_pct)
    sa, ra = nonneg("sales-after", a.sales_after), pct("refund-after-pct", a.refund_after_pct)
    net_b, net_a = sb * (1 - rb / 100), sa * (1 - ra / 100)
    if net_b == 0:
        raise InputError("net sales before must be > 0")
    vals = {"net_sales_before": round(net_b, 1), "net_sales_after": round(net_a, 1), "net_lift_multiple": round(net_a / net_b, 3)}
    if ra < 100:
        vals["sales_multiple_needed_to_break_even"] = round((1 - rb / 100) / (1 - ra / 100), 3)
    notes = ["OF-066 [derived]: break-even when sales multiple x (1 - new refund rate) = (1 - old refund rate); 5% -> 10% needs x1.056."]
    if a.price is not None and a.delivery_cost_per_sale is not None:
        price, cost = nonneg("price", a.price), nonneg("delivery-cost-per-sale", a.delivery_cost_per_sale)
        before, after = net_b * price - sb * cost, net_a * price - sa * cost
        vals["contribution_before"], vals["contribution_after"] = round(before, 2), round(after, 2)
        notes.append("Contribution = kept revenue minus delivery cost on EVERY sale, refunded or not (OF-066 caution 3: 'eat the cost of the refund AND the cost of fulfilling').")
    else:
        notes.append("[FLAG] Without --price and --delivery-cost-per-sale this ignores fulfillment cost on refunded sales (OF-066 [our note]).")
    verdict = "More net sales after refunds." if vals["net_lift_multiple"] > 1 else "Refunds eat the gain."
    plain = verdict
    if "contribution_before" in vals:
        cb, ca = vals["contribution_before"], vals["contribution_after"]
        plain = (f"{verdict} After delivery costs on every sale, refunded or not, you keep {ca:g} instead of {cb:g}: "
                 + ("the stronger guarantee pays." if ca > cb else "the stronger guarantee does NOT pay."))
    return result(vals, plain, ["OF-066 [stated, derived]"], notes, ["Only promise a guarantee you can afford to honor."])


def cmd_affiliate_payout(a):
    gp, ratio = positive("gross-profit", a.gross_profit), positive("ratio", a.ratio)
    try:
        mix = [float(x) for x in a.mix.split(",")]
    except ValueError:
        raise InputError("mix must be three comma-separated numbers, e.g. 20,20,60")
    if len(mix) != 3 or abs(sum(mix) - 100) > 1e-6 or min(mix) < 0:
        raise InputError("mix must be three non-negative numbers that sum to 100")
    max_payout = gp / (ratio + 1)
    tiers = [max_payout * s for s in AFFILIATE_TIER_SHARES]
    blended = sum(t * m / 100 for t, m in zip(tiers, mix))
    vals = {"ratio_input": ratio, "mix_used_pct": mix, "max_allowable_payout": round(max_payout, 2), "business_keeps_at_max_payout": round(gp - max_payout, 2),
            "tier_payouts_25_50_100pct": [round(t, 2) for t in tiers], "blended_payout_for_mix": round(blended, 2),
            "ratio_business_share_to_payout_at_blend": round((gp - blended) / blended, 2) if blended else None,
            "ratio_gross_profit_to_payout_at_max": round(gp / max_payout, 2)}
    return result(vals, f"The most you can pay an affiliate per customer is {max_payout:g}; the blended payout is {blended:g}.",
                  ["LD-090 [stated, FLAG]"],
                  [f"You set ratio={ratio:g} and mix={'/'.join(f'{m:g}' for m in mix)}. The book's example mix is 20/20/60 (LD-090); it is a default only, not advice.",
                   f"Definition used: the business keeps {ratio:g} parts and the affiliate gets 1 part of the gross profit per customer (LD-090: $160 gross profit, '3:1' -> $120 kept, $40 max payout).",
                   "[FLAG] LD-090 calls this '3:1' although gross profit divided by payout is 4:1 ($160 / $40); 'improved to 4:1' divides $120 by $30; counting the $10 saved gives $130 / $30 = 4.33:1. "
                   "Always say which ratio you are showing."],
                  ["Check the rules on affiliate payments and disclosure before you start paying anyone."])


def cmd_affiliate_return(a):
    cac, monthly, months = positive("affiliate-cac", a.affiliate_cac), nonneg("monthly-sales", a.monthly_sales), nonneg("months", a.months)
    margin, payout = pct("margin-pct", a.margin_pct), pct("payout-pct-of-gp", a.payout_pct_of_gp)
    sales = monthly * months
    cogs = sales * (1 - margin / 100)
    gp = sales - cogs
    paid = gp * payout / 100
    left = gp - paid
    return result({"total_sales": round(sales, 2), "cost_of_goods": round(cogs, 2), "gross_profit": round(gp, 2), "payout": round(paid, 2),
                   "left_after_payout": round(left, 2), "left_to_affiliate_cac": round(left / cac, 2)},
                  f"Each affiliate brings {left:g} after payout against {cac:g} to win them: {left / cac:.1f} to 1.",
                  ["LD-095 [stated, FLAG: arithmetic]"],
                  ["The book's example ($4,000; $10,000/mo for 12 months; 75% margin; 40% payout) leaves $54,000; $54,000 / $4,000 = 13.5, but the book prints 12.5:1.",
                   "'LTGP' here is net of the payout; the example ignores the cost of running the program (Prestige Labs spent over $1,000,000, LD-094)."])


def cmd_referral_growth(a):
    ref, ch = pct("referred-pct", a.referred_pct), pct("churn-pct", a.churn_pct)
    net = ref - ch
    return result({"net_monthly_growth_pct": round(net, 2)},
                  f"Referrals add {ref:g}% a month and churn removes {ch:g}%, so the base grows {net:g}% a month.",
                  ["LD-070 [stated]"],
                  ["LD-070: % referred monthly minus % churned monthly = % monthly compounding growth. [FLAG] The book's 'referrals cost nothing' example conflicts with paying referrers."])


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--mode", choices=["strategist", "client"], default="strategist")
    common = argparse.ArgumentParser(add_help=False)   # also accept --json / --mode after the subcommand
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    common.add_argument("--mode", choices=["strategist", "client"], default=argparse.SUPPRESS)
    sub = p.add_subparsers(dest="command", required=True)

    def add(name, fn, required=(), optional=(), **special):
        sp = sub.add_parser(name, parents=[common])
        for flag in required:
            sp.add_argument(f"--{flag}", type=float, required=True)
        for flag in optional:
            sp.add_argument(f"--{flag}", type=float)
        for flag, kwargs in special.items():
            sp.add_argument("--" + flag.replace("_", "-"), **kwargs)
        sp.set_defaults(func=fn)
        return sp

    add("thirty-day", cmd_thirty_day, ["acquisition-cost", "collected", "pass-mark"], ["delivery-cost"],
        collected_as=dict(choices=["revenue", "cash", "gross-profit"], required=True),
        costs=dict(choices=["acquisition", "acquisition+delivery"], required=True))
    sp = add("efficiency", cmd_efficiency, ["ltgp", "cac"], ["industry-cac", "monthly-gross-profit"])
    sp.add_argument("--pattern-ratio", type=float, default=LTGP_CAC_PATTERN)
    sp.add_argument("--industry-multiple", type=float, default=CAC_INDUSTRY_PATTERN)
    add("lifetime-gross-profit", cmd_lifetime_gross_profit, [], ["revenue-per-period", "margin-pct", "periods", "price", "delivery-cost", "purchases"])
    add("growth-ceiling", cmd_growth_ceiling, ["new-per-month", "ltgp"])
    add("funnel", cmd_funnel, ["lead-cost", "book-pct", "show-pct", "close-pct"], ["price"])
    sp = sub.add_parser("stack", parents=[common])
    sp.add_argument("--offer", action="append")
    sp.set_defaults(func=cmd_stack)
    sp = add("continuity", cmd_continuity, ["price", "margin-pct", "churn-pct"])
    sp.add_argument("--horizon-months", type=int)
    add("standalone", cmd_standalone, ["continuity-monthly", "share-pct"], reading=dict(choices=["text", "examples"], required=True))
    sp = add("rollover", cmd_rollover, ["next-price", "credit"])
    sp.add_argument("--months", type=int)
    sp = add("billing", cmd_billing, ["price", "margin-pct"])
    sp.add_argument("--fee-pct", type=float, default=3.0)
    add("plan-check", cmd_plan_check, ["leads", "sold-before", "paid-full-before", "sold-after", "paid-full-after"], ["leads-after"])
    sp = add("ad-budget", cmd_ad_budget, [], ["first-30d-amount", "customers-wanted", "cac"], basis=dict(choices=["cash", "gross-profit"]))
    sp.add_argument("--buffer-pct", type=float, default=AD_SCALE_BUFFER * 100 - 100)
    add("outreach", cmd_outreach, ["actions-per-week", "reply-pct", "accept-pct", "convert-pct"], ["price"])
    sp = sub.add_parser("value-compare", parents=[common])
    sp.add_argument("--a", required=True)
    sp.add_argument("--b")
    sp.set_defaults(func=cmd_value_compare)
    add("guarantee", cmd_guarantee, ["sales-before", "refund-before-pct", "sales-after", "refund-after-pct"], ["price", "delivery-cost-per-sale"])
    sp = add("affiliate-payout", cmd_affiliate_payout, ["gross-profit", "ratio"], [])
    sp.add_argument("--mix", default="20,20,60")
    add("affiliate-return", cmd_affiliate_return, ["affiliate-cac", "monthly-sales", "months", "margin-pct", "payout-pct-of-gp"])
    add("referral-growth", cmd_referral_growth, ["referred-pct", "churn-pct"])
    return p


def emit(res, args):
    if args.json:
        if args.mode == "client":
            res = {"values": res["values"], "plain": res["plain"], "client_warnings": res["client_warnings"]}
        print(json.dumps(res, indent=2))
        return
    if args.mode == "client":
        print(res["plain"])
        for w in res["client_warnings"]:
            print("Careful: " + w)
        return
    for key, value in res["values"].items():
        print(f"{key}: {json.dumps(value) if isinstance(value, (list, dict)) else value}")
    print("Sources: " + "; ".join(res["sources"]))
    for n in res["notes"]:
        print("Note: " + n)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        res = args.func(args)
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    emit(res, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
