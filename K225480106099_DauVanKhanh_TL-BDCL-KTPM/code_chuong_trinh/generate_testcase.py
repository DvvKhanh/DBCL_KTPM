# Đọc tài liệu yêu cầu
with open(
    "requirement.txt",
    "r",
    encoding="utf-8"
) as f:
    requirement = f.read()

# ==========================
# PROMPT GỬI CHO LLM
# ==========================
prompt = f"""
Bạn là một Senior QA Engineer có kinh nghiệm trong kiểm thử phần mềm.

Nhiệm vụ:

Phân tích tài liệu yêu cầu sau:

{requirement}

Hãy áp dụng các kỹ thuật:

1. Equivalence Partitioning
2. Boundary Value Analysis
3. Error Guessing

Sinh danh sách Test Case theo định dạng:

- Test Case ID
- Mục tiêu kiểm thử
- Dữ liệu đầu vào
- Kết quả mong đợi

Đảm bảo bao phủ toàn bộ yêu cầu.
"""

print("=" * 60)
print("PROMPT GỬI CHO LLM")
print("=" * 60)
print(prompt)


# ==================================
# MÔ PHỎNG KẾT QUẢ LLM SINH RA
# ==================================

llm_output = """
TC001 | Truy cập trang chủ | GET / | HTTP 200

TC002 | Email để trống |
email='' password='Password123!'
| HTTP 400

TC003 | Password để trống |
email='K225480106099@tnut.edu.vn'
password=''
| HTTP 400

TC004 | Email sai định dạng |
abcgmail.com
| HTTP 400

TC005 | Email vượt quá 100 ký tự |
101 ký tự
| HTTP 400

TC006 | Email không tồn tại |
abc@gmail.com
| HTTP 401

TC007 | Sai mật khẩu |
abc123
| HTTP 401

TC008 | Đăng nhập thành công |
Email + Password đúng
| HTTP 200

TC009 | Sai liên tiếp 5 lần |
Wrong Password
| HTTP 403

TC010 | Đăng nhập khi tài khoản bị khóa |
Locked Account
| HTTP 403
"""


# Ghi ra file testcases.txt

with open(
    "testcases.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(llm_output)


print("\n")
print("=" * 60)
print("TEST CASE ĐƯỢC SINH RA")
print("=" * 60)

print(llm_output)

print("\nĐã lưu vào file testcases.txt")