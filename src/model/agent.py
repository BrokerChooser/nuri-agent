# langchain packages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import  StateGraph, MessagesState

# Nuclia tools
from src.tools.tools import nuclia_search,broker_scam_check,get_forex_price


def create_agent():
    # Define the tools
    tools = [nuclia_search, broker_scam_check,get_forex_price]

    # Define the model
    model = ChatOpenAI(model="gpt-4")
    model_with_tools = model.bind_tools(tools)

    # Create workflow
    def agent(state: MessagesState):
        messages = state['messages']
        response = model_with_tools.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    # Define a new graph
    workflow = StateGraph(MessagesState)

    # Add Nodes
    workflow.add_node("agent", agent)
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)

    # Add Edges
    workflow.add_conditional_edges("agent",tools_condition)

    # Any time a tool is called, we return to the agent to decide the next step
    workflow.add_edge("tools", "agent")
    workflow.set_entry_point("agent")
    app = workflow.compile()

    return app
