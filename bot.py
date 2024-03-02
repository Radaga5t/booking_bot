from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from typing import Union
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler , filters
from telegram.ext import ConversationHandler
from dotenv import load_dotenv
from os import getenv
import requests
from models import db, User, Chat
from datetime import datetime
load_dotenv()
bot_token = getenv('TOKEN')

TITLE, DESCRIPTION, START_TIME, END_TIME = range(4)

async def start_create_event(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите название события:")
    return TITLE

async def event_title(update: Update, context: CallbackContext) -> int:
    title = update.message.text
    context.user_data['title'] = title
    await update.message.reply_text("Введите описание события:")
    return DESCRIPTION

async def event_description(update: Update, context: CallbackContext) -> int:
    description = update.message.text
    context.user_data['description'] = description
    await update.message.reply_text("Введите дату и время начала события в формате YYYY-MM-DD HH:MM:SS:")
    return START_TIME

async def event_start_time(update: Update, context: CallbackContext) -> int:
    start_time_str = update.message.text
    context.user_data['start_time'] = start_time_str
    await update.message.reply_text("Введите дату и время окончания события в формате YYYY-MM-DD HH:MM:SS:")
    return END_TIME

async def event_end_time(update: Update, context: CallbackContext) -> int:
    end_time_str = update.message.text
    context.user_data['end_time'] = end_time_str

    user_id = update.message.from_user.id

    end_time_str = update.message.text
    context.user_data['end_time'] = end_time_str

    title = context.user_data.get('title')
    description = context.user_data.get('description')
    start_time_str = context.user_data.get('start_time')
    end_time_str = context.user_data.get('end_time')

    start_time = datetime.fromisoformat(start_time_str) if start_time_str else datetime.utcnow()
    end_time = datetime.fromisoformat(end_time_str) if end_time_str else datetime.utcnow()



    url = "http://localhost:5000/events"
    data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 201:
            await update.message.reply_text("Событие успешно создано!")
    else:
        await update.message.reply_text(f"Ошибка при создании события. Код ошибки: {response.status_code}")

    context.user_data.clear()
    return ConversationHandler.END



async def events(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    response = requests.get(f'http://localhost:5000/events/{user_id}')
    response.raise_for_status()
    if response.status_code == 200:
        event_list = response.json()
        if event_list:
            for event_info in event_list:
                title = event_info.get('title')
                description = event_info.get('description')
                start_time = event_info.get('start_time')
                end_time = event_info.get('end_time')
                message_text = f' Название: {title}\nОписание: {description}\nНачало: {start_time}\nКонец: {end_time}'
                await update.message.reply_text(message_text)
        else:
            await update.message.reply_text("У вас пока нет событий.")
    else:
        await update.message.reply_text(f'Ошибка: {response.status_code}')

async def start(update: Update, context: CallbackContext) -> None:
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

def main() -> None:
    application = Application.builder().token(bot_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_event', start_create_event)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, event_title)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, event_description)],
            START_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, event_start_time)],
            END_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, event_end_time)],
        },
        fallbacks=[],
    )


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("events", events))
    application.add_handler(conv_handler)


    application.run_polling()

if __name__ == '__main__':
    main()