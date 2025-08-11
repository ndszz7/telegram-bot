import os
import requests

TOKEN = os.getenv("TOKEN", "SEU_TOKEN_AQUI")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://telegram-bot-3ao7.onrender.com")

def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(url)
    print("Resposta do Telegram:", response.json())

if __name__ == "__main__":
    set_webhook()