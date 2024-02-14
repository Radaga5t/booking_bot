from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler , filters
from dotenv import load_dotenv
from os import getenv
import requests
from models import db, User, Chat

load_dotenv()
bot_token = getenv('TOKEN')


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = User.query.filter_by(user_id=user_id).first()
    
    if not user:
        user = User(id=user_id)
        db.session.add(user)
        db.session.commit()


async def handle_chat_join(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    
    new_chat = Chat(id=chat_id)
    db.session.add(new_chat)
    db.session.commit()

#test
async def users(update: Update, context: CallbackContext) -> None:
    response = requests.get('http://localhost:5000/users')
    response.raise_for_status()
    if response.status_code == 200:
        user_list = response.json().get('users', [])
        for user_info in user_list:
            user_id = user_info.get('id')
            username = user_info.get('username')
            is_admin = user_info.get('is_admin')
            message_text = f'User ID: {user_id}, Имя: {username}, Admin: {is_admin}'
            await update.message.reply_text(message_text)
    else:
        await update.message.reply_text(f'Ошибка: {response.status_code}')

#Доработать сортировку эвентов
async def events(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    response = requests.get(f'http://localhost:5000/events/?user_id={user_id}',)
    response.raise_for_status()
    if response.status_code == 200:
        event_list = response.json().get('events', [])
        for event_info in event_list:
            title = event_info.get('title')
            description = event_info.get('description')
            start_time = event_info.get('start_time')
            end_time = event_info.get('end_time')
            message_text = f'Название: {title}, Описание: {description}, Начало: {start_time}, Конец: {end_time}'
            await update.message.reply_text(message_text)
    else:
        await update.message.reply_text(f'Ошибка: {response.status_code}')

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Информация о пользователе", callback_data='user'),
            InlineKeyboardButton("Мероприятия", callback_data='events'),
        ],
        [
            InlineKeyboardButton("Создать мероприятие", callback_data='create'),
            InlineKeyboardButton("Детали конкретного мероприятия", callback_data='idevents'),
        ],
        [
            InlineKeyboardButton("Обновить мероприятие", callback_data='update'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите команду:', reply_markup=reply_markup)

async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    if data == 'user':
        await users(update, context)
    elif data == 'events':
        await events(update, context)
    # Добавьте обработку других кнопок

def main() -> None:
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users))
    application.add_handler(CommandHandler("events", events))


    # Добавление обработчика для кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    #application.add_handler(MessageHandler(filters.StatusUpdate._NewChatMembers, handle_chat_join))


    application.run_polling()

if __name__ == '__main__':
    main()