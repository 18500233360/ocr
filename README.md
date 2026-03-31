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


