# Day 7 — Agentic RAG

**Kiều Đình Văn · 2A202603376 · L3A · phần cơ bản**

Dùng lại 42 trang Think Stats và index B (91 chunks) của Day 6. Agent Gemini thật gọi tool search, trả lời có citation hoặc từ chối khi thiếu evidence. So sánh TF-IDF, dense pgvector và hybrid RRF; có 5 cấu hình dev và benchmark 17 dev / 7 test.

- [Báo cáo và kết quả](report/individual/2A202603376_KieuDinhVan.md)
- [Giao thức benchmark](benchmark/PROTOCOL.md)
- [Cấu hình và giả thuyết](configs/experiments.json)
- [Dev](benchmark/dev.json) · [Test](benchmark/test.json) · [Nguồn/giấy phép](data/ATTRIBUTION.md)
- [Checklist bài nộp](SUBMISSION_CHECKLIST.md)
- [Workbook rà soát câu trả lời](results/review_workbook.md)
- [Đề bài gốc](docs/LAB_ASSIGNMENT.md) · [Rubric](RUBRIC.md)

## Phiên bản và kiểm tra sau sửa

Benchmark đã công bố thuộc **frozen_v1**, được lưu nguyên vẹn trong [artifacts/frozen_v1](artifacts/frozen_v1). `src/` hiện tại là bản đã sửa lỗi. Không sửa selection_lock để gán benchmark cũ cho code mới. Lệnh `src.run test` ở bản mới sẽ từ chối chạy với lock cũ; đó là kiểm tra phiên bản có chủ đích.

Trong Git Bash, kiểm tra bản hiện tại mà không gọi API:

```bash
./.venv/Scripts/python.exe -B -X utf8 -m scripts.check_all
./.venv/Scripts/python.exe -B -X utf8 -m scripts.replay_regression
```

`check_all` báo riêng code hiện tại có khớp lock hay không, và xác minh archive/kết quả cũ. Replay dùng quyết định/tool result đã lưu; không phải test độc lập. Muốn đánh giá bản sửa độc lập phải tạo bộ test mới, chọn lại trên dev và khóa một thí nghiệm mới. Script prepare hiện tại tái tạo bộ câu hỏi cũ, nên không tự biến bộ đó thành test mới.

Hai script write_reviews/review_test giờ chỉ xác minh nhãn đã chấm, không tạo lại điểm hoặc đặt lại student_verified. Xem [các lỗi đã sửa](MAINTENANCE.md).

## Cài và kết nối

Python 3.11+, PowerShell, PostgreSQL/pgvector của Day 6. Từ thư mục repo:

```powershell
.\setup.ps1
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
.\.venv\Scripts\python.exe -B -X utf8 -m unittest discover -s tests -v
.\run.ps1 check
.\.venv\Scripts\python.exe -B -X utf8 -m scripts.verify
```

Có thể chạy cả unit tests và kiểm tra artifact bằng `python -B -X utf8 -m scripts.check_all`. Test offline chỉ kiểm tra code; kết quả agent thật nằm ở results/dev và results/test. Test mặc định không gọi API.

## Chạy thí nghiệm từ đầu

Trong bản sao chưa có selection lock (không xóa lock để chỉnh theo test):

```powershell
.\.venv\Scripts\python.exe -B -X utf8 -m scripts.prepare
.\run.ps1 retrieval
.\run.ps1 agent
.\run.ps1 freeze
.\run.ps1 test
```

prepare cần repo Day 6. Nó giữ chunk ID và không dùng lại câu test cũ. Những case thành công được giữ để resume; lỗi trước lưu trong previous_attempts. CLI không tự retry hoặc đổi model. Nếu gặp 503, chờ rồi chạy lại cùng lệnh; nếu 429, chờ quota Free Tier. Không chạy nhiều tiến trình lab đồng thời.

Sau khi đọc/điền nhãn trong results/review_labels.json, xuất báo cáo:

```powershell
.\.venv\Scripts\python.exe -B -X utf8 -m scripts.report
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
