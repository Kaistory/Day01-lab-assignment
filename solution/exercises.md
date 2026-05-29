# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Ở temperature 0.0 các phản hồi gần như giống hệt nhau qua nhiều lần chạy, thường lặp lại cùng một sự thật phổ biến và diễn đạt rất khuôn mẫu. Khi temperature tăng lên 0.5 rồi 1.0, câu trả lời đa dạng và sáng tạo hơn về cả nội dung lẫn cách hành văn nhưng vẫn chính xác. Đến 1.5 thì văn phong rất ngẫu nhiên, đôi khi lạc đề, lặp từ hoặc xuất hiện thông tin thiếu tin cậy. Nói cách khác, temperature càng cao thì độ ngẫu nhiên/đa dạng càng lớn nhưng độ ổn định và độ tin cậy càng giảm.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt temperature thấp, khoảng 0.0–0.3. Chatbot hỗ trợ khách hàng cần câu trả lời nhất quán, chính xác và có thể dự đoán được — cùng một câu hỏi nên cho ra cùng một hướng dẫn, đồng thời giảm rủi ro "bịa" thông tin (hallucination). Sự sáng tạo không quan trọng bằng tính đúng đắn và ổn định trong tình huống này.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng lượng token mỗi ngày = 10.000 × 3 × 350 = 10.500.000 token (10.500 nghìn token).
> Dùng đơn giá output trong đề bài (GPT-4o: $0,010 / 1K; GPT-4o-mini: $0,0006 / 1K):
> - GPT-4o: 10.500 × $0,010 = **$105/ngày** (≈ $3.150/tháng)
> - GPT-4o-mini: 10.500 × $0,0006 = **$6,30/ngày** (≈ $189/tháng)
>
> Vậy GPT-4o đắt hơn GPT-4o-mini khoảng **16,7 lần** (= 0,010 / 0,0006). (Đây là ước tính theo token output; nếu tính cả token input thì con số tuyệt đối sẽ cao hơn nhưng tỉ lệ chênh lệch vẫn tương tự.)

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> **Nên dùng GPT-4o:** các tác vụ đòi hỏi suy luận phức tạp và độ chính xác cao, nơi một lỗi sai gây hậu quả lớn — ví dụ phân tích/giải thích hợp đồng pháp lý, hỗ trợ chẩn đoán y tế, hay viết và rà soát code khó. Ở đây chất lượng lời giải quan trọng hơn chi phí.
> **Nên dùng GPT-4o-mini:** các tác vụ khối lượng lớn nhưng đơn giản và nhạy cảm về chi phí — ví dụ phân loại email/ticket, tóm tắt ngắn, tự động phản hồi câu hỏi thường gặp (FAQ), gắn nhãn dữ liệu. Mini đủ tốt, nhanh hơn và rẻ hơn ~16 lần nên tiết kiệm đáng kể khi nhân với hàng triệu lượt gọi.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các giao diện hội thoại thời gian thực mà con người đang chờ đọc — như chatbot hoặc trợ lý viết nội dung — vì hiển thị từng token ngay khi sinh ra giúp giảm "độ trễ cảm nhận": người dùng thấy phản hồi bắt đầu gần như tức thì thay vì nhìn màn hình trống vài giây, nhờ đó trải nghiệm mượt và tự nhiên hơn, đặc biệt với câu trả lời dài. Ngược lại, non-streaming phù hợp hơn khi đầu ra được xử lý bằng máy chứ không phải đọc trực tiếp — ví dụ khi cần nhận về một JSON hoàn chỉnh để parse, gọi trong pipeline/batch ở backend, hay khi logic phía sau cần toàn bộ kết quả trước khi xử lý — vì lúc đó hiển thị từng phần không mang lại lợi ích mà còn làm code phức tạp hơn.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định
