import requests

g_ocr_url = "http://10.80.59.138:8089/ocr"  # 默认使用ocr1

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
