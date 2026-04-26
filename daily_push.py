#!/usr/bin/env python3
"""German A1->B1 Daily Study Push Script (data-driven from plan.json)"""
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path('/Users/sijia/german-study')
SITE_DIR = ROOT / 'site'
LOG_DIR = ROOT / 'logs'
CONFIG_PATH = ROOT / 'config.json'
PLAN_JSON = SITE_DIR / 'plan.json'
TODAY_JSON = SITE_DIR / 'today.json'
HTML_PATH = SITE_DIR / 'index.html'
RUN_LOG = LOG_DIR / 'daily_push.log'
SLACK_CONFIG_PATH = ROOT / 'slack_config.json'


def load_json(path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def ensure_dirs():
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def find_today_task(plan, config):
    today = date.today()
    start = date.fromisoformat(config['start_date'])
    total = int(config['total_days'])
    day_num = (today - start).days + 1
    day_num = max(1, min(day_num, total))
    return plan[day_num - 1], day_num


def render_html(config, plan, today_task):
    rows = []
    for p in plan:
        rows.append(
            f"<tr class='lvl-{p['level']}'><td>{p['day']}</td><td>{p['date']}</td>"
            f"<td>{p['level']}</td><td>{p['phase']}</td>"
            f"<td>{p.get('topic','')}</td><td>{p.get('grammar_title','')}</td></tr>"
        )
    rows_html = '\n'.join(rows)

    vocab_lines = '\n'.join([
        f"<li><b>{w[0]}</b> - {w[1]}</li>" for w in today_task.get('vocabulary', [])
    ])
    ex_lines = '\n'.join([
        f"<li>{ex}</li>" for ex in today_task.get('exercises', [])
    ])

    level_colors = {'A1': '#22c55e', 'A2': '#3b82f6', 'B1': '#8b5cf6'}
    return _HTML_TEMPLATE.format(
        title=config['site_title'],
        start=config['start_date'],
        total=config['total_days'],
        levels=config.get('levels','A1-B1'),
        day=today_task['day'],
        pct=int(today_task['day']/int(config['total_days'])*100),
        level=today_task['level'],
        badge_color=level_colors.get(today_task['level'], '#6b7280'),
        phase=today_task['phase'],
        topic=today_task.get('topic',''),
        grammar_title=today_task.get('grammar_title',''),
        grammar_content=today_task.get('grammar_content',''),
        vocab_lines=vocab_lines,
        ex_lines=ex_lines,
        tip=today_task.get('tip',''),
        speaking=today_task.get('speaking_hw',''),
        writing=today_task.get('writing_hw',''),
        rows_html=rows_html,
    )


_HTML_TEMPLATE = """<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; margin: 24px; background:#f7f8fb; color:#1f2937; }}
    h1,h2,h3 {{ margin: 0 0 12px; }}
    .card {{ background: white; border-radius: 12px; padding: 16px 18px; box-shadow: 0 2px 10px rgba(0,0,0,.06); margin-bottom: 18px; }}
    table {{ width:100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ border:1px solid #e5e7eb; padding:8px; text-align:left; vertical-align: top; }}
    th {{ background:#f3f4f6; position: sticky; top: 0; }}
    .scroll {{ max-height: 520px; overflow:auto; border-radius: 10px; }}
    .meta {{ color:#4b5563; font-size:14px; }}
    .badge {{ display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:700; color:white; background:{badge_color}; }}
    .grammar {{ background:#fefce8; border-left:4px solid #eab308; padding:12px 16px; border-radius:0 8px 8px 0; margin:12px 0; white-space:pre-wrap; font-size:13px; font-family: monospace; }}
    .tip {{ background:#f0fdf4; border-left:4px solid #22c55e; padding:8px 14px; border-radius:0 8px 8px 0; margin:12px 0; font-size:13px; }}
    tr.lvl-A1 td:first-child {{ border-left:3px solid #22c55e; }}
    tr.lvl-A2 td:first-child {{ border-left:3px solid #3b82f6; }}
    tr.lvl-B1 td:first-child {{ border-left:3px solid #8b5cf6; }}
    .progress {{ background:#e5e7eb; border-radius:8px; height:10px; margin:8px 0; overflow:hidden; }}
    .progress-fill {{ background:linear-gradient(90deg,#22c55e,#3b82f6,#8b5cf6); height:100%; width:{pct}%; border-radius:8px; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p class='meta'>Start: {start} | {total} days | Levels: {levels}</p>
  <div class='progress'><div class='progress-fill'></div></div>
  <p class='meta'>Day {day} of {total} ({pct}%)</p>

  <div class='card'>
    <h2>Today's Lesson <span class='badge'>{level}</span></h2>
    <h3>{topic}</h3>
    <p><b>Phase:</b> {phase}</p>

    <h3>Grammar: {grammar_title}</h3>
    <div class='grammar'>{grammar_content}</div>

    <h3>Vocabulary</h3>
    <ul>{vocab_lines}</ul>

    <h3>Practice</h3>
    <ol>{ex_lines}</ol>

    <div class='tip'>Tip: {tip}</div>

    <p><b>Speaking:</b> {speaking}</p>
    <p><b>Writing:</b> {writing}</p>
  </div>

  <div class='card'>
    <h2>{total}-Day Roadmap</h2>
    <div class='scroll'>
      <table>
        <thead><tr><th>Day</th><th>Date</th><th>Level</th><th>Phase</th><th>Topic</th><th>Grammar</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>
</body>
</html>"""


def format_lesson(today_task):
    d = today_task
    lines = []
    total_days = 90
    pct = int(d['day'] / total_days * 100)
    bar = '\u2588' * (pct // 5) + '\u2591' * (20 - pct // 5)
    lines.append(f"\U0001f4da *GERMAN {d['level']} \u2014 DAY {d['day']}/90*")
    lines.append(f"\U0001f4c5 {d['date']} | {d['phase']}")
    lines.append(f"`{bar}` {pct}%")
    lines.append("")
    lines.append(f"\U0001f4d6 *TOPIC: {d['topic']}*")
    lines.append("\u2501" * 35)
    lines.append("")
    lines.append(f"\U0001f4dd *GRAMMAR: {d['grammar_title']}*")
    lines.append(d['grammar_content'])
    lines.append("")
    lines.append(f"\U0001f4da *VOCABULARY* ({len(d['vocabulary'])} words)")
    for ge, en in d['vocabulary']:
        lines.append(f"  \u2022 *{ge}* \u2014 {en}")
    lines.append("")
    lines.append(f"\u270f\ufe0f *PRACTICE*")
    for i, ex in enumerate(d['exercises'], 1):
        lines.append(f"  {i}. {ex}")
    lines.append("")
    lines.append(f"\U0001f4a1 *TIP*: {d['tip']}")
    lines.append("")
    lines.append(f"\U0001f5e3\ufe0f *SPEAKING*: {d.get('speaking_hw', '')}")
    lines.append(f"\u270d\ufe0f *WRITING*: {d.get('writing_hw', '')}")
    return '\n'.join(lines)


def post_to_slack(slack_cfg, today_task):
    import subprocess as sp
    msg = format_lesson(today_task)
    payload = json.dumps({
        "channel": slack_cfg["channel_id"],
        "text": msg,
        "mrkdwn": True,
    })
    cmd = [
        "curl", "-s", "-X", "POST", "https://slack.com/api/chat.postMessage",
        "-H", f"Authorization: Bearer {slack_cfg['bot_token']}",
        "-H", "Content-Type: application/json",
        "-d", payload,
    ]
    result = sp.run(cmd, capture_output=True, text=True, timeout=15)
    resp = json.loads(result.stdout)
    if not resp.get("ok"):
        raise RuntimeError(f"Slack post failed: {resp.get('error', result.stderr)}")
    return resp


def append_log(line):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with RUN_LOG.open('a', encoding='utf-8') as f:
        f.write(f'[{ts}] {line}\n')


def main():
    ensure_dirs()
    config = load_json(CONFIG_PATH)
    plan = load_json(PLAN_JSON)
    today_task, day_num = find_today_task(plan, config)

    TODAY_JSON.write_text(json.dumps(today_task, ensure_ascii=False, indent=2), encoding='utf-8')
    HTML_PATH.write_text(render_html(config, plan, today_task), encoding='utf-8')
    append_log(f"Site updated - Day {day_num} ({today_task['level']}: {today_task.get('topic','')})")

    msg = format_lesson(today_task)
    print(msg)

    result = {
        'success': True, 'day': day_num, 'level': today_task['level'],
        'phase': today_task['phase'], 'site': str(HTML_PATH),
        'today_json': str(TODAY_JSON), 'delivery': 'console',
    }

    if SLACK_CONFIG_PATH.exists():
        try:
            slack_cfg = load_json(SLACK_CONFIG_PATH)
            resp = post_to_slack(slack_cfg, today_task)
            append_log(f"Slack delivered - #{slack_cfg.get('channel_name','?')} (ts={resp.get('ts')})")
            result['delivery'] = 'slack'
            result['slack_ts'] = resp.get('ts')
        except Exception as e:
            append_log(f'Slack delivery failed: {e}')
            result['slack_error'] = str(e)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
