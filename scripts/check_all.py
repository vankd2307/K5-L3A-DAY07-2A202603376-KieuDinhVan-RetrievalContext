"""Run offline tests and artifact checks with UTF-8 logs on Windows/Linux."""
import subprocess
import sys
from src.common import ROOT, write, now


def main():
    completed = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                               cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    text = completed.stdout + completed.stderr
    (ROOT / 'results/unit_tests.txt').write_text(text, encoding='utf-8')
    write(ROOT / 'results/test_run.json', {'at': now(), 'returncode': completed.returncode,
          'command': 'python -B -X utf8 -m unittest discover -s tests -v', 'log': 'results/unit_tests.txt'})
    print(text, end='')
    if completed.returncode:
        raise SystemExit(completed.returncode)
    from scripts.verify import main as verify
    verify()


if __name__ == '__main__':
    main()
