import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool, StructuredTool
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from typing import Optional
from tools.baidu_translate import BaiduTranslateTool
from tools.email_sender import EmailSenderTool
from tools.search_tool import PolicySearchTool

load_dotenv()

class SendEmailSchema(BaseModel):
    subject: str = Field(description="邮件主题")
    content: str = Field(description="邮件正文内容，支持HTML")
    to_email: Optional[str] = Field(default=None, description="收件人邮箱地址。如果不指定，则使用默认配置。")

class PolicyAgent:
    def __init__(self):
        self._validate_env_vars()
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL")
        
        # 初始化 DeepSeek LLM
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=api_key,
            openai_api_base=base_url,
            temperature=0,
            streaming=True, # 开启流式输出
        )

        # 初始化工具实例
        self.baidu_tool = BaiduTranslateTool()
        self.email_tool = EmailSenderTool()
        self.search_tool = PolicySearchTool()

        # 定义 LangChain 工具列表
        self.tools = [
            Tool(
                name="policy_search",
                func=self.search_tool.search_policy,
                description="用于查找政府政策、公告和相关信息。输入应为具体的搜索关键词，如'深圳市政府补贴'、'进出口电机设备改造'等。"
            ),
            Tool(
                name="baidu_translate",
                func=lambda q: self.baidu_tool.translate(q, to_lang='zh'), # 默认翻译成中文，如需其他语言需在Prompt中说明
                description="专业的商务翻译工具，使用百度翻译引擎。用于将文本精准翻译成中文或其他语言。"
            ),
            StructuredTool.from_function(
                func=self.email_tool.send_email,
                name="send_email",
                description="发送专业的商务邮件。可以指定收件人。",
                args_schema=SendEmailSchema
            )
        ]

        # 定义 Agent Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的政策助手Agent，服务于政府和企业用户。你的主要职责是：
1. **政策查找**：在深圳市政府、商务局、工业局、市政府办公厅等官方渠道查找关于政府补贴、进出口设备改造、海关政策、城市更新、交易公告等信息。
2. **政策推送**：关注国家层面、广东省级、深圳市级以及江门市的政策动态。
3. **精准翻译**：使用百度翻译工具进行专业的商务翻译。
4. **邮件撰写与发送**：撰写专业、商务风格的邮件，并通过QQ邮箱发送。支持指定收件人邮箱。

在处理任务时，请遵循以下原则：
- 如果用户在指令中提供了收件人邮箱（如"发送给xxx@qq.com"），请务必在调用邮件工具时提取并传入该邮箱地址。
- 邮件风格必须专业、正式、商务。
- 翻译必须精准，符合商务语境。
- 搜索时，优先关注官方权威渠道。
- 如果用户要求发送邮件，请先生成邮件内容，然后调用发送邮件工具。

请一步步思考，根据用户需求选择合适的工具。
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # 创建 Agent
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def _validate_env_vars(self):
        """验证所有必要的环境变量"""
        required_vars = [
            "DEEPSEEK_API_KEY",
            "BAIDU_APP_ID",
            "BAIDU_SECRET_KEY",
            "QQ_EMAIL_USER",
            "QQ_EMAIL_PASSWORD"
        ]
        
        missing_vars = []
        invalid_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            elif "your_" in value and "_here" in value: # 检查是否还是默认的占位符
                invalid_vars.append(var)
        
        error_msg = []
        if missing_vars:
            error_msg.append(f"Missing environment variables: {', '.join(missing_vars)}")
        if invalid_vars:
            error_msg.append(f"Invalid (placeholder) values found for: {', '.join(invalid_vars)}. Please update them in .env file.")
            
        if error_msg:
            raise ValueError("\n".join(error_msg))
    def run(self, query: str, chat_history=None, callbacks=None):
        """
        运行 Agent
        :param query: 用户输入
        :param chat_history: 聊天历史列表
        :param callbacks: 回调函数列表
        """
        history = chat_history if chat_history else []
        return self.agent_executor.invoke(
            {
                "input": query,
                "chat_history": history
            },
            config={"callbacks": callbacks}
        )

# 简单的测试代码
if __name__ == "__main__":
    agent = PolicyAgent()
    # print(agent.run("帮我查一下深圳市关于工业用地城市更新的最新政策"))