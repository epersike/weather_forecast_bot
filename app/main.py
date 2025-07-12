import sys
from bot import start as start_bot
from llm import test as test_llm

args = {
    "bot.start": start_bot,
    "llm.test": test_llm
}

def help():
    print("""
        Welcome to the weatherbot project.
        Available commmands:
          
          1 - bot.start  - Start the Discord bot.
          2 - llm.test   - Run the LLM pipeline test.
    """)

if __name__ == "__main__":
    if "help" in sys.argv \
            or len(sys.argv) < 1 \
            or sys.argv[-1] not in args:
        print(help())
        sys.exit(0)
    
    if sys.argv[1] in args:
        args[sys.argv[-1]]()