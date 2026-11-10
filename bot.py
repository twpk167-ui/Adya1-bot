"""
Adya - Human-like Telegram Bot (Main File)
Run: python bot.py
Pehle .env file me BOT_TOKEN daalna hai.
"""

import asyncio
import logging
import os
import random
import time

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from brain import get_reply, split_messages, typing_delay, humanize

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("adya-bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Typing indicator - human jaisa lagta hai
    await update.message.reply_chat_action(ChatAction.TYPING)
    await asyncio.sleep(random.uniform(0.8, 1.5))
    await update.message.reply_text(
        humanize(
            f"heyy {user.first_name or ''}! 😊 mai Adya hu, "
            "Btech kar rahi hu Noida se. tumse baat karke accha lagega. "
            "bas aise hi bolo, jaise dost se baat karte ho."
        )
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "koi command ki tension nahi 😄 bas bolo:\n"
        "• hi / kaise ho\n"
        "• bore ho raha hu\n"
        "• joke sunao\n"
        "• tum kahan se ho\n"
        "• exam ka tension hai\n"
        "jaise dost se baat karte ho, waise hi bolo, mai samajh jaungi 💛"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text

    # 1. Typing... dikhao (human behavior)
    await update.message.reply_chat_action(ChatAction.TYPING)

    # 2. Reply banao
    reply = get_reply(user_id, text)
    parts = split_messages(reply)

    # 3. Typing delay ke baad pehla message
    await asyncio.sleep(typing_delay(parts[0]))
    await update.message.reply_text(parts[0])

    # 4. Kabhi-kabhi dusra chhota message (double texting)
    if len(parts) > 1:
        await update.message.reply_chat_action(ChatAction.TYPING)
        await asyncio.sleep(random.uniform(0.7, 1.4))
        await update.message.reply_text(parts[1])


def main():
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "yahan_apna_token_daalo":
        print("=" * 50)
        print("BOT_TOKEN nahi mila!")
        print("Steps:")
        print("1. Telegram par @BotFather kholo")
        print("2. /newbot likho, bot ka naam 'Adya' aur username do")
        print("3. Jo token milega, usko .env file me daalo:")
        print("   BOT_TOKEN=123456:ABC-DEF...")
        print("4. Fir dobara 'python bot.py' run karo")
        print("=" * 50)
        print("\nDemo mode me brain test karne ke liye: python brain.py")
        return

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Adya bot online hai! 💛 Telegram par /start karo.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
