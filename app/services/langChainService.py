import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages

from ..models import Pensamiento
from sqlmodel import select

load_dotenv()

class LangChainGemini:

    def getAllPensamientosByIDProfesor(self, profesor_id) -> list[Pensamiento]:
        return self.session.exec(select(Pensamiento).where(Pensamiento.profesor_id == profesor_id)).all()

    
    def getChatHistory(self, results) -> list[UserContent, ModelContent]:
        chat_history = []
        for row in results:
            if row.role == "user":
                chat_history.append(HumanMessage(content=row.content))
            elif row.role == "model":
                chat_history.append(AIMessage(cotent=row.content))
        return chat_history