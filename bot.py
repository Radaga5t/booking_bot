
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from os import getenv
import requests
from models import db, User, Chat, Event

load_dotenv()
bot=getenv('TOKEN')

# Должен быть один обработчик всех сообщений
# в функции main должен вызываться этот обработчик
# сделай const в которой будет обработчик список всех команд
# убрать async и await


def start_create_event(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Для создания события введите данные в следующем формате:\n'
                              'Название мероприятия\n'
                              'Описание мероприятия\n'
                              'Начальное время мероприятия\n'
                              'Конечное время мероприятия')

# Обработчик ввода данных пользователя для создания события
def create_event(update: Update, context: CallbackContext) -> None:
    # Получаем id пользователя
    user_id = update.message.from_user.id
    # Получаем текст сообщения пользователя
    message_text = update.message.text
    # Разбиваем сообщение на отдельные строки
    event_data = message_text.split('\n')
    # Проверяем корректность формата ввода
    if len(event_data) != 5:
        update.message.reply_text('Некорректный формат. Пожалуйста, введите данные в указанном формате.')
        return

    # Извлекаем данные о событии
    title, description, start_time, end_time = event_data[1:]

    # Отправляем POST запрос на сервер для создания события
    try:
        response = requests.post('http://localhost:5000/events', json={
            'user_id': user_id,
            'title': title,
            'description': description,
            'start_time': start_time,
            'end_time': end_time
        })

        # Проверяем успешность создания события и отправляем ответ пользователю
        if response.status_code == 201:
            update.message.reply_text('Событие успешно создано!')
        else:
            update.message.reply_text(f'Ошибка при создании события: {response.status_code}')
    except Exception as e:
        update.message.reply_text(f'Произошла ошибка при отправке запроса на сервер: {e}')





async def events(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    response = requests.get(f'http://localhost:5000/events/{user_id}')
    response.raise_for_status()
    if response.status_code == 200:
        event_list = response.json()  # Предполагаем, что сервер возвращает список событий
        if event_list:
            for event_info in event_list:
                title = event_info.get('title')
                description = event_info.get('description')
                start_time = event_info.get('start_time')
                end_time = event_info.get('end_time')
                message_text = f'Название: {title}, Описание: {description}, Начало: {start_time}, Конец: {end_time}'
                await update.message.reply_text(message_text)
        else:
            await update.message.reply_text("У вас пока нет событий.")
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

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:

    application = Application.builder().token(bot).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("events", events))
    application.add_handler(CommandHandler("create_event", start_create_event))

    application.run_polling()

if __name__ == '__main__':
    main()
