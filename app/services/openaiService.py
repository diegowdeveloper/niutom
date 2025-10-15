from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIService:

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def queryChatCompletions(self, user_message):

        try: 

            completion = await self.client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Eres un asistente virtual llamado Niutom dedicado al ámbito escolar de la Unidad Educativa Instituto San Antonio"},
                {"role": "assists", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
            )

            return completion.choices[0].message

        except Exception as e:
            return e
