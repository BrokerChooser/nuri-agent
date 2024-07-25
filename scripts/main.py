from src.model.agent import create_agent
from dotenv import load_dotenv

def main():

    load_dotenv() # load environment variables
    app=create_agent()
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        events=app.stream({"messages": ("user", user_input)},stream_mode='values')
        for event in events:
            event["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()