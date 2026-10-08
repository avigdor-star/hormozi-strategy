#!/usr/bin/env python3
"""State manager for the growth-strategy-coach skill: scaffold, create records, find due items, validate, rank ideas, set audience. No dependencies.

  state.py init     [--dir coach-state]
  state.py new      <decision|experiment|offer|channel|session|review> "Title" [--dir coach-state]
  state.py due      [--dir coach-state] [--days 7] [--today YYYY-MM-DD]
  state.py validate [--dir coach-state]
  state.py ice      "Idea A=8,6,7" "Idea B=5,9,9"      (Impact,Confidence,Ease each 1-10; coach scale, not from the books)
  state.py audience [--set strategist|client] [--dir coach-state]   (who the skill is talking to)

State is plain Markdown in a user-owned folder. Never overwrites existing files.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / "assets" / "templates"
DEFAULT_DIR = "coach-state"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_OPEN_PER_OWNER = 3

ROOT_FILES = {  # template -> filename in state folder
    "dashboard.md": "00-dashboard.md", "profile.md": "profile.md", "money-model-map.md": "money-model-map.md",
    "assumptions.md": "assumptions.md", "commitments.md": "commitments.md", "open-questions.md": "open-questions.md",
}
KINDS = {  # kind -> (subfolder, id prefix, template)
    "decision": ("decisions", "DEC", "decision-record.md"),
    "experiment": ("experiments", "EXP", "experiment-card.md"),
    "offer": ("offers", "OFR", "offer-card.md"),
    "channel": ("channels", "CH", "channel-card.md"),
    "session": ("sessions", None, "session-log.md"),
    "review": ("reviews", None, "weekly-review.md"),
}
REQUIRED = {
    "decisions": ["id", "title", "status", "door", "decided_on", "review_date", "confidence", "owner"],
    "experiments": ["id", "title", "status", "owner", "start", "end", "metric", "threshold", "kill_criteria"],
    "offers": ["id", "title", "type", "stage", "status", "owner"],
    "channels": ["id", "title", "status", "channel_type", "owner", "review_date"],
}
DATE_KEYS = {"decided_on", "review_date", "start", "end", "created", "started"}
CHANNEL_TYPES = {"warm", "content", "cold", "paid", "referral", "employees", "agency", "affiliate", "other"}
STATUSES = {
    "decisions": {"proposed", "accepted", "superseded", "rejected"},
    "experiments": {"planned", "running", "done", "killed"},
    "offers": {"draft", "testing", "live", "retired"},
    "channels": {"idea", "testing", "live", "paused", "retired"},
}
COMMIT_STATUSES = {"open", "doing", "done", "dropped"}
DOOR_VALUES = {"two-way", "one-way"}


def check_dir(path):
    """Refuse a state folder inside this skill's own folder."""
    try:
        Path(path).resolve().relative_to(SKILL_DIR)
    except ValueError:
        return True
    print(f"error: {path} is inside the skill folder; keep state in the user's own folder", file=sys.stderr)
    return False


def today_str(override=None):
    return override or dt.date.today().isoformat()


def parse_date(text):
    if not text or not DATE_RE.match(text):
        return None
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        return None


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            data[key.strip()] = value.split("#")[0].strip() if key.strip() in DATE_KEYS else value.strip()
    return data


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:50] or "untitled"


def next_number(folder, prefix):
    nums = [int(m.group(1)) for p in folder.glob(f"{prefix}-*.md") if (m := re.match(rf"{prefix}-(\d+)", p.name))]
    return max(nums, default=0) + 1


def render(template_name, **values):
    text = (TEMPLATES / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def table_rows(text):
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0].lower() in {"id", "#"} or set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def cmd_init(args):
    root = Path(args.dir)
    if not check_dir(root):
        return 2
    created, skipped = [], []
    root.mkdir(parents=True, exist_ok=True)
    for sub in ("decisions", "experiments", "offers", "channels", "sessions", "reviews"):
        (root / sub).mkdir(exist_ok=True)
    for template, name in ROOT_FILES.items():
        target = root / name
        if target.exists():
            skipped.append(name)
            continue
        target.write_text(render(template, DATE=today_str(), TITLE=""), encoding="utf-8")
        created.append(name)
    print(f"state folder: {root.resolve()}")
    print(f"created: {', '.join(created) or 'nothing'}")
    print(f"kept existing: {', '.join(skipped) or 'nothing'}")
    return 0


def cmd_new(args):
    root = Path(args.dir)
    if not check_dir(root):
        return 2
    if not root.exists():
        print(f"error: {root} not found; run init first", file=sys.stderr)
        return 2
    folder_name, prefix, template = KINDS[args.kind]
    folder = root / folder_name
    folder.mkdir(exist_ok=True)
    today = today_str()
    if prefix:
        ident = f"{prefix}-{next_number(folder, prefix):03d}"
        path = folder / f"{ident}-{slugify(args.title)}.md"
    else:
        ident = ""
        suffix = "-weekly" if args.kind == "review" else ""
        path = folder / f"{today}{suffix}.md"
        n = 2
        while path.exists():
            path = folder / f"{today}{suffix}-{n}.md"
            n += 1
    path.write_text(render(template, ID=ident, TITLE=args.title, DATE=today), encoding="utf-8")
    print(path)
    return 0


def load_records(root, folder_name):
    for path in sorted((root / folder_name).glob("*.md")):
        yield path, frontmatter(path.read_text(encoding="utf-8"))


def cmd_due(args):
    root = Path(args.dir)
    if not check_dir(root):
        return 2
    today = parse_date(today_str(args.today))
    if today is None:
        print("error: --today must be YYYY-MM-DD", file=sys.stderr)
        return 2
    horizon = today + dt.timedelta(days=args.days)
    overdue, soon = [], []

    commit_path = root / "commitments.md"
    if commit_path.exists():
        for cells in table_rows(commit_path.read_text(encoding="utf-8")):
            if len(cells) < 5 or cells[4].lower() in {"done", "dropped"}:
                continue
            due = parse_date(cells[3])
            label = f"{cells[0]} {cells[1]} (owner: {cells[2] or '?'}, due {cells[3] or '?'})"
            if due is None:
                overdue.append(f"commitment missing/invalid due date: {label}")
            elif due < today:
                overdue.append(f"commitment overdue: {label}")
            elif due <= horizon:
                soon.append(f"commitment due soon: {label}")

    for path, fm in load_records(root, "decisions"):
        if fm.get("status") in {"superseded", "rejected"}:
            continue
        review = parse_date(fm.get("review_date", ""))
        if review is None:
            overdue.append(f"decision has no valid review_date: {path.name}")
        elif review < today:
            overdue.append(f"decision review overdue: {path.name} (was {fm['review_date']})")
        elif review <= horizon:
            soon.append(f"decision review soon: {path.name} ({fm['review_date']})")

    for path, fm in load_records(root, "experiments"):
        status, end, start = fm.get("status"), parse_date(fm.get("end", "")), parse_date(fm.get("start", ""))
        if status == "running" and end and end < today:
            overdue.append(f"experiment past end date, needs result + decision: {path.name} (end {fm['end']})")
        elif status == "planned" and start and start < today:
            overdue.append(f"experiment should have started: {path.name} (start {fm['start']})")
        elif status in {"running", "planned"} and end and end <= horizon:
            soon.append(f"experiment ending soon: {path.name} (end {fm['end']})")

    for path, fm in load_records(root, "channels"):
        if fm.get("status") == "retired":
            continue
        review = parse_date(fm.get("review_date", ""))
        if review is None:
            overdue.append(f"channel has no valid review_date: {path.name}")
        elif review < today:
            overdue.append(f"channel review overdue: {path.name} (was {fm['review_date']})")
        elif review <= horizon:
            soon.append(f"channel review soon: {path.name} ({fm['review_date']})")

    print(f"as of {today}")
    print("OVERDUE:" if overdue else "OVERDUE: none")
    for item in overdue:
        print(f"  - {item}")
    print(f"DUE WITHIN {args.days} DAYS:" if soon else f"DUE WITHIN {args.days} DAYS: none")
    for item in soon:
        print(f"  - {item}")
    return 0


def cmd_validate(args):
    root = Path(args.dir)
    if not check_dir(root):
        return 2
    if not root.exists():
        print(f"error: {root} not found", file=sys.stderr)
        return 2
    errors, warnings = [], []

    for folder_name, keys in REQUIRED.items():
        for path, fm in load_records(root, folder_name):
            if fm.get("status") == "superseded":
                continue
            for key in keys:
                if folder_name == "decisions" and key == "decided_on" and fm.get("status") == "proposed":
                    continue
                if not fm.get(key):
                    errors.append(f"{folder_name}/{path.name}: empty required field '{key}'")
            for key in DATE_KEYS & set(fm):
                if fm[key] and parse_date(fm[key]) is None:
                    errors.append(f"{folder_name}/{path.name}: '{key}' must be YYYY-MM-DD (got '{fm[key]}')")
            if fm.get("status") and fm["status"] not in STATUSES[folder_name]:
                errors.append(f"{folder_name}/{path.name}: invalid status '{fm['status']}'")
            if folder_name == "decisions" and fm.get("door") and fm["door"] not in DOOR_VALUES:
                errors.append(f"decisions/{path.name}: door must be two-way or one-way")
            if folder_name == "channels" and fm.get("channel_type") and fm["channel_type"] not in CHANNEL_TYPES:
                errors.append(f"channels/{path.name}: channel_type must be one of {sorted(CHANNEL_TYPES)}")
            if fm.get("id") and not path.name.startswith(fm["id"]):
                errors.append(f"{folder_name}/{path.name}: id '{fm['id']}' does not match filename")

    commit_path = root / "commitments.md"
    if commit_path.exists():
        open_by_owner = {}
        for cells in table_rows(commit_path.read_text(encoding="utf-8")):
            if len(cells) != 6:
                errors.append(f"commitments.md: row has {len(cells)} columns, expected 6: {' | '.join(cells)[:60]}")
                continue
            cid, _action, owner, due, status, done_means = cells
            if status.lower() not in COMMIT_STATUSES:
                errors.append(f"commitments.md {cid}: invalid status '{status}'")
            if parse_date(due) is None:
                errors.append(f"commitments.md {cid}: due must be YYYY-MM-DD (got '{due}')")
            if not owner:
                errors.append(f"commitments.md {cid}: missing owner")
            if not done_means:
                warnings.append(f"commitments.md {cid}: empty 'Done means'")
            if status.lower() in {"open", "doing"}:
                open_by_owner[owner] = open_by_owner.get(owner, 0) + 1
        for owner, count in open_by_owner.items():
            if count > MAX_OPEN_PER_OWNER:
                warnings.append(f"commitments.md: {owner or '(no owner)'} has {count} open items (limit {MAX_OPEN_PER_OWNER})")

    running_by_stage = {}
    for _p, fm in load_records(root, "experiments"):
        if fm.get("status") == "running":
            stage = fm.get("stage") or "unspecified"
            running_by_stage[stage] = running_by_stage.get(stage, 0) + 1
    for stage, count in running_by_stage.items():
        if count > 1:
            warnings.append(f"{count} experiments running in stage '{stage}'; WIP limit is 1 per stage (set 'stage:' on each experiment card)")

    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN:  {item}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


AUDIENCES = {"strategist", "client"}


def cmd_audience(args):
    root = Path(args.dir)
    if not check_dir(root):
        return 2
    profile = root / "profile.md"
    if not profile.exists():
        print(f"error: {profile} not found; run init first", file=sys.stderr)
        return 2
    text = profile.read_text(encoding="utf-8")
    if args.set:
        if args.set not in AUDIENCES:
            print("error: --set must be strategist or client", file=sys.stderr)
            return 2
        if re.search(r"^audience:.*$", text, re.M):
            text = re.sub(r"^audience:.*$", f"audience: {args.set}", text, count=1, flags=re.M)
        else:
            text = text.replace("---\n", f"---\naudience: {args.set}\n", 1)
        profile.write_text(text, encoding="utf-8")
    fm = frontmatter(text)
    print(f"audience: {fm.get('audience') or 'not set'}")
    return 0


def cmd_ice(args):
    scored = []
    for item in args.ideas:
        name, sep, nums = item.rpartition("=")
        parts = nums.split(",")
        try:
            i, c, e = (float(x) for x in parts)
        except ValueError:
            print(f'error: "{item}" must look like Name=impact,confidence,ease', file=sys.stderr)
            return 2
        if not sep or len(parts) != 3 or not all(1 <= v <= 10 for v in (i, c, e)):
            print(f'error: "{item}" needs Name=I,C,E with each value 1-10', file=sys.stderr)
            return 2
        scored.append((i * c * e, name, i, c, e))
    for rank, (score, name, i, c, e) in enumerate(sorted(scored, reverse=True), 1):
        print(f"{rank}. {name}: ICE {score:g} (I{i:g} C{c:g} E{e:g})")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)
    for name, fn in (("init", cmd_init), ("due", cmd_due), ("validate", cmd_validate)):
        sp = sub.add_parser(name)
        sp.add_argument("--dir", default=DEFAULT_DIR)
        if name == "due":
            sp.add_argument("--days", type=int, default=7)
            sp.add_argument("--today")
        sp.set_defaults(func=fn)
    sp = sub.add_parser("new")
    sp.add_argument("kind", choices=sorted(KINDS))
    sp.add_argument("title")
    sp.add_argument("--dir", default=DEFAULT_DIR)
    sp.set_defaults(func=cmd_new)
    sp = sub.add_parser("audience")
    sp.add_argument("--set")
    sp.add_argument("--dir", default=DEFAULT_DIR)
    sp.set_defaults(func=cmd_audience)
    sp = sub.add_parser("ice")
    sp.add_argument("ideas", nargs="+")
    sp.set_defaults(func=cmd_ice)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
