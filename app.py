from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

# 全域設定 Jinja2 自訂變數分隔符（如果你確定要使用 {{% ... %}}）
app.jinja_env.variable_start_string = '{{%'
app.jinja_env.variable_end_string = '%}}'

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
    return render_template('music.html', music_info=music_info)

# 其他路由同上...
@app.route('/game')
def game():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_info = [{'url': url_for('static', filename='images/' + file), 'name': file} for file in image_files]
    return render_template('game.html', image_info=image_info)

if __name__ == '__main__':
    # 本地測試用：production 時由 gunicorn 啟動，不需要 debug=True
    app.run(host='0.0.0.0', debug=False)
