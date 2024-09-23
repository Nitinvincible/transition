from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, ImageClip, vfx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'jpg', 'jpeg', 'png', 'mp3', 'wav'}

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return "Welcome to the Video Editor"

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/edit', methods=['POST'])
def editVideo():
    data = request.json
    timeline = data['timeline']
    
    def createVideoClip(item):
        clip = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], item['filename']))
        return clip.subclip(item['start'], item['end'])

    def createImageClip(item):
        clip = ImageClip(os.path.join(app.config['UPLOAD_FOLDER'], item['filename']))
        return clip.set_duration(item['duration'])

    def createAudioClip(item):
        return AudioFileClip(os.path.join(app.config['UPLOAD_FOLDER'], item['filename']))

    clip_creators = {
        'video': createVideoClip,
        'image': createImageClip,
        'audio': createAudioClip
    }

    clips = []
    for i, item in enumerate(timeline):
        clip = clip_creators.get(item['type'])(item)
        
        if 'effects' in item:
            for effect in item['effects']:
                if effect['type'] == 'resize':
                    clip = clip.resize(width=effect['width'])
        
        if i > 0 and 'transition' in item:
            prev_clip = clips[-1]
            transition_duration = item['transition']['duration']
            if item['transition']['type'] == 'fade':
                clip = clip.crossfadein(transition_duration)
                prev_clip = prev_clip.crossfadeout(transition_duration)
                clips[-1] = prev_clip
            # Add more transition types as needed
        
        clips.append(clip)
    
    final_clip = concatenate_videoclips(clips)
    
    if 'audio' in data:
        audio = AudioFileClip(os.path.join(app.config['UPLOAD_FOLDER'], data['audio']))
        final_clip = final_clip.set_audio(audio)
    
    output_filename = 'output.mp4'
    final_clip.write_videofile(os.path.join(app.config['UPLOAD_FOLDER'], output_filename))
    
    return jsonify({'success': True, 'output': output_filename})

@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('files')
    filenames = []
    for file in files:
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return jsonify(filenames)

if __name__ == '__main__':
    app.run(debug=True)
