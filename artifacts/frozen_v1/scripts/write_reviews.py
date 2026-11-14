"""Record the source-based judgments read by Codex; this script is not an automatic judge.

These explicit labels correspond to the stored responses. Student confirmation
is intentionally false. Re-read the source if rerunning with different responses.
"""
from src.common import ROOT, read, write, now, digest


def reviewed_support(existing, name, qid, path, citations):
    """Reuse a stored citation judgment only for the exact trace that was read.

    A changed trace must be re-read by a person; never mark new citations as supported.
    """
    old = existing.get((name, qid))
    if old is None:
        raise ValueError('No human/source review recorded for ' + name + '/' + qid + '; read it before labelling.')
    if old.get('trace_sha256') != digest(path) or len(old.get('citation_support', [])) != len(citations):
        raise ValueError('Trace changed since review: ' + name + '/' + qid + '; re-read context and citations.')
    return list(old['citation_support'])

# (answer grade, context grade); every case was read against context and source.
DEV = {
    'baseline': [(2,2),(2,2),(2,2),(0,0),(2,2),(2,2),(2,2),(0,1),(2,2),(2,2),(1,1),(0,1),(0,0),(0,0),(2,2)],
    'dense': [(0,0),(2,2),(2,2),(2,2),(2,2),(2,2),(0,0),(0,1),(0,0),(2,2),(0,0),(0,1),(2,2),(1,1),(2,2)],
    'hybrid': [(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(0,1),(0,1),(2,2),(1,1),(0,1),(0,0),(0,0),(2,2)],
    'dense_context': [(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(0,1),(2,2),(2,2),(0,1),(2,2),(2,2),(2,2)],
    'hybrid_context': [(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2)]
}
REASONS = {
 'd7-q01': 'Đối chiếu PDF 22: người tham gia có con đầu sinh muộn tự chọn vào thảo luận, làm lệch mẫu/kết quả.',
 'd7-q02': 'PDF 23 hoặc glossary PDF 35 nêu snapshot một thời điểm và theo dõi lặp cùng nhóm theo thời gian. Glossary là evidence tương đương dù strict gold chỉ ở PDF 23.',
 'd7-q03': 'PDF 23 ghi rõ quần thể Hoa Kỳ 15–44 tuổi, đúng cả địa lý và khoảng tuổi.',
 'd7-q04': 'PDF 24 nêu đủ Hispanics, African-Americans, teenagers và mục đích có đủ respondents cho statistical inference.',
 'd7-q05': 'PDF 25 mô tả variable names/types/indices cùng ví dụ _column. Answer giữ đủ ba thuộc tính.',
 'd7-q06': 'PDF 26–27: shape có 13593 rows và 244 columns; đoạn Variables cũng xác nhận 244 biến. Đọc cả hai citation nếu được gộp.',
 'd7-q07': 'PDF 28 hoặc bảng kiểm chứng PDF 30: outcome=1 là live birth. Không lẫn với pregordr/birthord.',
 'd7-q08': 'PDF 29 giải thích agepreg là integer centiyears; chia 100 đổi sang floating-point years, không chỉ nhắc phép chia.',
 'd7-q09': 'PDF 29 nêu 97/98/99 là mã thiếu/refused/unknown; replace thành np.nan tránh số liệu giả.',
 'd7-q10': 'PDF 30: dot notation thêm attribute, không thêm column; phải dùng dictionary syntax.',
 'd7-q11': 'PDF 30–31 hoặc đoạn codebook PDF 33: so sánh thống kê/value counts với published table là một cách validation cụ thể.',
 'd7-q12': 'PDF 42 nêu thay birthwgt_lb >20 thành np.nan. Thay mã 97/98/99 không trả lời điều kiện >20.',
 'd7-q13': 'PDF 37 hoặc glossary PDF 50 và API Hist PDF 38: histogram ánh xạ value→frequency, frequency là số lần xuất hiện.',
 'd7-q14': 'PDF 45 phân biệt mean theo công thức và average là lựa chọn summary statistic của central tendency; ví dụ pumpkin PDF 46 chỉ minh họa một phần.',
 'd7-q15': 'PDF 46/50 nêu standard deviation là square root of variance; đúng quan hệ được hỏi.'
}


def main():
    target = ROOT / 'results/review_labels.json'
    existing = read(target) if target.exists() else []
    by_key = {(r['config'], r['query_id']): r for r in existing}
    output = []
    for name, grades in DEV.items():
        for q in read(ROOT / 'benchmark/dev.json'):
            p = ROOT / 'results/dev' / name / 'agent' / (q['id'] + '.json')
            t = read(p)
            r = {'config': name, 'query_id': q['id'], 'reviewer': 'Codex source-based reading',
                 'reviewed_at': now(), 'student_verified': False, 'trace_sha256': digest(p),
                 'citation_support': reviewed_support(by_key, name, q['id'], p, t['citations'])}
            if q['answerable']:
                grade, context = grades[int(q['id'].split('q')[-1]) - 1]
                r.update(answer_grade=grade, context_grade=context, abstention_correct=None, reason=REASONS[q['id']])
                if t['status'] == 'abstain':
                    if grade != 0:
                        raise ValueError('Explicit review conflicts with current response: ' + name + '/' + q['id'])
                    r['reason'] += ' Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context ' + str(context) + '/2 theo nội dung thực sự còn trong budget.'
                elif grade == 1 and q['id'] == 'd7-q11':
                    r['reason'] = 'PDF 30 chỉ nói nên validation để tránh lỗi. Answer nhắc mục tiêu nhưng không đưa cách tính thống kê rồi đối chiếu published table; đúng một phần, context thiếu bước cụ thể. Citation hỗ trợ phát biểu chung.'
                elif name == 'dense' and q['id'] == 'd7-q14':
                    r['reason'] = 'PDF 46 có ví dụ mean và typical average nhưng không chứa công thức mean hoặc phân biệt average là một trong nhiều summary statistics. Answer đúng một phần; citation không hỗ trợ đầy đủ các khẳng định đã thêm.'
                    r['citation_support'] = [False] * len(t['citations'])
                elif name == 'hybrid' and q['id'] == 'd7-q12':
                    r['reason'] = 'Answer nói về 97/98/99 thay vì điều kiện >20 và kết luận tài liệu không đề cập dù PDF 42 có xử lý >20. Chunk PDF 29 được cite không chứng minh kết luận thiếu thông tin toàn corpus. Answer=0, context=1, citation không hỗ trợ toàn câu.'
                    r['citation_support'] = [False] * len(t['citations'])
            else:
                correct = t['status'] == 'abstain'
                r.update(answer_grade=None, context_grade=None, abstention_correct=correct,
                         reason='Đã đối chiếu phạm vi 42 trang và absence_reason. ' + ('Agent từ chối rõ ràng, không thêm suy đoán.' if correct else 'Agent đổi câu hỏi mã API thành caseid. Citation hỗ trợ câu factual về respondent ID nhưng không trả lời câu hỏi gốc; abstention không đạt.'))
            output.append(r)
    output.extend(r for r in existing if r['query_id'].startswith('d7-t') or r['query_id'] in ('d7-u03','d7-u04'))
    write(target, output)
    print('Recorded', len(output), 'explicit source-based labels; student verification remains pending.')


if __name__ == '__main__':
    main()
