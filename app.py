from flask import Flask, render_template, url_for
import os
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# Configure custom Jinja2 environment
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.variable_start_string = '{{%'
env.variable_end_string = '%}}'
env.globals.update(url_for=url_for)  # Add url_for to the Jinja2 environment

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

if __name__ == '__main__':
    app.run(debug=True)
