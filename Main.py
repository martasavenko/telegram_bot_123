from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3

# Функция для подключения к базе данных и проверки слотов
def check_slot(day, time):
    conn = sqlite3.connect('test_schedule.db')
    c = conn.cursor()
    c.execute("SELECT * FROM schedule WHERE day = ? AND time = ?", (day, time))
    result = c.fetchone()
    conn.close()
    return result is None

# Функция для добавления записи
def book_slot(day, time, user):
    conn = sqlite3.connect('test_schedule.db')
    c = conn.cursor()
    c.execute("INSERT INTO schedule (day, time, user) VALUES (?, ?, ?)", (day, time, user))
    conn.commit()
    conn.close()

# Функция команды /start
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Привет, {user.first_name}! Выберите тип занятия:", reply_markup=ReplyKeyboardMarkup(
        [['Занятия в мини-группе', 'Индивидуальные занятия'], ['Разговорный клуб', 'Творческая мастерская']], one_time_keyboard=True))

# Обработчик выбора занятий
def handle_choice(update, context):
    user_choice = update.message.text
    user = update.message.from_user.username

    if user_choice == 'Занятия в мини-группе':
        update.message.reply_text('Вы выбрали занятия в мини-группе.')
        update.message.reply_text('Выберите день недели:', reply_markup=ReplyKeyboardMarkup(
            [['Понедельник', 'Вторник'], ['Четверг', 'Пятница'], ['Суббота', 'Воскресенье']], one_time_keyboard=True))

    elif user_choice == 'Понедельник':
        if check_slot('Понедельник', '14:00'):
            update.message.reply_text('Свободное время: 14:00', reply_markup=ReplyKeyboardMarkup(
                [['14:00', '14:30'], ['15:00', '15:30']], one_time_keyboard=True))
        else:
            update.message.reply_text('14:00 уже занято.')

    elif user_choice in ['14:00', '14:30', '15:00', '15:30']:
        update.message.reply_text(f"Вы выбрали {user_choice}. Пожалуйста, внесите оплату.")
        book_slot('Понедельник', user_choice, user)

# Запуск бота
def main():
    updater = Updater("7517614723:AAFzOSWUuRWZc8HxI74xI2tyoEjPyqca43A", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_choice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
