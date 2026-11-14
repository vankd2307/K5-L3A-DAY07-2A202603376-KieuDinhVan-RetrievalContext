"""Read-only provenance checks for the benchmarked source and immutable results."""
from pathlib import Path
from src.common import ROOT, read, digest
from src.run import fingerprint


def historical_state():
    lock_path = ROOT / 'results/selection_lock.json'
    lock = read(lock_path)
    live_matches = lock['fingerprint'] == fingerprint()
    archive = ROOT / 'artifacts/frozen_v1'
    manifest_path = archive / 'manifest.json'
    archive_matches = False
    trace_matches = False
    lock_preserved = False
    if manifest_path.exists():
        manifest = read(manifest_path)
        archive_matches = all((archive / p).is_file() and digest(archive / p) == sha for p, sha in manifest['files'].items())
        archive_matches = archive_matches and all((archive / p).is_file() and digest(archive / p) == sha for p, sha in lock['fingerprint'].items())
        lock_preserved = (archive / 'results/selection_lock.json').is_file() and digest(archive / 'results/selection_lock.json') == digest(lock_path)
        trace_files = {p: sha for p, sha in manifest['files'].items() if p.startswith(('results/dev/', 'results/test/'))}
        trace_matches = bool(trace_files) and all((ROOT / p).is_file() and digest(ROOT / p) == sha for p, sha in trace_files.items())
    return {'current_pipeline_matches_lock': live_matches, 'archived_pipeline_matches_lock': archive_matches,
            'historical_lock_preserved': lock_preserved, 'historical_traces_unchanged': trace_matches,
            'benchmark_version': 'frozen_v1', 'corrected_code_independently_benchmarked': False,
            'note': 'The existing benchmark measures frozen_v1. Current fixes have regression tests, not a new held-out evaluation.'}
