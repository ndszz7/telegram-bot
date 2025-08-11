import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://seu-bot.onrender.com")
TOKEN = os.getenv("TOKEN", "SEU_TOKEN_AQUI")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_username = context.bot.username
    await update.message.reply_text(f"Olá, {user.first_name}! Eu sou @{bot_username}, pronto para baixar TikToks para você. Envie o link!")

async def download_tiktok(url):
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'mp4',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    filename = ydl.prepare_filename(info)
    return filename

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "tiktok.com" in text:
        await update.message.reply_text("Baixando seu vídeo, aguarde...")
        try:
            filepath = await download_tiktok(text)
            await update.message.reply_video(open(filepath, "rb"),
                                            caption=f"Vídeo baixado para você, {update.effective_user.first_name}!
@{context.bot.username}")
            os.remove(filepath)
        except Exception as e:
            await update.message.reply_text("Erro ao baixar o vídeo. Verifique o link ou os cookies.")
    else:
        await update.message.reply_text("Envie um link válido do TikTok.")

def main():
    import asyncio
    from telegram.ext import Application

    app = ApplicationBuilder().token(TOKEN).webhook(url=WEBHOOK_URL).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot iniciado!")
    app.run_webhook(listen="0.0.0.0",
                    port=8443,
                    webhook_url=WEBHOOK_URL)

if __name__ == "__main__":
    main()