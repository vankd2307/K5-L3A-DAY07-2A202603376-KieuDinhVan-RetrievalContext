"""Write documentation-only clarifications; frozen pipeline code remains unchanged."""
from pathlib import Path
from src.common import ROOT


def once(text, old, new):
    """Idempotent replace: skip when the clarification is already present."""
    return text if new in text else text.replace(old, new)


p = ROOT / 'scripts/report.py'
s = p.read_text(encoding='utf-8-sig')
s = once(s, 'Latency có thể gồm cache, API và chờ rate limit; xem từng request trong trace, không suy ra tốc độ model thuần từ bảng này.',
              'Median agent dùng thời gian tham chiếu của lượt thực thi trước cache replay khi có; có thể gồm cache, API và chờ rate limit. agent_current_median_ms ghi riêng lượt replay. Xem từng request trong trace; không suy ra tốc độ model thuần từ bảng này.')
s = once(s, "    lines += ['## Ví dụ và trace', '']", """    lines += ['## Sửa lỗi citation trên dev', '',
              'Model có thể xuất [id1, id2]. Bộ đọc ban đầu đòi [id1] [id2] nên từ chối nhầm dù ID đều đúng. '
              'Đã chuẩn hóa cú pháp gộp, vẫn kiểm tra mọi ID thuộc context và thêm test ID giả. '
              'Đánh giá lại toàn dev từ response cache trước khi khóa pipeline; previous_attempts giữ kết quả và thời gian trước sửa. '
              'Không đổi gold hay nội dung model response.', '',
              '## Ví dụ và trace', '']""")
s = once(s, "    lines += ['', 'Context distribution, citation coverage", """    lines += ['', 'Cấu hình hybrid_context có điểm answer dev cao hơn dense_context, nhưng không thay tiêu chí chọn sau khi xem kết quả. '
              'Hai cấu hình hòa strict context 13/15; dense_context thắng theo Hit@3 query gốc 13/15 so với 12/15. '
              'Đây là đánh đổi của tiêu chí dựa vào evidence, không chứng minh cấu hình được chọn tối ưu mọi chỉ số. '
              'Hai cấu hình context lớn đều có lỗi dev u02: trả respondent ID thay cho mã API; citation hỗ trợ câu về ID nhưng không đáp ứng ý định câu hỏi.', '',
              'Context distribution, citation coverage""")
s = once(s, "        lines += ['', 'Giả thuyết: tăng số candidate/context giúp giữ điều kiện và đoạn bổ sung. '",
              "        lines += ['', 'Với q04, đổi retrieval từ lexical sang dense tìm đúng đoạn các nhóm oversampling. Với q08, dense budget nhỏ giữ code phép chia nhưng bỏ phần giải thích centiyears; context lớn giữ được phần giải thích. Giả thuyết tăng số candidate/context được kiểm tra bằng kết quả trước/sau. '")
s = once(s, 'Test offline chỉ kiểm tra code; kết quả agent thật nằm ở results/dev và results/test. Test mặc định không gọi API.',
              'Có thể chạy cả unit tests và kiểm tra artifact bằng `python -B -X utf8 -m scripts.check_all`. Test offline chỉ kiểm tra code; kết quả agent thật nằm ở results/dev và results/test. Test mặc định không gọi API.')
s = once(s, '- [Checklist bài nộp](SUBMISSION_CHECKLIST.md)', '- [Checklist bài nộp](SUBMISSION_CHECKLIST.md)\n- [Workbook rà soát câu trả lời](results/review_workbook.md)')
s = once(s, 'Code và nhãn do Codex hỗ trợ; học viên cần rà soát nhãn trước nộp.',
              'Kết quả test của cấu hình đã chọn: Hit@1/Hit@3 và evidence trong context đều 5/5; trả lời đúng đủ 5/5 câu có đáp án, từ chối đúng 2/2 câu thiếu evidence theo nhãn Codex. Benchmark nhỏ, không suy rộng kết quả này.\n\nCode và nhãn do Codex hỗ trợ; học viên cần rà soát nhãn trước nộp.')
p.write_text(s, encoding='utf-8')
p = ROOT / '.gitignore'
p.write_text(p.read_text(encoding='utf-8-sig').rstrip() + '\n', encoding='utf-8')
p = ROOT / 'setup.ps1'
p.write_text(p.read_text(encoding='utf-8-sig').replace('-r requirements.txt', '-r requirements-lock.txt'), encoding='utf-8-sig')
print('Documentation and checkout reproducibility updated; frozen source untouched.')
