"""Prepare the reproducible Day 7 corpus and a new held-out benchmark."""
import sys
from pathlib import Path
from dataclasses import asdict
from src.common import ROOT, settings, read, write, digest, canonical, now


def main():
    if (ROOT / 'results/selection_lock.json').exists():
        raise RuntimeError('Selection already locked; do not regenerate inputs.')
    day6 = Path(settings()['DAY6_ROOT'])
    sys.path.insert(0, str(day6))
    from starter.src.models import DocumentPage
    from starter.src.chunking import by_paragraph
    pages = read(day6 / 'data/pages.json')
    chunks = []
    for p in pages:
        for c in by_paragraph(DocumentPage(**p), 900):
            row = asdict(c)
            row['id'], row['source_id'] = row.pop('chunk_id'), row.pop('document_id')
            chunks.append(row)
    write(ROOT / 'data/chunks.json', chunks)
    write(ROOT / 'data/pages.json', pages)
    manifest = read(day6 / 'data/manifest.json')
    manifest.update(day6_strategy='B', day7_chunk_count=len(chunks), day7_created_at=now(),
                    derivation='Read-only reuse of Day 6 42-page corpus, paragraph chunks <=900 normalized characters.')
    write(ROOT / 'data/manifest.json', manifest)
    dev = []
    for q in read(day6 / 'benchmark/questions.json'):
        if q['split'] != 'dev':
            continue
        dev.append({'id': 'd7-' + q['id'], 'split': 'dev', 'question': q['question'],
                    'answerable': True, 'expected_answer': q['expected_answer'],
                    'gold': [{'source_id': g['document_id'], 'page': g['page'], 'evidence': g['evidence_quote']}
                             for g in q['gold_alternatives']],
                    'provenance': 'Reused Day 6 dev only. No metadata filter applied in Day 7 comparison.'})
    test_specs = [
        ('t01', 'Pmf.Copy dùng để làm gì và có làm thay đổi Pmf gốc không?',
         'Tạo bản sao Pmf để có thể sửa bản sao mà không ảnh hưởng bản gốc.', 53,
         'Pmf objects provide aCopymethod so you can make and modify a copy\nwithout affecting the original.'),
        ('t02', 'UnbiasPmf hiệu chỉnh xác suất theo sĩ số lớp x bằng cách nào, và bước cuối là gì?',
         'Chia từng xác suất cho x (nhân với 1.0/x), sau đó Normalize để chuẩn hóa lại.', 58,
         'for x, p in pmf.Items():\nnew_pmf.Mult(x, 1.0/x)\n\nnew_pmf.Normalize()'),
        ('t03', 'Vì sao tỷ lệ sinh viên trên giảng viên khoảng 10:1 không đồng nghĩa lớp trung bình có 10 người? Nêu hai lý do.',
         'Sinh viên học 4–5 lớp mỗi kỳ trong khi giảng viên thường dạy 1–2; lớp đông có nhiều sinh viên quan sát hơn lớp nhỏ.', 56,
         '•Students typically take 4–5 classes per semester, but professors often\nteach 1 or 2.\n•The number of students who enjoy a small class is small, but the num-\nber of students in a large class is (ahem!) large.'),
        ('t04', 'Trong ví dụ chạy tiếp sức, xác suất hai người chạy vượt nhau tỷ lệ với đại lượng nào, và vì sao ít gặp người cùng tốc độ?',
         'Tỷ lệ với chênh lệch tốc độ; người cùng tốc độ ít có khả năng vượt hoặc bị vượt nên khó gặp nhau.', 62,
         'During my time on the course, the chance\nof overtaking a runner, or being overtaken, is proportional to the difference\nin our speeds. I am more likely to catch a slow runner, and more likely to be\ncaught by a fast runner. But runners at the same speed are unlikely to see\neach other.'),
        ('t05', 'Bài tập yêu cầu kiểm tra hai hàm PmfMean và PmfVar tự viết bằng cách đối chiếu với các phương thức nào?',
         'Đối chiếu với Mean và Var do Pmf cung cấp.', 62,
         'To test these methods, check that they are\nconsistent with the methodsMeanandVarprovided by Pmf.')]
    test = []
    for qid, question, answer, page, evidence in test_specs:
        test.append({'id': 'd7-' + qid, 'split': 'test', 'question': question, 'answerable': True,
                     'expected_answer': answer, 'gold': [{'source_id': manifest['source_id'], 'page': page, 'evidence': evidence}],
                     'provenance': 'New Day 7 question/answer target; not the five published Day 6 test questions.'})
    absence = [
        ('dev', 'u01', 'Trong bộ tài liệu, tỷ lệ người trả lời NSFG sử dụng Python 3.12 là bao nhiêu phần trăm?',
         'Corpus describes NSFG and Python but does not report respondent Python-version usage.', ['Python 3.12']),
        ('dev', 'u02', 'Trong nghiên cứu NSFG được mô tả, mã API cá nhân của từng người tham gia là gì?',
         'The book reports survey methodology, not participants personal API credentials.', ['API key', 'API keys']),
        ('test', 'u03', 'Trong ví dụ khảo sát sĩ số lớp, học phí chính xác của từng sinh viên là bao nhiêu USD?',
         'The class-size example contains sizes/counts, not student-level tuition amounts.', ['tuition']),
        ('test', 'u04', 'Tác giả báo cáo độ trễ trung bình bao nhiêu mili giây khi chạy PmfMean trên GPU NVIDIA H100?',
         'The corpus has no H100 hardware benchmark or PmfMean timing result.', ['H100'])]
    for split, qid, question, reason, markers in absence:
        if any(marker.casefold() in p['text'].casefold() for p in pages for marker in markers):
            raise ValueError('Absence marker unexpectedly found: ' + qid)
        row = {'id': 'd7-' + qid, 'split': split, 'question': question, 'answerable': False,
               'expected_behavior': 'search_and_abstain', 'absence_reason': reason,
               'absence_check': {'scope': 'All 42 indexed pages, PDF 21-63 except 41; not the entire 264-page book.',
                   'method': 'Read source corpus; case-insensitive marker scan plus semantic inspection of relevant examples.', 'markers': markers}, 'gold': []}
        (dev if split == 'dev' else test).append(row)
    lookup = {(p['document_id'], p['page']): p for p in pages}
    for q in dev + test:
        for g in q['gold']:
            if canonical(g['evidence']) not in canonical(lookup[(g['source_id'], g['page'])]['text']):
                raise ValueError('Evidence not in source page: ' + q['id'])
    # Never overwrite a benchmark after any held-out execution.
    if (ROOT / 'results/selection_lock.json').exists():
        raise RuntimeError('Selection already locked; refuse to regenerate benchmark.')
    write(ROOT / 'benchmark/dev.json', dev)
    write(ROOT / 'benchmark/test.json', test)
    write(ROOT / 'benchmark/frozen.json', {'created_at': now(), 'authoring': 'AI-assisted source-based labels; student review required.',
          'dev': digest(ROOT / 'benchmark/dev.json'), 'test': digest(ROOT / 'benchmark/test.json'),
          'chunks': digest(ROOT / 'data/chunks.json'), 'configs': digest(ROOT / 'configs/experiments.json')})
    print(f'Prepared {len(pages)} pages, {len(chunks)} chunks, {len(dev)} dev and {len(test)} new test cases.')

if __name__ == '__main__':
    main()
