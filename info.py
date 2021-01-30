from telegram.ext import CommandHandler


def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)


info_text = " "
with open('info_text', 'r', encoding='utf-8') as f:
    print("open file")
    info_text = f.read()
info_handler = CommandHandler("info", info)
