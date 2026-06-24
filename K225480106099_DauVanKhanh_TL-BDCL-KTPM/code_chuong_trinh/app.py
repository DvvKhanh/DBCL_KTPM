from flask import Flask, request, jsonify, render_template
import re
import time

app = Flask(__name__)

# Tài khoản mẫu
EMAIL_DUNG = "K225480106099@tnut.edu.vn"
PASSWORD_DUNG = "123"

# Biến quản lý đăng nhập
so_lan_sai = 0
tai_khoan_bi_khoa = False
thoi_gian_mo_khoa = 0


def kiem_tra_email(email):
    if len(email) > 100:
        return False

    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)


@app.route("/")
def home():
    try:
        return render_template("index.html")
    except:
        return jsonify({
            "de_tai": "LLM trong phân tích yêu cầu và sinh ca kiểm thử",
            "sinh_vien": "Đậu Văn Khánh",
            "trang_thai": "Đang hoạt động"
        })


@app.route("/api/login", methods=["POST"])
def login():

    global so_lan_sai
    global tai_khoan_bi_khoa
    global thoi_gian_mo_khoa

    data = request.get_json()

    if not data:
        return jsonify({
            "ket_qua": "Lỗi",
            "thong_bao": "Không có dữ liệu"
        }), 400

    email = data.get("email", "")
    password = data.get("password", "")

    # TC002
    if email == "":
        return jsonify({
            "ket_qua": "Lỗi",
            "thong_bao": "Email không được để trống"
        }), 400

    # TC003
    if password == "":
        return jsonify({
            "ket_qua": "Lỗi",
            "thong_bao": "Mật khẩu không được để trống"
        }), 400

    # TC004 + TC005
    if not kiem_tra_email(email):
        return jsonify({
            "ket_qua": "Lỗi",
            "thong_bao": "Email không hợp lệ"
        }), 400

    # TC008
    if tai_khoan_bi_khoa:

        if time.time() < thoi_gian_mo_khoa:

            return jsonify({
                "ket_qua": "Lỗi",
                "thong_bao": "Tài khoản đang bị khóa"
            }), 403

        else:
            tai_khoan_bi_khoa = False
            so_lan_sai = 0

    # Đăng nhập thành công
    if email == EMAIL_DUNG and password == PASSWORD_DUNG:

        so_lan_sai = 0

        return jsonify({
            "ket_qua": "Thành công",
            "thong_bao": "Đăng nhập thành công"
        }), 200

    # Đăng nhập thất bại
    so_lan_sai += 1

    # TC009 + TC010
    if so_lan_sai >= 5:

        tai_khoan_bi_khoa = True

        # 15 phút
        thoi_gian_mo_khoa = time.time() + 900

        return jsonify({
            "ket_qua": "Lỗi",
            "thong_bao": "Tài khoản bị khóa 15 phút"
        }), 403

    # TC006 + TC007
    return jsonify({
        "ket_qua": "Lỗi",
        "thong_bao": f"Sai thông tin lần {so_lan_sai}"
    }), 401

if __name__ == "__main__":
    app.run(debug=True)