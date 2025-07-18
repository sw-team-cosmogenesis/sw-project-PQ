import os
import json
from openai import OpenAI

# 初始化 DashScope 兼容客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 发起流式请求
response = client.chat.completions.create(
    model="qwen-omni-turbo-latest",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "请用中文介绍一下Python的优点。"}
    ],
    stream=True,
)

# 逐块读取并拼接响应内容
full_content = ""
for chunk in response:
    delta = chunk.choices[0].delta
    content = delta.content or ""
    full_content += content

# 写入 JSON 文件
output_data = {"response": full_content}
output_path = "ai_response.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"✅ 已保存结果到 {output_path}")
