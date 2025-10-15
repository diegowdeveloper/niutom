import os
from fastapi import APIRouter
from dotenv import load_dotenv
import httpx

load_dotenv()
HTTP_CLIENT = httpx.AsyncClient()

class WhatsAppService:

    @staticmethod
    async def sendWhatsappMessage(to: str, text_body: str, context_message_id: str = None):
        """
        Envía una respuesta de texto a un usuario de WhatsApp.
        """
        headers = {
            "Authorization": f"Bearer {os.getenv("API_TOKEN")}",
            "Content-Type": "application/json",
        }

        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "text": {
                "body": text_body
            }
        }

        if context_message_id:
            # Esto hace que el mensaje de respuesta aparezca como una respuesta al original
            data["context"] = {"message_id": context_message_id}

        try:
            response = await HTTP_CLIENT.post(f"{os.getenv("API_URL")}/{os.getenv("API_VERSION")}/{os.getenv("BUSINESS_PHONE")}/messages", headers=headers, json=data)
            response.raise_for_status() # Lanza una excepción para códigos de estado 4xx/5xx
            print("Mensaje de respuesta enviado con éxito.")
        except httpx.HTTPStatusError as e:
            print(f"Error al enviar el mensaje de WhatsApp: {e.response.text}")
        except Exception as e:
            print(f"Error de conexión al enviar el mensaje: {e}")


    @staticmethod
    async def markMessageAsRead(message_id: str):
        """
        Marca un mensaje entrante como leído en WhatsApp.
        """
        headers = {
            "Authorization": f"Bearer {os.getenv("API_TOKEN")}",
            "Content-Type": "application/json",
        }
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        try:
            response = await HTTP_CLIENT.post(f"{os.getenv("API_URL")}/{os.getenv("API_VERSION")}/{os.getenv("BUSINESS_PHONE")}/messages", headers=headers, json=data)
            response.raise_for_status()
            print(f"Mensaje {message_id} marcado como leído.")
        except httpx.HTTPStatusError as e:
            print(f"Error al marcar como leído: {e.response.text}")

    
    @staticmethod
    async def sendInteractiveButtons(to, body_text, buttons):

        headers = {
            "Authorization": f"Bearer {os.getenv("API_TOKEN")}",
            "Content-Type": "application/json",
        }

        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body_text
                },
                "action": {
                    "buttons": buttons
                }
            }
        }

        try:
            response = await HTTP_CLIENT.post(f"{os.getenv("API_URL")}/{os.getenv("API_VERSION")}/{os.getenv("BUSINESS_PHONE")}/messages", headers=headers, json=data)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Error al enviar el mensaje de WhatsApp: {e.response.text}")
        except Exception as e:
            print(f"Error de conexión al enviar el mensaje: {e}")


    @staticmethod
    async def sendMediaMessage(to: str, type: str, media_url: str, caption: str = None):
        try:
            pass
        except Exception as e:
            print(e)