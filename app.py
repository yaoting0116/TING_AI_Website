from flask import Flask, render_template, url_for, Response
import os

app = Flask(__name__)

# -------------------------
# 你的現有 Jinja 自訂設定（保留）
# -------------------------
from jinja2 import Environment, FileSystemLoader
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.variable_start_string = '{{%'
env.variable_end_string = '%}}'
env.globals.update(url_for=url_for)  # Add url_for to the Jinja2 environment

# -------------------------
# 小工具：列出 static 子資料夾檔案
# -------------------------
def list_files_in_folder(folder_relative):
    folder = os.path.join(app.static_folder, folder_relative)
    try:
        if not os.path.isdir(folder):
            return []
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except Exception:
        return []

# -------------------------
# Routes（保留你原有的路由） 
# -------------------------
@app.route('/')
def index():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('index.html', image_info=image_info)

@app.route('/music')
def music():
    music_folder = os.path.join(app.static_folder, 'music')
    music_files = [f for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))]
    music_info = [{'url': url_for('static', filename='music/' + file), 'name': file} for file in music_files]
    template = env.get_template('music.html')
    return template.render(music_info=music_info)

@app.route('/game')
def game():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('game.html', image_info=image_info)

@app.route('/learning')
def learning():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('learning.html', image_info=image_info)

@app.route('/NLP')
def NLP():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('NLP.html', image_info=image_info)

# -------------------------
# after_request：自動注入 viewport、CSS、並載入外部 JS（僅對 HTML 回應）
# -------------------------
@app.after_request
def inject_responsive(response: Response):
    try:
        content_type = response.headers.get('Content-Type', '')
        # 只對 HTML 回應進行注入（避免影響 JSON、圖片等）
        if response.status_code == 200 and 'text/html' in content_type.lower():
            html = response.get_data(as_text=True)

            # head 要注入的內容（meta + css link）
            head_injection = (
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                f'<link rel="stylesheet" href="{url_for("static", filename="css/responsive.css")}" />\n'
            )

            # body 底部注入外部 JS（避免 inline script 被 CSP 阻擋）
            body_script_tag = f'<script src="{url_for("static", filename="js/responsive.js")}"></script>\n'

            # 插入 head_injection 到 </head> 前（若沒有 head，則嘗試放到 html 開頭）
            if '</head>' in html:
                html = html.replace('</head>', head_injection + '</head>', 1)
            else:
                html = head_injection + html

            # 插入 body_script_tag 到 </body> 前（若沒有 body，則 append）
            if '</body>' in html:
                html = html.replace('</body>', body_script_tag + '</body>', 1)
            else:
                html = html + body_script_tag

            # 設定回應內容與長度
            response.set_data(html)
            response.headers['Content-Length'] = len(response.get_data())
    except Exception as e:
        # 發生例外也不要阻斷回應，並記錄錯誤
        app.logger.exception("inject_responsive failed: %s", e)
    return response

if __name__ == '__main__':
    # 若需要在局域網測試手機，改 host='0.0.0.0'（測試時再改）
    app.run(debug=True)
