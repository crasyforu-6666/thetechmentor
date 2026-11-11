#!/usr/bin/env python3
"""Decide what (if anything) is due right now and run it.

GitHub's scheduler delays and sometimes skips cron runs, so the workflow runs
every hour and this script publishes whatever today's plan still owes:
  by 08:45 IST -> 1 new article
  by 14:10 IST -> 1 refresh (rewrite of an old thin post)
  by 19:35 IST -> 2 new articles in total
Progress is stored in content/publish-state.json (committed with each run).
"""
import datetime
import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE_DIR, "content", "publish-state.json")
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
PLAN = [((8, 45), "new"), ((14, 10), "refresh"), ((19, 35), "new")]


def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    now = datetime.datetime.now(IST)
    today = now.date().isoformat()
    state = load()
    done = state.get(today, {"new": 0, "refresh": 0})
    due = {"new": 0, "refresh": 0}
    for (h, m), kind in PLAN:
        if (now.hour, now.minute) >= (h, m):
            due[kind] += 1
    mode = "new" if done["new"] < due["new"] else ("refresh" if done["refresh"] < due["refresh"] else None)
    print(f"[publish_due] {now:%Y-%m-%d %H:%M} IST done={done} due={due} -> {mode or 'nothing due'}")
    if not mode:
        return 0
    res = subprocess.run([sys.executable, os.path.join(BASE_DIR, "scripts", "auto_daily_blog_scheduler.py"),
                          "--mode", mode], cwd=BASE_DIR)
    if res.returncode != 0:
        return res.returncode
    done[mode] += 1
    state[today] = done
    for k in sorted(state)[:-14]:  # keep two weeks
        state.pop(k)
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
