# Báo cáo Day 7 — Agentic RAG

**Kiều Đình Văn · 2A202603376 · L3A**

## Phiên bản của kết quả

Các bảng benchmark trong báo cáo thuộc **frozen_v1**, có đầy đủ mã nguồn, input, lock và kết quả lưu tại [artifacts/frozen_v1](../../artifacts/frozen_v1). Mã nguồn src hiện tại đã sửa các nhánh xử lý lỗi và tổng hợp nhãn sau benchmark; không tuyên bố kết quả cũ là đánh giá độc lập của bản sửa. Xem [MAINTENANCE.md](../../MAINTENANCE.md) và kiểm tra hồi quy offline 99 trường hợp.

## Phạm vi và tính trung thực

Phần cơ bản, không thực hiện bonus. Code, benchmark và đánh giá được Codex hỗ trợ. Nhãn nội dung do Codex đọc đối chiếu nguồn; học viên cần rà soát trước nộp. Không gọi nhãn này là chấm mù hay audit độc lập. Kết quả dưới đây lấy từ trace thật, không phải mock.

## Dữ liệu và kết nối Day 6

- Think Stats: Exploratory Data Analysis in Python, Allen B. Downey, v2.2.1, CC BY-NC-SA 4.0.
- 42 trang nội dung, trang PDF 21–63 trừ 41; 91 chunks paragraph tối đa 900 ký tự, giữ ID/nguồn/trang/offset Day 6.
- Index B trong bảng day6_chunks; truy vấn read-only PostgreSQL 16/pgvector 0.8.7, exact cosine. Không ghi sửa Day 6.
- gemini-embedding-001, 768 chiều, RETRIEVAL_DOCUMENT/RETRIEVAL_QUERY và L2 normalization tương thích Day 6.
- 17 dev = 15 có đáp án + 2 thiếu evidence; 7 test = 5 có đáp án mới + 2 thiếu evidence. Test cũ Day 6 không được dùng lại.
- Dùng cùng corpus/nhãn cho mọi cấu hình, không đưa gold/expected_answer vào agent. Filter rỗng ở tất cả thí nghiệm.
- Nguồn/giấy phép: [attribution](../../data/ATTRIBUTION.md), [manifest](../../data/manifest.json).

## Kiến trúc agent và context

Model: `gemini-3.5-flash-lite`. Native function calling với hai function search và finish. Lượt đầu bắt buộc search; lượt sau model có thể trả lời hoặc tìm tiếp nếu cấu hình cho phép. Khi hết lượt tìm, chỉ cho finish. Giữ nguyên model content/thought signature khi gửi function response.

Search query có thể được model viết lại sang tiếng Anh; các query này được ghi trong từng trace. Context gồm chunk ID, URL nguồn, số trang PDF và toàn bộ text; loại trùng, không cắt mất điều kiện giữa chunk. Budget tính ký tự Unicode gồm cả header/dấu phân cách. Trả lời cần citation trong context cuối. Chỉ kiểm tra ID bằng code, grounding được chấm riêng. Nếu không đủ evidence, trả lời từ chối. Tài liệu/tool là dữ liệu, không phải chỉ dẫn. Lỗi API/DB là error, không bị thay bằng mock hoặc abstention.

## Cấu hình và giả thuyết

| Cấu hình | Retrieval | top-k | Budget ký tự | Tối đa search | Giả thuyết |
|---|---|---:|---:|---:|---|
| baseline | tfidf | 3 | 1200 | 1 | Lexical baseline; Vietnamese questions versus English source may miss synonyms. |
| dense | dense | 3 | 1200 | 1 | Cross-lingual embeddings improve evidence retrieval relative to lexical baseline. |
| hybrid | hybrid | 3 | 1200 | 1 | RRF combines lexical terms and dense semantic evidence. |
| dense_context | dense | 5 | 5000 | 1 | Larger top-k and context reduce loss of complete evidence during packing. |
| hybrid_context | hybrid | 5 | 5000 | 2 | More context and optional query refinement improve evidence coverage at additional latency. |

Hybrid dùng reciprocal rank fusion, k=60, 12 candidate mỗi nhánh; không cộng trực tiếp score khác thang đo. Dense_context và hybrid_context là hai cấu hình cải thiện; vì cùng đổi nhiều thành phần, không xem đây là ablation một biến.

## Kết quả retrieval và context

Hit@1 và Hit@3 dưới đây dùng **query gốc**. Context gốc cũng dùng query gốc; context agent có thể từ query viết lại/nhiều lượt. Chỉ câu có đáp án vào mẫu số. Mỗi hit cần đúng nguồn/trang và đầy đủ evidence sau chuẩn hóa case/khoảng trắng.

| Split / cấu hình | Hit@1 | Evidence Hit@3 | Context gốc | Context agent | Agent hoàn thành | Median agent ms |
|---|---|---|---|---|---|---:|
| dev/baseline | 4/15 (26.7%) | 8/15 (53.3%) | 5/15 (33.3%) | 8/15 (53.3%) | 17/17 | 8382.0 |
| dev/dense | 10/15 (66.7%) | 13/15 (86.7%) | 10/15 (66.7%) | 8/15 (53.3%) | 17/17 | 8451.4 |
| dev/hybrid | 8/15 (53.3%) | 12/15 (80.0%) | 8/15 (53.3%) | 8/15 (53.3%) | 17/17 | 20.5 |
| dev/dense_context | 10/15 (66.7%) | 13/15 (86.7%) | 15/15 (100.0%) | 13/15 (86.7%) | 17/17 | 4021.6 |
| dev/hybrid_context | 8/15 (53.3%) | 12/15 (80.0%) | 13/15 (86.7%) | 13/15 (86.7%) | 17/17 | 12382.1 |
| test/baseline | 1/5 (20.0%) | 3/5 (60.0%) | 2/5 (40.0%) | 3/5 (60.0%) | 7/7 | 8610.9 |
| test/dense_context | 5/5 (100.0%) | 5/5 (100.0%) | 5/5 (100.0%) | 5/5 (100.0%) | 7/7 | 8448.2 |

Metric context tự động là strict evidence match, không thay thế việc đọc semantic context/citation. Median agent dùng thời gian tham chiếu của lượt thực thi trước cache replay khi có; có thể gồm cache, API và chờ rate limit. agent_current_median_ms ghi riêng lượt replay. Xem từng request trong trace; không suy ra tốc độ model thuần từ bảng này.

## Chọn cấu hình trước test

Among configurations with complete successful dev agent runs, maximize dev Context Evidence Rate, then Evidence Hit@3, then Hit@1; ties favor smaller context budget, then fewer allowed searches, then config name. Answer/citation audits are reported as limitations, not used to silently retune test.

Đã khóa **dense_context** lúc 2026-11-14T07:41:14.887615+00:00. Hash code/corpus/configs/dev/test được lưu trong [selection_lock](../../results/selection_lock.json). Test chỉ chạy baseline và cấu hình được chọn, không chỉnh pipeline bằng kết quả test.

## Đánh giá nội dung

Nhãn được lưu theo query/config và có lý do. Answer: 0 sai/thiếu evidence hoặc từ chối nhầm; 1 đúng một phần; 2 đúng đủ. Context: 0 không có evidence; 1 có nhưng thiếu điều kiện/nguồn; 2 đầy đủ. Citation chấm từng ID về hỗ trợ ngữ nghĩa. Tỷ lệ từ chối đúng chỉ chấm câu thiếu evidence; false abstention chấm riêng câu có đáp án.

| Split / cấu hình | Nhãn đã đọc | Answer 0/1/2 | Mean /2 | Citation hỗ trợ | Từ chối đúng | Từ chối nhầm |
|---|---:|---|---:|---|---|---|
| dev/baseline | 17 | 5/1/9 | 1.27 | 10/10 (100.0%) | 2/2 (100.0%) | 5/15 (33.3%) |
| dev/dense | 17 | 6/1/8 | 1.13 | 8/9 (88.9%) | 2/2 (100.0%) | 6/15 (40.0%) |
| dev/hybrid | 17 | 5/1/9 | 1.27 | 11/12 (91.7%) | 2/2 (100.0%) | 4/15 (26.7%) |
| dev/dense_context | 17 | 2/0/13 | 1.73 | 16/16 (100.0%) | 1/2 (50.0%) | 2/15 (13.3%) |
| dev/hybrid_context | 17 | 0/0/15 | 2.00 | 21/21 (100.0%) | 1/2 (50.0%) | 0/15 (0.0%) |
| test/baseline | 7 | 2/0/3 | 1.20 | 3/3 (100.0%) | 2/2 (100.0%) | 2/5 (40.0%) |
| test/dense_context | 7 | 0/0/5 | 2.00 | 5/5 (100.0%) | 2/2 (100.0%) | 0/5 (0.0%) |

Cấu hình hybrid_context có điểm answer dev cao hơn dense_context, nhưng không thay tiêu chí chọn sau khi xem kết quả. Hai cấu hình hòa strict context 13/15; dense_context thắng theo Hit@3 query gốc 13/15 so với 12/15. Đây là đánh đổi của tiêu chí dựa vào evidence, không chứng minh cấu hình được chọn tối ưu mọi chỉ số. Hai cấu hình context lớn đều có lỗi dev u02: trả respondent ID thay cho mã API; citation hỗ trợ câu về ID nhưng không đáp ứng ý định câu hỏi.

Context distribution, citation coverage và trạng thái học viên xác nhận có trong audit_dev.json/audit_test.json. Nếu chưa có nhãn thì không suy điểm từ ID citation.

## Hai lỗi dev và thay đổi

### d7-q04

Câu hỏi cần cả ba nhóm oversampling và lý do; budget nhỏ có thể giữ sai đoạn hoặc bỏ mất điều kiện.

| Cấu hình | Trạng thái | Context đủ strict evidence | Câu trả lời |
|---|---|---|---|
| baseline | abstain | False | Không đủ bằng chứng trong tài liệu để trả lời. |
| dense | answered | True | Trong Chương 1, NSFG lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm là: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e].   Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn nhằm đưa ra các suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e]. |
| dense_context | answered | True | Trong chương 1, các nhà thiết kế của cuộc khảo sát NSFG đã lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e].   Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn, nhằm có thể đưa ra các suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e]. |

Với q04, đổi retrieval từ lexical sang dense tìm đúng đoạn các nhóm oversampling. Với q08, dense budget nhỏ giữ code phép chia nhưng bỏ phần giải thích centiyears; context lớn giữ được phần giải thích. Giả thuyết tăng số candidate/context được kiểm tra bằng kết quả trước/sau. Đối chiếu trước/sau ở bảng; nếu không cải thiện, vẫn báo nguyên trạng. Không suy lỗi chỉ từ strict matching.

### d7-q08

Câu hỏi cần lý do đổi centiyears sang năm; retrieval/context và việc model suy luận phải được phân biệt.

| Cấu hình | Trạng thái | Context đủ strict evidence | Câu trả lời |
|---|---|---|---|
| baseline | abstain | False | Không đủ bằng chứng trong tài liệu để trả lời. |
| dense | abstain | False | Không đủ bằng chứng trong tài liệu để trả lời. |
| dense_context | answered | True | Trong `CleanFemPreg`, biến `agepreg` được chia cho 100 vì trong tệp dữ liệu, tuổi của người mẹ (`agepreg`) được mã hóa dưới dạng số nguyên tính theo phần trăm của năm (centiyears) [50718039f1ba18056fe56194]. Việc chia cho 100 giúp chuyển đổi các giá trị này thành một giá trị dấu phẩy động (floating-point value) tính bằng năm [50718039f1ba18056fe56194]. |

Với q04, đổi retrieval từ lexical sang dense tìm đúng đoạn các nhóm oversampling. Với q08, dense budget nhỏ giữ code phép chia nhưng bỏ phần giải thích centiyears; context lớn giữ được phần giải thích. Giả thuyết tăng số candidate/context được kiểm tra bằng kết quả trước/sau. Đối chiếu trước/sau ở bảng; nếu không cải thiện, vẫn báo nguyên trạng. Không suy lỗi chỉ từ strict matching.

## Sửa lỗi citation trên dev

Model có thể xuất [id1, id2]. Bộ đọc ban đầu đòi [id1] [id2] nên từ chối nhầm dù ID đều đúng. Đã chuẩn hóa cú pháp gộp, vẫn kiểm tra mọi ID thuộc context và thêm test ID giả. Đánh giá lại toàn dev từ response cache trước khi khóa pipeline; previous_attempts giữ kết quả và thời gian trước sửa. Không đổi gold hay nội dung model response.

## Ví dụ và trace

- **d7-q01 (answered)**: Việc chỉ lấy ý kiến hoặc dựa vào những người tham gia thảo luận về con đầu sinh muộn có thể gây ra hiện tượng thiên vị lựa chọn (selection bias) vì những người tham gia vào một cuộc thảo luận như vậy có thể bị thu hút hoặc quan tâm đến chủ đề này chính vì con đầu của họ sinh muộn [54f0c801e3aa64b436f8c68f]. Do đó, quá trình chọn lọc dữ liệu này sẽ làm lệch kết quả của toàn bộ khảo sát/thảo luận [54f0c801e3aa64b436f8c68f].
  [Trace](../../results/dev/dense_context/agent/d7-q01.json)
- **d7-u01 (abstain)**: Không đủ bằng chứng trong tài liệu để trả lời.
  [Trace](../../results/dev/dense_context/agent/d7-u01.json)
- **d7-q04 (answered)**: Trong chương 1, các nhà thiết kế của cuộc khảo sát NSFG đã lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e]. 

Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn, nhằm có thể đưa ra các suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e].
  [Trace](../../results/dev/dense_context/agent/d7-q04.json)

## Thời gian, usage và chi phí

- API ledger gồm 165 lần gửi request; trạng thái: `{"HTTP_404": 1, "ok": 163, "HTTP_503": 1}`.
- Usage do provider trả: prompt 127208 token, candidate 11718 token; không quy đổi ký tự thành token.
- Học viên xác nhận project Free Tier; không bật billing, không chuyển sang provider trả phí. Chi phí hóa đơn chưa được API xác minh; không bịa con số chi phí.
- Model probe ban đầu với 2.5 Flash-Lite trả HTTP 404. Đã lấy danh sách model và chọn 3.5 Flash-Lite trước benchmark agent. Ledger giữ cả lỗi.
- HTTP 503 được lưu, tiến trình dừng; chạy lại giữ lần lỗi trong previous_attempts và bỏ qua case đã thành công. 429 dừng để chờ quota.
- Response cache theo model + toàn bộ request; embedding cache task-aware, tận dụng cache Day 6. Không gửi lại request đã cache.

## Tái lập và giới hạn

- Xem README.md và run.ps1; Python 3.12.6, dependencies được pin trong requirements-lock.txt.
- Corpus text tiếng Anh, câu hỏi tiếng Việt, quy mô nhỏ. Các trang test đã thuộc sách Day 6; test mới về mục tiêu trả lời, không độc lập hoàn toàn với lịch sử đọc tài liệu.
- Strict evidence match có thể bỏ sót paraphrase; nhãn semantic được công bố riêng, không tự sửa gold sau khi xem test.
- Citation gate chỉ kiểm tra ID/format, không bảo đảm mọi phát biểu đều đúng. Cần đọc nhãn audit và đối chiếu nguồn.
- Metadata filter, reranker và multimodal bonus không được triển khai. Không tuyên bố đạt điểm rubric cụ thể.
- Repo nộp cần quyền xem của giảng viên; không commit .env/API key/cache private. Chưa push hay nộp thay học viên.

## Nguồn kỹ thuật

- https://ai.google.dev/gemini-api/docs/function-calling
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/billing
- https://greenteapress.com/thinkstats2/thinkstats2.pdf
