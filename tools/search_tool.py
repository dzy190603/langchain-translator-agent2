from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

class PolicySearchTool:
    """
    政策搜索工具封装
    """
    def __init__(self):
        self.wrapper = DuckDuckGoSearchAPIWrapper(region="cn-zh")
        self.search = DuckDuckGoSearchRun(api_wrapper=self.wrapper)

    def search_policy(self, query: str) -> str:
        """
        执行搜索
        :param query: 搜索关键词
        :return: 搜索结果摘要
        """
        try:
            return self.search.invoke(query)
        except Exception as e:
            return f"Search Error: {str(e)}"

# 简单的测试代码
if __name__ == "__main__":
    tool = PolicySearchTool()
    print(tool.search_policy("深圳市政府 政策"))