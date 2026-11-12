import requests

g_ocr_url = "http://127.0.0.1:8089/ocr"  # 默认本地 OCR 服务；实际地址由用例配置的 ocr_srv_url 经 init() 注入

def proc(encoded_image, debug_level=0):
    global g_ocr_url
    # 发送OCR请求
    try:
        response = requests.post(g_ocr_url, files={"image_body": encoded_image.tobytes()})
        if debug_level>4:
            print(response.json()['result'])
        return response.json()['result']

    except Exception as e:
        print(f"处理失败: {e}")
        return None

def init(ocr_srv_url):
    global g_ocr_url
    g_ocr_url = ocr_srv_url
