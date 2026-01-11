import sys
from agent import PolicyAgent
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    print("Initializing Policy Agent...")
    try:
        agent = PolicyAgent()
        print("Policy Agent initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize Policy Agent: {e}")
        print("Please check your .env configuration.")
        return

    print("\nWelcome to the Policy Agent CLI!")
    print("Type 'exit' or 'quit' to end the session.")
    print("Example commands:")
    print(" - 帮我查一下深圳市政府关于政府补贴的最新政策")
    print(" - 翻译一下这段话：Hello World")
    print(" - 帮我给领导写一封关于海关新政的汇报邮件")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue

            print("Agent is thinking...")
            result = agent.run(user_input)
            
            print(f"\nAgent: {result['output']}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()