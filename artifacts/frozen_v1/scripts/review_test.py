"""Explicit judgments after reading all fourteen held-out answers and source evidence."""
from src.common import ROOT, read, write, digest, now
from scripts.write_reviews import reviewed_support

REASONS = {
 'd7-t01': 'PDF 53 nêu Copy tạo và sửa bản sao mà không ảnh hưởng bản gốc; answer giữ đủ cả mục đích và điều kiện không sửa gốc.',
 'd7-t02': 'PDF 58: UnbiasPmf nhân từng xác suất với 1.0/x rồi Normalize. Đúng phép toán và đúng bước cuối.',
 'd7-t03': 'PDF 56 nêu sinh viên học 4–5 lớp, giảng viên dạy 1–2 và nhiều sinh viên quan sát lớp đông hơn lớp nhỏ; answer bao phủ hai lý do.',
 'd7-t04': 'PDF 62 nói cơ hội vượt/bị vượt tỷ lệ chênh lệch tốc độ, ít gặp người cùng tốc độ; answer đúng đại lượng và cơ chế.',
 'd7-t05': 'PDF 62 yêu cầu kiểm tra PmfMean/PmfVar nhất quán với Mean/Var của Pmf, đúng cả hai tên phương thức.'
}


def main():
    existing = read(ROOT / 'results/review_labels.json')
    by_key = {(r['config'], r['query_id']): r for r in existing}
    lock = read(ROOT / 'results/selection_lock.json')
    rows = [r for r in existing if r['query_id'] not in {'d7-t01','d7-t02','d7-t03','d7-t04','d7-t05','d7-u03','d7-u04'}]
    for name in [lock['baseline'], lock['selected']]:
        for q in read(ROOT / 'benchmark/test.json'):
            p = ROOT / 'results/test' / name / 'agent' / (q['id'] + '.json')
            t = read(p)
            r = {'config': name, 'query_id': q['id'], 'reviewer': 'Codex source-based reading',
                 'reviewed_at': now(), 'student_verified': False, 'trace_sha256': digest(p),
                 'citation_support': reviewed_support(by_key, name, q['id'], p, t['citations'])}
            if q['answerable']:
                grade = 0 if name == 'baseline' and q['id'] in ('d7-t02', 'd7-t05') else 2
                context = (1 if q['id'] == 'd7-t02' else 0) if grade == 0 else 2
                reason = REASONS[q['id']]
                if grade == 0:
                    reason += (' Baseline giữ đoạn BiasPmf PDF 57, thiếu UnbiasPmf/Normalize; từ chối nhầm, context chỉ liên quan một phần.'
                               if q['id'] == 'd7-t02' else ' Baseline có context rỗng, không đủ evidence và từ chối câu có đáp án.')
                r.update(answer_grade=grade, context_grade=context, abstention_correct=None, reason=reason)
                if (grade == 0) != (t['status'] == 'abstain'):
                    raise ValueError('Stored response differs from reviewed case.')
            else:
                if t['status'] != 'abstain':
                    raise ValueError('Stored unanswerable response differs from reviewed case.')
                r.update(answer_grade=None, context_grade=None, abstention_correct=True,
                         reason='Đối chiếu toàn bộ 42 trang và câu hỏi: không có học phí từng sinh viên (u03) hoặc benchmark H100/PmfMean (u04). Agent từ chối rõ ràng, không thêm số liệu suy đoán.')
            rows.append(r)
    write(ROOT / 'results/review_labels.json', rows)
    print('Saved', len(rows), 'source-based dev/test labels; student verification remains pending.')


if __name__ == '__main__':
    main()
