import os
import re
import sqlite3
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from dotenv import load_dotenv

from create_and_write_db import create_db, write_message_to_db, DATABASE
from write_to_file import write

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
updater = Updater(token=TOKEN)


def monitors_messages(update, context):
    """Мониторим сообщения и готовим для записи в БД"""
    chat_id = "tab"+str(update.effective_chat.id)[1:]+".sqlite3"
    create_db(chat_id)
    user_message = []
    message = update.message.text
    date = update.message.date
    data = (
        update.message.from_user.username,
        message,
        f"{date.strftime('%Y.%m.%d %H:%M:%S')}"
    )
    user_message.append(data)
    if re.search(r"https:\/\/kaiten.x5.ru\/[\d+]{7}", message):
        kaiten = "kaiten_tasks"
        write_message_to_db(user_message, chat_id, kaiten)
    else:
        write_message_to_db(user_message, chat_id)


def stats(update, context):
    """Готовим и отправляем стату в чат"""
    chat = update.effective_chat
    chat_for_db = "tab"+str(update.effective_chat.id)[1:]+".sqlite3"
    con = sqlite3.connect(f"{DATABASE}{chat_for_db}")
    cur = con.cursor()
    try:
        request = cur.execute(
            """
            SELECT username, COUNT(*)
            FROM user_messages
            GROUP BY username
            """
        )
    except sqlite3.OperationalError:
        context.bot.send_message(
            chat_id=chat.id,
            text="Нет данных для отображения"
        )
    else:
        output_lst = []

        for res in request:
            output_lst.append(f"{res[0]} sent {res[1]} messages")

        output = "\n".join(output_lst)
        context.bot.send_message(chat_id=chat.id, text=output)


def export(update, context):
    chat = update.effective_chat.id
    chat_for_db = "tab"+str(chat)[1:]+".sqlite3"
    con = sqlite3.connect(f"{DATABASE}{chat_for_db}")
    cur = con.cursor()
    try:
        request = cur.execute(
            """
            SELECT *
            FROM kaiten_tasks
            """
        )
    except sqlite3.OperationalError:
        context.bot.send_message(
            chat_id=chat.id,
            text="Нет данных для отображения"
        )
    else:
        write(request)
        context.bot.send_document(
            chat_id=chat,
            document=open("output/tasks_kaiten.csv")
        )


def hello(update, context):
    """Приветствие бота"""
    chat = update.effective_chat
    output = f"Привет {update.message.from_user.username}, я ботяра ботетский, я незаметно слежу за всеми сообщениями в чате и сохраняю, что бы потом когда ты попросишь выдать кол-во. Для выдачи используй команды /stat и /export"
    context.bot.send_message(chat_id=chat.id, text=output)


def main():
    updater.dispatcher.add_handler(CommandHandler('start', hello))
    updater.dispatcher.add_handler(
        CommandHandler('stat', stats))
    updater.dispatcher.add_handler(
        CommandHandler('export', export)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, monitors_messages)
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
