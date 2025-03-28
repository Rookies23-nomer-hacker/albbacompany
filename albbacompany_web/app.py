from flask import Flask, request, session, redirect, url_for
import subprocess
import requests

app = Flask(__name__)

@app.route("/")
def dashboard():
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

# 컨테이너 내부에서 명령 실행 API
@app.route("/execute", methods=["GET"])
def execute():
    cmd = request.args.get("cmd")
    if cmd:
        try:
            result = subprocess.run(
                ["docker", "exec", "albbacompany_web", "sh", "-c", cmd],
                capture_output=True,
                text=True
            )
            return f"<pre>{result.stdout}{result.stderr}</pre>"
        except Exception as e:
            return f"오류 발생: {str(e)}"

    return "명령어를 입력하세요."

# 파일 서버에서 특정 파일 가져오기
@app.route("/get_file", methods=["GET"])
def get_file():
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
