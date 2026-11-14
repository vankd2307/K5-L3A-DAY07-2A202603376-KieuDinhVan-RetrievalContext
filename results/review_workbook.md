# Workbook rà soát Day 7

Nhãn dưới đây do Codex đọc đối chiếu nguồn. Chưa đánh dấu học viên xác nhận. Hãy đọc ít nhất toàn bộ 7 test × 2 cấu hình và các lỗi dev trước nộp. Nếu đồng ý/sửa nhãn, cập nhật student_verified và lý do trong review_labels.json rồi xuất lại báo cáo.

## TEST

### baseline / d7-t01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Pmf.Copy dùng để làm gì và có làm thay đổi Pmf gốc không?

**Kết quả:** Phương thức `Pmf.Copy` được dùng để tạo ra một bản sao của đối tượng Pmf, cho phép bạn thực hiện việc tạo và chỉnh sửa bản sao đó mà không làm ảnh hưởng đến đối tượng Pmf gốc [43bd289ef6813bfb7273739b].

**Chuẩn:** Tạo bản sao Pmf để có thể sửa bản sao mà không ảnh hưởng bản gốc.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 53 nêu Copy tạo và sửa bản sao mà không ảnh hưởng bản gốc; answer giữ đủ cả mục đích và điều kiện không sửa gốc.

[Trace đầy đủ](test/baseline/agent/d7-t01.json)

- Citation `43bd289ef6813bfb7273739b`: PDF page 53, printed page 33; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-t02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** UnbiasPmf hiệu chỉnh xác suất theo sĩ số lớp x bằng cách nào, và bước cuối là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Chia từng xác suất cho x (nhân với 1.0/x), sau đó Normalize để chuẩn hóa lại.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 58: UnbiasPmf nhân từng xác suất với 1.0/x rồi Normalize. Đúng phép toán và đúng bước cuối. Baseline giữ đoạn BiasPmf PDF 57, thiếu UnbiasPmf/Normalize; từ chối nhầm, context chỉ liên quan một phần.

[Trace đầy đủ](test/baseline/agent/d7-t02.json)


### baseline / d7-t03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao tỷ lệ sinh viên trên giảng viên khoảng 10:1 không đồng nghĩa lớp trung bình có 10 người? Nêu hai lý do.

**Kết quả:** Tỷ lệ sinh viên trên giảng viên khoảng 10:1 không đồng nghĩa với việc lớp học trung bình có 10 người vì hai lý do sau:
1. Sinh viên thường học 4–5 lớp mỗi học kỳ, trong khi giảng viên thường chỉ dạy 1 hoặc 2 lớp [710efd907cbf9c83dd4f8018].
2. Số lượng sinh viên học trong các lớp nhỏ thì ít, trong khi số lượng sinh viên tham gia các lớp lớn thì rất nhiều (hiệu ứng quy mô lớp học lớn thu hút đông sinh viên hơn) [710efd907cbf9c83dd4f8018].

**Chuẩn:** Sinh viên học 4–5 lớp mỗi kỳ trong khi giảng viên thường dạy 1–2; lớp đông có nhiều sinh viên quan sát hơn lớp nhỏ.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 56 nêu sinh viên học 4–5 lớp, giảng viên dạy 1–2 và nhiều sinh viên quan sát lớp đông hơn lớp nhỏ; answer bao phủ hai lý do.

[Trace đầy đủ](test/baseline/agent/d7-t03.json)

- Citation `710efd907cbf9c83dd4f8018`: PDF page 56, printed page 36; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-t04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong ví dụ chạy tiếp sức, xác suất hai người chạy vượt nhau tỷ lệ với đại lượng nào, và vì sao ít gặp người cùng tốc độ?

**Kết quả:** Trong ví dụ chạy tiếp sức, xác suất vượt qua một người chạy khác (hoặc bị vượt) tỷ lệ thuận với **độ chênh lệch tốc độ** giữa hai người ($$is proportional to the difference in our speeds$$) [004c768971ba76dd4ebdb170]. 

Vì lý do này, bạn có nhiều khả năng bắt kịp một người chạy chậm hơn và nhiều khả năng bị bắt bởi một người chạy nhanh hơn [004c768971ba76dd4ebdb170]. Do đó, những người chạy ở cùng tốc độ có độ chênh lệch tốc độ bằng 0 (hoặc rất nhỏ), khiến xác suất họ gặp và nhìn thấy nhau là cực kỳ thấp [004c768971ba76dd4ebdb170].

**Chuẩn:** Tỷ lệ với chênh lệch tốc độ; người cùng tốc độ ít có khả năng vượt hoặc bị vượt nên khó gặp nhau.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 62 nói cơ hội vượt/bị vượt tỷ lệ chênh lệch tốc độ, ít gặp người cùng tốc độ; answer đúng đại lượng và cơ chế.

[Trace đầy đủ](test/baseline/agent/d7-t04.json)

- Citation `004c768971ba76dd4ebdb170`: PDF page 62, printed page 42; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-t05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Bài tập yêu cầu kiểm tra hai hàm PmfMean và PmfVar tự viết bằng cách đối chiếu với các phương thức nào?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Đối chiếu với Mean và Var do Pmf cung cấp.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 62 yêu cầu kiểm tra PmfMean/PmfVar nhất quán với Mean/Var của Pmf, đúng cả hai tên phương thức. Baseline có context rỗng, không đủ evidence và từ chối câu có đáp án.

[Trace đầy đủ](test/baseline/agent/d7-t05.json)


### baseline / d7-u03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong ví dụ khảo sát sĩ số lớp, học phí chính xác của từng sinh viên là bao nhiêu USD?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The class-size example contains sizes/counts, not student-level tuition amounts.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đối chiếu toàn bộ 42 trang và câu hỏi: không có học phí từng sinh viên (u03) hoặc benchmark H100/PmfMean (u04). Agent từ chối rõ ràng, không thêm số liệu suy đoán.

[Trace đầy đủ](test/baseline/agent/d7-u03.json)


### baseline / d7-u04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả báo cáo độ trễ trung bình bao nhiêu mili giây khi chạy PmfMean trên GPU NVIDIA H100?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The corpus has no H100 hardware benchmark or PmfMean timing result.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đối chiếu toàn bộ 42 trang và câu hỏi: không có học phí từng sinh viên (u03) hoặc benchmark H100/PmfMean (u04). Agent từ chối rõ ràng, không thêm số liệu suy đoán.

[Trace đầy đủ](test/baseline/agent/d7-u04.json)


### dense_context / d7-t01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Pmf.Copy dùng để làm gì và có làm thay đổi Pmf gốc không?

**Kết quả:** Phương thức `Pmf.Copy()` được dùng để tạo và chỉnh sửa một bản sao mà không làm ảnh hưởng đến Pmf gốc [43bd289ef6813bfb7273739b]. Do đó, nó không làm thay đổi Pmf gốc [43bd289ef6813bfb7273739b].

**Chuẩn:** Tạo bản sao Pmf để có thể sửa bản sao mà không ảnh hưởng bản gốc.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 53 nêu Copy tạo và sửa bản sao mà không ảnh hưởng bản gốc; answer giữ đủ cả mục đích và điều kiện không sửa gốc.

[Trace đầy đủ](test/dense_context/agent/d7-t01.json)

- Citation `43bd289ef6813bfb7273739b`: PDF page 53, printed page 33; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-t02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** UnbiasPmf hiệu chỉnh xác suất theo sĩ số lớp x bằng cách nào, và bước cuối là gì?

**Kết quả:** Hàm `UnbiasPmf` hiệu chỉnh xác suất theo sĩ số lớp $x$ bằng cách chia xác suất của mỗi lớp cho $x$ (hoặc nhân với $1.0/x$) [28f79f47128ffffd50f881e4]. Bước cuối cùng của hàm là chuẩn hóa phân phối (normalization) thông qua phương thức `new_pmf.Normalize()` [28f79f47128ffffd50f881e4].

**Chuẩn:** Chia từng xác suất cho x (nhân với 1.0/x), sau đó Normalize để chuẩn hóa lại.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 58: UnbiasPmf nhân từng xác suất với 1.0/x rồi Normalize. Đúng phép toán và đúng bước cuối.

[Trace đầy đủ](test/dense_context/agent/d7-t02.json)

- Citation `28f79f47128ffffd50f881e4`: PDF page 58, printed page 38; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-t03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao tỷ lệ sinh viên trên giảng viên khoảng 10:1 không đồng nghĩa lớp trung bình có 10 người? Nêu hai lý do.

**Kết quả:** Tỷ lệ sinh viên trên giảng viên khoảng 10:1 không đồng nghĩa lớp trung bình có 10 người vì hai lý do sau:

1. Sinh viên thường học từ 4 đến 5 lớp mỗi học kỳ, trong khi giảng viên thường dạy 1 hoặc 2 lớp [710efd907cbf9c83dd4f8018].
2. Số lượng sinh viên trải nghiệm lớp học nhỏ thì ít, nhưng số lượng sinh viên có mặt trong một lớp học lớn lại rất nhiều (hiệu ứng quy mô lớp học hoặc lấy mẫu bị chệch) [710efd907cbf9c83dd4f8018].

**Chuẩn:** Sinh viên học 4–5 lớp mỗi kỳ trong khi giảng viên thường dạy 1–2; lớp đông có nhiều sinh viên quan sát hơn lớp nhỏ.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 56 nêu sinh viên học 4–5 lớp, giảng viên dạy 1–2 và nhiều sinh viên quan sát lớp đông hơn lớp nhỏ; answer bao phủ hai lý do.

[Trace đầy đủ](test/dense_context/agent/d7-t03.json)

- Citation `710efd907cbf9c83dd4f8018`: PDF page 56, printed page 36; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-t04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong ví dụ chạy tiếp sức, xác suất hai người chạy vượt nhau tỷ lệ với đại lượng nào, và vì sao ít gặp người cùng tốc độ?

**Kết quả:** Trong ví dụ chạy tiếp sức, xác suất vượt qua một người chạy khác (hoặc bị vượt) tỷ lệ thuận với **độ chênh lệch tốc độ** giữa hai người (the difference in our speeds) [004c768971ba76dd4ebdb170]. 

Lý do ít gặp người có cùng tốc độ là vì bạn có nhiều khả năng bắt kịp một người chạy chậm hơn và có nhiều khả năng bị vượt bởi một người chạy nhanh hơn, trong khi những người chạy ở cùng mức tốc độ với bạn rất ít khi có cơ hội nhìn thấy nhau trên đường đua [004c768971ba76dd4ebdb170].

**Chuẩn:** Tỷ lệ với chênh lệch tốc độ; người cùng tốc độ ít có khả năng vượt hoặc bị vượt nên khó gặp nhau.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 62 nói cơ hội vượt/bị vượt tỷ lệ chênh lệch tốc độ, ít gặp người cùng tốc độ; answer đúng đại lượng và cơ chế.

[Trace đầy đủ](test/dense_context/agent/d7-t04.json)

- Citation `004c768971ba76dd4ebdb170`: PDF page 62, printed page 42; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-t05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Bài tập yêu cầu kiểm tra hai hàm PmfMean và PmfVar tự viết bằng cách đối chiếu với các phương thức nào?

**Kết quả:** Bài tập yêu cầu kiểm tra hai hàm `PmfMean` và `PmfVar` tự viết bằng cách đối chiếu xem chúng có nhất quán (consistent) với các phương thức `Mean` và `Var` do lớp `Pmf` cung cấp hay không [54dd11dc5985db806f55aedd].

**Chuẩn:** Đối chiếu với Mean và Var do Pmf cung cấp.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 62 yêu cầu kiểm tra PmfMean/PmfVar nhất quán với Mean/Var của Pmf, đúng cả hai tên phương thức.

[Trace đầy đủ](test/dense_context/agent/d7-t05.json)

- Citation `54dd11dc5985db806f55aedd`: PDF page 62, printed page 42; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-u03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong ví dụ khảo sát sĩ số lớp, học phí chính xác của từng sinh viên là bao nhiêu USD?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The class-size example contains sizes/counts, not student-level tuition amounts.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đối chiếu toàn bộ 42 trang và câu hỏi: không có học phí từng sinh viên (u03) hoặc benchmark H100/PmfMean (u04). Agent từ chối rõ ràng, không thêm số liệu suy đoán.

[Trace đầy đủ](test/dense_context/agent/d7-u03.json)


### dense_context / d7-u04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả báo cáo độ trễ trung bình bao nhiêu mili giây khi chạy PmfMean trên GPU NVIDIA H100?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The corpus has no H100 hardware benchmark or PmfMean timing result.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đối chiếu toàn bộ 42 trang và câu hỏi: không có học phí từng sinh viên (u03) hoặc benchmark H100/PmfMean (u04). Agent từ chối rõ ràng, không thêm số liệu suy đoán.

[Trace đầy đủ](test/dense_context/agent/d7-u04.json)


## DEV

### baseline / d7-q01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao việc chỉ lấy ý kiến người tham gia thảo luận về con đầu sinh muộn có thể gây selection bias?

**Kết quả:** Việc chỉ lấy ý kiến của những người tham gia thảo luận về con đầu sinh muộn có thể gây ra lựa chọn chệch (selection bias) vì những người tham gia có thể là những người có sự quan tâm đặc biệt đến vấn đề này (ví dụ: con đầu lòng của họ sinh muộn), do đó quá trình lựa chọn dữ liệu sẽ làm chệch kết quả của phân tích [54f0c801e3aa64b436f8c68f].

**Chuẩn:** Người tham gia có thể quan tâm vì con đầu của họ sinh muộn; cách chọn dữ liệu làm lệch kết quả.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** Đối chiếu PDF 22: người tham gia có con đầu sinh muộn tự chọn vào thảo luận, làm lệch mẫu/kết quả.

[Trace đầy đủ](dev/baseline/agent/d7-q01.json)

- Citation `54f0c801e3aa64b436f8c68f`: PDF page 22, printed page 2; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nghiên cứu cross-sectional khác longitudinal về thời điểm quan sát như thế nào?

**Kết quả:** Nghiên cứu cross-sectional (cắt ngang) và nghiên cứu longitudinal (dọc) khác nhau về thời điểm quan sát như sau:
- Nghiên cứu cross-sectional thu thập dữ liệu về một tổng thể tại một thời điểm cụ thể [a6a5f497332f50f7f5a86fb6].
- Nghiên cứu longitudinal theo dõi một tổng thể theo thời gian, thu thập dữ liệu từ cùng một nhóm đối tượng lặp đi lặp lại [a6a5f497332f50f7f5a86fb6].

**Chuẩn:** Cross-sectional chụp một nhóm tại một thời điểm; longitudinal quan sát lặp lại qua thời gian.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 hoặc glossary PDF 35 nêu snapshot một thời điểm và theo dõi lặp cùng nhóm theo thời gian. Glossary là evidence tương đương dù strict gold chỉ ở PDF 23.

[Trace đầy đủ](dev/baseline/agent/d7-q02.json)

- Citation `a6a5f497332f50f7f5a86fb6`: PDF page 35, printed page 15; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Quần thể mục tiêu của khảo sát NSFG trong sách gồm những ai?

**Kết quả:** Quần thể mục tiêu của khảo sát NSFG (National Survey of Family Growth) trong sách là những người ở Hoa Kỳ trong độ tuổi từ 15 đến 44 [f40266243aa427f23fa90b4e].

**Chuẩn:** Người ở Hoa Kỳ từ 15 đến 44 tuổi.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 ghi rõ quần thể Hoa Kỳ 15–44 tuổi, đúng cả địa lý và khoảng tuổi.

[Trace đầy đủ](dev/baseline/agent/d7-q03.json)

- Citation `f40266243aa427f23fa90b4e`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 1, NSFG lấy mẫu vượt tỷ lệ ở ba nhóm nào và nhằm mục đích gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Hispanics, African-Americans và teenagers; để đủ số người trả lời cho suy luận thống kê hợp lệ trong từng nhóm.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 24 nêu đủ Hispanics, African-Americans, teenagers và mục đích có đủ respondents cho statistical inference. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/baseline/agent/d7-q04.json)


### baseline / d7-q05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Stata dictionary mô tả những thuộc tính nào để tìm biến trong mỗi dòng dữ liệu?

**Kết quả:** Stata dictionary mô tả các thuộc tính bao gồm tên biến (variable names), kiểu dữ liệu (types), và các chỉ số (indices) xác định vị trí ở mỗi dòng để tìm ra từng biến [5869e54397098a669dd0b81e].

**Chuẩn:** Tên biến, kiểu và chỉ số/vị trí của biến trên mỗi dòng.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 25 mô tả variable names/types/indices cùng ví dụ _column. Answer giữ đủ ba thuộc tính.

[Trace đầy đủ](dev/baseline/agent/d7-q05.json)

- Citation `5869e54397098a669dd0b81e`: PDF page 25, printed page 5; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q06

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** DataFrame NSFG được minh họa có bao nhiêu bản ghi và biến?

**Kết quả:** DataFrame NSFG được minh họa có 13.593 bản ghi (hàng/rows) và 244 biến (cột/variables) [ee672fe7059e3b9d2b8e2207].

**Chuẩn:** 13.593 bản ghi và 244 biến.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 26–27: shape có 13593 rows và 244 columns; đoạn Variables cũng xác nhận 244 biến. Đọc cả hai citation nếu được gộp.

[Trace đầy đủ](dev/baseline/agent/d7-q06.json)

- Citation `ee672fe7059e3b9d2b8e2207`: PDF page 26, printed page 6; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q07

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Mã outcome nào thể hiện một ca sinh sống?

**Kết quả:** Mã outcome là 1 thể hiện một ca sinh sống (live birth) [f5d4f52297470390e5b98ec6].

**Chuẩn:** Mã 1.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 28 hoặc bảng kiểm chứng PDF 30: outcome=1 là live birth. Không lẫn với pregordr/birthord.

[Trace đầy đủ](dev/baseline/agent/d7-q07.json)

- Citation `f5d4f52297470390e5b98ec6`: PDF page 28, printed page 8; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q08

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tại sao CleanFemPreg chia agepreg cho 100?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Dữ liệu lưu tuổi bằng số nguyên centiyears; chia 100 để đổi sang số năm dạng số thực.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 29 giải thích agepreg là integer centiyears; chia 100 đổi sang floating-point years, không chỉ nhắc phép chia. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/baseline/agent/d7-q08.json)


### baseline / d7-q09

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nếu cân nặng chứa mã 97, 98 hoặc 99 thì phải xử lý thế nào để tránh kết quả sai?

**Kết quả:** Các giá trị đặc biệt mã hóa bằng số (như 97, 98, hoặc 99 biểu thị NOT ASCERTAINED, REFUSED, DON'T KNOW) có thể gây ra kết quả sai (chẳng hạn như một em bé nặng 99 pound nếu không được xử lý đúng cách) [50718039f1ba18056fe56194]. Để tránh điều này, bạn cần sử dụng phương thức `replace` để thay thế các giá trị này bằng `np.nan` (một giá trị số thực đặc biệt đại diện cho "không phải là số" - "not a number") [50718039f1ba18056fe56194]. Theo chuẩn dấu phẩy động IEEE, mọi phép toán sẽ trả về `nan` nếu có ít nhất một đối số là `nan` [50718039f1ba18056fe56194].

**Chuẩn:** Đó là mã thiếu thông tin, từ chối hoặc không biết; thay bằng np.nan trước khi tính toán.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 29 nêu 97/98/99 là mã thiếu/refused/unknown; replace thành np.nan tránh số liệu giả.

[Trace đầy đủ](dev/baseline/agent/d7-q09.json)

- Citation `50718039f1ba18056fe56194`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q10

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Khi thêm cột vào DataFrame, vì sao không nên gán bằng dot notation?

**Kết quả:** Khi thêm cột vào một DataFrame, bạn không nên gán bằng cú pháp chấm (dot notation) vì cách này sẽ chỉ thêm một thuộc tính (attribute) vào đối tượng DataFrame chứ không xem thuộc tính đó là một cột mới [798698989f39c80a59059a9a]. Thay vào đó, bạn phải sử dụng cú pháp từ điển (dictionary syntax, ví dụ: `df['ten_cot'] = ...`) [798698989f39c80a59059a9a].

**Chuẩn:** Phải dùng dictionary syntax; dot notation chỉ thêm thuộc tính và không được coi là cột mới.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 30: dot notation thêm attribute, không thêm column; phải dùng dictionary syntax.

[Trace đầy đủ](dev/baseline/agent/d7-q10.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q11

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Một cách kiểm chứng dữ liệu sau khi chuyển giữa hai môi trường phần mềm là gì?

**Kết quả:** Một cách kiểm chứng dữ liệu khi chuyển từ môi trường phần mềm này sang môi trường phần mềm khác là thực hiện bước xác thực dữ liệu (validation) nhằm phòng tránh các lỗi có thể phát sinh trong quá trình xuất và nhập dữ liệu [798698989f39c80a59059a9a].

**Chuẩn:** Tính thống kê cơ bản rồi đối chiếu kết quả đã công bố, ví dụ bảng tổng hợp trong codebook.

**Nhãn:** answer=1, context=1, citation=[True], abstention=None

**Lý do:** PDF 30 chỉ nói nên validation để tránh lỗi. Answer nhắc mục tiêu nhưng không đưa cách tính thống kê rồi đối chiếu published table; đúng một phần, context thiếu bước cụ thể. Citation hỗ trợ phát biểu chung.

[Trace đầy đủ](dev/baseline/agent/d7-q11.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-q12

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** CleanFemPreg xử lý birthwgt_lb vượt 20 như thế nào?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Thay các giá trị vượt 20 bằng np.nan.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 42 nêu thay birthwgt_lb >20 thành np.nan. Thay mã 97/98/99 không trả lời điều kiện >20. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/baseline/agent/d7-q12.json)


### baseline / d7-q13

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 2, histogram thể hiện điều gì và frequency nghĩa là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Histogram cho biết tần số từng giá trị; frequency là số lần giá trị xuất hiện.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 37 hoặc glossary PDF 50 và API Hist PDF 38: histogram ánh xạ value→frequency, frequency là số lần xuất hiện. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/baseline/agent/d7-q13.json)


### baseline / d7-q14

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả phân biệt mean và average như thế nào?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Mean là thống kê tính theo công thức tổng chia số lượng; average có thể là một trong nhiều thống kê mô tả xu hướng trung tâm.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 45 phân biệt mean theo công thức và average là lựa chọn summary statistic của central tendency; ví dụ pumpkin PDF 46 chỉ minh họa một phần. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/baseline/agent/d7-q14.json)


### baseline / d7-q15

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Độ lệch chuẩn có quan hệ gì với phương sai?

**Kết quả:** Độ lệch chuẩn là căn bậc hai của phương sai [d3270a2b867639b7ed5e52b2].

**Chuẩn:** Độ lệch chuẩn là căn bậc hai của phương sai, cũng đo độ phân tán.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 46/50 nêu standard deviation là square root of variance; đúng quan hệ được hỏi.

[Trace đầy đủ](dev/baseline/agent/d7-q15.json)

- Citation `d3270a2b867639b7ed5e52b2`: PDF page 46, printed page 26; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### baseline / d7-u01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong bộ tài liệu, tỷ lệ người trả lời NSFG sử dụng Python 3.12 là bao nhiêu phần trăm?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Corpus describes NSFG and Python but does not report respondent Python-version usage.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/baseline/agent/d7-u01.json)


### baseline / d7-u02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong nghiên cứu NSFG được mô tả, mã API cá nhân của từng người tham gia là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The book reports survey methodology, not participants personal API credentials.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/baseline/agent/d7-u02.json)


### dense / d7-q01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao việc chỉ lấy ý kiến người tham gia thảo luận về con đầu sinh muộn có thể gây selection bias?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Người tham gia có thể quan tâm vì con đầu của họ sinh muộn; cách chọn dữ liệu làm lệch kết quả.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** Đối chiếu PDF 22: người tham gia có con đầu sinh muộn tự chọn vào thảo luận, làm lệch mẫu/kết quả. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense/agent/d7-q01.json)


### dense / d7-q02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nghiên cứu cross-sectional khác longitudinal về thời điểm quan sát như thế nào?

**Kết quả:** Nghiên cứu cross-sectional (cắt ngang) khác với nghiên cứu longitudinal (dọc) ở điểm: nghiên cứu cắt ngang ghi lại một bức ảnh chụp nhanh (snapshot) của một nhóm đối tượng tại một thời điểm, trong khi nghiên cứu dọc quan sát một nhóm đối tượng lặp đi lặp lại trong một khoảng thời gian [c820376c2fde59d33d4d8bc8].

**Chuẩn:** Cross-sectional chụp một nhóm tại một thời điểm; longitudinal quan sát lặp lại qua thời gian.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 hoặc glossary PDF 35 nêu snapshot một thời điểm và theo dõi lặp cùng nhóm theo thời gian. Glossary là evidence tương đương dù strict gold chỉ ở PDF 23.

[Trace đầy đủ](dev/dense/agent/d7-q02.json)

- Citation `c820376c2fde59d33d4d8bc8`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Quần thể mục tiêu của khảo sát NSFG trong sách gồm những ai?

**Kết quả:** Quần thể mục tiêu của khảo sát NSFG (National Survey of Family Growth) trong sách là những người ở Hoa Kỳ trong độ tuổi từ 15 đến 44 [f40266243aa427f23fa90b4e].

**Chuẩn:** Người ở Hoa Kỳ từ 15 đến 44 tuổi.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 ghi rõ quần thể Hoa Kỳ 15–44 tuổi, đúng cả địa lý và khoảng tuổi.

[Trace đầy đủ](dev/dense/agent/d7-q03.json)

- Citation `f40266243aa427f23fa90b4e`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 1, NSFG lấy mẫu vượt tỷ lệ ở ba nhóm nào và nhằm mục đích gì?

**Kết quả:** Trong Chương 1, NSFG lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm là: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e]. 

Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn nhằm đưa ra các suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e].

**Chuẩn:** Hispanics, African-Americans và teenagers; để đủ số người trả lời cho suy luận thống kê hợp lệ trong từng nhóm.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 24 nêu đủ Hispanics, African-Americans, teenagers và mục đích có đủ respondents cho statistical inference.

[Trace đầy đủ](dev/dense/agent/d7-q04.json)

- Citation `8bca2eddf8d8ed85185da77e`: PDF page 24, printed page 4; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Stata dictionary mô tả những thuộc tính nào để tìm biến trong mỗi dòng dữ liệu?

**Kết quả:** Trong ngữ cảnh của file Stata dictionary, "dictionary" là một danh sách bao gồm tên biến (variable names), kiểu dữ liệu (types) và chỉ số (indices) – cụ thể là vị trí cột (_column) – mô tả vị trí tìm thấy từng biến trong mỗi dòng dữ liệu [5869e54397098a669dd0b81e].

**Chuẩn:** Tên biến, kiểu và chỉ số/vị trí của biến trên mỗi dòng.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 25 mô tả variable names/types/indices cùng ví dụ _column. Answer giữ đủ ba thuộc tính.

[Trace đầy đủ](dev/dense/agent/d7-q05.json)

- Citation `5869e54397098a669dd0b81e`: PDF page 25, printed page 5; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q06

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** DataFrame NSFG được minh họa có bao nhiêu bản ghi và biến?

**Kết quả:** DataFrame NSFG được minh họa có 13.593 bản ghi (hàng/rows) và 244 biến (cột/columns) [ee672fe7059e3b9d2b8e2207].

**Chuẩn:** 13.593 bản ghi và 244 biến.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 26–27: shape có 13593 rows và 244 columns; đoạn Variables cũng xác nhận 244 biến. Đọc cả hai citation nếu được gộp.

[Trace đầy đủ](dev/dense/agent/d7-q06.json)

- Citation `ee672fe7059e3b9d2b8e2207`: PDF page 26, printed page 6; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q07

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Mã outcome nào thể hiện một ca sinh sống?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Mã 1.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 28 hoặc bảng kiểm chứng PDF 30: outcome=1 là live birth. Không lẫn với pregordr/birthord. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense/agent/d7-q07.json)


### dense / d7-q08

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tại sao CleanFemPreg chia agepreg cho 100?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Dữ liệu lưu tuổi bằng số nguyên centiyears; chia 100 để đổi sang số năm dạng số thực.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 29 giải thích agepreg là integer centiyears; chia 100 đổi sang floating-point years, không chỉ nhắc phép chia. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense/agent/d7-q08.json)


### dense / d7-q09

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nếu cân nặng chứa mã 97, 98 hoặc 99 thì phải xử lý thế nào để tránh kết quả sai?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Đó là mã thiếu thông tin, từ chối hoặc không biết; thay bằng np.nan trước khi tính toán.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 29 nêu 97/98/99 là mã thiếu/refused/unknown; replace thành np.nan tránh số liệu giả. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense/agent/d7-q09.json)


### dense / d7-q10

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Khi thêm cột vào DataFrame, vì sao không nên gán bằng dot notation?

**Kết quả:** Khi thêm cột vào DataFrame, bạn không nên gán bằng dot notation (ví dụ: `df.totalwgt_lb = ...`) vì cách viết này chỉ thêm một thuộc tính (attribute) vào đối tượng DataFrame chứ không được xem như một cột mới [798698989f39c80a59059a9a]. Thay vào đó, bạn phải sử dụng cú pháp từ điển (ví dụ: `df['totalwgt_lb'] = ...`) [798698989f39c80a59059a9a].

**Chuẩn:** Phải dùng dictionary syntax; dot notation chỉ thêm thuộc tính và không được coi là cột mới.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 30: dot notation thêm attribute, không thêm column; phải dùng dictionary syntax.

[Trace đầy đủ](dev/dense/agent/d7-q10.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q11

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Một cách kiểm chứng dữ liệu sau khi chuyển giữa hai môi trường phần mềm là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Tính thống kê cơ bản rồi đối chiếu kết quả đã công bố, ví dụ bảng tổng hợp trong codebook.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 30–31 hoặc đoạn codebook PDF 33: so sánh thống kê/value counts với published table là một cách validation cụ thể. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense/agent/d7-q11.json)


### dense / d7-q12

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** CleanFemPreg xử lý birthwgt_lb vượt 20 như thế nào?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Thay các giá trị vượt 20 bằng np.nan.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 42 nêu thay birthwgt_lb >20 thành np.nan. Thay mã 97/98/99 không trả lời điều kiện >20. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense/agent/d7-q12.json)


### dense / d7-q13

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 2, histogram thể hiện điều gì và frequency nghĩa là gì?

**Kết quả:** Trong Chương 2, histogram là một biểu đồ thể hiện tần suất (frequency) của từng giá trị xuất hiện trong tập dữ liệu [8849532a0610912f69f6978d]. Trong ngữ cảnh này, "frequency" (tần suất) có nghĩa là số lần mà một giá trị xuất hiện [8849532a0610912f69f6978d].

**Chuẩn:** Histogram cho biết tần số từng giá trị; frequency là số lần giá trị xuất hiện.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 37 hoặc glossary PDF 50 và API Hist PDF 38: histogram ánh xạ value→frequency, frequency là số lần xuất hiện.

[Trace đầy đủ](dev/dense/agent/d7-q13.json)

- Citation `8849532a0610912f69f6978d`: PDF page 37, printed page 17; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q14

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả phân biệt mean và average như thế nào?

**Kết quả:** Trong sách *Think Stats*, tác giả phân biệt khái niệm "mean" (số trung bình) và "average" (giá trị trung bình/đại diện) qua các ví dụ như sau:

* **Mean (Số trung bình):** Là một phép tính toán học cụ thể (tổng của các giá trị chia cho số lượng giá trị) [4321b3f26f9d26c0b20e8a04]. Ví dụ, khi thu hoạch 6 quả bí ngô có trọng lượng lần lượt là 1, 1, 1, 3, 3 và 591 pound, số trung bình (mean) của mẫu này là 100 pound [4321b3f26f9d26c0b20e8a04].
* **Average (Giá trị đại diện/trung bình thông thường):** Thường được dùng như một bản tóm tắt hoặc mô tả cho một tập hợp giá trị [4321b3f26f9d26c0b20e8a04]. Tác giả chỉ ra rằng khi các giá trị khá đồng đều (chẳng hạn như những quả táo trong siêu thị có kích thước tương tự nhau), mean là một mô tả tốt và việc nói "mỗi quả nặng khoảng nửa cân" là một cách diễn đạt "average" hợp lý [4321b3f26f9d26c0b20e8a04]. Tuy nhiên, khi tập hợp dữ liệu có sự chênh lệch lớn (như các loại bí ngô khác nhau trong ví dụ trên), việc nói rằng "quả bí ngô trung bình (average) trong vườn của tôi nặng 100 pound" sẽ mang tính đánh lừa, bởi vì trong trường hợp này không có một giá trị "average" nào có ý nghĩa hay đại diện cho một quả bí ngô điển hình cả [4321b3f26f9d26c0b20e8a04].

**Chuẩn:** Mean là thống kê tính theo công thức tổng chia số lượng; average có thể là một trong nhiều thống kê mô tả xu hướng trung tâm.

**Nhãn:** answer=1, context=1, citation=[False], abstention=None

**Lý do:** PDF 46 có ví dụ mean và typical average nhưng không chứa công thức mean hoặc phân biệt average là một trong nhiều summary statistics. Answer đúng một phần; citation không hỗ trợ đầy đủ các khẳng định đã thêm.

[Trace đầy đủ](dev/dense/agent/d7-q14.json)

- Citation `4321b3f26f9d26c0b20e8a04`: PDF page 46, printed page 26; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-q15

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Độ lệch chuẩn có quan hệ gì với phương sai?

**Kết quả:** Độ lệch chuẩn là căn bậc hai của phương sai [d3270a2b867639b7ed5e52b2].

**Chuẩn:** Độ lệch chuẩn là căn bậc hai của phương sai, cũng đo độ phân tán.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 46/50 nêu standard deviation là square root of variance; đúng quan hệ được hỏi.

[Trace đầy đủ](dev/dense/agent/d7-q15.json)

- Citation `d3270a2b867639b7ed5e52b2`: PDF page 46, printed page 26; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense / d7-u01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong bộ tài liệu, tỷ lệ người trả lời NSFG sử dụng Python 3.12 là bao nhiêu phần trăm?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Corpus describes NSFG and Python but does not report respondent Python-version usage.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/dense/agent/d7-u01.json)


### dense / d7-u02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong nghiên cứu NSFG được mô tả, mã API cá nhân của từng người tham gia là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The book reports survey methodology, not participants personal API credentials.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/dense/agent/d7-u02.json)


### hybrid / d7-q01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao việc chỉ lấy ý kiến người tham gia thảo luận về con đầu sinh muộn có thể gây selection bias?

**Kết quả:** Việc chỉ lấy ý kiến của những người tham gia thảo luận về con đầu sinh muộn có thể gây ra lựa chọn chệch (selection bias) vì những người tham gia có thể là những người có sự quan tâm đặc biệt đến vấn đề này (ví dụ: con đầu lòng của họ sinh muộn), do đó quá trình lựa chọn dữ liệu sẽ làm chệch kết quả của phân tích [54f0c801e3aa64b436f8c68f].

**Chuẩn:** Người tham gia có thể quan tâm vì con đầu của họ sinh muộn; cách chọn dữ liệu làm lệch kết quả.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** Đối chiếu PDF 22: người tham gia có con đầu sinh muộn tự chọn vào thảo luận, làm lệch mẫu/kết quả.

[Trace đầy đủ](dev/hybrid/agent/d7-q01.json)

- Citation `54f0c801e3aa64b436f8c68f`: PDF page 22, printed page 2; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nghiên cứu cross-sectional khác longitudinal về thời điểm quan sát như thế nào?

**Kết quả:** Nghiên cứu cross-sectional (cắt ngang) và nghiên cứu longitudinal (dọc) khác nhau về thời điểm quan sát như sau:
- Nghiên cứu cross-sectional thu thập dữ liệu về một tổng thể tại một thời điểm cụ thể [a6a5f497332f50f7f5a86fb6].
- Nghiên cứu longitudinal theo dõi một tổng thể theo thời gian, thu thập dữ liệu từ cùng một nhóm đối tượng lặp đi lặp lại [a6a5f497332f50f7f5a86fb6].

**Chuẩn:** Cross-sectional chụp một nhóm tại một thời điểm; longitudinal quan sát lặp lại qua thời gian.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 hoặc glossary PDF 35 nêu snapshot một thời điểm và theo dõi lặp cùng nhóm theo thời gian. Glossary là evidence tương đương dù strict gold chỉ ở PDF 23.

[Trace đầy đủ](dev/hybrid/agent/d7-q02.json)

- Citation `a6a5f497332f50f7f5a86fb6`: PDF page 35, printed page 15; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Quần thể mục tiêu của khảo sát NSFG trong sách gồm những ai?

**Kết quả:** Quần thể mục tiêu của khảo sát NSFG (National Survey of Family Growth) trong sách là những người ở Hoa Kỳ trong độ tuổi từ 15 đến 44 [f40266243aa427f23fa90b4e].

**Chuẩn:** Người ở Hoa Kỳ từ 15 đến 44 tuổi.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 ghi rõ quần thể Hoa Kỳ 15–44 tuổi, đúng cả địa lý và khoảng tuổi.

[Trace đầy đủ](dev/hybrid/agent/d7-q03.json)

- Citation `f40266243aa427f23fa90b4e`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 1, NSFG lấy mẫu vượt tỷ lệ ở ba nhóm nào và nhằm mục đích gì?

**Kết quả:** Trong Chương 1, NSFG lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm là: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e]. 

Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn nhằm đưa ra các suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e].

**Chuẩn:** Hispanics, African-Americans và teenagers; để đủ số người trả lời cho suy luận thống kê hợp lệ trong từng nhóm.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 24 nêu đủ Hispanics, African-Americans, teenagers và mục đích có đủ respondents cho statistical inference.

[Trace đầy đủ](dev/hybrid/agent/d7-q04.json)

- Citation `8bca2eddf8d8ed85185da77e`: PDF page 24, printed page 4; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Stata dictionary mô tả những thuộc tính nào để tìm biến trong mỗi dòng dữ liệu?

**Kết quả:** Stata dictionary mô tả các thuộc tính bao gồm tên biến (variable names), kiểu dữ liệu (types), và các chỉ số (indices) xác định vị trí ở mỗi dòng để tìm ra từng biến [5869e54397098a669dd0b81e].

**Chuẩn:** Tên biến, kiểu và chỉ số/vị trí của biến trên mỗi dòng.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 25 mô tả variable names/types/indices cùng ví dụ _column. Answer giữ đủ ba thuộc tính.

[Trace đầy đủ](dev/hybrid/agent/d7-q05.json)

- Citation `5869e54397098a669dd0b81e`: PDF page 25, printed page 5; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q06

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** DataFrame NSFG được minh họa có bao nhiêu bản ghi và biến?

**Kết quả:** DataFrame NSFG được minh họa có 13.593 bản ghi (rows) và 244 biến (columns/variables) [2302c0aa2fd4d36ec776cd0e] [ee672fe7059e3b9d2b8e2207].

**Chuẩn:** 13.593 bản ghi và 244 biến.

**Nhãn:** answer=2, context=2, citation=[True, True], abstention=None

**Lý do:** PDF 26–27: shape có 13593 rows và 244 columns; đoạn Variables cũng xác nhận 244 biến. Đọc cả hai citation nếu được gộp.

[Trace đầy đủ](dev/hybrid/agent/d7-q06.json)

- Citation `2302c0aa2fd4d36ec776cd0e`: PDF page 27, printed page 7; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `ee672fe7059e3b9d2b8e2207`: PDF page 26, printed page 6; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q07

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Mã outcome nào thể hiện một ca sinh sống?

**Kết quả:** Mã outcome là 1 thể hiện một ca sinh sống (live birth) [f5d4f52297470390e5b98ec6].

**Chuẩn:** Mã 1.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 28 hoặc bảng kiểm chứng PDF 30: outcome=1 là live birth. Không lẫn với pregordr/birthord.

[Trace đầy đủ](dev/hybrid/agent/d7-q07.json)

- Citation `f5d4f52297470390e5b98ec6`: PDF page 28, printed page 8; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q08

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tại sao CleanFemPreg chia agepreg cho 100?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Dữ liệu lưu tuổi bằng số nguyên centiyears; chia 100 để đổi sang số năm dạng số thực.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 29 giải thích agepreg là integer centiyears; chia 100 đổi sang floating-point years, không chỉ nhắc phép chia. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/hybrid/agent/d7-q08.json)


### hybrid / d7-q09

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nếu cân nặng chứa mã 97, 98 hoặc 99 thì phải xử lý thế nào để tránh kết quả sai?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Đó là mã thiếu thông tin, từ chối hoặc không biết; thay bằng np.nan trước khi tính toán.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 29 nêu 97/98/99 là mã thiếu/refused/unknown; replace thành np.nan tránh số liệu giả. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/hybrid/agent/d7-q09.json)


### hybrid / d7-q10

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Khi thêm cột vào DataFrame, vì sao không nên gán bằng dot notation?

**Kết quả:** Khi thêm cột vào một DataFrame, bạn không nên gán bằng cú pháp chấm (dot notation) vì cách này sẽ chỉ thêm một thuộc tính (attribute) vào đối tượng DataFrame chứ không xem thuộc tính đó là một cột mới [798698989f39c80a59059a9a]. Thay vào đó, bạn phải sử dụng cú pháp từ điển (dictionary syntax, ví dụ: `df['ten_cot'] = ...`) [798698989f39c80a59059a9a].

**Chuẩn:** Phải dùng dictionary syntax; dot notation chỉ thêm thuộc tính và không được coi là cột mới.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 30: dot notation thêm attribute, không thêm column; phải dùng dictionary syntax.

[Trace đầy đủ](dev/hybrid/agent/d7-q10.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q11

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Một cách kiểm chứng dữ liệu sau khi chuyển giữa hai môi trường phần mềm là gì?

**Kết quả:** Một cách kiểm chứng dữ liệu khi chuyển từ môi trường phần mềm này sang môi trường phần mềm khác là thực hiện bước xác thực dữ liệu (validation) nhằm phòng tránh các lỗi có thể phát sinh trong quá trình xuất và nhập dữ liệu [798698989f39c80a59059a9a].

**Chuẩn:** Tính thống kê cơ bản rồi đối chiếu kết quả đã công bố, ví dụ bảng tổng hợp trong codebook.

**Nhãn:** answer=1, context=1, citation=[True], abstention=None

**Lý do:** PDF 30 chỉ nói nên validation để tránh lỗi. Answer nhắc mục tiêu nhưng không đưa cách tính thống kê rồi đối chiếu published table; đúng một phần, context thiếu bước cụ thể. Citation hỗ trợ phát biểu chung.

[Trace đầy đủ](dev/hybrid/agent/d7-q11.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q12

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** CleanFemPreg xử lý birthwgt_lb vượt 20 như thế nào?

**Kết quả:** Trong hàm `CleanFemPreg`, các giá trị NA (97, 98, 99) trong `birthwgt_lb` được thay thế thành `np.nan` [378c9ef8a37471ebdc49dd13]. Tài liệu không đề cập đến việc xử lý các giá trị `birthwgt_lb` vượt quá 20 [378c9ef8a37471ebdc49dd13].

**Chuẩn:** Thay các giá trị vượt 20 bằng np.nan.

**Nhãn:** answer=0, context=1, citation=[False], abstention=None

**Lý do:** Answer nói về 97/98/99 thay vì điều kiện >20 và kết luận tài liệu không đề cập dù PDF 42 có xử lý >20. Chunk PDF 29 được cite không chứng minh kết luận thiếu thông tin toàn corpus. Answer=0, context=1, citation không hỗ trợ toàn câu.

[Trace đầy đủ](dev/hybrid/agent/d7-q12.json)

- Citation `378c9ef8a37471ebdc49dd13`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-q13

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 2, histogram thể hiện điều gì và frequency nghĩa là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Histogram cho biết tần số từng giá trị; frequency là số lần giá trị xuất hiện.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 37 hoặc glossary PDF 50 và API Hist PDF 38: histogram ánh xạ value→frequency, frequency là số lần xuất hiện. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/hybrid/agent/d7-q13.json)


### hybrid / d7-q14

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả phân biệt mean và average như thế nào?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Mean là thống kê tính theo công thức tổng chia số lượng; average có thể là một trong nhiều thống kê mô tả xu hướng trung tâm.

**Nhãn:** answer=0, context=0, citation=[], abstention=None

**Lý do:** PDF 45 phân biệt mean theo công thức và average là lựa chọn summary statistic của central tendency; ví dụ pumpkin PDF 46 chỉ minh họa một phần. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 0/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/hybrid/agent/d7-q14.json)


### hybrid / d7-q15

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Độ lệch chuẩn có quan hệ gì với phương sai?

**Kết quả:** Độ lệch chuẩn là căn bậc hai của phương sai [d3270a2b867639b7ed5e52b2].

**Chuẩn:** Độ lệch chuẩn là căn bậc hai của phương sai, cũng đo độ phân tán.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 46/50 nêu standard deviation là square root of variance; đúng quan hệ được hỏi.

[Trace đầy đủ](dev/hybrid/agent/d7-q15.json)

- Citation `d3270a2b867639b7ed5e52b2`: PDF page 46, printed page 26; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid / d7-u01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong bộ tài liệu, tỷ lệ người trả lời NSFG sử dụng Python 3.12 là bao nhiêu phần trăm?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Corpus describes NSFG and Python but does not report respondent Python-version usage.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/hybrid/agent/d7-u01.json)


### hybrid / d7-u02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong nghiên cứu NSFG được mô tả, mã API cá nhân của từng người tham gia là gì?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** The book reports survey methodology, not participants personal API credentials.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/hybrid/agent/d7-u02.json)


### dense_context / d7-q01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao việc chỉ lấy ý kiến người tham gia thảo luận về con đầu sinh muộn có thể gây selection bias?

**Kết quả:** Việc chỉ lấy ý kiến hoặc dựa vào những người tham gia thảo luận về con đầu sinh muộn có thể gây ra hiện tượng thiên vị lựa chọn (selection bias) vì những người tham gia vào một cuộc thảo luận như vậy có thể bị thu hút hoặc quan tâm đến chủ đề này chính vì con đầu của họ sinh muộn [54f0c801e3aa64b436f8c68f]. Do đó, quá trình chọn lọc dữ liệu này sẽ làm lệch kết quả của toàn bộ khảo sát/thảo luận [54f0c801e3aa64b436f8c68f].

**Chuẩn:** Người tham gia có thể quan tâm vì con đầu của họ sinh muộn; cách chọn dữ liệu làm lệch kết quả.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** Đối chiếu PDF 22: người tham gia có con đầu sinh muộn tự chọn vào thảo luận, làm lệch mẫu/kết quả.

[Trace đầy đủ](dev/dense_context/agent/d7-q01.json)

- Citation `54f0c801e3aa64b436f8c68f`: PDF page 22, printed page 2; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nghiên cứu cross-sectional khác longitudinal về thời điểm quan sát như thế nào?

**Kết quả:** Nghiên cứu cross-sectional (cắt ngang) và nghiên cứu longitudinal (dọc) khác nhau về thời điểm và cách thức quan sát nhóm đối tượng như sau:

* **Nghiên cứu cross-sectional (Nghiên cứu cắt ngang):** Thu thập dữ liệu để ghi lại bức ảnh chụp (snapshot) của một nhóm đối tượng tại một thời điểm cụ thể [c820376c2fde59d33d4d8bc8].
* **Nghiên cứu longitudinal (Nghiên cứu dọc):** Quan sát một nhóm đối tượng lặp đi lặp lại trong một khoảng thời gian bằng cách thu thập dữ liệu từ cùng một nhóm đó theo thời gian [c820376c2fde59d33d4d8bc8] [a6a5f497332f50f7f5a86fb6].

**Chuẩn:** Cross-sectional chụp một nhóm tại một thời điểm; longitudinal quan sát lặp lại qua thời gian.

**Nhãn:** answer=2, context=2, citation=[True, True], abstention=None

**Lý do:** PDF 23 hoặc glossary PDF 35 nêu snapshot một thời điểm và theo dõi lặp cùng nhóm theo thời gian. Glossary là evidence tương đương dù strict gold chỉ ở PDF 23.

[Trace đầy đủ](dev/dense_context/agent/d7-q02.json)

- Citation `c820376c2fde59d33d4d8bc8`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `a6a5f497332f50f7f5a86fb6`: PDF page 35, printed page 15; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Quần thể mục tiêu của khảo sát NSFG trong sách gồm những ai?

**Kết quả:** Quần thể mục tiêu của khảo sát NSFG (National Survey of Family Growth) trong sách là những người ở Hoa Kỳ trong độ tuổi từ 15 đến 44 [f40266243aa427f23fa90b4e].

**Chuẩn:** Người ở Hoa Kỳ từ 15 đến 44 tuổi.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 ghi rõ quần thể Hoa Kỳ 15–44 tuổi, đúng cả địa lý và khoảng tuổi.

[Trace đầy đủ](dev/dense_context/agent/d7-q03.json)

- Citation `f40266243aa427f23fa90b4e`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 1, NSFG lấy mẫu vượt tỷ lệ ở ba nhóm nào và nhằm mục đích gì?

**Kết quả:** Trong chương 1, các nhà thiết kế của cuộc khảo sát NSFG đã lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e]. 

Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn, nhằm có thể đưa ra các suy luận thống kê hợp lệ [8bca2eddf8d8ed85185da77e].

**Chuẩn:** Hispanics, African-Americans và teenagers; để đủ số người trả lời cho suy luận thống kê hợp lệ trong từng nhóm.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 24 nêu đủ Hispanics, African-Americans, teenagers và mục đích có đủ respondents cho statistical inference.

[Trace đầy đủ](dev/dense_context/agent/d7-q04.json)

- Citation `8bca2eddf8d8ed85185da77e`: PDF page 24, printed page 4; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Stata dictionary mô tả những thuộc tính nào để tìm biến trong mỗi dòng dữ liệu?

**Kết quả:** Trong ngữ cảnh của Stata dictionary, một dictionary là danh sách gồm tên biến (variable names), kiểu dữ liệu (types), và các chỉ số (indices) để xác định vị trí tìm thấy mỗi biến trong mỗi dòng dữ liệu [5869e54397098a669dd0b81e]. Ví dụ như vị trí cột (`_column`), kiểu dữ liệu và độ rộng của biến, tên biến, và mô tả [5869e54397098a669dd0b81e].

**Chuẩn:** Tên biến, kiểu và chỉ số/vị trí của biến trên mỗi dòng.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 25 mô tả variable names/types/indices cùng ví dụ _column. Answer giữ đủ ba thuộc tính.

[Trace đầy đủ](dev/dense_context/agent/d7-q05.json)

- Citation `5869e54397098a669dd0b81e`: PDF page 25, printed page 5; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q06

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** DataFrame NSFG được minh họa có bao nhiêu bản ghi và biến?

**Kết quả:** DataFrame NSFG được minh họa có tổng cộng 13.593 bản ghi (rows/records) và 244 biến (columns/variables). [ee672fe7059e3b9d2b8e2207]

**Chuẩn:** 13.593 bản ghi và 244 biến.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 26–27: shape có 13593 rows và 244 columns; đoạn Variables cũng xác nhận 244 biến. Đọc cả hai citation nếu được gộp.

[Trace đầy đủ](dev/dense_context/agent/d7-q06.json)

- Citation `ee672fe7059e3b9d2b8e2207`: PDF page 26, printed page 6; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q07

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Mã outcome nào thể hiện một ca sinh sống?

**Kết quả:** Mã outcome thể hiện một ca sinh sống (live birth) là 1 [4f0610284ca731ebc56f0974] [f5d4f52297470390e5b98ec6].

**Chuẩn:** Mã 1.

**Nhãn:** answer=2, context=2, citation=[True, True], abstention=None

**Lý do:** PDF 28 hoặc bảng kiểm chứng PDF 30: outcome=1 là live birth. Không lẫn với pregordr/birthord.

[Trace đầy đủ](dev/dense_context/agent/d7-q07.json)

- Citation `4f0610284ca731ebc56f0974`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `f5d4f52297470390e5b98ec6`: PDF page 28, printed page 8; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q08

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tại sao CleanFemPreg chia agepreg cho 100?

**Kết quả:** Trong `CleanFemPreg`, biến `agepreg` được chia cho 100 vì trong tệp dữ liệu, tuổi của người mẹ (`agepreg`) được mã hóa dưới dạng số nguyên tính theo phần trăm của năm (centiyears) [50718039f1ba18056fe56194]. Việc chia cho 100 giúp chuyển đổi các giá trị này thành một giá trị dấu phẩy động (floating-point value) tính bằng năm [50718039f1ba18056fe56194].

**Chuẩn:** Dữ liệu lưu tuổi bằng số nguyên centiyears; chia 100 để đổi sang số năm dạng số thực.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 29 giải thích agepreg là integer centiyears; chia 100 đổi sang floating-point years, không chỉ nhắc phép chia.

[Trace đầy đủ](dev/dense_context/agent/d7-q08.json)

- Citation `50718039f1ba18056fe56194`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q09

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nếu cân nặng chứa mã 97, 98 hoặc 99 thì phải xử lý thế nào để tránh kết quả sai?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Đó là mã thiếu thông tin, từ chối hoặc không biết; thay bằng np.nan trước khi tính toán.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 29 nêu 97/98/99 là mã thiếu/refused/unknown; replace thành np.nan tránh số liệu giả. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense_context/agent/d7-q09.json)


### dense_context / d7-q10

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Khi thêm cột vào DataFrame, vì sao không nên gán bằng dot notation?

**Kết quả:** Khi thêm một cột mới vào DataFrame, bạn không nên dùng ký hiệu chấm (dot notation) vì nó chỉ thêm một thuộc tính (attribute) vào đối tượng DataFrame chứ không xem thuộc tính đó là một cột mới [798698989f39c80a59059a9a]. Thay vào đó, bạn phải sử dụng cú pháp từ điển (dictionary syntax, ví dụ: `df['ten_cot']`) [798698989f39c80a59059a9a].

**Chuẩn:** Phải dùng dictionary syntax; dot notation chỉ thêm thuộc tính và không được coi là cột mới.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 30: dot notation thêm attribute, không thêm column; phải dùng dictionary syntax.

[Trace đầy đủ](dev/dense_context/agent/d7-q10.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q11

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Một cách kiểm chứng dữ liệu sau khi chuyển giữa hai môi trường phần mềm là gì?

**Kết quả:** Một cách để kiểm chứng dữ liệu (validation) sau khi chuyển từ môi trường phần mềm này sang môi trường phần mềm khác là tính toán các thống kê cơ bản và so sánh chúng với các kết quả đã được công bố (ví dụ: so sánh các bảng tóm tắt hoặc số liệu thống kê trong tài liệu hướng dẫn/codebook của tập dữ liệu) [4f0610284ca731ebc56f0974].

**Chuẩn:** Tính thống kê cơ bản rồi đối chiếu kết quả đã công bố, ví dụ bảng tổng hợp trong codebook.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 30–31 hoặc đoạn codebook PDF 33: so sánh thống kê/value counts với published table là một cách validation cụ thể.

[Trace đầy đủ](dev/dense_context/agent/d7-q11.json)

- Citation `4f0610284ca731ebc56f0974`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q12

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** CleanFemPreg xử lý birthwgt_lb vượt 20 như thế nào?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Thay các giá trị vượt 20 bằng np.nan.

**Nhãn:** answer=0, context=1, citation=[], abstention=None

**Lý do:** PDF 42 nêu thay birthwgt_lb >20 thành np.nan. Thay mã 97/98/99 không trả lời điều kiện >20. Kết quả hiện tại từ chối dù câu có đáp án; answer=0. Context 1/2 theo nội dung thực sự còn trong budget.

[Trace đầy đủ](dev/dense_context/agent/d7-q12.json)


### dense_context / d7-q13

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 2, histogram thể hiện điều gì và frequency nghĩa là gì?

**Kết quả:** Trong Chương 2 của sách Think Stats, biểu đồ histogram là một đồ thị thể hiện tần suất (frequency) của từng giá trị trong tập dữ liệu [8849532a0610912f69f6978d]. 

Trong bối cảnh này, "frequency" (tần suất/tần số) có nghĩa là số lần mà một giá trị xuất hiện trong tập dữ liệu [8849532a0610912f69f6978d].

**Chuẩn:** Histogram cho biết tần số từng giá trị; frequency là số lần giá trị xuất hiện.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 37 hoặc glossary PDF 50 và API Hist PDF 38: histogram ánh xạ value→frequency, frequency là số lần xuất hiện.

[Trace đầy đủ](dev/dense_context/agent/d7-q13.json)

- Citation `8849532a0610912f69f6978d`: PDF page 37, printed page 17; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q14

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả phân biệt mean và average như thế nào?

**Kết quả:** Tác giả phân biệt hai thuật ngữ này như sau [7b3b142d5d2b25996d5b4bbb]:
- **Mean (Số trung bình):** Là một thống kê tóm tắt (summary statistic) cụ thể được tính bằng tổng các giá trị chia cho số lượng giá trị (theo công thức tính $\bar{x}$) [7b3b142d5d2b25996d5b4bbb].
- **Average (Giá trị trung bình):** Là một thuật ngữ tổng quát hơn, chỉ một trong số các thống kê tóm tắt khác nhau mà bạn có thể lựa chọn để mô tả xu hướng trung tâm (central tendency) của tập dữ liệu [7b3b142d5d2b25996d5b4bbb].

**Chuẩn:** Mean là thống kê tính theo công thức tổng chia số lượng; average có thể là một trong nhiều thống kê mô tả xu hướng trung tâm.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 45 phân biệt mean theo công thức và average là lựa chọn summary statistic của central tendency; ví dụ pumpkin PDF 46 chỉ minh họa một phần.

[Trace đầy đủ](dev/dense_context/agent/d7-q14.json)

- Citation `7b3b142d5d2b25996d5b4bbb`: PDF page 45, printed page 25; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-q15

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Độ lệch chuẩn có quan hệ gì với phương sai?

**Kết quả:** Độ lệch chuẩn là căn bậc hai của phương sai [d3270a2b867639b7ed5e52b2]. Cả hai đều là các thống kê tóm tắt dùng để mô tả độ phân tán hoặc sự biến động của một phân phối [d3270a2b867639b7ed5e52b2].

**Chuẩn:** Độ lệch chuẩn là căn bậc hai của phương sai, cũng đo độ phân tán.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 46/50 nêu standard deviation là square root of variance; đúng quan hệ được hỏi.

[Trace đầy đủ](dev/dense_context/agent/d7-q15.json)

- Citation `d3270a2b867639b7ed5e52b2`: PDF page 46, printed page 26; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### dense_context / d7-u01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong bộ tài liệu, tỷ lệ người trả lời NSFG sử dụng Python 3.12 là bao nhiêu phần trăm?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Corpus describes NSFG and Python but does not report respondent Python-version usage.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/dense_context/agent/d7-u01.json)


### dense_context / d7-u02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong nghiên cứu NSFG được mô tả, mã API cá nhân của từng người tham gia là gì?

**Kết quả:** Trong nghiên cứu NSFG được mô tả, mã định danh (ID) số nguyên của mỗi người tham gia là `caseid` [2302c0aa2fd4d36ec776cd0e].

**Chuẩn:** The book reports survey methodology, not participants personal API credentials.

**Nhãn:** answer=None, context=None, citation=[True], abstention=False

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent đổi câu hỏi mã API thành caseid. Citation hỗ trợ câu factual về respondent ID nhưng không trả lời câu hỏi gốc; abstention không đạt.

[Trace đầy đủ](dev/dense_context/agent/d7-u02.json)

- Citation `2302c0aa2fd4d36ec776cd0e`: PDF page 27, printed page 7; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Vì sao việc chỉ lấy ý kiến người tham gia thảo luận về con đầu sinh muộn có thể gây selection bias?

**Kết quả:** Việc chỉ lấy ý kiến của những người tham gia thảo luận về con đầu sinh muộn có thể gây ra hiện tượng thiên vị chọn mẫu (selection bias), bởi vì những người tham gia vào cuộc thảo luận đó có thể bị thu hút hoặc quan tâm đến vấn đề này chính vì con đầu lòng của họ sinh muộn [54f0c801e3aa64b436f8c68f]. Khi quá trình chọn lọc dữ liệu diễn ra theo cách này, nó sẽ làm lệch kết quả phân tích [54f0c801e3aa64b436f8c68f].

**Chuẩn:** Người tham gia có thể quan tâm vì con đầu của họ sinh muộn; cách chọn dữ liệu làm lệch kết quả.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** Đối chiếu PDF 22: người tham gia có con đầu sinh muộn tự chọn vào thảo luận, làm lệch mẫu/kết quả.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q01.json)

- Citation `54f0c801e3aa64b436f8c68f`: PDF page 22, printed page 2; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nghiên cứu cross-sectional khác longitudinal về thời điểm quan sát như thế nào?

**Kết quả:** Nghiên cứu cross-sectional (cắt ngang) và nghiên cứu longitudinal (dọc) khác nhau về thời điểm và cách thức quan sát dân số như sau:

* **Nghiên cứu cross-sectional (cắt ngang):** Thu thập dữ liệu về một quần thể tại một thời điểm cụ thể, giống như việc chụp lại một bức ảnh (snapshot) của nhóm đối tượng tại thời điểm đó [c820376c2fde59d33d4d8bc8].
* **Nghiên cứu longitudinal (dọc):** Theo dõi một quần thể theo thời gian và thu thập dữ liệu từ cùng một nhóm đối tượng đó một cách lặp đi lặp lại [a6a5f497332f50f7f5a86fb6] [c820376c2fde59d33d4d8bc8].

**Chuẩn:** Cross-sectional chụp một nhóm tại một thời điểm; longitudinal quan sát lặp lại qua thời gian.

**Nhãn:** answer=2, context=2, citation=[True, True], abstention=None

**Lý do:** PDF 23 hoặc glossary PDF 35 nêu snapshot một thời điểm và theo dõi lặp cùng nhóm theo thời gian. Glossary là evidence tương đương dù strict gold chỉ ở PDF 23.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q02.json)

- Citation `a6a5f497332f50f7f5a86fb6`: PDF page 35, printed page 15; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `c820376c2fde59d33d4d8bc8`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q03

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Quần thể mục tiêu của khảo sát NSFG trong sách gồm những ai?

**Kết quả:** Quần thể mục tiêu của khảo sát NSFG trong sách là những người ở Hoa Kỳ trong độ tuổi từ 15 đến 44 [f40266243aa427f23fa90b4e].

**Chuẩn:** Người ở Hoa Kỳ từ 15 đến 44 tuổi.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 23 ghi rõ quần thể Hoa Kỳ 15–44 tuổi, đúng cả địa lý và khoảng tuổi.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q03.json)

- Citation `f40266243aa427f23fa90b4e`: PDF page 23, printed page 3; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q04

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 1, NSFG lấy mẫu vượt tỷ lệ ở ba nhóm nào và nhằm mục đích gì?

**Kết quả:** Trong Chương 1, các nhà thiết kế của cuộc khảo sát NSFG đã lấy mẫu vượt tỷ lệ (oversampled) ở ba nhóm: người gốc Tây Ban Nha (Hispanics), người Mỹ gốc Phi (African-Americans) và thanh thiếu niên (teenagers) [8bca2eddf8d8ed85185da77e]. 

Mục đích của việc này là để đảm bảo rằng số lượng người trả lời (respondents) trong mỗi nhóm này đủ lớn, nhằm rút ra các suy luận thống kê hợp lệ (valid statistical inferences) [8bca2eddf8d8ed85185da77e].

**Chuẩn:** Hispanics, African-Americans và teenagers; để đủ số người trả lời cho suy luận thống kê hợp lệ trong từng nhóm.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 24 nêu đủ Hispanics, African-Americans, teenagers và mục đích có đủ respondents cho statistical inference.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q04.json)

- Citation `8bca2eddf8d8ed85185da77e`: PDF page 24, printed page 4; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q05

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Stata dictionary mô tả những thuộc tính nào để tìm biến trong mỗi dòng dữ liệu?

**Kết quả:** Trong bối cảnh này, một "dictionary" (từ điển) Stata là một danh sách gồm các **tên biến (variable names)**, **kiểu dữ liệu (types)** và **các chỉ số/vị trí (indices)** dùng để xác định vị trí tìm thấy từng biến ở mỗi dòng dữ liệu [5869e54397098a669dd0b81e].

**Chuẩn:** Tên biến, kiểu và chỉ số/vị trí của biến trên mỗi dòng.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 25 mô tả variable names/types/indices cùng ví dụ _column. Answer giữ đủ ba thuộc tính.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q05.json)

- Citation `5869e54397098a669dd0b81e`: PDF page 25, printed page 5; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q06

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** DataFrame NSFG được minh họa có bao nhiêu bản ghi và biến?

**Kết quả:** DataFrame NSFG được minh họa có 13.593 bản ghi (rows/records) và 244 biến (columns/variables) [ee672fe7059e3b9d2b8e2207].

**Chuẩn:** 13.593 bản ghi và 244 biến.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 26–27: shape có 13593 rows và 244 columns; đoạn Variables cũng xác nhận 244 biến. Đọc cả hai citation nếu được gộp.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q06.json)

- Citation `ee672fe7059e3b9d2b8e2207`: PDF page 26, printed page 6; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q07

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Mã outcome nào thể hiện một ca sinh sống?

**Kết quả:** Mã outcome là **1** thể hiện một ca sinh sống (live birth) [f5d4f52297470390e5b98ec6].

**Chuẩn:** Mã 1.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 28 hoặc bảng kiểm chứng PDF 30: outcome=1 là live birth. Không lẫn với pregordr/birthord.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q07.json)

- Citation `f5d4f52297470390e5b98ec6`: PDF page 28, printed page 8; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q08

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tại sao CleanFemPreg chia agepreg cho 100?

**Kết quả:** Hàm `CleanFemPreg` chia `agepreg` cho 100 vì trong tệp dữ liệu gốc, `agepreg` (tuổi của người mẹ tại thời điểm kết thúc thai kỳ) được mã hóa dưới dạng số nguyên tính bằng đơn vị phần trăm năm (centiyears). Việc chia cho 100 giúp chuyển đổi các giá trị này thành giá trị dấu phẩy động tính bằng năm [50718039f1ba18056fe56194].

**Chuẩn:** Dữ liệu lưu tuổi bằng số nguyên centiyears; chia 100 để đổi sang số năm dạng số thực.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 29 giải thích agepreg là integer centiyears; chia 100 đổi sang floating-point years, không chỉ nhắc phép chia.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q08.json)

- Citation `50718039f1ba18056fe56194`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q09

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Nếu cân nặng chứa mã 97, 98 hoặc 99 thì phải xử lý thế nào để tránh kết quả sai?

**Kết quả:** Các giá trị đặc biệt được mã hóa bằng số (như 97 cho "NOT ASCERTAINED", 98 cho "REFUSED", và 99 cho "DON'T KNOW") có thể gây ra kết quả sai lệch (như tính ra một em bé nặng 99 pound) nếu không được xử lý đúng cách [50718039f1ba18056fe56194]. 

Để tránh tình trạng này, các giá trị này cần được thay thế bằng `np.nan` (một giá trị số thực đặc biệt biểu thị "không phải là số" - not a number) [50718039f1ba18056fe56194]. Trong Python và pandas, việc này thường được thực hiện bằng phương thức `.replace()`, ví dụ [378c9ef8a37471ebdc49dd13]:

```python
na_vals = [97, 98, 99]
df['birthwgt_lb'] = df.birthwgt_lb.replace(na_vals, np.nan)
df['birthwgt_oz'] = df.birthwgt_oz.replace(na_vals, np.nan)
```

Khi sử dụng `np.nan`, các phép toán sẽ trả về `nan` nếu một trong các đối số là `nan` và hầu hết các hàm của pandas đều xử lý các giá trị `nan` này một cách phù hợp [50718039f1ba18056fe56194] [49643149477ca2ae881fb71f].

**Chuẩn:** Đó là mã thiếu thông tin, từ chối hoặc không biết; thay bằng np.nan trước khi tính toán.

**Nhãn:** answer=2, context=2, citation=[True, True, True], abstention=None

**Lý do:** PDF 29 nêu 97/98/99 là mã thiếu/refused/unknown; replace thành np.nan tránh số liệu giả.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q09.json)

- Citation `50718039f1ba18056fe56194`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `378c9ef8a37471ebdc49dd13`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `49643149477ca2ae881fb71f`: PDF page 29, printed page 9; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q10

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Khi thêm cột vào DataFrame, vì sao không nên gán bằng dot notation?

**Kết quả:** Khi thêm một cột mới vào DataFrame, bạn không nên sử dụng cú pháp dấu chấm (dot notation) vì nó chỉ thêm một thuộc tính (attribute) vào đối tượng DataFrame chứ không xem thuộc tính đó là một cột mới [798698989f39c80a59059a9a]. Thay vào đó, bạn phải sử dụng cú pháp từ điển (dictionary syntax, ví dụ: `df['totalwgt_lb'] = ...`) [798698989f39c80a59059a9a].

**Chuẩn:** Phải dùng dictionary syntax; dot notation chỉ thêm thuộc tính và không được coi là cột mới.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 30: dot notation thêm attribute, không thêm column; phải dùng dictionary syntax.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q10.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q11

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Một cách kiểm chứng dữ liệu sau khi chuyển giữa hai môi trường phần mềm là gì?

**Kết quả:** Theo sách Think Stats, khi dữ liệu được xuất từ một môi trường phần mềm này và nhập vào môi trường phần mềm khác, lỗi có thể phát sinh [798698989f39c80a59059a9a]. Một cách để kiểm chứng (validate) dữ liệu sau khi chuyển đổi là so sánh các kết quả tính toán (chẳng hạn như đếm giá trị - value counts) với bảng kết quả đã được công bố (published table) để đảm bảo các giá trị là chính xác [4fcfe0efa8b50ff228b30f81].

**Chuẩn:** Tính thống kê cơ bản rồi đối chiếu kết quả đã công bố, ví dụ bảng tổng hợp trong codebook.

**Nhãn:** answer=2, context=2, citation=[True, True], abstention=None

**Lý do:** PDF 30–31 hoặc đoạn codebook PDF 33: so sánh thống kê/value counts với published table là một cách validation cụ thể.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q11.json)

- Citation `798698989f39c80a59059a9a`: PDF page 30, printed page 10; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `4fcfe0efa8b50ff228b30f81`: PDF page 31, printed page 11; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q12

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** CleanFemPreg xử lý birthwgt_lb vượt 20 như thế nào?

**Kết quả:** Trong hàm `CleanFemPreg`, các giá trị `birthwgt_lb` vượt quá 20 (như trường hợp 51 pound) được xử lý bằng cách thay thế chúng thành `np.nan` (giá trị đại diện cho "không phải số") thông qua dòng lệnh:
`df.loc[df.birthwgt_lb > 20, 'birthwgt_lb'] = np.nan` [9766333af7f057a687bda0c0]

**Chuẩn:** Thay các giá trị vượt 20 bằng np.nan.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 42 nêu thay birthwgt_lb >20 thành np.nan. Thay mã 97/98/99 không trả lời điều kiện >20.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q12.json)

- Citation `9766333af7f057a687bda0c0`: PDF page 32, printed page 12; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q13

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong chương 2, histogram thể hiện điều gì và frequency nghĩa là gì?

**Kết quả:** Trong Chương 2 của sách Think Stats, **histogram** được định nghĩa là một ánh xạ từ các giá trị sang tần suất của chúng (a mapping from values to frequencies), hoặc là một biểu đồ thể hiện ánh xạ đó [26ae64c96e1b06d8f4423144]. 

Trong ngữ cảnh này, **frequency** (tần suất/tần số) thể hiện số lần một giá trị xuất hiện (ví dụ: trong cấu trúc `Hist`, phương thức `Freq` nhận một giá trị và trả về số lần xuất hiện của giá trị đó) [75d221237f5bb07a3d603472].

**Chuẩn:** Histogram cho biết tần số từng giá trị; frequency là số lần giá trị xuất hiện.

**Nhãn:** answer=2, context=2, citation=[True, True], abstention=None

**Lý do:** PDF 37 hoặc glossary PDF 50 và API Hist PDF 38: histogram ánh xạ value→frequency, frequency là số lần xuất hiện.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q13.json)

- Citation `75d221237f5bb07a3d603472`: PDF page 38, printed page 18; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
- Citation `26ae64c96e1b06d8f4423144`: PDF page 49, printed page 29; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q14

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Tác giả phân biệt mean và average như thế nào?

**Kết quả:** Mặc dù các từ “mean” (số trung bình) và “average” (giá trị trung bình) đôi khi được sử dụng thay thế cho nhau, tác giả đã đưa ra sự phân biệt rõ ràng:

* **“Mean” của một mẫu** là một thống kê tóm tắt (summary statistic) được tính toán theo công thức cụ thể (tổng các giá trị chia cho số lượng giá trị) [7b3b142d5d2b25996d5b4bbb].
* **“Average”** là một trong số các thống kê tóm tắt mà bạn có thể chọn để mô tả xu hướng trung tâm (central tendency) [7b3b142d5d2b25996d5b4bbb].

**Chuẩn:** Mean là thống kê tính theo công thức tổng chia số lượng; average có thể là một trong nhiều thống kê mô tả xu hướng trung tâm.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 45 phân biệt mean theo công thức và average là lựa chọn summary statistic của central tendency; ví dụ pumpkin PDF 46 chỉ minh họa một phần.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q14.json)

- Citation `7b3b142d5d2b25996d5b4bbb`: PDF page 45, printed page 25; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-q15

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Độ lệch chuẩn có quan hệ gì với phương sai?

**Kết quả:** Độ lệch chuẩn là căn bậc hai của phương sai [d3270a2b867639b7ed5e52b2].

**Chuẩn:** Độ lệch chuẩn là căn bậc hai của phương sai, cũng đo độ phân tán.

**Nhãn:** answer=2, context=2, citation=[True], abstention=None

**Lý do:** PDF 46/50 nêu standard deviation là square root of variance; đúng quan hệ được hỏi.

[Trace đầy đủ](dev/hybrid_context/agent/d7-q15.json)

- Citation `d3270a2b867639b7ed5e52b2`: PDF page 46, printed page 26; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)

### hybrid_context / d7-u01

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong bộ tài liệu, tỷ lệ người trả lời NSFG sử dụng Python 3.12 là bao nhiêu phần trăm?

**Kết quả:** Không đủ bằng chứng trong tài liệu để trả lời.

**Chuẩn:** Corpus describes NSFG and Python but does not report respondent Python-version usage.

**Nhãn:** answer=None, context=None, citation=[], abstention=True

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent từ chối rõ ràng, không thêm suy đoán.

[Trace đầy đủ](dev/hybrid_context/agent/d7-u01.json)


### hybrid_context / d7-u02

- [ ] Học viên đã đối chiếu nguồn

**Câu hỏi:** Trong nghiên cứu NSFG được mô tả, mã API cá nhân của từng người tham gia là gì?

**Kết quả:** Trong nghiên cứu NSFG được mô tả, mã định danh (ID) số nguyên của từng người tham gia là `caseid` [2302c0aa2fd4d36ec776cd0e].

**Chuẩn:** The book reports survey methodology, not participants personal API credentials.

**Nhãn:** answer=None, context=None, citation=[True], abstention=False

**Lý do:** Đã đối chiếu phạm vi 42 trang và absence_reason. Agent đổi câu hỏi mã API thành caseid. Citation hỗ trợ câu factual về respondent ID nhưng không trả lời câu hỏi gốc; abstention không đạt.

[Trace đầy đủ](dev/hybrid_context/agent/d7-u02.json)

- Citation `2302c0aa2fd4d36ec776cd0e`: PDF page 27, printed page 7; [nguồn](https://greenteapress.com/thinkstats2/thinkstats2.pdf)
