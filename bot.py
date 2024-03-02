from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
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

SELECT_EVENT, SELECT_ATTRIBUTE, ENTER_NEW_VALUE = range(3)

async def start_update_event(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    response = requests.get(f'http://localhost:5000/events/{user_id}')

    if response.status_code == 200:
        events_list = response.json()

        if events_list:
            keyboard = []
            for event in events_list:
                keyboard.append([event['title']])
            keyboard.append(['Отмена'])

            await update.message.reply_text("Выберите мероприятие, которое вы хотите обновить:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return SELECT_EVENT

async def select_event(update: Update, context: CallbackContext) -> int:
    selected_event_title = update.message.text  # Сохраняем название события

    # Найдем ID выбранного события по его названию
    user_id = update.message.from_user.id
    response = requests.get(f'http://localhost:5000/events/{user_id}')
    if response.status_code == 200:
        events_list = response.json()
        for event in events_list:
            if event['title'] == selected_event_title:
                context.user_data['selected_event_id'] = event['id']  # Сохраняем ID события
                break

    keyboard = [['title', 'description'], ['start_time', 'end_time'], ['Отмена']]
    await update.message.reply_text("Выберите параметр для изменения:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return SELECT_ATTRIBUTE

async def select_attribute(update: Update, context: CallbackContext) -> int:
    context.user_data['selected_attribute'] = update.message.text.lower()
    await update.message.reply_text(f"Введите новое значение для {context.user_data['selected_attribute']}:")
    return ENTER_NEW_VALUE

async def enter_new_value(update: Update, context: CallbackContext) -> int:
    new_value = update.message.text
    user_id = update.message.from_user.id
    event_id = context.user_data['selected_event_id']  # Получаем ID выбранного события из user_data
    attribute = context.user_data['selected_attribute']

    try:
        response = requests.patch(f'http://localhost:5000/events/{event_id}', json={attribute: new_value})

        if response.status_code == 200:
            await update.message.reply_text(f"{attribute.capitalize()} успешно обновлено.")
        else:
            await update.message.reply_text("Произошла ошибка при обновлении. Код ошибки: " + str(response.status_code)) # 404
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обновлении: " + str(e)) #500

    context.user_data.clear()
    return ConversationHandler.END









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

   # Добавляем обработчики команд для обновления событий
    conv_handler_update_event = ConversationHandler(
        entry_points=[CommandHandler('update_events', start_update_event)],
        states={
            SELECT_EVENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_event)],
            SELECT_ATTRIBUTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_attribute)],
            ENTER_NEW_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_new_value)],
        },
        fallbacks=[],
    )


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("events", events))
    application.add_handler(conv_handler)
    application.add_handler(conv_handler_update_event)


    application.run_polling()

if __name__ == '__main__':
    main()