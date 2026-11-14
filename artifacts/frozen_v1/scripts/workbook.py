"""Readable review workbook, generated from explicit labels and trace artifacts."""
from src.common import ROOT, read


def main():
    reviews = read(ROOT / 'results/review_labels.json')
    output = ['# Workbook rà soát Day 7', '',
              'Nhãn dưới đây do Codex đọc đối chiếu nguồn. Chưa đánh dấu học viên xác nhận. '
              'Hãy đọc ít nhất toàn bộ 7 test × 2 cấu hình và các lỗi dev trước nộp. '
              'Nếu đồng ý/sửa nhãn, cập nhật student_verified và lý do trong review_labels.json rồi xuất lại báo cáo.', '']
    for split in ('test', 'dev'):
        questions = {q['id']: q for q in read(ROOT / 'benchmark' / (split + '.json'))}
        output += ['## ' + split.upper(), '']
        for r in reviews:
            if r['query_id'] not in questions:
                continue
            q = questions[r['query_id']]
            t = read(ROOT / 'results' / split / r['config'] / 'agent' / (q['id'] + '.json'))
            output += [f"### {r['config']} / {q['id']}", '', '- [ ] Học viên đã đối chiếu nguồn', '',
                       '**Câu hỏi:** ' + q['question'], '', '**Kết quả:** ' + t.get('answer', t.get('error', '')), '',
                       '**Chuẩn:** ' + q.get('expected_answer', q.get('absence_reason', '')), '',
                       f"**Nhãn:** answer={r.get('answer_grade')}, context={r.get('context_grade')}, "
                       f"citation={r['citation_support']}, abstention={r.get('abstention_correct')}", '',
                       '**Lý do:** ' + r['reason'], '',
                       f"[Trace đầy đủ]({split}/{r['config']}/agent/{q['id']}.json)", '']
            rows = {c['id']: c for e in t['events'] if e['event'] == 'search' for c in e['results']}
            for cid in t['citations']:
                c = rows[cid]
                output += [f"- Citation `{cid}`: PDF page {c['page']}, printed page {c['metadata'].get('printed_page')}; "
                           f"[nguồn]({c['source']})"]
            output += ['']
    (ROOT / 'results/review_workbook.md').write_text('\n'.join(output), encoding='utf-8')
    print('Review workbook generated.')


if __name__ == '__main__':
    main()
