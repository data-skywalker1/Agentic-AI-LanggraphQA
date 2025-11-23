import os
os.environ["LANGGRAPH_DISABLE_DAG_RENDER"] = "1"
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google import genai
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY_SELF") # or os.getenv("GEMINI_API_KEY")
if not api_key:
	raise EnvironmentError("GEMINI_API_KEY_SELF (or GEMINI_API_KEY) not set in environment. Add it to your .env or export it.")

model = ChatOpenAI(
   model="gemini-2.5-flash",
   api_key=api_key,
   base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages ]

def llm_chat(state: ChatState):

    msg= state['messages']

    response= model.invoke(msg)
    print(state)
    return {'messages': [response]}

## adding check pointer as memory saver type
checkpointer= InMemorySaver()
graph= StateGraph(ChatState)

graph.add_node('chatbot', llm_chat)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

chatbotnoob2= graph.compile(checkpointer = checkpointer)


