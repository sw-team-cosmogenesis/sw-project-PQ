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


def upload_images_to_oss(image_paths):
    """
    上传图片到阿里云 OSS，返回公开访问 URL 列表
    """
    auth = oss2.Auth(os.getenv("OSS_ACCESS_KEY_ID"), os.getenv("OSS_ACCESS_KEY_SECRET"))
    bucket = oss2.Bucket(auth, os.getenv("OSS_ENDPOINT"), os.getenv("OSS_BUCKET_NAME"))

    urls = []
    for path in image_paths:
        filename = f"{uuid.uuid4().hex}.png"
        with open(path, 'rb') as f:
            bucket.put_object(f"quiz-images/{filename}", f)
        url = f"https://{bucket.bucket_name}.{os.getenv('OSS_ENDPOINT')}/quiz-images/{filename}"
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

    messages = []
    for url in image_urls:
        messages.append({"type": "image_url", "image_url": {"url": url}})

    try:
        completion = client.chat.completions.create(
            model=os.getenv("AI_MODEL"),
            messages=[{"role": "user", "content": messages + """
                根据以上所有图片为我生成三道单选题，要求：
                1.结合所有图片，深度思考并综合后再出题，让每道题目都能覆盖多张图片的内容
                2.每道单选题包含一个题干，四个选项，只有一个是正确答案
                3.每道都题目按照如下格式生成,使用#包围的部分要替换成对应内容：
                [
                    {
                    "question": "#此处替换为题干#",
                    "options": ["A.#此处替换为第一个选项#", "B.#此处替换为第一个选项#", "C.#此处替换为第一个选项#", "D.#此处替换为第一个选项#"],
                    "answer": "#此处替换为正确选项的编号（ABCD）#.#此处替换为正确选项内容#"
                    },
                    {
                    #第二题...#
                    },
                    {
                    #第三题...#
                    },
                ]
                """}],
                stream=True,
            )

        full_response = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                full_response += delta.content

        return full_response

    except Exception as e:
        raise RuntimeError(f"AI 生成题目失败: {e}")