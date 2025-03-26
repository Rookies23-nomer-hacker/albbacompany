from flask import Flask, request, session, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = "albbasecretkey"  # 세션을 위한 키

# 사내 사용자 정보 (사내번호: 비밀번호)
users = {
    "1001": "password123",  
    "1002": "admin123"
}

# 로그인 페이지
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        emp_id = request.form.get("emp_id")
        password = request.form.get("password")

        if emp_id in users and users[emp_id] == password:
            session["emp_id"] = emp_id
            return redirect(url_for("dashboard"))
        else:
            return "로그인 실패"

    return '''
        <h2>사내 로그인 시스템</h2>
        <form method="POST">
            사내번호: <input type="text" name="emp_id"><br>
            비밀번호: <input type="password" name="password"><br>
            <input type="submit" value="로그인">
        </form>
    '''

# 대시보드 페이지 (로그인 필요)
@app.route("/dashboard")
def dashboard():
    if "emp_id" not in session:
        return redirect(url_for("login"))

    return '''
        <h2>사내 시스템 대시보드</h2>
        <p>파일 서버에서 파일을 가져오려면 아래 입력창에 파일명을 입력하세요.</p>
        <form action="/get_file" method="GET">
            파일명: <input type="text" name="filename">
            <input type="submit" value="조회">
        </form>
        <br>
        <p>Command Injection 테스트:</p>
        <form action="/execute" method="GET">
            명령어: <input type="text" name="cmd">
            <input type="submit" value="실행">
        </form>
    '''

# 취약한 명령 실행 API (Command Injection)
@app.route("/execute", methods=["GET"])
def execute():
    if "emp_id" not in session:
        return "로그인이 필요합니다."

    cmd = request.args.get("cmd")
    if cmd:
        output = os.popen(cmd).read()  # 사용자 입력을 검증 없이 실행 (취약점)
        return f"<pre>{output}</pre>"

    return "명령어를 입력하세요."

# 파일 서버에서 특정 파일 가져오기
@app.route("/get_file", methods=["GET"])
def get_file():
    if "emp_id" not in session:
        return "로그인이 필요합니다."

    filename = request.args.get("filename")
    if not filename:
        return "파일명을 입력하세요."

    # 파일 서버 URL (Ubuntu 내부 네트워크 사용)
    file_server_url = f"http://file_server/{filename}"

    try:
        response = requests.get(file_server_url)
        if response.status_code == 200:
            return f"<h3>파일 내용:</h3><pre>{response.text}</pre>"
        else:
            return "파일을 찾을 수 없습니다."
    except Exception as e:
        return f"오류 발생: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
