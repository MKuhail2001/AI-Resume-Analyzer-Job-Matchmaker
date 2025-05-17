from flask import Flask, request, jsonify
import os
import base64
from http import HTTPStatus
import oss2
from dashscope import Application
import dashscope

# === OSS Configuration ===
ACCESS_KEY_ID = 'LTAI5tJMi2JjCiAL7Fc3kGfR'
ACCESS_KEY_SECRET = 'vLUtNHN5boBGF72Q5YSBsAn6OAA21a'
ENDPOINT = 'oss-ap-southeast-1.aliyuncs.com'
BUCKET_NAME = 'resumejob-sing'
OBJECT_NAME = 'uploads/resume.jpg'  # You can append a timestamp for uniqueness if needed

# === Qwen DashScope Configuration ===
API_KEY = 'sk-89b7cd5acee04ae7a5d1b329487352be'
APP_ID = 'cad1489eabea4c66a7fdea6c3d4865ef'
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Backend ready to receive resume uploads and analyze with Qwen AI.'

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        # Save locally
        local_path = "resume.jpg"
        file.save(local_path)

        # Upload to OSS
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, 'https://' + ENDPOINT, BUCKET_NAME)

        with open(local_path, "rb") as f:
            bucket.put_object(OBJECT_NAME, f)

        public_url = f"https://{BUCKET_NAME}.{ENDPOINT}/{OBJECT_NAME}"
        print(f"✅ Uploaded to OSS: {public_url}")

        # Prepare Qwen AI prompt
        prompt = [
            {"image_list": [public_url]},
            {"text": "You are an expert career advisor. Analyze this resume and provide strengths, weaknesses, job matches, and career suggestions."}
        ]

        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt
        )

        if response.status_code != HTTPStatus.OK:
            return jsonify({
                'error': f"Qwen API error: {response.message}",
                'code': response.status_code,
                'request_id': response.request_id
            })

        return jsonify({'result': response.output.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '_main_':
    host = '127.0.0.1'
    port = 5000
    print(f"🚀 Server running at http://{host}:{port}")
    app.run(host=host, port=port, debug=True)