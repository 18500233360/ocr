import sys
import os
import io
import base64
from typing import Optional

from fastapi import Request
import json

# 尝试导入依赖
try:
    import ddddocr
    from fastapi import FastAPI, File, UploadFile, Body
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError as e:
    print(f"缺少依赖: {e}")
    sys.exit(1)

# 定义请求模型，适配插件的 JSON 格式
class PredictRequest(BaseModel):
    image: str

app = FastAPI(title="验证码识别接口")

# 初始化 OCR
try:
    ocr = ddddocr.DdddOcr(show_ad=False)
except Exception as e:
    print(f"OCR 初始化失败: {e}")
    ocr = None

@app.get("/", response_class=HTMLResponse)
async def index():
    """测试页面"""
    return """
    <html>
        <body style="text-align: center; padding-top: 50px;">
            <h2>验证码识别服务已启动</h2>
            <p>API 接口地址: <code>/predict</code></p>
            <p>请使用插件或网页进行测试</p>
        </body>
    </html>
    """

@app.post("/predict")
async def predict_captcha(request: Request):
    """
    终极兼容版本：手动解析原始数据流
    """
    if ocr is None:
        return {"status": "error", "message": "OCR 引擎未初始化"}

    try:
        # 1. 直接读取原始字节
        raw_bytes = await request.body()
        if not raw_bytes:
            return {"status": "error", "message": "接收到的 Body 为空"}
            
        # 2. 尝试将字节转为字符串
        body_str = raw_bytes.decode("utf-8").strip()
        print(f"收到原始数据长度: {len(body_str)}")

        image_bytes = None

        # 3. 核心逻辑：判断是 JSON 还是 纯 Base64
        if body_str.startswith("{"):
            # 如果是 JSON 格式 {"image": "..."}
            try:
                data_json = json.loads(body_str)
                img_str = data_json.get("image", "")
                if "," in img_str:
                    img_str = img_str.split(",")[-1]
                image_bytes = base64.b64decode(img_str)
                print("JSON 格式解析成功")
            except Exception as je:
                return {"status": "error", "message": f"JSON 解析失败: {str(je)}"}
        else:
            # 如果是纯 Base64 字符串
            img_str = body_str
            if "," in img_str:
                img_str = img_str.split(",")[-1]
            image_bytes = base64.b64decode(img_str)
            print("纯文本 Base64 格式解析成功")

        if not image_bytes:
            return {"status": "error", "message": "解析后未获取到有效的图片字节"}

        # 4. 识别
        print(f"准备识别，字节长度: {len(image_bytes)}")
        result = ocr.classification(image_bytes)
        print(f"识别成功: {result}")
        
        return {"status": "success", "result": result}

    except Exception as e:
        print(f"发生异常: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print("\n服务启动成功！")
    print("本地访问地址: http://127.0.0.1:8000")
    print("插件配置地址: http://127.0.0.1:8000/predict\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)