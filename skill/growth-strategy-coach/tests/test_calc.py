"""Checks the calculator against the worked examples in the framework entries. Run: python3 -I tests/test_calc.py"""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import calc  # noqa: E402


def run(*argv, mode=None):
    out, err = io.StringIO(), io.StringIO()
    args = (["--mode", mode] if mode else ["--json"]) + list(argv)
    if mode is None:
        args = ["--json"] + list(argv)
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = calc.main(args)
    return code, out.getvalue(), err.getvalue()


def vals(*argv):
    code, out, err = run(*argv)
    assert code == 0, err
    return json.loads(out)["values"]


class Calc(unittest.TestCase):
    def test_thirty_day_ld061_example(self):  # LD-061: $10 + 20% x $100 = $30 against CAC $30
        v = vals("thirty-day", "--acquisition-cost", "30", "--collected", "30", "--collected-as", "gross-profit",
                 "--costs", "acquisition", "--pass-mark", "1")
        self.assertEqual(v["ratio"], 1.0)
        self.assertTrue(v["meets_pass_mark"])

    def test_thirty_day_refuses_double_count(self):
        code, _, err = run("thirty-day", "--acquisition-cost", "30", "--delivery-cost", "5", "--collected", "30",
                           "--collected-as", "gross-profit", "--costs", "acquisition+delivery", "--pass-mark", "1")
        self.assertEqual(code, 2)
        self.assertIn("double counts", err)

    def test_thirty_day_needs_delivery_cost_when_counted(self):
        code, _, _ = run("thirty-day", "--acquisition-cost", "30", "--collected", "100", "--collected-as", "cash",
                         "--costs", "acquisition+delivery", "--pass-mark", "2")
        self.assertEqual(code, 2)

    def test_thirty_day_choices_are_required(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            calc.main(["thirty-day", "--acquisition-cost", "30", "--collected", "30", "--pass-mark", "1"])

    def test_thirty_day_warns_when_delivery_ignored(self):
        code, out, _ = run("thirty-day", "--acquisition-cost", "30", "--collected", "100", "--collected-as", "cash",
                           "--costs", "acquisition", "--pass-mark", "2")
        self.assertEqual(code, 0)
        self.assertIn("Delivery cost is ignored", out)

    def test_lifetime_gross_profit_of008(self):  # $1,000/mo x 90% x 5 months = $4,500
        self.assertEqual(vals("lifetime-gross-profit", "--revenue-per-period", "1000", "--margin-pct", "90", "--periods", "5")["lifetime_gross_profit"], 4500)

    def test_lifetime_gross_profit_ld060(self):  # $15 sale, $5 delivery, ten purchases = $100
        self.assertEqual(vals("lifetime-gross-profit", "--price", "15", "--delivery-cost", "5", "--purchases", "10")["lifetime_gross_profit"], 100)

    def test_efficiency_ld061(self):  # LTGP $100, CAC $30 -> 3.33
        v = vals("efficiency", "--ltgp", "100", "--cac", "30", "--industry-cac", "10", "--monthly-gross-profit", "10")
        self.assertEqual(v["ltgp_to_cac"], 3.33)
        self.assertEqual(v["max_cac_at_pattern_ratio"], 33.33)
        self.assertEqual(v["cac_vs_industry_multiple"], 3.0)
        self.assertEqual(v["monthly_payments_to_recover_cac"], 3.0)

    def test_growth_ceiling_of006(self):
        self.assertEqual(vals("growth-ceiling", "--new-per-month", "10", "--ltgp", "1000")["ceiling_gross_profit_per_month"], 10000)

    def test_funnel_mm002(self):  # $5 per lead, half show, half of those buy -> $20 per customer
        v = vals("funnel", "--lead-cost", "5", "--book-pct", "100", "--show-pct", "50", "--close-pct", "50", "--price", "600")
        self.assertEqual(v["cost_per_sale"], 20)
        self.assertEqual(v["revenue_per_lead"], 150)

    def test_continuity_churn(self):
        self.assertEqual(vals("continuity", "--price", "50", "--margin-pct", "100", "--churn-pct", "10")["avg_months_retained"], 10)

    def test_standalone_mm056_examples(self):  # $199 membership; $399 standalone at 50%, $799 at 90%
        v50 = vals("standalone", "--continuity-monthly", "199", "--share-pct", "50", "--reading", "examples")
        v90 = vals("standalone", "--continuity-monthly", "199", "--share-pct", "90", "--reading", "examples")
        self.assertAlmostEqual(v50["standalone_price"], 399, delta=399 * 0.01)
        self.assertAlmostEqual(v90["standalone_price"], 799, delta=799 * 0.01)
        t50 = vals("standalone", "--continuity-monthly", "199", "--share-pct", "50", "--reading", "text")
        self.assertAlmostEqual(t50["standalone_price"], 264.67, places=2)
        self.assertAlmostEqual(t50["other_reading_would_give"], v50["standalone_price"], places=2)

    def test_standalone_reading_required_and_range(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            calc.main(["standalone", "--continuity-monthly", "199", "--share-pct", "50"])
        self.assertEqual(run("standalone", "--continuity-monthly", "199", "--share-pct", "40", "--reading", "text")[0], 2)

    def test_rollover_mm012(self):  # $600 credit against $2,400 = 25%, exactly the 4x boundary
        v = vals("rollover", "--next-price", "2400", "--credit", "600", "--months", "12")
        self.assertEqual(v["discount_pct"], 25.0)
        self.assertTrue(v["meets_4x_rule"])
        self.assertEqual(v["monthly_credit"], 50.0)
        self.assertFalse(vals("rollover", "--next-price", "2400", "--credit", "601")["meets_4x_rule"])

    def test_billing_mm059(self):  # 13/12 = +8.3%; 20% margin -> +41.7% profit; 3% fee on 10% margin -> +30%
        v = vals("billing", "--price", "100", "--margin-pct", "20")
        self.assertEqual(v["four_week_revenue_lift_pct"], 8.33)
        self.assertEqual(v["four_week_profit_lift_pct"], 41.7)
        self.assertEqual(vals("billing", "--price", "100", "--margin-pct", "10")["fee_profit_lift_pct"], 30.0)

    def test_plan_check(self):
        self.assertTrue(vals("plan-check", "--leads", "100", "--sold-before", "30", "--paid-full-before", "20",
                             "--sold-after", "40", "--paid-full-after", "15")["cannibalized"])

    def test_ad_budget_ld059(self):  # $12,000 over 30 days = $400/day
        v = vals("ad-budget", "--first-30d-amount", "450", "--basis", "cash", "--customers-wanted", "10", "--cac", "1000")
        self.assertEqual(v["test_spend_cap_per_ad"], 900)
        self.assertEqual(v["stop_line_with_zero_leads"], 450)
        self.assertEqual(v["scale_budget_per_30_days"], 12000)
        self.assertEqual(v["scale_budget_per_day"], 400)
        self.assertEqual(run("ad-budget", "--first-30d-amount", "450")[0], 2)

    def test_value_compare_is_relative_and_checks_range(self):
        v = vals("value-compare", "--a", "8,6,3,4", "--b", "5,5,5,5")
        self.assertEqual(v["offer_a_relative_score"], 4.0)
        self.assertEqual(v["offer_b_relative_score"], 1.0)
        self.assertNotIn("max_possible", v)
        self.assertEqual(run("value-compare", "--a", "11,6,3,4")[0], 2)

    def test_guarantee_of066(self):  # 100 sales/5% vs 130 sales/10% -> 95 vs 117; break-even x1.056
        v = vals("guarantee", "--sales-before", "100", "--refund-before-pct", "5", "--sales-after", "130", "--refund-after-pct", "10")
        self.assertEqual((v["net_sales_before"], v["net_sales_after"]), (95.0, 117.0))
        self.assertEqual(v["net_lift_multiple"], 1.232)
        self.assertEqual(v["sales_multiple_needed_to_break_even"], 1.056)

    def test_guarantee_with_delivery_cost(self):
        v = vals("guarantee", "--sales-before", "100", "--refund-before-pct", "5", "--sales-after", "130", "--refund-after-pct", "10",
                 "--price", "100", "--delivery-cost-per-sale", "60")
        self.assertEqual(v["contribution_before"], 95 * 100 - 100 * 60)
        self.assertEqual(v["contribution_after"], 117 * 100 - 130 * 60)

    def test_affiliate_payout_ld090(self):  # $160 gross profit at "3:1" -> $40 max; blend 20/20/60 -> $30
        v = vals("affiliate-payout", "--gross-profit", "160", "--ratio", "3")
        self.assertEqual(v["max_allowable_payout"], 40.0)
        self.assertEqual(v["business_keeps_at_max_payout"], 120.0)
        self.assertEqual(v["tier_payouts_25_50_100pct"], [10.0, 20.0, 40.0])
        self.assertEqual(v["blended_payout_for_mix"], 30.0)
        self.assertEqual(v["ratio_business_share_to_payout_at_blend"], 4.33)
        self.assertEqual(v["ratio_gross_profit_to_payout_at_max"], 4.0)

    def test_affiliate_return_ld095_corrects_book(self):  # the book prints 12.5:1; the arithmetic is 13.5:1
        v = vals("affiliate-return", "--affiliate-cac", "4000", "--monthly-sales", "10000", "--months", "12", "--margin-pct", "75", "--payout-pct-of-gp", "40")
        self.assertEqual(v["left_after_payout"], 54000.0)
        self.assertEqual(v["left_to_affiliate_cac"], 13.5)

    def test_referral_growth_ld070(self):
        self.assertEqual(vals("referral-growth", "--referred-pct", "10", "--churn-pct", "4")["net_monthly_growth_pct"], 6.0)

    def test_stack_and_outreach_run(self):
        v = vals("stack", "--offer", "front:100:50", "--offer", "upsell:500:10")
        self.assertEqual(v["expected_amount_per_front_customer"], 100.0)
        self.assertEqual(vals("outreach", "--actions-per-week", "100", "--reply-pct", "50", "--accept-pct", "20", "--convert-pct", "10")["customers_per_week"], 1.0)

    def test_client_mode_is_plain_and_short(self):
        code, out, _ = run("efficiency", "--ltgp", "100", "--cac", "30", mode="client")
        self.assertEqual(code, 0)
        self.assertNotIn("LD-0", out)
        self.assertNotIn("Sources", out)
        self.assertLess(len(out.split()), 70)

    def test_flags_work_after_the_command_name(self):
        code, out, _ = run("efficiency", "--ltgp", "100", "--cac", "30", "--mode", "client")
        self.assertEqual(code, 0)
        self.assertNotIn("Sources", out)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(calc.main(["referral-growth", "--referred-pct", "10", "--churn-pct", "4", "--json"]), 0)

    def test_client_json_has_no_ids_or_notes(self):
        code, out, _ = run("--mode", "client", "referral-growth", "--referred-pct", "10", "--churn-pct", "4")
        self.assertEqual(code, 0)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            calc.main(["--mode", "client", "--json", "referral-growth", "--referred-pct", "10", "--churn-pct", "4"])
        data = json.loads(buf.getvalue())
        self.assertNotIn("sources", data)
        self.assertNotIn("notes", data)
        self.assertNotIn("LD-", buf.getvalue())

    def test_client_guarantee_uses_contribution(self):
        code, out, _ = run("--mode", "client", "guarantee", "--sales-before", "100", "--refund-before-pct", "5", "--sales-after", "130",
                           "--refund-after-pct", "10", "--price", "100", "--delivery-cost-per-sale", "90")
        self.assertIn("does NOT pay", out)

    def test_client_ad_budget_and_plan_check_show_numbers(self):
        _, out, _ = run("--mode", "client", "ad-budget", "--first-30d-amount", "100", "--basis", "cash", "--customers-wanted", "10", "--cac", "1000")
        self.assertIn("12000", out)
        self.assertIn("200", out)
        _, out, _ = run("--mode", "client", "plan-check", "--leads", "100", "--sold-before", "30", "--paid-full-before", "20",
                        "--sold-after", "40", "--paid-full-after", "25")
        self.assertIn("30%", out)

    def test_plan_check_says_when_closes_fell(self):
        v = vals("plan-check", "--leads", "100", "--sold-before", "40", "--paid-full-before", "20", "--sold-after", "30", "--paid-full-after", "20")
        self.assertEqual(v["verdict"], "The close rate fell.")

    def test_bad_numbers_are_rejected(self):
        self.assertEqual(run("billing", "--price", "0", "--margin-pct", "50")[0], 2)
        self.assertEqual(run("efficiency", "--ltgp", "nan", "--cac", "30")[0], 2)
        self.assertEqual(run("efficiency", "--ltgp", "inf", "--cac", "30")[0], 2)
        self.assertEqual(run("rollover", "--next-price", "100", "--credit", "125")[0], 2)
        self.assertEqual(run("rollover", "--next-price", "100", "--credit", "10", "--months", "-3")[0], 2)
        self.assertEqual(run("continuity", "--price", "50", "--margin-pct", "50", "--churn-pct", "10", "--horizon-months", "-1")[0], 2)
        self.assertEqual(run("lifetime-gross-profit", "--revenue-per-period", "100", "--margin-pct", "50", "--periods", "2", "--price", "10",
                             "--delivery-cost", "1", "--purchases", "2")[0], 2)

    def test_affiliate_payout_needs_a_ratio(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            calc.main(["affiliate-payout", "--gross-profit", "160"])

    def test_efficiency_pattern_is_an_input(self):
        v = vals("efficiency", "--ltgp", "100", "--cac", "30", "--pattern-ratio", "4")
        self.assertEqual(v["pattern_ratio_used"], 4.0)
        self.assertEqual(v["max_cac_at_pattern_ratio"], 25.0)

    def test_invalid_input_exit_code(self):
        self.assertEqual(run("efficiency", "--ltgp", "100", "--cac", "0")[0], 2)
        self.assertEqual(run("billing", "--price", "100", "--margin-pct", "150")[0], 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
