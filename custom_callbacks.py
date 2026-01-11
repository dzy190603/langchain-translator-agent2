import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List, Union

class StreamlitStreamingCallback(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
        self.placeholder = container.empty()
        self.tool_expander = None

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.text += token
        self.placeholder.markdown(self.text + "▌")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        self.placeholder.markdown(self.text)

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        if self.tool_expander is None:
            self.tool_expander = self.container.status("Agent 正在执行工具调用...", expanded=True)
        self.tool_expander.write(f"调用工具: {serialized.get('name')}...")
        self.tool_expander.write(f"输入: {input_str}")

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        if self.tool_expander:
            self.tool_expander.write(f"工具输出: {output[:500]}..." if len(output) > 500 else f"工具输出: {output}")
            self.tool_expander.update(label="工具调用完成", state="complete", expanded=False)
            self.tool_expander = None # 重置，以便下一次调用创建新的 status