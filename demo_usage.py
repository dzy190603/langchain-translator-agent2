from tools.baidu_translate import BaiduTranslateTool
from tools.email_sender import EmailSenderTool
from tools.search_tool import PolicySearchTool
import os

# 模拟设置环境变量（实际使用请在 .env 文件中配置）
os.environ["BAIDU_APP_ID"] = "test_app_id"
os.environ["BAIDU_SECRET_KEY"] = "test_secret_key"
os.environ["QQ_EMAIL_USER"] = "test_user@qq.com"
os.environ["QQ_EMAIL_PASSWORD"] = "test_auth_code"
os.environ["TARGET_EMAIL"] = "target@example.com"

def demo_tools():
    print("=== Testing Tools Individually ===")
    
    # 1. 测试搜索工具
    print("\n[1] Testing Search Tool:")
    search_tool = PolicySearchTool()
    # 注意：如果没有真实的 API Key，这里可能会报错或者返回模拟数据（取决于库的实现）
    # 但我们至少可以初始化它
    print("Search Tool Initialized.")
    
    # 2. 测试翻译工具
    print("\n[2] Testing Baidu Translate Tool:")
    trans_tool = BaiduTranslateTool()
    print("Translate Tool Initialized.")
    # result = trans_tool.translate("Hello World") # 真实调用需要 Key
    # print(f"Translation Result: {result}")

    # 3. 测试邮件工具
    print("\n[3] Testing Email Tool:")
    email_tool = EmailSenderTool()
    print("Email Tool Initialized.")
    # result = email_tool.send_email("Test Subject", "<h1>Test Content</h1>") # 真实调用需要配置
    # print(f"Email Send Result: {result}")

if __name__ == "__main__":
    demo_tools()
    print("\n=== Demo Complete ===")
    print("To run the full agent, please configure .env and run 'python main.py'")