# backend/langchain_agent.py

from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from .calendar_utils import get_availability, book_event
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

tools = [
    Tool(name="CheckAvailability", func=get_availability, description="Check available time slots"),
    Tool(name="BookAppointment", func=book_event, description="Book appointment to calendar"),
]

agent = initialize_agent(tools, llm, agent="chat-conversational-react-description", verbose=True)

def run_agent(message):
    reply = agent.invoke({
        "input": message,
        "chat_history": []  # Empty list if you’re not using memory
    })
    return str(reply)



