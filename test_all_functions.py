#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证所有功能是否正常工作
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_env_vars():
    """测试环境变量是否配置正确"""
    print("=== 测试环境变量 ===")
    
    required_vars = [
        "DEEPSEEK_API_KEY",
        "BAIDU_APP_ID",
        "BAIDU_SECRET_KEY",
        "QQ_EMAIL_USER",
        "QQ_EMAIL_PASSWORD"
    ]
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if not value or "your_" in value:
            print(f"❌ {var}: 未配置或使用了占位符")
            all_good = False
        else:
            print(f"✅ {var}: 已配置")
    
    return all_good

def test_agent_import():
    """测试Agent导入是否正常"""
    print("\n=== 测试Agent导入 ===")
    try:
        from agent import PolicyAgent
        print("✅ Agent导入成功")
        return True
    except Exception as e:
        print(f"❌ Agent导入失败: {e}")
        return False

def test_tools_import():
    """测试工具导入是否正常"""
    print("\n=== 测试工具导入 ===")
    try:
        from tools.baidu_translate import BaiduTranslateTool
        from tools.email_sender import EmailSenderTool
        from tools.search_tool import PolicySearchTool
        print("✅ 所有工具导入成功")
        return True
    except Exception as e:
        print(f"❌ 工具导入失败: {e}")
        return False

def test_custom_callbacks():
    """测试自定义回调函数"""
    print("\n=== 测试自定义回调函数 ===")
    try:
        from custom_callbacks import StreamlitStreamingCallback
        print("✅ 自定义回调函数导入成功")
        return True
    except Exception as e:
        print(f"❌ 自定义回调函数导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试所有功能...\n")
    
    tests = [
        test_env_vars,
        test_agent_import,
        test_tools_import,
        test_custom_callbacks
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n=== 测试结果 ===")
    if all(results):
        print("🎉 所有测试通过！项目可以正常运行。")
        print("\n运行以下命令启动应用：")
        print("streamlit run app.py")
    else:
        print("❌ 部分测试失败，请检查配置和代码。")
        sys.exit(1)

if __name__ == "__main__":
    main()