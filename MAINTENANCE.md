# Các sửa lỗi sau benchmark frozen_v1

Các kết quả 5/5 câu có đáp án và 2/2 câu thiếu bằng chứng đã công bố thuộc bản **frozen_v1**, không phải một lần đánh giá độc lập cho mã nguồn mới.

Toàn bộ source, benchmark, config, dữ liệu, trace, review và lock cũ được chép giữ nguyên byte trong `artifacts/frozen_v1`. Manifest ghi hash từng file. Không có .env, .venv, .cache hay khóa API trong snapshot. Không chạy các script ghi file bên trong snapshot vì sẽ làm đổi bằng chứng gốc.

| Vấn đề | Sửa ở bản hiện tại |
|---|---|
| Citation không hợp lệ bị chuyển thành abstain | Ghi status=error, giữ raw_answer/raw_citations và reason. Từ chối vì thật sự thiếu bằng chứng vẫn là abstain. |
| ValueError/KeyError từ hệ thống ngoài có thể chứa thông tin kết nối | Chỉ công khai thông báo từ ProviderError và AgentValidationError do ứng dụng kiểm soát; exception ngoài được ghi tên loại và thông báo chung. |
| Tool tìm kiếm thất bại không có event | Ghi search_error, query, tên tool, loại lỗi và số lượt đã thử. |
| Answer rỗng/citation lặp có thể lọt gate | Được xem là lỗi output, không phải câu trả lời thành công. |
| .env Windows có UTF-8 BOM | Đọc cả cấu hình Day 7 và Day 6 bằng utf-8-sig; giữ ưu tiên biến môi trường. |
| Split không có câu answerable gây chia cho 0 | Metric không áp dụng là null; freeze từ chối dev không đủ số câu. |
| Agent lỗi làm bỏ qua bước tổng hợp | Lưu summary/packet một phần trong finally; không thay lỗi bằng kết quả giả. |
| Review generator ghi đè điểm, tác giả và student_verified | Hai script chỉ xác minh nhãn đã tồn tại và đúng hash; không viết lại file nhãn. |
| Aggregator dùng nhãn lỗi thời và reviewer cố định | Kiểm tra trace hash, lấy reviewer/xác nhận từ nhãn thật, loại trace error khỏi điểm chất lượng. |
| Thiếu trace làm verifier crash ở nhánh aggregate | Ghi check không đạt và exit code 1; vẫn xuất báo cáo kiểm tra. |
| Code thay đổi sau selection lock | Giữ nguyên lock và snapshot cũ; verifier báo rõ current_pipeline_matches_lock=false, kiểm tra riêng archive và trace cũ. |

## Ý nghĩa metric citation

`answer_citation_n/N` chỉ tính trên output có status=answered. Vì agent chỉ cho answered khi citation hợp lệ về hình thức, chỉ số này có thể là 100% theo thiết kế. Đây không phải bằng chứng câu trả lời đúng. `citation_n/N` dùng nhãn đọc nguồn, grounded answer và false abstention mới phản ánh các khía cạnh chất lượng tương ứng. Bản sửa thêm mô tả phạm vi metric để tránh diễn giải nhầm.

## Kiểm chứng

```bash
./.venv/Scripts/python.exe -B -X utf8 -m scripts.check_all
./.venv/Scripts/python.exe -B -X utf8 -m scripts.replay_regression
```

Bộ test mới kiểm tra nhánh lỗi bằng tình huống giả lập; không gọi Gemini. Replay phát lại 99 quyết định/tool result đã lưu và so trạng thái, answer, citation, context, context ID và số search. Nó không đo lại model và không phải held-out benchmark mới. Không lấy kết quả này để tuyên bố code mới đã được đánh giá độc lập.

Nhãn do học viên sửa phải được giữ nguyên, bao gồm reviewer, reason, grade, thời gian và student_verified. Sau khi đọc/sửa review_labels.json, dùng scripts.report để tổng hợp; scripts.workbook để xuất workbook. Không tự đánh dấu đã rà soát khi chưa đọc nguồn.
