"""Shared IO and configuration; no implicit writes to the Day 6 project."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DAY6 = ROOT.parent.parent / 'day6/K5-L3A-DAY06-KieuDinhVan-2A202603376-DataIngestion'


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def settings():
    local = dotenv_values(ROOT / '.env', encoding='utf-8-sig')
    day6 = Path(os.getenv('DAY6_ROOT') or local.get('DAY6_ROOT') or DEFAULT_DAY6)
    inherited = dotenv_values(day6 / 'starter/.env', encoding='utf-8-sig')
    cfg = {**inherited, **{k: v for k, v in local.items() if v}, **os.environ}
    cfg['DAY6_ROOT'] = str(day6)
    cfg['GEMINI_MODEL'] = cfg.get('GEMINI_MODEL') or 'gemini-3.5-flash-lite'
    cfg['DATABASE_URL'] = cfg.get('DATABASE_URL') or 'postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab'
    return cfg


def canonical(text):
    return ' '.join(text.casefold().split())


def supports(chunk, gold):
    return any(bool(canonical(g['evidence'])) and chunk['source_id'] == g['source_id'] and chunk['page'] == g['page']
               and canonical(g['evidence']) in canonical(chunk['text']) for g in gold)

