# Checklist bài nộp — 2A202603376 Kiều Đình Văn, L3A

Phần cơ bản. Không cam kết điểm rubric; các nhãn nội dung do Codex hỗ trợ, học viên chưa xác nhận.

- [x] Tái sử dụng 42 trang/91 chunks, embedding Gemini 768 chiều và index B Day 6; kiểm tra index khớp, truy vấn read-only.
- [x] Ba phương pháp TF-IDF, dense pgvector và hybrid RRF; cùng corpus/benchmark, score/rank/nguồn/trang được lưu.
- [x] Agent Gemini thật dùng native function calling, context budget, citation gate và từ chối thiếu evidence.
- [x] Benchmark 17 dev / 7 test, đúng số câu có/thiếu evidence; năm câu test có mục tiêu trả lời mới so với Day 6.
- [x] Năm cấu hình dev, trong đó hai cấu hình thử cải thiện; giữ giả thuyết và kết quả cả khi không tốt hơn.
- [x] Chọn dense_context theo tiêu chí đăng ký, selection_lock trước test và hash pipeline/benchmark.
- [x] Baseline và cấu hình đã chọn chạy trên cùng test; giữ trace, query gốc/viết lại, context, answer, citation, lỗi và usage.
- [x] Đọc đối chiếu tất cả 85 kết quả dev và 14 kết quả test, lưu nhãn/lý do do Codex hỗ trợ; không dùng ID citation làm bằng chứng grounding tự động.
- [x] Phân tích ít nhất hai lỗi dev, ghi trước/sau và giới hạn; giữ cả lỗi HTTP 404/503 trong ledger.
- [x] README, setup/run, dependencies pin, báo cáo cá nhân và workbook rà soát.
- [x] Unit tests và script kiểm tra artifacts; xem results/unit_tests.txt và results/delivery_checks.json.
- [ ] Học viên rà soát/điều chỉnh nhãn, nhất là 14 kết quả test và các lỗi dev; cập nhật student_verified nếu đã đọc.
  - Đã có lượt kiểm tra lại bằng AI (Claude) cho 14 nhãn test, đồng ý với điểm; ghi ở trường ai_recheck. Chưa phải xác nhận của học viên.
- [ ] Kiểm tra repo cá nhân/remote, commit/push và quyền xem của giảng viên; nộp link theo thông báo lớp.

Không có API key trong file nộp; .env và .cache bị Git bỏ qua. Không tự bật billing; chỉ dùng project Free Tier đã xác nhận.

## Bản sửa sau benchmark

Benchmark và source gốc được giữ tại artifacts/frozen_v1. src hiện tại đã sửa các nhánh lỗi; kết quả v1 không được trình bày như test độc lập của bản sửa. Xem MAINTENANCE.md, kết quả unit test hiện tại và hồi quy offline 99 trường hợp. Lock gốc không bị sửa.
