# Benchmark Day 7 — giao thức cố định trước chạy agent

- Phạm vi: 42 trang nội dung Think Stats v2.2.1 được index ở Day 6; không phải toàn bộ sách 264 trang.
- Dev: 15 câu có đáp án từ **dev Day 6**, thêm 2 câu thiếu evidence. Test: 5 câu có mục tiêu trả lời mới, thêm 2 câu thiếu evidence.
- Năm câu test Day 6 đã công bố không được dùng lại làm test Day 7. Các trang nguồn/chủ đề có thể gần nhau; đây không phải benchmark từ nguồn độc lập.
- Gold, expected_answer và absence_reason chỉ dùng trong evaluator/review; agent chỉ nhận question. Không suy filter từ gold. Mọi cấu hình Day 7 dùng filter rỗng.
- Cùng corpus/index B, embedding gemini-embedding-001 768 chiều, cùng câu hỏi và nhãn. Lexical dùng token Unicode; dense dùng pgvector exact cosine; hybrid dùng RRF (k=60), 12 candidate mỗi nhánh.
- Có hai cách báo riêng: retrieval với **query gốc** và agent có thể dùng query tiếng Anh do model tự tạo. Không dùng bảng query gốc làm kết quả của query viết lại.
- Hit@1/Evidence Hit@3: đúng source/page và evidence đầy đủ nằm trong một chunk, chuẩn hóa case/khoảng trắng. Gold là các phương án thay thế. Không cộng câu thiếu evidence vào mẫu số.
- Context Evidence Rate: đủ evidence và nguồn trong context cuối. Ghi riêng context query gốc và context agent. Đơn vị budget là **ký tự Unicode**, gồm ID, URL, trang và dấu phân cách; không phải token.
- Năm cấu hình và giả thuyết được đăng ký trong configs/experiments.json. Dense_context và hybrid_context là hai thử nghiệm cải thiện; thay đổi nhiều thành phần cùng lúc nên không quy nguyên nhân cho riêng một thành phần.
- Điều kiện chọn: mọi cấu hình có đủ dev agent thành công; tối đa Context Evidence Rate của agent, rồi Hit@3 query gốc, rồi Hit@1; hòa thì budget nhỏ hơn, ít lượt search hơn, rồi tên cấu hình. Chấm câu trả lời/citation được báo riêng, không đổi tiêu chí sau khi xem kết quả.
- Chạy baseline và cấu hình đã chọn trên cùng 7 test **sau** selection_lock. Hash code, configs, corpus và benchmark phải khớp lock. Không chỉnh pipeline bằng test; cần test mới nếu đã chỉnh.
- Citation ID có trong context chưa chứng minh grounding. Đọc từng answer/context/evidence, chấm context 0/1/2, answer 0/1/2, từng citation true/false và abstention. Lỗi hệ thống giữ status=error và báo riêng.
- Gold và nhãn review do Codex hỗ trợ soạn/đối chiếu; không gọi API judge. Học viên cần rà soát trước nộp. Không tuyên bố là audit độc lập hoặc học viên đã chấm khi chưa xác nhận.
- Agent dừng sau giới hạn search cấu hình; retrieval là tool read-only; dữ liệu tài liệu không phải chỉ dẫn. Không fallback mock khi API lỗi.
- Chỉ project Free Tier được học viên xác nhận. Dừng ở lỗi 429, không tự bật billing hoặc đổi sang dịch vụ trả phí. API không cung cấp hóa đơn: báo usage/request và chi phí là chưa xác minh, không giả định token bằng số ký tự.
- Response cache theo toàn bộ model/request; embedding cache gồm model, số chiều, task và text. Cache không chứa gold. Thời gian cache và thời gian request mới được phân biệt trong trace.
