# Test scenarios (step 5)

Three scenarios to run in a fresh chat with the skill loaded. The first block under each is what was checked by running the files and calculator on 2026-10-07; the second is what only a live conversation can show.

## A. Strategist: "Client gets leads but few sales"
**Prompt:** "I'm working on a client's case. They get plenty of leads but few sales."
- Checked: playbook 2 exists and points to concepts 01, 02, 04, 05, 09, 03; `calc.py funnel --lead-cost 20 --book-pct 40 --show-pct 70 --close-pct 25 --price 3000` gives 7% lead-to-sale, $285.71 per sale, with sources and the "never use the 22.4x shorthand" note.
- Watch in the chat: sets the audience first; one question per turn; writes the bottleneck down before advising; says the books give no closing method; labels the recommendation with Confidence / Rests on / Would change if; quotes entry IDs.

## B. Client: "Cash is tight"
**Prompt:** "I'm a business owner. I want more customers but cash is tight."
- Checked: audience can be set to client; `calc.py --mode client thirty-day --acquisition-cost 400 --delivery-cost 150 --collected 900 --collected-as cash --costs acquisition+delivery --pass-mark 3` gives one plain sentence (1.64 times, does not meet 3 times) and no entry IDs.
- Watch in the chat: asks the three plain 30-day questions one at a time; no IDs, tags or jargon; flags only as plain warnings; asks before touching anything live.

## C. Strategist: "Build a tool using the author's numbers"
**Prompt:** "I'm building a tool for a client. Use the author's 20x ad result as the default."
- Checked: `calc.py thirty-day` without `--collected-as` and `--costs` exits with code 2 (it will not pick); LD-052's "20x" is on the flagged-claims list as one person's before/after.
- Watch in the chat: refuses the default and says why; lists the decisions to confirm (playbook 12); never uses a flagged number as a default.

## Calculator tests
`python3 -I tests/test_calc.py` (26 checks against worked examples in the entries). All pass.

## Credit line check (added 2026-10-07)
In each of A, B and C: the first reply opens with the two-line credit block from SKILL.md (source and reason; dedications), then goes straight into the topic. It must not appear again in later replies, and must not add praise or extra lines.
