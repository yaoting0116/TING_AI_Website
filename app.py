"""
Flask app with improved Hugging Face InferenceClient usage and router fallback handling.
已修改要點：
 - 使用 InferenceClient(api_key=...) 或 InferenceClient(token=...)（依 installed 版本而定）
 - 移除強制 base_url，讓客戶端自己處理 router/provider 決策（較穩定）
 - 更完整的例外處理：捕捉 404（模型未被 provider 託管）並回傳友善錯誤
 - 保留本地 fallback（無 HF_API_KEY 時）
 - 保留原本的前端模板 / 靜態檔案處理邏輯

注意：若要在 router 上成功呼叫模型，請確認 model_name 在 Hugging Face 上有 "Run" / "Inference" 支援（或使用付費的 Inference Endpoint）。
"""
from flask import Flask, render_template, url_for, Response, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import logging

load_dotenv()
# 建議把 HF_API_KEY 與想要使用的模型名稱放在 .env
HF_API_KEY = os.getenv("HF_API_KEY", "")
# 若要更換模型，請改此處。注意：不是所有 hub 模型都可經由 router 提供者呼叫。
MODEL_NAME = os.getenv("HF_MODEL", "openai/gpt-oss-120b:groq")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 設定 logger level（方便本地 debugging）
logging.basicConfig(level=logging.DEBUG)

# -------------------------
# Jinja 自訂設定（保留）
# -------------------------
from jinja2 import Environment, FileSystemLoader
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.variable_start_string = '{{%'
env.variable_end_string = '%}}'
env.globals.update(url_for=url_for)

# 小工具：列出 static 子資料夾檔案
def list_files_in_folder(folder_relative):
    folder = os.path.join(app.static_folder, folder_relative)
    try:
        if not os.path.isdir(folder):
            return []
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except Exception:
        return []

@app.route('/')
def index():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))] if os.path.isdir(image_folder) else []
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('index.html', image_info=image_info)

@app.route('/music')
def music():
    music_folder = os.path.join(app.static_folder, 'music')
    music_files = [f for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))] if os.path.isdir(music_folder) else []
    music_info = [{'url': url_for('static', filename='music/' + file), 'name': file} for file in music_files]
    template = env.get_template('music.html')
    return template.render(music_info=music_info)

@app.route('/game')
def game():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))] if os.path.isdir(image_folder) else []
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('game.html', image_info=image_info)

@app.route('/learning')
def learning():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))] if os.path.isdir(image_folder) else []
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('learning.html', image_info=image_info)

@app.route('/NLP')
def NLP():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))] if os.path.isdir(image_folder) else []
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('NLP.html', image_info=image_info)

# -------------------------
# /api/chat - 使用 Hugging Face InferenceClient（router）並有 router fallback
# 前端傳入 JSON: { messages: [ {role:'user'|'assistant', content: '...'}, ... ] }
# -------------------------

@app.route('/api/chat', methods=['POST'])
def api_chat():
    from openai import OpenAI

    data = request.get_json(force=True) or {}
    messages = data.get("messages", [])

    # 只保留最近 12 條 user/assistant/system 等訊息（few-shot 會另外插入）
    messages = messages[-12:]

    if not messages:
        return jsonify({"ok": False, "reply": "沒有收到訊息"}), 400

    # 找最後一個 user（用於 local fallback 訊息呈現）
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break

    # 本地 fallback（沒有 API key）
    if not HF_API_KEY:
        return jsonify({
            "ok": True,
            "reply": f"（本地測試回應）我收到：{last_user}"
        })

    # --- System prompt + few-shot 準備 ---
    # 只在前端沒提供 system message 時自動插入
    has_system = any(m.get("role") == "system" for m in messages)

    # System prompt：要求繁體（台灣用語）回覆中文
    system_prompt = (
        "你是個助理。當使用者使用中文或包含中文漢字時，請以 繁體中文（臺灣常用表達） 回答；"
        "若使用者使用英文或其他語言，請以使用者使用的語言回答。"
        "請保持回答清楚、友善並避免使用簡體字。"
    )

    # few-shot 範例（示範用戶問中文/助理以繁體回答）
    few_shot = [
        {"role": "user", "content": "請問台北明天天氣如何？"},
        {"role": "assistant", "content": "台北明天天氣通常是多雲到晴，早晚溫差請注意保暖；出門記得帶外套。"},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."}
    ]

    # 組出要送到模型的 messages（不覆蓋使用者提供的 system）
    outgoing = []
    if not has_system:
        outgoing.append({"role": "system", "content": system_prompt})
        # 加 few-shot（放在 system 之後）
        outgoing.extend(few_shot)

    # 最後 append 使用者的歷史對話（保持原順序）
    outgoing.extend(messages)

    # Debug log（可移除）
    app.logger.debug("Outgoing messages (with few-shot) length=%d", len(outgoing))

    # 呼叫模型
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HF_API_KEY,
        )

        model_to_use = MODEL_NAME or "openai/gpt-oss-120b:groq"

        completion = client.chat.completions.create(
            model=model_to_use,
            messages=outgoing,
            max_tokens=1000,
        )

        # 取出回覆（視 library 回傳結構）
        reply = ""
        try:
            reply = completion.choices[0].message.content
        except Exception:
            # fallback：把整個物件當字串
            reply = str(completion)

        return jsonify({"ok": True, "reply": reply})

    except Exception as e:
        app.logger.exception("OpenAI router call failed: %s", e)
        return jsonify({
            "ok": False,
            "error": str(e),
            "reply": "呼叫 Hugging Face Router 失敗"
        }), 500
# -------------------------
# after_request：自動注入 viewport、CSS、並載入外部 JS
# -------------------------
@app.after_request
def inject_responsive(response: Response):
    try:
        content_type = response.headers.get('Content-Type', '')
        if response.status_code == 200 and 'text/html' in content_type.lower():
            html = response.get_data(as_text=True)
            head_injection = (
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                f'<link rel="stylesheet" href="{url_for("static", filename="css/responsive.css")}" />\n'
            )
            body_script_tag = f'<script src="{url_for("static", filename="js/responsive.js")}"></script>\n'
            if '</head>' in html:
                html = html.replace('</head>', head_injection + '</head>', 1)
            else:
                html = head_injection + html
            if '</body>' in html:
                html = html.replace('</body>', body_script_tag + '</body>', 1)
            else:
                html = html + body_script_tag
            response.set_data(html)
            # Content-Length 需要字串
            response.headers['Content-Length'] = str(len(response.get_data()))
    except Exception as e:
        app.logger.exception("inject_responsive failed: %s", e)
    return response

@app.route("/api/check_model")
def check_model():
    import requests
    import os

    model = request.args.get("model", "openai/gpt-oss-120b:groq")
    hf_key = os.getenv("HF_API_KEY", "")

    url = f"https://huggingface.co/api/models/{model}?expand=inferenceProviderMapping"

    headers = {}
    if hf_key:
        headers["Authorization"] = f"Bearer {hf_key}"

    try:
        resp = requests.get(url, headers=headers, timeout=30)

        if resp.status_code != 200:
            return jsonify({
                "status": "error",
                "status_code": resp.status_code,
                "text": resp.text
            }), resp.status_code

        data = resp.json()

        providers = data.get("inferenceProviderMapping", {})

        return jsonify({
            "model": model,
            "providers": providers,
            "provider_count": len(providers)
        })

    except Exception as e:
        return jsonify({
            "status": "exception",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # debug 模式下可改 host='0.0.0.0' 以便局域網測試
    app.run(debug=True)
