from .whatsAppService import WhatsAppService
from fastapi import Response

class MessageHandler:

    def __init__(self, message, sender_info):
        self.message      = message
        self.sender_info  = sender_info
        self.message_from = message.get("from")
        self.message_body = message["text"]["body"]
        self.message_id   = message.get("id")


    async def handleIncomingMessage(self):
        
        if self.message and self.message.get("type") == "text":

            await WhatsAppService.markMessageAsRead(self.message_id)

            try:
                if "hola" in self.message_body.lower().strip() and len(self.message_body.lower().strip()) <= 12:
                    await self.sendWelcomeMessage()
                    await self.sendWelcomeMenu()
                else: 
                    await self.sendMessageAgent()

            except Exception as e:
                print(e)

        elif self.message.get("type") == "interactive":

            option_id = self.message.get("interactive", {}).get("button_reply", {}).get("id")

            try:
                await WhatsAppService.markMessageAsRead(self.message_id)
                await self.handleMenuOption(option_id)
            except Exception as e:
                print(e)

        return Response(status_code=200)
    

    async def sendWelcomeMessage(self):

        name_user = self.getSenderName()
        message = f"*¡Hola {name_user}!* Un gusto en saludar, ¿Qué te gustaría hacer?"
        await WhatsAppService.sendWhatsappMessage(self.message_from, message, self.message.get("id"))

    
    async def sendMessageAgent(self, message):
        await WhatsAppService.sendWhatsappMessage(self.message_from, message, self.message.get("id"))


    async def sendWelcomeMenu(self):

        menu_message = "Por favor elije una opción:"
        buttons = [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "niutom_basico",
                                "title": "Niutom básico"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "niutom_avanzado",
                                "title": "Niutom avanzado"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "niutom_info",
                                "title": "¿Qué es Niutom?"
                            }
                        }
                    ]

        await WhatsAppService.sendInteractiveButtons(self.message_from, menu_message, buttons)


    async def handleMenuOption(self, option_id):

        message_reply = "Disculpa, no he entendido tu respuesta"

        if option_id == 'niutom_basico':
            message_reply = "Desplegar bot básico con Open AI"
        elif option_id == 'niutom_avanzado':
            message_reply = "Desplegar bot avanzado con Azure"
        elif option_id == 'niutom_avanzado':
            message_reply = "Niutom es Agente Inteligente híbrido, entrenado con documentación de la escuela y sostenido con un modelo LLM para ayudar a los docentes a asistir en sus labores diarias"

        await WhatsAppService.sendWhatsappMessage(self.message_from, message_reply)

    def getSenderName(self):
        return self.sender_info.get("profile", {})["name"].split(" ")[0] or self.sender_info.get("wa_id") or ""

