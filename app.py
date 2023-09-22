from flask import Flask, request, jsonify,send_file, render_template
import os

app = Flask(__name__)


CONVERTED_FOLDER = 'converted'


app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/convert', methods=['POST'])
def convert():
    mp4_file = request.files['mp4_file']
    mp4_path = os.path.join( mp4_file.filename)
    mkv_file = os.path.splitext(mp4_file.filename)[0] + '.mkv'
    mkv_path = os.path.join(app.config['CONVERTED_FOLDER'], mkv_file)

    mp4_file.save(mp4_path)

    
    os.system(f'ffmpeg -i {mp4_path} -c:v libx265 -preset medium -crf 28 -c:a aac -strict experimental -b:a 128k -movflags +faststart -y {mkv_path}')

    return jsonify({'The Video was downloaded in converted folder as': mkv_file})
@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['CONVERTED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
