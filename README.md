# 政府政策助手 Agent

一个基于 LangChain 的智能政策助手，集成政策搜索、翻译和邮件发送功能。

## 功能特性

- 🔍 **政策搜索**：从深圳市政府、商务局等官方渠道查找政策信息
- 🌐 **精准翻译**：商务级中英互译（百度翻译API）
- 📧 **邮件发送**：自动生成并发送专业邮件（QQ邮箱SMTP）
- 💬 **多会话支持**：创建多个独立对话窗口，保持各自记忆
- ⚡ **流式输出**：实时响应，提升用户体验
- 🧠 **对话记忆**：保持上下文，支持多轮对话

## 技术栈

- **Framework**: LangChain, Streamlit
- **LLM**: DeepSeek API
- **Search**: DuckDuckGo Search
- **Translation**: Baidu Translate API
- **Email**: QQ Mail SMTP

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填写真实的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下信息：

```
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 百度翻译 API 配置
BAIDU_APP_ID=your_baidu_app_id_here
BAIDU_SECRET_KEY=your_baidu_secret_key_here

# QQ 邮箱配置 (发送方)
QQ_EMAIL_USER=your_qq_email@qq.com
QQ_EMAIL_PASSWORD=your_qq_email_authorization_code

# 接收方邮箱 (默认)
TARGET_EMAIL=recipient_email@example.com
```

### 3. 运行应用

```bash
streamlit run app.py
```

## 使用说明

### 基本使用

1. 在聊天框中输入您的需求，例如：
   - "帮我查一下深圳政府补贴政策"
   - "翻译这段英文政策到中文"
   - "发送一封关于政策调研的邮件给xxx@qq.com"

2. 查看实时流式响应

### 多会话管理

- 在侧边栏可以创建新的对话会话
- 每个会话有独立的对话历史和记忆
- 可以删除不需要的会话（默认会话不可删除）

## 开发指南

### 项目结构

```
.
├── agent.py              # 主Agent逻辑
├── app.py                # Streamlit Web界面
├── custom_callbacks.py   # 自定义回调函数
├── requirements.txt      # 项目依赖
├── .env.example          # 环境变量模板
├── test_all_functions.py # 功能测试脚本
├── tools/                # 工具模块
│   ├── baidu_translate.py # 百度翻译工具
│   ├── email_sender.py    # 邮件发送工具
│   └── search_tool.py     # 政策搜索工具
└── main.py               # CLI版本（已弃用）
```

### 测试

运行测试脚本验证所有功能：

```bash
python test_all_functions.py
```

### 扩展功能

如需添加新工具，请参考 `tools/` 目录中的现有工具实现，并在 `agent.py` 中注册。

## 注意事项

1. **API密钥安全**：请妥善保管您的API密钥，不要提交到版本控制系统
2. **邮箱配置**：QQ邮箱需要使用授权码而非登录密码
3. **网络连接**：确保可以访问DeepSeek、百度翻译和QQ邮箱服务

## 故障排除

### 常见问题

1. **Agent初始化失败**：检查 `.env` 文件中的API密钥是否正确
2. **邮件发送失败**：确认QQ邮箱授权码是否正确，并检查邮箱设置
3. **翻译功能异常**：验证百度翻译API密钥和APP ID

### 日志查看

在Streamlit界面中可以查看详细的工具调用过程和结果。

## 更新日志

- 2024-01-11: 实现多会话支持
- 2024-01-10: 添加流式输出和对话记忆
- 2024-01-09: 完成Web界面开发
- 2024-01-08: 实现基本功能和工具集成

## 许可证

MIT License