# Pthon版本
Python 3.13.12
# 安装依赖
pip install -r requirements.txt
python main.python
# 接口调用
接口url：http://127.0.0.1:8000

Request template：

POST /predict HTTP/1.1

Host: 127.0.0.1:8000

Content-Type: application/json


{
  "image": "<@BASE64><@IMG_RAW></@IMG_RAW></@BASE64>"
}

匹配方式：正则表达式

匹配规则："result"\s*:\s*"([^"]+)"

<img width="1440" height="868" alt="image" src="https://github.com/user-attachments/assets/77ef81d6-d873-4d91-8771-426ea1aabdce" />
