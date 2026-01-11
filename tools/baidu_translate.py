import os
import random
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

class BaiduTranslateTool:
    """
    百度通用翻译API封装
    """
    def __init__(self):
        self.appid = os.getenv("BAIDU_APP_ID")
        self.secret_key = os.getenv("BAIDU_SECRET_KEY")
        self.base_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"

    def translate(self, query: str, from_lang: str = 'auto', to_lang: str = 'zh') -> str:
        """
        执行翻译
        :param query: 待翻译文本
        :param from_lang: 源语言
        :param to_lang: 目标语言
        :return: 翻译结果
        """
        if not self.appid or not self.secret_key:
            return "Error: Baidu Translate API credentials not configured in .env"

        salt = random.randint(32768, 65536)
        sign_str = f"{self.appid}{query}{salt}{self.secret_key}"
        sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()

        params = {
            "q": query,
            "from": from_lang,
            "to": to_lang,
            "appid": self.appid,
            "salt": salt,
            "sign": sign
        }

        try:
            response = requests.get(self.base_url, params=params)
            result = response.json()
            
            if "trans_result" in result:
                return "\n".join([item['dst'] for item in result['trans_result']])
            else:
                return f"Translation Error: {result}"
        except Exception as e:
            return f"Request Error: {str(e)}"

# 简单的测试代码
if __name__ == "__main__":
    tool = BaiduTranslateTool()
    print(tool.translate("Hello World", to_lang="zh"))