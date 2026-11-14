"""Generate the student report and README from real artifacts and explicit reviews."""
import json
import platform
from collections import Counter
from pathlib import Path
from src.common import ROOT, read, write, now
from src.reviews import aggregate_reviews


def frac(n, total):
    return f'{n}/{total} ({n / total:.1%})' if total else '0/0 (không áp dụng)'


def main():
    experiment = read(ROOT / 'configs/experiments.json')
    lock_path = ROOT / 'results/selection_lock.json'
    lock = read(lock_path) if lock_path.exists() else None
    lines = ['# Báo cáo Day 7 — Agentic RAG', '', '**Kiều Đình Văn · 2A202603376 · L3A**', '',
        '## Phạm vi và tính trung thực', '',
        'Phần cơ bản, không thực hiện bonus. Code, benchmark và đánh giá được Codex hỗ trợ. '
        'Nhãn nội dung do Codex đọc đối chiếu nguồn; học viên cần rà soát trước nộp. '
        'Không gọi nhãn này là chấm mù hay audit độc lập. Kết quả dưới đây lấy từ trace thật, không phải mock.', '',
        '## Dữ liệu và kết nối Day 6', '',
        '- Think Stats: Exploratory Data Analysis in Python, Allen B. Downey, v2.2.1, CC BY-NC-SA 4.0.',
        '- 42 trang nội dung, trang PDF 21–63 trừ 41; 91 chunks paragraph tối đa 900 ký tự, giữ ID/nguồn/trang/offset Day 6.',
        '- Index B trong bảng day6_chunks; truy vấn read-only PostgreSQL 16/pgvector 0.8.7, exact cosine. Không ghi sửa Day 6.',
        '- gemini-embedding-001, 768 chiều, RETRIEVAL_DOCUMENT/RETRIEVAL_QUERY và L2 normalization tương thích Day 6.',
        '- 17 dev = 15 có đáp án + 2 thiếu evidence; 7 test = 5 có đáp án mới + 2 thiếu evidence. Test cũ Day 6 không được dùng lại.',
        '- Dùng cùng corpus/nhãn cho mọi cấu hình, không đưa gold/expected_answer vào agent. Filter rỗng ở tất cả thí nghiệm.',
        '- Nguồn/giấy phép: [attribution](../../data/ATTRIBUTION.md), [manifest](../../data/manifest.json).', '',
        '## Kiến trúc agent và context', '',
        f"Model: `{experiment['agent_model']}`. Native function calling với hai function search và finish. "
        'Lượt đầu bắt buộc search; lượt sau model có thể trả lời hoặc tìm tiếp nếu cấu hình cho phép. '
        'Khi hết lượt tìm, chỉ cho finish. Giữ nguyên model content/thought signature khi gửi function response.', '',
        'Search query có thể được model viết lại sang tiếng Anh; các query này được ghi trong từng trace. '
        'Context gồm chunk ID, URL nguồn, số trang PDF và toàn bộ text; loại trùng, không cắt mất điều kiện giữa chunk. '
        'Budget tính ký tự Unicode gồm cả header/dấu phân cách. Trả lời cần citation trong context cuối. '
        'Chỉ kiểm tra ID bằng code, grounding được chấm riêng. Nếu không đủ evidence, trả lời từ chối. '
        'Tài liệu/tool là dữ liệu, không phải chỉ dẫn. Lỗi API/DB là error, không bị thay bằng mock hoặc abstention.', '',
        '## Cấu hình và giả thuyết', '',
        '| Cấu hình | Retrieval | top-k | Budget ký tự | Tối đa search | Giả thuyết |',
        '|---|---|---:|---:|---:|---|']
    for s in experiment['configs']:
        lines.append(f"| {s['name']} | {s['method']} | {s['top_k']} | {s['budget_chars']} | {s['max_searches']} | {s['hypothesis']} |")
    lines += ['', 'Hybrid dùng reciprocal rank fusion, k=60, 12 candidate mỗi nhánh; không cộng trực tiếp score khác thang đo. '
        'Dense_context và hybrid_context là hai cấu hình cải thiện; vì cùng đổi nhiều thành phần, không xem đây là ablation một biến.', '',
        '## Kết quả retrieval và context', '',
        'Hit@1 và Hit@3 dưới đây dùng **query gốc**. Context gốc cũng dùng query gốc; context agent có thể từ query viết lại/nhiều lượt. '
        'Chỉ câu có đáp án vào mẫu số. Mỗi hit cần đúng nguồn/trang và đầy đủ evidence sau chuẩn hóa case/khoảng trắng.', '',
        '| Split / cấu hình | Hit@1 | Evidence Hit@3 | Context gốc | Context agent | Agent hoàn thành | Median agent ms |',
        '|---|---|---|---|---|---|---:|']
    for split in ('dev', 'test'):
        summary_path = ROOT / 'results' / ('summary_' + split + '.json')
        if not summary_path.exists():
            continue
        for r in read(summary_path):
            n = r['expected_answerable']
            latency = f"{r['agent_median_ms']:.1f}" if r['agent_median_ms'] is not None else 'chưa có'
            lines.append(f"| {split}/{r['config']} | {frac(r['hit1_n'], n)} | {frac(r['hit3_n'], n)} | "
                         f"{frac(r['retrieval_context_n'], n)} | {frac(r['agent_context_n'], n)} | "
                         f"{r['agent_completed']}/{r['expected_total']} | {latency} |")
    lines += ['', 'Metric context tự động là strict evidence match, không thay thế việc đọc semantic context/citation. '
              'Median agent dùng thời gian tham chiếu của lượt thực thi trước cache replay khi có; có thể gồm cache, API và chờ rate limit. agent_current_median_ms ghi riêng lượt replay. Xem từng request trong trace; không suy ra tốc độ model thuần từ bảng này.', '',
              '## Chọn cấu hình trước test', '', experiment['selection_rule'], '']
    if lock:
        lines += [f"Đã khóa **{lock['selected']}** lúc {lock['at']}. "
                  'Hash code/corpus/configs/dev/test được lưu trong [selection_lock](../../results/selection_lock.json). '
                  'Test chỉ chạy baseline và cấu hình được chọn, không chỉnh pipeline bằng kết quả test.', '']
    else:
        lines += ['**Chưa khóa cấu hình; test chưa được chạy.**', '']
    lines += ['## Đánh giá nội dung', '',
        'Nhãn được lưu theo query/config và có lý do. Answer: 0 sai/thiếu evidence hoặc từ chối nhầm; 1 đúng một phần; 2 đúng đủ. '
        'Context: 0 không có evidence; 1 có nhưng thiếu điều kiện/nguồn; 2 đầy đủ. Citation chấm từng ID về hỗ trợ ngữ nghĩa. '
        'Tỷ lệ từ chối đúng chỉ chấm câu thiếu evidence; false abstention chấm riêng câu có đáp án.', '',
        '| Split / cấu hình | Nhãn đã đọc | Answer 0/1/2 | Mean /2 | Citation hỗ trợ | Từ chối đúng | Từ chối nhầm |',
        '|---|---:|---|---:|---|---|---|']
    for split in ('dev', 'test'):
        for r in aggregate_reviews(split):
            dist = '/'.join(str(r['answer_distribution'][str(i)]) for i in range(3))
            mean = f"{r['grounded_mean_out_of_2']:.2f}" if r['grounded_mean_out_of_2'] is not None else 'N/A'
            lines.append(f"| {split}/{r['config']} | {r['reviewed']} | {dist} | {mean} | "
                         f"{frac(r['citation_n'], r['citation_N'])} | {frac(r['abstention_n'], r['abstention_N'])} | "
                         f"{frac(r['false_abstention_n'], r['false_abstention_N'])} |")
    lines += ['', 'Cấu hình hybrid_context có điểm answer dev cao hơn dense_context, nhưng không thay tiêu chí chọn sau khi xem kết quả. '
              'Hai cấu hình hòa strict context 13/15; dense_context thắng theo Hit@3 query gốc 13/15 so với 12/15. '
              'Đây là đánh đổi của tiêu chí dựa vào evidence, không chứng minh cấu hình được chọn tối ưu mọi chỉ số. '
              'Hai cấu hình context lớn đều có lỗi dev u02: trả respondent ID thay cho mã API; citation hỗ trợ câu về ID nhưng không đáp ứng ý định câu hỏi.', '',
              'Context distribution, citation coverage và trạng thái học viên xác nhận có trong audit_dev.json/audit_test.json. '
              'Nếu chưa có nhãn thì không suy điểm từ ID citation.', '', '## Hai lỗi dev và thay đổi', '']
    for qid, description in [('d7-q04', 'Câu hỏi cần cả ba nhóm oversampling và lý do; budget nhỏ có thể giữ sai đoạn hoặc bỏ mất điều kiện.'),
                              ('d7-q08', 'Câu hỏi cần lý do đổi centiyears sang năm; retrieval/context và việc model suy luận phải được phân biệt.')]:
        lines += [f'### {qid}', '', description, '', '| Cấu hình | Trạng thái | Context đủ strict evidence | Câu trả lời |', '|---|---|---|---|']
        for name in ('baseline', 'dense', 'dense_context'):
            path = ROOT / 'results/dev' / name / 'agent' / (qid + '.json')
            if path.exists():
                t = read(path)
                answer = t.get('answer', t.get('error', '')).replace('|', '/').replace('\n', ' ')
                lines.append(f"| {name} | {t['status']} | {t.get('context_hit')} | {answer} |")
        lines += ['', 'Với q04, đổi retrieval từ lexical sang dense tìm đúng đoạn các nhóm oversampling. Với q08, dense budget nhỏ giữ code phép chia nhưng bỏ phần giải thích centiyears; context lớn giữ được phần giải thích. Giả thuyết tăng số candidate/context được kiểm tra bằng kết quả trước/sau. '
                  'Đối chiếu trước/sau ở bảng; nếu không cải thiện, vẫn báo nguyên trạng. Không suy lỗi chỉ từ strict matching.', '']
    lines += ['## Sửa lỗi citation trên dev', '',
              'Model có thể xuất [id1, id2]. Bộ đọc ban đầu đòi [id1] [id2] nên từ chối nhầm dù ID đều đúng. '
              'Đã chuẩn hóa cú pháp gộp, vẫn kiểm tra mọi ID thuộc context và thêm test ID giả. '
              'Đánh giá lại toàn dev từ response cache trước khi khóa pipeline; previous_attempts giữ kết quả và thời gian trước sửa. '
              'Không đổi gold hay nội dung model response.', '',
              '## Ví dụ và trace', '']
    chosen = lock['selected'] if lock else 'baseline'
    for qid in ('d7-q01', 'd7-u01', 'd7-q04'):
        path = ROOT / 'results/dev' / chosen / 'agent' / (qid + '.json')
        if path.exists():
            t = read(path)
            lines += [f"- **{qid} ({t['status']})**: {t.get('answer', t.get('error', ''))}",
                      f"  [Trace](../../results/dev/{chosen}/agent/{qid}.json)"]
    ledger_path = ROOT / 'results/api_usage.json'
    ledger = read(ledger_path) if ledger_path.exists() else []
    statuses = dict(Counter(r['status'] for r in ledger))
    input_tokens = sum(r.get('usage', {}).get('promptTokenCount', 0) for r in ledger)
    output_tokens = sum(r.get('usage', {}).get('candidatesTokenCount', 0) for r in ledger)
    lines += ['', '## Thời gian, usage và chi phí', '',
        f'- API ledger gồm {len(ledger)} lần gửi request; trạng thái: `{json.dumps(statuses)}`.',
        f'- Usage do provider trả: prompt {input_tokens} token, candidate {output_tokens} token; không quy đổi ký tự thành token.',
        '- Học viên xác nhận project Free Tier; không bật billing, không chuyển sang provider trả phí. Chi phí hóa đơn chưa được API xác minh; không bịa con số chi phí.',
        '- Model probe ban đầu với 2.5 Flash-Lite trả HTTP 404. Đã lấy danh sách model và chọn 3.5 Flash-Lite trước benchmark agent. Ledger giữ cả lỗi.',
        '- HTTP 503 được lưu, tiến trình dừng; chạy lại giữ lần lỗi trong previous_attempts và bỏ qua case đã thành công. 429 dừng để chờ quota.',
        '- Response cache theo model + toàn bộ request; embedding cache task-aware, tận dụng cache Day 6. Không gửi lại request đã cache.', '',
        '## Tái lập và giới hạn', '',
        '- Xem README.md và run.ps1; Python ' + platform.python_version() + ', dependencies được pin trong requirements-lock.txt.',
        '- Corpus text tiếng Anh, câu hỏi tiếng Việt, quy mô nhỏ. Các trang test đã thuộc sách Day 6; test mới về mục tiêu trả lời, không độc lập hoàn toàn với lịch sử đọc tài liệu.',
        '- Strict evidence match có thể bỏ sót paraphrase; nhãn semantic được công bố riêng, không tự sửa gold sau khi xem test.',
        '- Citation gate chỉ kiểm tra ID/format, không bảo đảm mọi phát biểu đều đúng. Cần đọc nhãn audit và đối chiếu nguồn.',
        '- Metadata filter, reranker và multimodal bonus không được triển khai. Không tuyên bố đạt điểm rubric cụ thể.',
        '- Repo nộp cần quyền xem của giảng viên; không commit .env/API key/cache private. Chưa push hay nộp thay học viên.', '',
        '## Nguồn kỹ thuật', '',
        '- https://ai.google.dev/gemini-api/docs/function-calling',
        '- https://ai.google.dev/gemini-api/docs/pricing',
        '- https://ai.google.dev/gemini-api/docs/billing',
        '- https://greenteapress.com/thinkstats2/thinkstats2.pdf', '']
    report = '\n'.join(lines)
    notice = ('## Phiên bản của kết quả\n\n'
              'Các bảng benchmark trong báo cáo thuộc **frozen_v1**, có đầy đủ mã nguồn, input, lock và kết quả '
              'lưu tại [artifacts/frozen_v1](../../artifacts/frozen_v1). '
              'Mã nguồn src hiện tại đã sửa các nhánh xử lý lỗi và tổng hợp nhãn sau benchmark; '
              'không tuyên bố kết quả cũ là đánh giá độc lập của bản sửa. '
              'Xem [MAINTENANCE.md](../../MAINTENANCE.md) và kiểm tra hồi quy offline 99 trường hợp.\n\n')
    report = report.replace('## Phạm vi và tính trung thực', notice + '## Phạm vi và tính trung thực', 1)
    (ROOT / 'report/individual/2A202603376_KieuDinhVan.md').write_text(report, encoding='utf-8')
    readme = '''# Day 7 — Agentic RAG

**Kiều Đình Văn · 2A202603376 · L3A · phần cơ bản**

Dùng lại 42 trang Think Stats và index B (91 chunks) của Day 6. Agent Gemini thật gọi tool search, trả lời có citation hoặc từ chối khi thiếu evidence. So sánh TF-IDF, dense pgvector và hybrid RRF; có 5 cấu hình dev và benchmark 17 dev / 7 test.

- [Báo cáo và kết quả](report/individual/2A202603376_KieuDinhVan.md)
- [Giao thức benchmark](benchmark/PROTOCOL.md)
- [Cấu hình và giả thuyết](configs/experiments.json)
- [Dev](benchmark/dev.json) · [Test](benchmark/test.json) · [Nguồn/giấy phép](data/ATTRIBUTION.md)
- [Checklist bài nộp](SUBMISSION_CHECKLIST.md)
- [Workbook rà soát câu trả lời](results/review_workbook.md)
- [Đề bài gốc](docs/LAB_ASSIGNMENT.md) · [Rubric](RUBRIC.md)

## Cài và kết nối

Python 3.11+, PowerShell, PostgreSQL/pgvector của Day 6. Từ thư mục repo:

```powershell
.\\setup.ps1
```

Nếu PowerShell chặn script, dùng trực tiếp các lệnh Python tương ứng trong setup.ps1, không cần đổi chính sách máy.

Sửa `.env` theo `.env.example`: DAY6_ROOT trỏ repo Day 6, DATABASE_URL trỏ index B. GEMINI_API_KEY có thể đặt trong môi trường/.env Day 7; trên máy hiện tại đọc local từ starter/.env Day 6 nếu Day 7 chưa đặt key. Không ghi đè hay commit key. FREE_TIER_CONFIRMED chỉ đặt true khi project không gắn billing; quota hết thì dừng, không tự chuyển trả phí.

Model đã chốt trong configs/experiments.json phải khớp GEMINI_MODEL. Cổng mặc định 55433. Nếu container Day 6 chưa chạy:

```powershell
docker compose -f "$env:DAY6_ROOT/starter/docker-compose.yml" -p day6_student_starter up -d --wait
```

Biến PowerShell DAY6_ROOT cần được đặt riêng nếu dùng lệnh Docker trên; `.env` chỉ được ứng dụng Python đọc. Index cần được dựng theo README Day 6 trên máy mới. Snapshot chunks/pages/manifest và benchmark đã nằm trong repo, không cần gọi lại embedding tài liệu cho máy hiện tại.

## Kiểm chứng bài đã chạy

```powershell
.\\.venv\\Scripts\\python.exe -B -X utf8 -m unittest discover -s tests -v
.\\run.ps1 check
.\\.venv\\Scripts\\python.exe -B -X utf8 -m scripts.verify
```

Có thể chạy cả unit tests và kiểm tra artifact bằng `python -B -X utf8 -m scripts.check_all`. Test offline chỉ kiểm tra code; kết quả agent thật nằm ở results/dev và results/test. Test mặc định không gọi API.

## Chạy thí nghiệm từ đầu

Trong bản sao chưa có selection lock (không xóa lock để chỉnh theo test):

```powershell
.\\.venv\\Scripts\\python.exe -B -X utf8 -m scripts.prepare
.\\run.ps1 retrieval
.\\run.ps1 agent
.\\run.ps1 freeze
.\\run.ps1 test
```

prepare cần repo Day 6. Nó giữ chunk ID và không dùng lại câu test cũ. Những case thành công được giữ để resume; lỗi trước lưu trong previous_attempts. CLI không tự retry hoặc đổi model. Nếu gặp 503, chờ rồi chạy lại cùng lệnh; nếu 429, chờ quota Free Tier. Không chạy nhiều tiến trình lab đồng thời.

Sau khi đọc/điền nhãn trong results/review_labels.json, xuất báo cáo:

```powershell
.\\.venv\\Scripts\\python.exe -B -X utf8 -m scripts.report
```

Khi có lock, lệnh test chỉ chạy baseline và cấu hình đã chọn, kiểm tra hash code/dữ liệu/configs. Case đã thành công được bỏ qua nên chạy lại trên máy này không gửi lại API cho chúng. Kết quả benchmark kém vẫn được giữ nguyên.

## Tổ chức mã nguồn

- src/provider.py: Gemini REST, response/query cache, rate limit, usage ledger và gate Free Tier.
- src/retrieval.py: TF-IDF, dense pgvector read-only, hybrid RRF, context packing.
- src/agent.py: native function-calling search/finish, citation gate, trace và xử lý lỗi.
- src/run.py: CLI retrieval/dev/freeze/test, metric và fingerprint.
- src/reviews.py: kiểm tra và tổng hợp nhãn nội dung đã được đọc, không tự chấm grounding.
- scripts/prepare.py: xuất corpus và soạn benchmark cố định từ nguồn.
- scripts/report.py, scripts/verify.py: báo cáo và kiểm tra artifacts.

Kết quả test của cấu hình đã chọn: Hit@1/Hit@3 và evidence trong context đều 5/5; trả lời đúng đủ 5/5 câu có đáp án, từ chối đúng 2/2 câu thiếu evidence theo nhãn Codex. Benchmark nhỏ, không suy rộng kết quả này.

Code và nhãn do Codex hỗ trợ; học viên cần rà soát nhãn trước nộp. Không có đánh giá độc lập/LLM judge qua API. Không làm phần bonus trong bài này.
'''
    notice = ('## Phiên bản và kiểm tra sau sửa\n\n'
              'Benchmark đã công bố thuộc **frozen_v1**, được lưu nguyên vẹn trong '
              '[artifacts/frozen_v1](artifacts/frozen_v1). `src/` hiện tại là bản đã sửa lỗi. '
              'Không sửa selection_lock để gán benchmark cũ cho code mới. '
              'Lệnh `src.run test` ở bản mới sẽ từ chối chạy với lock cũ; đó là kiểm tra phiên bản có chủ đích.\n\n'
              'Trong Git Bash, kiểm tra bản hiện tại mà không gọi API:\n\n'
              '```bash\n'
              './.venv/Scripts/python.exe -B -X utf8 -m scripts.check_all\n'
              './.venv/Scripts/python.exe -B -X utf8 -m scripts.replay_regression\n'
              '```\n\n'
              '`check_all` báo riêng code hiện tại có khớp lock hay không, và xác minh archive/kết quả cũ. '
              'Replay dùng quyết định/tool result đã lưu; không phải test độc lập. '
              'Muốn đánh giá bản sửa độc lập phải tạo bộ test mới, chọn lại trên dev và khóa một thí nghiệm mới. '
              'Script prepare hiện tại tái tạo bộ câu hỏi cũ, nên không tự biến bộ đó thành test mới.\n\n'
              'Hai script write_reviews/review_test giờ chỉ xác minh nhãn đã chấm, không tạo lại điểm '
              'hoặc đặt lại student_verified. Xem [các lỗi đã sửa](MAINTENANCE.md).\n\n')
    readme = readme.replace('## Cài và kết nối', notice + '## Cài và kết nối', 1)
    (ROOT / 'README.md').write_text(readme, encoding='utf-8')
    print('Report and README regenerated from artifacts.')


if __name__ == '__main__':
    main()
