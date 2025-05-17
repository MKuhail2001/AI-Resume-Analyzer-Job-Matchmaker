import os
import base64
from http import HTTPStatus
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dashscope import Application
import dashscope
import oss2


# === STEP 1: CONFIGURE OSS ===
ACCESS_KEY_ID = 'LTAI5tJMi2JjCiAL7Fc3kGfR'
ACCESS_KEY_SECRET = 'vLUtNHN5boBGF72Q5YSBsAn6OAA21a'
ENDPOINT = 'oss-ap-southeast-1.aliyuncs.com'
BUCKET_NAME = 'resumejob-sing'
OBJECT_NAME = 'uploads/resume.jpg'  # Replace dynamically if needed

# === INIT FASTAPI APP ===
app = FastAPI()

# Allow CORS for local HTML/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MAIN ROUTE ===
@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    # === STEP 2: Upload to OSS ===
    contents = await file.read()
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, f'https://{ENDPOINT}', BUCKET_NAME)
    bucket.put_object(OBJECT_NAME, contents)
    oss_image_url = f"https://{BUCKET_NAME}.{ENDPOINT}/{OBJECT_NAME}"
    print(f"✅ Uploaded image to: {oss_image_url}")

    # === STEP 3: Call Qwen-VL ===
    client = OpenAI(
        api_key="sk-89b7cd5acee04ae7a5d1b329487352be",  # Replace with your working DashScope key
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    )

    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[
            {"role": "system", "content": "Structure the content in json format."},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract the information from the resume."},
                {"type": "image_url", "image_url": {"url": oss_image_url}}
            ]}
        ]
    )

    json_c = completion.choices[0].message.content

    # === STEP 4: Optional - Call Application Agent (comment out if not using App ID) ===
    dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
    response = Application.call(
        api_key="sk-89b7cd5acee04ae7a5d1b329487352be",  # Same key
        app_id="cad1489eabea4c66a7fdea6c3d4865ef",  # Your Agent App ID (optional)
        prompt='"Return the resume analysis as clean, readable plain text. Use line breaks for separation. Do not use Markdown symbols (like **, *, _, #), and do not return any HTML. Format everything using only plain text, such as dashes for bullet points and numbers for lists.", Analyze the resume and give the information based on the information ==>' + json_c + 'Return the resume analysis in readable bullet point format for UI display. Do not use JSON. Include: Summary (as a paragraph), '
        'Scores (as bullet points), Suggestions (as numbered list), Matching job roles (bullet list), Career path suggestions (as paragraph)"'
    )

    if response.status_code != HTTPStatus.OK:
        return {
            "error": response.message,
            "status": response.status_code,
            "request_id": response.request_id
        }
    


   
    return {"analysis": response.output.text}