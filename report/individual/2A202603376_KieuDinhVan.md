# Báo cáo Day 7

**Kiều Đình Văn · 2A202603376 · L3A**

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:** *Think Stats: Exploratory Data Analysis in Python*, Allen B. Downey, v2.2.1, giấy phép CC BY-NC-SA 4.0, dùng cho mục đích học tập phi thương mại ([attribution](../../data/ATTRIBUTION.md), [manifest](../../data/manifest.json)). Dùng lại corpus Day 6: 42 trang nội dung (trang PDF 21–63, bỏ trang 41 vì chủ yếu là hình), 91 chunk theo đoạn, tối đa 900 ký tự, giữ nguyên ID, nguồn, trang và offset của Day 6.
- **Vector store, embedding model, phiên bản và số chiều:** PostgreSQL 16.16 + pgvector 0.8.7 của Day 6, bảng `day6_chunks`, index B, exact cosine (không dùng ANN index). Day 7 chỉ đọc, không ghi vào database. Embedding `gemini-embedding-001`, 768 chiều, task `RETRIEVAL_DOCUMENT` cho chunk và `RETRIEVAL_QUERY` cho câu hỏi, chuẩn hóa L2, giống Day 6.
- **Agent model, cách chạy và phân chia dev/test:** `gemini-3.5-flash-lite` qua Gemini API (Free Tier), native function calling. Dev có 17 câu (15 câu có đáp án + 2 câu thiếu evidence); test có 7 câu (5 câu có đáp án viết mới + 2 câu thiếu evidence). Tôi không dùng lại test của Day 6.
- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:** câu có đáp án có gold gồm nguồn, trang và đoạn evidence trích nguyên văn. Câu thiếu evidence là câu gần chủ đề nhưng corpus không có thông tin để trả lời ([benchmark](../../benchmark/)). Retrieval dùng strict match giống Day 6: chunk phải đúng nguồn, đúng trang và chứa đủ evidence sau khi chuẩn hóa chữ hoa/thường và khoảng trắng; câu thiếu evidence không tính vào mẫu số. Câu trả lời được chấm 0/1/2 (0 = sai, thiếu evidence hoặc từ chối nhầm; 1 = đúng một phần; 2 = đúng và đủ); citation được chấm theo từng ID xem chunk có thực sự hỗ trợ câu trả lời không. Gold và `expected_answer` không được đưa vào agent; không thí nghiệm nào dùng metadata filter.

## Retrieval và thử nghiệm

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| Baseline | TF-IDF, top-3, không filter, không rerank, 1200 ký tự, 1 lần search | Mốc lexical; câu hỏi tiếng Việt, tài liệu tiếng Anh nên dễ trượt | dev | 4/15 (26.7%) | 8/15 (53.3%) | 8/15 (53.3%) | Agent 8382 ms; retrieval 0.4 ms; 34 request LLM |
| Phương pháp 2 | Dense (pgvector Day 6), top-3, không filter, không rerank, 1200 ký tự, 1 lần search | Embedding đa ngôn ngữ tìm evidence tốt hơn lexical | dev | 10/15 (66.7%) | 13/15 (86.7%) | 8/15 (53.3%) | Agent 8451 ms; retrieval 15.2 ms; 34 request LLM |
| Phương pháp 3 | Hybrid RRF (k = 60, 12 candidate mỗi nhánh), top-3, không filter, không rerank, 1200 ký tự, 1 lần search | Kết hợp được cả từ khóa và ngữ nghĩa | dev | 8/15 (53.3%) | 12/15 (80.0%) | 8/15 (53.3%) | Agent 20.5 ms; retrieval 16.9 ms; 34 request LLM |
| Cải thiện 1 | Dense, top-5, không filter, không rerank, 5000 ký tự, 1 lần search | Tăng top-k và budget để không làm rơi evidence khi đóng gói context | dev | 10/15 (66.7%) | 13/15 (86.7%) | 13/15 (86.7%) | Agent 4022 ms; retrieval 23.4 ms; 34 request LLM |
| Cải thiện 2 | Hybrid RRF, top-5, không filter, không rerank, 5000 ký tự, tối đa 2 lần search | Thêm context và cho tìm lượt 2 để tăng độ phủ, đổi lại chậm hơn | dev | 8/15 (53.3%) | 12/15 (80.0%) | 13/15 (86.7%) | Agent 12382 ms; retrieval 27.7 ms; 46 request LLM |
| Cấu hình đã chọn | `dense_context` (= Cải thiện 1) | Khóa trên dev trước khi chạy test | test | 5/5 (100.0%) | 5/5 (100.0%) | 5/5 (100.0%) | Agent 8448 ms; retrieval 4099 ms; 14 request LLM |
| Baseline | TF-IDF như baseline dev | So sánh trên cùng test | test | 1/5 (20.0%) | 3/5 (60.0%) | 3/5 (60.0%) | Agent 8611 ms; retrieval 0.3 ms; 14 request LLM |

Ghi chú về bảng:

- Hit@1 và Evidence Hit@3 tính trên query gốc. Context Evidence Rate là số câu có đủ evidence trong context cuối mà agent gửi cho model, chia cho số câu có đáp án; context này có thể đến từ query viết lại hoặc nhiều lượt search. Nếu chỉ đóng gói top-k của query gốc thì tỷ lệ trên dev lần lượt là 5/15, 10/15, 8/15, 15/15 và 13/15 theo thứ tự các dòng.
- Thời gian là median mỗi câu, tính trên lượt chạy thật trước khi đọc lại từ cache, gồm cả thời gian gọi API và chờ rate limit. Retrieval trên test chậm hơn (khoảng 4 giây) vì phải gọi API để embed query mới.
- Chi phí: tôi dùng Gemini API Free Tier, không bật billing nên không có hóa đơn (0 USD). Tổng usage do API trả về là 127.208 token prompt và 11.718 token output, trên 165 request.
- Cả hai cấu hình cải thiện đều đổi nhiều tham số cùng lúc, nên đây không phải ablation từng biến. Hybrid là phương pháp mới, đồng thời Cải thiện 2 là phiên bản hybrid có thêm context và lượt search.

**Hai lỗi dev:**

1. **d7-q04 (baseline):** câu hỏi cần đủ ba nhóm được lấy mẫu vượt tỷ lệ và lý do. TF-IDF không khớp được câu hỏi tiếng Việt với đoạn tiếng Anh nên context không có evidence và agent từ chối. Cách thử: đổi sang dense. Kết quả: dense tìm đúng đoạn, agent trả lời đủ ba nhóm (Hispanics, African-Americans, teenagers) và mục đích [8bca2eddf8d8ed85185da77e].
2. **d7-q08 (dense):** câu hỏi hỏi vì sao `CleanFemPreg` chia `agepreg` cho 100. Với budget 1200 ký tự, context giữ được đoạn code có phép chia nhưng mất đoạn giải thích centiyears, nên agent từ chối. Cách thử: tăng top-k lên 5 và budget lên 5000 ký tự (`dense_context`). Kết quả: context giữ cả hai đoạn, agent trả lời đúng [50718039f1ba18056fe56194]. Lỗi này cũng giải thích vì sao dense có Hit@3 13/15 nhưng context cuối chỉ đạt 8/15.

Ngoài ra, model đôi khi viết citation gộp dạng `[id1, id2]`, trong khi bộ kiểm tra ban đầu chỉ chấp nhận `[id1] [id2]`, nên một số câu đúng bị chuyển thành từ chối. Tôi sửa bộ đọc để chấp nhận dạng gộp nhưng vẫn kiểm tra từng ID có trong context, thêm test cho ID giả, rồi chạy lại toàn bộ dev từ response cache trước khi khóa cấu hình. Kết quả trước khi sửa được giữ trong `previous_attempts`.

**Lý do chọn cấu hình:** tiêu chí là chọn cấu hình chạy hết dev không lỗi và có Context Evidence Rate dev cao nhất; nếu hòa thì xét Evidence Hit@3, rồi Hit@1, rồi budget nhỏ hơn, ít lượt search hơn, cuối cùng theo tên. Điểm chấm câu trả lời không dùng để chọn. `dense_context` và `hybrid_context` hòa ở context (13/15); `dense_context` thắng nhờ Evidence Hit@3 cao hơn (13/15 so với 12/15), đồng thời ít request hơn (34 so với 46) và nhanh hơn. Tôi khóa `dense_context` lúc 14:41 ngày 14/11/2026 (giờ Việt Nam, tức 07:41:14 UTC); hash của code, corpus, config, dev và test nằm trong [selection_lock](../../results/selection_lock.json). Test chỉ chạy baseline và cấu hình đã chọn, sau khi đã khóa.

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:** agent có hai function là `search(query)` và `finish(answer, citations)`. Lượt đầu bắt buộc phải search; sau đó model tự chọn trả lời hoặc tìm tiếp, trong giới hạn số lần search của cấu hình (1 hoặc 2). Hết lượt search thì model chỉ còn được gọi `finish`. Model có thể viết lại query sang tiếng Anh; query viết lại được lưu trong trace. Context gồm chunk ID, nguồn, số trang và toàn bộ text chunk, đã loại trùng, sắp theo thứ hạng; tôi không cắt giữa chunk để tránh mất điều kiện, và budget tính bằng ký tự Unicode gồm cả header. Câu trả lời phải cite chunk có trong context cuối, nếu không sẽ bị chuyển thành từ chối; khi không đủ evidence, agent trả lời "Không đủ bằng chứng trong tài liệu để trả lời." Nội dung tài liệu được coi là dữ liệu, không phải chỉ dẫn. Lỗi API hoặc database được ghi `status: "error"`, không thay bằng mock. Thực tế gặp 1 HTTP 404 (model 2.5 Flash-Lite không khả dụng, nên tôi đổi sang `gemini-3.5-flash-lite` trước khi chạy benchmark) và 1 HTTP 503 (tiến trình dừng, lần lỗi được ghi lại, khi chạy tiếp thì giữ các câu đã thành công). Gặp HTTP 429 thì dừng chờ quota.

| Cấu hình / split | Tool use | Số lượt gọi | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| baseline / dev | 17/17 | 1 search: 17 câu | 5/1/9; 1.27 | 10/10 (100.0%) | 10/10 | 2/2 (100.0%) | 5/15 (33.3%) |
| dense / dev | 17/17 | 1 search: 17 câu | 6/1/8; 1.13 | 8/9 (88.9%) | 9/9 | 2/2 (100.0%) | 6/15 (40.0%) |
| hybrid / dev | 17/17 | 1 search: 17 câu | 5/1/9; 1.27 | 11/12 (91.7%) | 11/11 | 2/2 (100.0%) | 4/15 (26.7%) |
| dense_context / dev | 17/17 | 1 search: 17 câu | 2/0/13; 1.73 | 16/16 (100.0%) | 14/14 | 1/2 (50.0%) | 2/15 (13.3%) |
| hybrid_context / dev | 17/17 | 1 search: 5 câu; 2 search: 12 câu | 0/0/15; 2.00 | 21/21 (100.0%) | 16/16 | 1/2 (50.0%) | 0/15 (0.0%) |
| baseline / test | 7/7 | 1 search: 7 câu | 2/0/3; 1.20 | 3/3 (100.0%) | 3/3 | 2/2 (100.0%) | 2/5 (40.0%) |
| dense_context / test | 7/7 | 1 search: 7 câu | 0/0/5; 2.00 | 5/5 (100.0%) | 5/5 | 2/2 (100.0%) | 0/5 (0.0%) |

Citation hợp lệ là số citation có trong context và hỗ trợ câu trả lời, chia cho tổng số citation. Câu có citation là số câu đã trả lời có ít nhất một citation, chia cho số câu đã trả lời. Không có lần chạy nào bị lỗi.

| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| d7-q01 (dense_context, dev) | Có đáp án | 1 lần search; context chứa chunk 54f0c801e3aa64b436f8c68f có đoạn về selection bias | Người tham gia thảo luận có thể quan tâm chính vì con đầu của họ sinh muộn, nên cách chọn dữ liệu làm lệch kết quả [54f0c801e3aa64b436f8c68f] | 2: đúng ý evidence, citation hỗ trợ |
| d7-q04 (baseline → dense_context, dev) | Có đáp án | Baseline: TF-IDF không lấy được đoạn oversampling. Dense: lấy đúng chunk 8bca2eddf8d8ed85185da77e | Baseline từ chối. Dense_context: đủ ba nhóm Hispanics, African-Americans, teenagers và mục đích suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e] | Baseline 0: từ chối nhầm. Dense_context 2: đúng và đủ |
| d7-q08 (dense → dense_context, dev) | Có đáp án | Dense (budget 1200): context có code phép chia nhưng mất đoạn giải thích. Dense_context (budget 5000): giữ cả hai đoạn | Dense từ chối. Dense_context: `agepreg` được mã hóa theo centiyears, chia cho 100 để đổi sang số năm [50718039f1ba18056fe56194] | Dense 0: từ chối nhầm. Dense_context 2: đúng và đủ |
| d7-u01 (dense_context, dev) | Thiếu evidence | 1 lần search; context không có thông tin trả lời | "Không đủ bằng chứng trong tài liệu để trả lời." | Abstention đúng |
| d7-u02 (dense_context, dev) | Thiếu evidence | 1 lần search; context có chunk nói về respondent ID | Trả lời bằng respondent ID trong khi câu hỏi hỏi về mã API | Abstention sai: citation nói về ID nhưng không trả lời điều câu hỏi hỏi |

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:**
  - Trace từng câu: `results/dev/<cấu hình>/agent/<query-id>.json` và `results/test/<cấu hình>/agent/<query-id>.json`, ví dụ [d7-q01](../../results/dev/dense_context/agent/d7-q01.json), [d7-u01](../../results/dev/dense_context/agent/d7-u01.json), [d7-u02](../../results/dev/dense_context/agent/d7-u02.json).
  - Nhãn và lý do từng câu: [review_labels.json](../../results/review_labels.json), [audit_dev.json](../../results/audit_dev.json), [audit_test.json](../../results/audit_test.json), [review_workbook.md](../../results/review_workbook.md). Codex đề xuất nhãn ban đầu kèm lý do; tôi đọc đối chiếu với nguồn rồi chốt. Đây không phải chấm mù hay chấm độc lập.
  - Tổng hợp: [summary_dev.json](../../results/summary_dev.json), [summary_test.json](../../results/summary_test.json), usage API: [api_usage.json](../../results/api_usage.json).
  - Lệnh chạy (cài đặt xem [README](../../README_STUDENT.md) và `run.ps1`):
    ```
    .\.venv\Scripts\python.exe -X utf8 -m src.run check
    .\.venv\Scripts\python.exe -X utf8 -m src.run retrieval --split dev
    .\.venv\Scripts\python.exe -X utf8 -m src.run agent --split dev
    .\.venv\Scripts\python.exe -X utf8 -m src.run freeze
    .\.venv\Scripts\python.exe -X utf8 -m src.run test
    .\.venv\Scripts\python.exe -X utf8 -m src.run summarize --split dev
    .\.venv\Scripts\python.exe -X utf8 -m src.run summarize --split test
    ```
  - Response LLM được cache theo model và toàn bộ request; embedding được cache theo task và dùng lại cache Day 6, nên chạy lại không gửi lại request đã có.
- **Kết quả trước/sau, ví dụ lỗi, đánh đổi và giới hạn:**
  - Trước/sau: tăng top-k và budget (dense → dense_context) nâng Context Evidence Rate dev từ 8/15 lên 13/15, điểm trả lời trung bình từ 1.13 lên 1.73, và giảm từ chối nhầm từ 6/15 xuống 2/15.
  - Đánh đổi: `hybrid_context` có điểm trả lời dev cao nhất (2.00/2) nhưng cần thêm 12 request và chậm gấp khoảng 3 lần `dense_context`. Tôi vẫn giữ `dense_context` theo tiêu chí đã chốt và không đổi tiêu chí sau khi xem kết quả. Cả hai cấu hình context lớn đều trả lời câu thiếu evidence d7-u02, nên abstention đúng chỉ còn 1/2: context nhiều hơn giúp trả lời được nhiều câu hơn, nhưng cũng làm agent dễ trả lời khi lẽ ra phải từ chối.
  - Giới hạn: corpus chỉ có một cuốn sách, test chỉ 7 câu nên kết quả 5/5 chưa đủ để kết luận về chất lượng tổng quát. Test được viết mới nhưng vẫn nằm trong cuốn sách tôi đã đọc ở Day 6. Strict match có thể bỏ sót đoạn diễn đạt khác. Kiểm tra citation bằng code chỉ xác nhận ID và định dạng. Chưa thử metadata filter và reranker.
  - Tái lập: các bảng lấy từ bản đóng băng [artifacts/frozen_v1](../../artifacts/frozen_v1), gồm code, input, lock và kết quả. Sau benchmark, tôi có sửa thêm phần xử lý lỗi và tổng hợp nhãn trong `src/` (xem [MAINTENANCE.md](../../MAINTENANCE.md), kèm 99 ca kiểm tra hồi quy offline); kết quả trên không được coi là đánh giá lại bản sửa này. Tôi sửa `tests/test_baseline.py` của đề để đọc file bằng UTF-8 trên Windows, không đổi assertion nào.


