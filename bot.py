from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from os import getenv
from server import get_users

load_dotenv()
bot=getenv('TOKEN')
bot1='6735056096:AAEnBYpWkWrl03WFV-AfdISjgE4bVXLHWL4'

async def users(update: Update, context: CallbackContext) -> None:

    list_users=get_users()
    print(list_users)
    await update.message.reply_text(list_users)

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Информация о пользователе", callback_data='user'),
            InlineKeyboardButton("Мероприятия", callback_data='events'),
        ],
        [
            InlineKeyboardButton("Создать ивент", callback_data='create'),
            InlineKeyboardButton("Детали конкретного ивента", callback_data='idevents'),
        ],
        [
            InlineKeyboardButton("Обновить ивент", callback_data='update'),
            InlineKeyboardButton("Какие чаты", callback_data='chats'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите команду:', reply_markup=reply_markup)


async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:

    application = Application.builder().token(bot1).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users))
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()