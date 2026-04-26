German A1 → B1 Study Push Setup (90-Day Plan)

Files:
  /Users/sijia/german-study/site/plan.json          (full 90-day curriculum — A1/A2/B1)
  /Users/sijia/german-study/site/today.json          (today's lesson data)
  /Users/sijia/german-study/site/index.html           (study dashboard webpage)
  /Users/sijia/german-study/daily_push.py             (run to generate today's lesson)
  /Users/sijia/german-study/config.json               (start date, levels, settings)
  /Users/sijia/german-study/plan_resources.json       (graded resources per level)
  /Users/sijia/german-study/logs/daily_push.log       (run logs)

Levels:
  Days 1-30:   A1 — Foundations (Survival German)
  Days 31-60:  A2 — Everyday Communication
  Days 61-90:  B1 — Independent Expression

Run manually (prints today's goal):
  python3 /Users/sijia/german-study/daily_push.py

Open study dashboard:
  open /Users/sijia/german-study/site/index.html

Cron delivery:
  The script outputs formatted text ready for delivery.
  Last plan: Telegram via hermes_bot cron (not iMessage — no Full Disk Access needed).
