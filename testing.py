import os
from openai import OpenAI
from dashscope import Application
import dashscope
from http import HTTPStatus


client = OpenAI(
    # If environment variables are not configured, replace the following line with: api_key="sk-xxx",
    api_key="sk-89b7cd5acee04ae7a5d1b329487352be",
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-plus",  # This example uses qwen-vl-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/zh/model-studio/getting-started/models
    messages=[ {"role": "system", "content": "Structure the content in json format."},
        {"role": "user","content": [
            {"type": "text","text": "Extract the information from the resume."},
            {"type": "image_url",
             "image_url": {"url": "https://resume-testing.oss-ap-southeast-1.aliyuncs.com/resume_test.png"}}
            ]}]
    )
json_c = completion.choices[0].message.content


dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
response = Application.call(
    # If environment variables are not configured, you can replace the following line with api_key="sk-xxx". However, it is not recommended to hard code the API Key directly into the code in a production environment to reduce the risk of API Key leakage.
    api_key= "sk-89b7cd5acee04ae7a5d1b329487352be",  # Safer to use env var
    app_id='cad1489eabea4c66a7fdea6c3d4865ef',  # Replace with your real app ID

    prompt='Analyze the resume and give the information '+ json_c)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'Refer to: https://www.alibabacloud.com/help/en/model-studio/developer-reference/error-code')
else:
    print(response.output.text)