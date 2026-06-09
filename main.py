from flask import Flask, request, send_file
import yt_dlp, os, glob

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('q')
    if not query:
        return {'error': 'no query'}, 400
    
    os.makedirs('/tmp/sc', exist_ok=True)
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/sc/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'default_search': 'scsearch',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([query])
    
    files = glob.glob('/tmp/sc/*.mp3')
    if not files:
        return {'error': 'not found'}, 404
    
    path = files[0]
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))