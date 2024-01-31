from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from os import getenv
load_dotenv()
bot=getenv('TOKEN')

# Должен быть один обработчик всех сообщений
# в функции main должен вызываться этот обработчик
# сделай const в которой будет обработчик список всех команд
# убрать async и await

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Привет, {user.first_name or user.username}, я ваш телеграм бот!")

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Справка: Используйте эти команды...')

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:

    application = Application.builder().token(bot).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()