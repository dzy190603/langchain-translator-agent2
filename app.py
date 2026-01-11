import streamlit as st
from agent import PolicyAgent
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from custom_callbacks import StreamlitStreamingCallback

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="政府政策助手 Agent", page_icon="🏛️")

st.title("🏛️ 政府政策助手 Agent")
st.markdown("""
本助手可以帮助您：
- 🔍 **查找政策**：深圳市政府、商务局等官方渠道
- 🌐 **精准翻译**：商务级中英互译 (百度翻译)
- 📧 **发送邮件**：自动生成并发送汇报邮件 (QQ邮箱)
""")

# 侧边栏 - 会话管理
st.sidebar.title("会话管理")

# 初始化会话状态
if "sessions" not in st.session_state:
    st.session_state.sessions = {"默认会话": {"messages": []}}
    st.session_state.current_session = "默认会话"

# 创建新会话
with st.sidebar.form("new_session_form"):
    new_session_name = st.text_input("新会话名称")
    if st.form_submit_button("创建新会话"):
        if new_session_name and new_session_name not in st.session_state.sessions:
            st.session_state.sessions[new_session_name] = {"messages": []}
            st.session_state.current_session = new_session_name
            st.rerun()

# 删除会话
if len(st.session_state.sessions) > 1:
    sessions_to_delete = st.sidebar.multiselect(
        "选择要删除的会话",
        [name for name in st.session_state.sessions.keys() if name != "默认会话"]
    )
    if st.sidebar.button("删除选中的会话"):
        for session_name in sessions_to_delete:
            del st.session_state.sessions[session_name]
        if st.session_state.current_session in sessions_to_delete:
            st.session_state.current_session = "默认会话"
        st.rerun()

# 切换会话
session_options = list(st.session_state.sessions.keys())
current_session = st.sidebar.selectbox(
    "选择会话",
    session_options,
    index=session_options.index(st.session_state.current_session)
)

if current_session != st.session_state.current_session:
    st.session_state.current_session = current_session
    st.rerun()

# 显示当前会话名称
st.sidebar.markdown(f"**当前会话**: `{st.session_state.current_session}`")

# 初始化 Agent（全局）
if "agent" not in st.session_state:
    try:
        st.session_state.agent = PolicyAgent()
        st.sidebar.success("Agent 初始化成功！")
    except Exception as e:
        st.sidebar.error(f"Agent 初始化失败: {str(e)}")
        st.sidebar.info("请检查 .env 文件配置是否正确。")

# 获取当前会话的消息
current_messages = st.session_state.sessions[st.session_state.current_session]["messages"]

# 显示聊天历史
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("请输入您的需求（例如：帮我查一下深圳政府补贴政策）"):
    # 显示用户消息
    st.chat_message("user").markdown(prompt)
    current_messages.append({"role": "user", "content": prompt})

    # 调用 Agent
    if "agent" in st.session_state:
        with st.chat_message("assistant"):
            # 使用自定义 StreamlitStreamingCallback
            st_callback = StreamlitStreamingCallback(st.container())
            
            # 构建聊天历史
            chat_history = []
            for msg in current_messages[:-1]: # 排除最新的一条用户消息，因为它是 input
                if msg["role"] == "user":
                    chat_history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    chat_history.append(AIMessage(content=msg["content"]))

            try:
                response = st.session_state.agent.run(prompt, chat_history=chat_history, callbacks=[st_callback])
                output = response['output']
                # 注意：Callback 已经流式输出了内容，这里不需要再次 st.markdown(output)
                # 除非为了确保格式完全正确（Callback 的流式可能是纯文本拼接）
                # 为了防止重复，我们只更新 session state
                current_messages.append({"role": "assistant", "content": output})
            except Exception as e:
                st.error(f"执行出错: {str(e)}")
    else:
        st.error("Agent 未初始化，无法处理请求。")