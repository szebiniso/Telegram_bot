import os
import json
import telebot

TOKEN = '1391407864:AAHcdAjngbEIIagrwD93gqhZ2vx5Zexvzu4'


bot = telebot.TeleBot(TOKEN)


def read_from_file():
    with open('data.json', 'r') as f:
        json_data = json.load(f)
        return json_data


def write_to_file(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)
if not os.path.exists('data.json'):
    write_to_file({})

keyboard = telebot.types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True)
show_task_btn = telebot.types.KeyboardButton(text='View to-do list')
add_task_btn = telebot.types.KeyboardButton(text='Add new task')
clean_tasks_btn = telebot.types.KeyboardButton(text='Clear to-do list')
keyboard.add(show_task_btn, add_task_btn, clean_tasks_btn)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hey, there', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handle_button(message):
    if message.text == show_task_btn.text:
        data = read_from_file()
        todo_list = data.get(str(message.chat.id))
        if not len(todo_list):
            bot.send_message(
                message.chat.id, "You haven't added any tasks",
                reply_markup=keyboard)
            return
        to_dos = 'Your to-do list: \n'
        for i, value in enumerate(todo_list, start=1):
            to_dos += f'{i}: {value}\n'
        bot.send_message(message.chat.id, to_dos)
        action_keyboard = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True)
        edit_btn = telebot.types.KeyboardButton(text='Edit task')
        delete_btn = telebot.types.KeyboardButton(text='')
        cancel_btn = telebot.types.KeyboardButton(text='Exit to the main menu')
        action_keyboard.add(edit_btn, delete_btn, cancel_btn)
        bot.send_message(
            message.chat.id, 'Select an action',
            reply_markup=action_keyboard)
    if message.text == 'Edit task':
        bot.send_message(message.chat.id, 'Enter the task number to edit')
        bot.register_next_step_handler(message, edit_task)
    if message.text == 'Delete task':
        bot.send_message(message.chat.id, 'Enter the task number to delete')
        bot.register_next_step_handler(message, delete_task)

    if message.text == 'Exit to the main menu':
        bot.send_message(
            message.chat.id, 'You have returned to the main menu',
            reply_markup=keyboard)

    if message.text == add_task_btn.text:
        bot.send_message(
            message.chat.id, 'Enter the text of the task you want to add')
        bot.register_next_step_handler(message, add_task)

    if message.text == clean_tasks_btn.text:
        data = read_from_file()
        data[message.chat.id] = []
        write_to_file(data)
        bot.send_message(
            message.chat.id, 'Task list cleared',
            reply_markup=keyboard)


def edit_task(message):
    data = read_from_file()
    user_to_dos = data.get(str(message.chat.id), [])
    try:
        task_number = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Enter the task number')
        return
    if task_number not in range(1, len(user_to_dos) + 1):
        bot.send_message(message.chat.id, 'There is no task with this number')
        return

    def edit(message):
        user_to_dos[task_number - 1] = message.text
        data[message.chat.id] = user_to_dos
        write_to_file(data)
        bot.send_message(message.chat.id, 'All saved', reply_markup=keyboard)

    bot.send_message(message.chat.id, 'Enter new task text')
    bot.register_next_step_handler(message, edit)


def delete_task(message):
    data = read_from_file()
    user_to_dos = data.get(str(message.chat.id), [])
    try:
        task_number = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Enter the task number')
        return

    if task_number not in range(1, len(user_to_dos) + 1):
        bot.send_message(message.chat.id, 'There is no task with this number')
        return
    del user_to_dos[task_number - 1]
    data[message.chat.id] = user_to_dos
    write_to_file(data)
    bot.send_message(
        message.chat.id, 'Task successfully removed from the list',
        reply_markup=keyboard)


def add_task(message):
    data = read_from_file()
    user_to_dos = data.get(str(message.chat.id), [])
    user_to_dos.append(message.text)
    data[message.chat.id] = user_to_dos
    write_to_file(data)
    bot.send_message(message.chat.id, 'Task added', reply_markup=keyboard)
bot.polling()
