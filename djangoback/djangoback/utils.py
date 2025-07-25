import json
import os
import comtypes.client


def pptx_to_pdf(filepath: str, pdf_path: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"输入文件不存在: {filepath}")

    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    try:
        presentation = powerpoint.Presentations.Open(filepath, WithWindow=False)
        presentation.SaveAs(pdf_path, FileFormat=32)  # 32 表示 PDF 格式
        presentation.Close()
    finally:
        powerpoint.Quit()


import os
import uuid
import oss2
from openai import OpenAI

from django.conf import settings


def upload_images_to_oss(image_paths, presentation_uuid):
    """
    上传图片到阿里云 OSS，返回公开访问 URL 列表
    """
    auth = oss2.Auth(os.getenv("OSS_ACCESS_KEY_ID"), os.getenv("OSS_ACCESS_KEY_SECRET"))
    bucket = oss2.Bucket(auth, os.getenv("OSS_ENDPOINT"), os.getenv("OSS_BUCKET_NAME"))

    urls = []
    for path in image_paths:
        filename = f"{uuid.uuid4().hex}.png"
        with open(path, 'rb') as f:
            bucket.put_object(f"{presentation_uuid}/{filename}", f)
        url = f"https://{bucket.bucket_name}.{os.getenv('OSS_ENDPOINT')}/{presentation_uuid}/{filename}"
        urls.append(url)
    return urls


def generate_quiz_from_images(image_urls):
    """
    调用通义千问大模型分析图像并生成三道选择题，返回题目结构
    """
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    if not image_urls:
        raise ValueError("图片列表为空，无法生成题目")

        # 构建图像 + 文本 prompt 消息
    content = [
        {"type": "image_url", "image_url": {"url": url}}
        for url in image_urls
    ]

    # 文字 prompt
    prompt_text = """
    根据以上所有图片为我生成三道单选题，要求：
    1. 结合所有图片，深度思考并综合后再出题，让每道题目都能覆盖多张图片的内容
    2. 每道单选题包含一个题干，四个选项，只有一个是正确答案
    3. 生成的题目不要用markdown格式包裹，返回纯文本
    4. 每道题目按照如下格式生成，返回合法 JSON 格式数组：
    [
      {
        "question": "题目内容，不包括选项",
        "options": [
          "A. 选项A",
          "B. 选项B",
          "C. 选项C",
          "D. 选项D"
        ],
        "answer": "只有正确选项序号"
      },
      {
        "question": "题干内容2",
        ...
      },
      ...
    ]
        """
    content.append({"type": "text", "text": prompt_text})

    messages = [
        {
            "role": "user",
            "content": content
        }
    ]

    # 调用 DashScope 多模态接口
    try:
        completion = client.chat.completions.create(
            model=os.getenv("AI_MODEL", "qwen-omni-turbo"),
            messages=messages,
            modalities=["text"],
            stream=True,
            stream_options={"include_usage": True}
        )

        full_content = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content

        return full_content

    except Exception as e:
        raise RuntimeError("AI 生成题目失败: " + str(e))