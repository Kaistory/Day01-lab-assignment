# Ngày 1 — Nền Tảng LLM API 

## Mục Tiêu

Học cách gọi OpenAI API, hiểu các tham số sinh text quan trọng, so sánh GPT-4o và GPT-4o-mini, xây dựng chatbot streaming có lịch sử hội thoại.

---

## Cài Đặt

### Yêu Cầu
- Python 3.10+
- OpenAI API key (chỉ để chạy thủ công — kiểm thử dùng mock)

### 1. Tạo & kích hoạt virtual environment (venv)

**Windows (Command Prompt / cmd):**
```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
> Nếu PowerShell báo lỗi chính sách thực thi, chạy một lần:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Khi kích hoạt thành công, dấu nhắc terminal sẽ có tiền tố `(.venv)`.

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Thiết lập API key bằng file `.env`
Tạo file `.env` ở thư mục gốc của project (đã được `.gitignore` bỏ qua — **không bao giờ commit**):
```
OPENAI_API_KEY=sk-...
```
Có thể copy từ mẫu: `cp .env.example .env` rồi điền key. `template.py` tự nạp `.env` khi chạy.

### 4. Chạy
```bash
pytest tests/ -v     # chạy kiểm thử (dùng mock, không cần key)
python template.py   # chạy thật (cần key trong .env)
```

### Thoát venv
```bash
deactivate
```

---

## Nhiệm Vụ

### Nhiệm vụ 1: Triển khai `call_openai`
Gọi OpenAI Chat Completions API với model GPT-4o và trả về nội dung phản hồi cùng với độ trễ đo được.

**Tham số:**
- `prompt` (str): Tin nhắn của người dùng
- `model` (str): Model OpenAI sử dụng (mặc định: gpt-4o)
- `temperature` (float): Kiểm soát mức độ ngẫu nhiên (0.0–2.0)
- `max_tokens` (int): Số token tối đa được sinh ra

**Trả về:** `tuple[str, float]` — (response_text, latency_seconds)

---

### Nhiệm vụ 2: Triển khai `call_openai_mini`
Gọi OpenAI API với model GPT-4o-mini — nhanh hơn và rẻ hơn. Gợi ý: tái sử dụng `call_openai` với `model=OPENAI_MINI_MODEL`.

**Trả về:** `tuple[str, float]` — (response_text, latency_seconds)

---

### Nhiệm vụ 3: Triển khai `compare_models`
Gọi cả GPT-4o và GPT-4o-mini với cùng một prompt và trả về từ điển so sánh bao gồm phản hồi, độ trễ và chi phí ước tính.

**Ước tính chi phí output:**
- GPT-4o: $0.010 mỗi 1K token đầu ra
- GPT-4o-mini: $0.0006 mỗi 1K token đầu ra

**Trả về dict với các key:**
- `gpt4o_response`, `mini_response`
- `gpt4o_latency`, `mini_latency`
- `gpt4o_cost_estimate`

---

### Nhiệm vụ 4: Triển khai `streaming_chatbot`
Xây dựng chatbot dòng lệnh tương tác dùng streaming để hiển thị token khi chúng được sinh ra. Duy trì lịch sử hội thoại 3 lượt gần nhất.

---

## Hướng Dẫn Nộp Bài

```bash
# 1. Copy template.py vào folder solution và đổi tên
cp template.py solution/solution.py

# 2. Copy exercises.md vào folder solution
cp exercises.md solution/exercises.md

# 3. Zip folder solution
zip -r solution.zip solution/

# 4. Đổi tên file solution.zip thành thành <mã sinh viên>_lab_1.zip và upload lên hệ thống LMS 
```

**Cấu trúc folder solution trước khi zip:**
```
solution/
├── solution.py      # template.py đã hoàn thiện
└── exercises.md     # bài tập và phản ánh đã điền
```

---

## Chạy Kiểm Thử

```bash
pytest tests/ -v
```

Tất cả kiểm thử dùng `unittest.mock` — **không cần API key thật**.

---

## Chấm Điểm

| Tiêu Chí | Điểm |
|----------|------|
| Tất cả pytest tests pass | 50 |
| `compare_models` trả về cấu trúc dict đúng | 10 |
| `streaming_chatbot` duy trì lịch sử hội thoại | 10 |
| Exercise 2.1 — Phân tích temperature | 10 |
| Exercise 2.2 — Phân tích chi phí | 10 |
| Exercise 2.3 — Streaming UX | 10 |
| **Tổng** | **100** |

---

## Hướng Dẫn Thời Gian Lab

| Thời Gian | Hoạt Động |
|-----------|-----------|
| 0:00–1:00 | Lập trình cốt lõi: Triển khai tất cả TODO trong `template.py` |
| 1:00–1:30 | Mở rộng: Hoàn thành Phần 2 của `exercises.md` |



## Danh Sách Kiểm Tra Nộp Bài

- [ ] `pytest tests/ -v` — tất cả kiểm thử pass
- [ ] `solution/exercises.md` — tất cả câu trả lời đã điền
- [ ] `solution/solution.py` — triển khai cuối cùng của bạn

end