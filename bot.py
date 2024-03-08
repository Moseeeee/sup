import telebot
from telebot import types
import time 
import re
import requests
from datetime import datetime, timedelta
import sqlite3 
from bs4 import BeautifulSoup
import wikipediaapi
import json
import os
import random
from functools import wraps
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import subprocess
from datetime import date
from textblob import TextBlob
from telebot import TeleBot
from telebot.types import Message
import logging
from tinydb import TinyDB, Query
import schedule
import threading
from collections import deque
from telebot.types import BotCommand, BotCommandScopeChat
import sys





API_TOKEN = '6438279714:AAGH7A6JoEtefmJNYgUBPryUzPYPTuqU0Fs'
bot = telebot.TeleBot(API_TOKEN)


errors_chat_id = '-1002125356812'  # ID чата для отправки уведомлений об ошибках

def error_handler(exception_type, exception, traceback):
    chat_member_info = bot.get_chat_member(errors_chat_id, bot.get_me().id)
    bot_username = chat_member_info.user.username if chat_member_info.user.username else 'Бот'
    error_message = f"Произошла ошибка:\n{exception_type.name}: {exception}"
    bot.send_message(errors_chat_id, error_message)

sys.excepthook = error_handler



#Чат для общения


commands_chat1 = [
    BotCommand('report', '🚫 Пожаловаться на пользователя'),
    BotCommand('commands', '📖 Команды'),
    BotCommand('rules', '📝 Правила чата'),
    BotCommand('grid', '🗂️ Чаты сетки')
]
scope_chat1 = BotCommandScopeChat(chat_id=-1002011140937)
bot.set_my_commands(commands_chat1, scope=scope_chat1)

commands_chat2 = [
    BotCommand('commands', '📖 Команды'),
    BotCommand('rules', '📝 Правила чата'),
    BotCommand('grid', '🗂️ Чаты сетки'),
    BotCommand('addhelper', '✅ Добавиться в список админов'),
    BotCommand('unhelper', '❌ Удалиться из списка админов'),
    BotCommand('admncommands', '📝 Список админских команд')
]
scope_chat2 = BotCommandScopeChat(chat_id=-1002129257694)
bot.set_my_commands(commands_chat2, scope=scope_chat2)    

#чат для тест драйва
commands = [BotCommand('report', '🚫пожаловаться на пользователя'), BotCommand('commands', '📖команды'), BotCommand ('rules', '📝правила чата'), BotCommand ('grid', '🗂️чаты сетки'), BotCommand ('addcomands', '📝команды для админов')]
scope = BotCommandScopeChat(chat_id=-1001940482569)
bot.set_my_commands(commands, scope=scope)  
      
         
               
# Старт
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        welcome_message = (
            f"👋Здравствуйте, [{message.from_user.first_name}](tg://user?id={user_id}).\n"
            "🤖Я бот помощник для сетки чатов «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ».\n"
            "💡Если у вас есть идеи для бота, напишите [в этот чат](https://t.me/+LDPqIG1XW7dkNzgy)"
        )

        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Команды", url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button)

        bot.send_message(message.chat.id, welcome_message, parse_mode='Markdown', reply_markup=keyboard)




        
        
        







@bot.message_handler(func=lambda message: message.text.strip().lower() in ['команды', 'сап команды', '.команды', '!команды', '/commands@sapcmbot', '/commands', '/команды'])
def handle_help(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if user_id in admin_ids:
            admin_name = message.from_user.first_name
            admin_greeting = "💡Мой список админских команд доступен ниже.\n🚫Разглашение админских команд запрещено\n❗️Караеться снятием и удалением"

            admin_keyboard = types.InlineKeyboardMarkup()
            admin_url_button = types.InlineKeyboardButton(text="Админские команды", url="https://teletype.in/@drmotory/98olfMhylw5")
            user_url_button = types.InlineKeyboardButton(text="Обычные команды", url="https://teletype.in/@drmotory/commands_support")
            admin_keyboard.add(admin_url_button, user_url_button)

            bot.send_message(message.chat.id, admin_greeting, parse_mode='Markdown', reply_markup=admin_keyboard)
        else:
            welcome_message = (
                "Мой список команд доступен ниже\n"
                "💡Если у вас есть идеи для бота, напишите [создателю](https://t.me/ww0qn) бота."
            )

            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Команды", url="https://teletype.in/@drmotory/commands_support")
            keyboard.add(url_button)

            bot.send_message(message.chat.id, welcome_message, parse_mode='Markdown', reply_markup=keyboard)
    else:
        welcome_message = "Мой список команд доступен ниже"
        
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Команды", url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button)
        
        bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)





        
                
                        
                                
                                        
                                                
                                                                

          
                
                        

                                        
                                                
                                                        
                                                                
                                                                        
                                                                                
                                                                                                
        
        
        
        
        

#приветствие новичков
@bot.message_handler(func=lambda message: message.text.strip().lower() in ['адм команды', '.адм команды', '/admncommands@sapcmbot'])
def send_rules(message):
    rules_message = "[Админские команды](https://teletype.in/@drmotory/98olfMhylw5)\nНезабывайте искать участников😉"
    bot.reply_to(message, rules_message, parse_mode="Markdown") 

        
        
        
                
        
        
        
        
        
#правила
allowed_users = ['6282374712'] 

helpers = {}


default_message = "😕Админы холтурщики, напишите глав. админам об этом.\n"

# Функция отправки правил
@bot.message_handler(func=lambda message: message.text.strip().lower() in ['правила', 'сап правила', '.правила', '!правила', '/rules@sapcmbot', '/rules', '/правила'])
def send_rules(message):
    rules_message = "[Правила чата](https://teletype.in/@drmotory/psc)\n\n"\
                    "Если у вас появятся вопросы, пишите админам:\n"

    if not helpers:  
        rules_message += default_message
    else:
        for user_id, user_link in helpers.items():
            user_info = bot.get_chat_member(message.chat.id, user_id)
            user_name = user_info.user.first_name
            user_link = user_info.user.id
            rules_message += f"[{user_name}](tg://openmessage?user_id={user_link})\n"
    rules_message += "❗️В случае если админов нет рядом отправьте [репорт](https://teletype.in/@drmotory/commands_support#G56k)."
    bot.reply_to(message, rules_message, parse_mode="Markdown")
    
@bot.message_handler(func=lambda message: message.text.strip().lower() in ['+хелп','/addhelper@sapcmbot'])
def add_helper(message):
    user_id = message.from_user.id
    user_info = bot.get_chat_member(message.chat.id, user_id)
    user_name = user_info.user.first_name
    user_link = user_info.user.id
    helpers[user_id] = f"[{user_name}](tg://openmessage?user_id={user_link})"
    bot.reply_to(message, "Вы были добавлены в список помощников.")

# Обработчик команды -помощь
@bot.message_handler(func=lambda message: message.text.strip().lower() in ['-хелп','/unhelper@sapcmbot'])
def remove_helper(message):
    user_id = message.from_user.id
    if user_id in helpers:
        del helpers[user_id]
        bot.reply_to(message, "Вы были удалены из списка помощников.")
    else:
        bot.reply_to(message, "Вы не были добавлены в список помощников.")


# Обработчик команды !отозвать из помощи @username
@bot.message_handler(func=lambda message: message.text.startswith('!отозвать из помощи'))
def remove_specific_helper(message):
   if str(message.from_user.id) in allowed_users:    
    to_remove = message.text.split('@')[-1].strip()
    for user_id, user_link in helpers.items():
        if to_remove in user_link:
            del helpers[user_id]
            bot.reply_to(message, f"Пользователь {to_remove} был удален из списка помощников.")
            return
    
    bot.reply_to(message, f"Пользователь {to_remove} не найден в списке помощников.")

    
    
    
    
    
    
    
    
    
    #как влиться в колектив
@bot.message_handler(func=lambda message: message.text.strip().lower() == '.кк')
def send_rules(message):
    rules_message = "[Как влиться в колектив?](https://teletype.in/@drmotory/chatrules)\nудачного общения ребята🧸"
    bot.reply_to(message, rules_message, parse_mode="Markdown")    
    
    
    
    
    
    
    
    

#чат 1 закреп
allowed_users = ['6282374712']

@bot.message_handler(func=lambda message: message.text.strip().lower() == '!дорпин')
def send_and_pin_messages(message):
   if str(message.from_user.id) in allowed_users:
    messages_to_send = [
        "[👋](https://teletype.in/@drmotory/collective-2)Добро пожаловать в «[🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чат для общения](https://t.me/drmitory)».\nЗдесь ты можешь найти себе новых знакомых, друзей и может даже пару!\n\nОчень надеемся что вам у нас понравится. Если хотите влиться в коллектив то не надо молчать, а нужно писать и общаться с участниками чата.\n\n[🫂 Как влиться в коллектив](https://teletype.in/@drmotory/collective-2)\n\nℹ️ Мы хотим создать приятную атмосферу в чате. Если вас человек попросил не тегать / отвечать ему на сообщения, то не стоит этого делать, ведь за это вам выдадут мут.\n\nВсе наши чаты:\n[🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чат для общения](https://t.me/drmotory)\n[🎮ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | Игры](https://t.me/drmitory_play)\n\nПеред тем как начать общение ознакомьтесь с правилами чата.\nПравила чатов сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ»🔽",
        "[Правила сетки чатов «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ»](https://teletype.in/@drmotory/psc)\n[Правила голосового чата](https://teletype.in/@drmotory/chatrules#Cgz9)\n❗ Админы и модеры вправе выдать те наказания, которые посчитают нужным.",
        "Если вы заметили проблемы с поведением других участников или возникли технические трудности, обратитесь к модераторам или администраторам чата для решения проблемы.\n\nПриятного общения 🌺"
    ]
    
    sent_messages = []  
    for text in messages_to_send:
        sent_message = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        sent_messages.append(sent_message)

    
    bot.pin_chat_message(message.chat.id, sent_messages[0].message_id)







@bot.message_handler(func=lambda message: message.text.strip().lower() == '!плпин')
def send_and_pin_messages(message):
   if str(message.from_user.id) in allowed_users:
    messages_to_send = [
        "[👋](https://teletype.in/@drmotory/chatrules)Добро пожаловать в «[🎮ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | Игры](https://t.me/drmitory_play)»\nЗдесь ты можешь поиграть в игры,при этом не засоряя основной чат.\n\nМы собрали часто используемых ботов для игр,и готовы дать вам сыграть во многие игры!\nЕсли есть предложения то отметьте кого из админов и напишите имя бота и что он делает,а там админы решат,добавлять или нет.\n\nосновной чат для [общения](https://t.me/drmitory),где можно пообщаться без игровых ботов.\n‼️Перед тем как начать общаться,прочитайте [правила сетки.](https://teletype.in/@drmotory/psc)\n[🫂Гайд как влиться в коллектив](https://teletype.in/@drmotory/collective-2)\n\nВсе наши чаты:\n[🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чат для общения](https://t.me/drmitory)\n[🎮ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | Игры](https://t.me/drmitory_play)",
        "Если вы заметили проблемы с поведением других участников или возникли технические трудности, обратитесь к модераторам или администраторам чата для решения проблемы.\n\nПриятных игр🌺"
    ]
    
    sent_messages = []  
    for text in messages_to_send:
        sent_message = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        sent_messages.append(sent_message)

    
    bot.pin_chat_message(message.chat.id, sent_messages[0].message_id)










    

    
    
    


# РЕПОРТЫ
ADMIN_CHATS = [-1002129257694]

MUTE_DURATION = 3600 

user_reports = {}

@bot.message_handler(func=lambda message: message.text.strip().lower() in ['репорт', 'сап репорт', '.репорт', '!репорт', '/report@sapcmbot', '/report', '.жалоба'])
def handle_report(message):
    user_id = message.from_user.id
    current_time = time.time()

    replied_message = message.reply_to_message
    if replied_message:
        report_reason = ' '.join(message.text.split()[1:]) if len(message.text.split()) > 1 else ''
        
        report_content = get_report_content(replied_message)  
        reported_user_link = f"[{replied_message.from_user.first_name}](https://t.me/{replied_message.from_user.username}) ({replied_message.from_user.id})"
        report_text = f'🛑Новая жалоба\n📝Текст: {report_content}\n🗣Отправитель жалобы: [{message.from_user.first_name}](https://t.me/{message.from_user.username}) ({message.from_user.id})\n👤Жалоба кинули на: {reported_user_link}'
        inline_keyboard = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton(text="Удалить сообщение", callback_data=f"delete_report_{replied_message.message_id}")
        goto_button = types.InlineKeyboardButton(text="Перейти к сообщению", url=f"https://t.me/{replied_message.chat.username}/{replied_message.message_id}")
        inline_keyboard.row(goto_button, delete_button)

        for admin_chat_id in ADMIN_CHATS:
            sent_message = bot.send_message(admin_chat_id, report_text, parse_mode="Markdown", reply_markup=inline_keyboard)
            if replied_message:
                bot.reply_to(message, f'✅ Жалоба отправлена администраторам.')
                
    if user_id in user_reports:
        reports, last_check_time = user_reports[user_id]
        if current_time - last_check_time < 60:  
            reports += 1
            if reports >= 5:
                bot.restrict_chat_member(message.chat.id, user_id, until_date=int(current_time + MUTE_DURATION))  
                bot.send_message(message.chat.id, f"Пользователь @{message.from_user.username} замучен на 1 час за частые репорты.")
                reports = 0  
        else:
            reports = 1

        user_reports[user_id] = (reports, current_time)

def get_report_content(message):
    if message.content_type == 'text':
        return message.text
    else:
        content_types = {
            'photo': 'фото',
            'video': 'видео',
            'animation': 'гиф',
            'sticker': 'стикер'
        }
        return f"прикреплена {content_types.get(message.content_type, 'контент')}"

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_report_'))
def handle_delete_report(call):
    message_id_to_delete = int(call.data.split('_')[2])
    bot.delete_message(call.message.chat.id, message_id_to_delete)
    bot.delete_message(call.message.chat.id, call.message.message_id)




        
        
        
        
        
           # ЗАКРЕПЛЕНИЕ СООБЩЕНИЙ
@bot.message_handler(func=lambda message: message.text.lower() == '+пин')
def pin_message(message):
    if str(message.from_user.id) in allowed_users:
        if message.reply_to_message:
            bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        else:
            bot.reply_to(message, "Чтобы закрепить сообщение, ответьте на него командой '+пин'.")
    else:
        bot.reply_to(message, "🔒 у вас недостаточно прав")

@bot.message_handler(func=lambda message: message.text.lower() == '-пин')
def unpin_message(message):
    if str(message.from_user.id) in allowed_users:
        bot.unpin_chat_message(message.chat.id)
    else:
        bot.reply_to(message, "🔒у вас недостаточно прав")









# ПАСХАЛКИ

@bot.message_handler(func=lambda message: message.text.strip().lower() == 'трахнуть')
def trahnyt(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI4KmWQQn1IgBruxORYEt2U63SKP_f3AAIiGwACLfMgSY5qlUuuShdkNAQ",
        reply_to_message_id=message.message_id
    )    
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'мойша лучший')
def arlan_gay(message):
    bot.reply_to(message, 'факты..')
      
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'мойша')
def lustra(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI4IWWQQb1lgPL7dUdDT7PxgN1159MwAAJWAAMdHI0jdnCU7xj5UYw0BA",
        reply_to_message_id=message.message_id
    )    
        
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'дормитори')
def arlan_gay(message):
    bot.reply_to(message, 'лучший чатик')
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'выебать')
def trahnyt(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI4KmWQQn1IgBruxORYEt2U63SKP_f3AAIiGwACLfMgSY5qlUuuShdkNAQ",
        reply_to_message_id=message.message_id
    )    
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'умри')
def trahnyt(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI4KmWQQn1IgBruxORYEt2U63SKP_f3AAIiGwACLfMgSY5qlUuuShdkNAQ", 
        reply_to_message_id=message.message_id
    )
    
    
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'кринж')
def arlan_gay(message):
    bot.reply_to(message, 'ты.')
        
    
            

@bot.message_handler(func=lambda message: message.text.lower() == 'админы чмощники')
def admins_are_cool(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Отправка "набор текста" в качестве реакции
    bot.reply_to(message, "🤡")    
    

 #ЛС
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'лс сапа')
def handle_message(message):
    bot.reply_to(message, "тыкните на мой профиль")
    
    
    
    
    
    
    
    
    
    
#РАССЫЛКА    
allowed_users = ['6282374712', '5369435686', '5707946795']

@bot.message_handler(func=lambda message: message.text.strip().lower() == '.сетка')
def send_to_channels(message):
   if str(message.from_user.id) in allowed_users:  
    chat_ids = [-1002011140937, -1002129257694, -1001940482569] 
    text = message.text.replace('.сетка', '') 
    for chat_id in chat_ids:
        sent_message = bot.send_message(chat_id, text)
        bot.pin_chat_message(chat_id, sent_message.message_id) 
        
        
        
        
        
#пинги
@bot.message_handler(func=lambda message: message.text.strip().lower() == '.пиу')
def ping(message): 
    start_time = time.time()
    sent = bot.send_message(message.chat.id, 'Подсчет...')
    end_time = time.time()
    bot.edit_message_text(f'🔫ПАУ!\n🚀Скорость ответа: {round((end_time - start_time) * 1000, 2)} мс', message.chat.id, sent.message_id)
    
    

    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'пиу')
def ping(message): 
    start_time = time.time()
    sent = bot.send_message(message.chat.id, 'Подсчет...')
    end_time = time.time()
    bot.edit_message_text(f'🔫ПАУ!\n🚀Скорость ответа: {round((end_time - start_time) * 1000, 2)} мс', message.chat.id, sent.message_id)
    
    
    
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == '.пинг')
def ping(message):  
    start_time = time.time()
    sent = bot.send_message(message.chat.id, 'Подсчет...')
    end_time = time.time()
    bot.edit_message_text(f'🏓ПОНГ!\n🚀Скорость ответа: {round((end_time - start_time) * 1000, 2)} мс', message.chat.id, sent.message_id)   
    
       
          
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'пинг')
def ping(message): 
    start_time = time.time()
    sent = bot.send_message(message.chat.id, 'Подсчет...')
    end_time = time.time()
    bot.edit_message_text(f'🏓ПОНГ!\n🚀Скорость ответа: {round((end_time - start_time) * 1000, 2)} мс', message.chat.id, sent.message_id)    
    
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == 'сап')
def ping(message): 
    start_time = time.time()
    sent = bot.send_message(message.chat.id, 'Подсчет...')
    end_time = time.time()
    bot.edit_message_text(f'👋WUSAP\n🚀Скорость ответа: {round((end_time - start_time) * 1000, 2)} мс', message.chat.id, sent.message_id)    
   
    
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == '.сап')
def ping(message): 
    start_time = time.time()
    sent = bot.send_message(message.chat.id, 'Подсчет...')
    end_time = time.time()
    bot.edit_message_text(f'👋WUSAP\n🚀Скорость ответа: {round((end_time - start_time) * 1000, 2)} мс', message.chat.id, sent.message_id)   
    
    
    
    #СЕТКА

@bot.message_handler(func=lambda message: message.text.strip().lower() in ['сетка', 'сап сетка', '/grid@sapcmbot', '.сетка', '/grid'])
def send_chat_grid(message):
    chat_grid_message = "🥸 Ᏼᴄᴇ чᴀᴛы ᴋᴏᴛᴏᴩыᴇ ᴇᴄᴛь ʙ ᴄᴇᴛᴋᴇ"
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чатик", url="https://t.me/drmitory")
    button2 = types.InlineKeyboardButton(text="Чат закрыт", url="https://t.me/drmitory_play")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, chat_grid_message, reply_markup=markup)
    
    
    
    
    
    
    
    
    #ВЫХОД ИЗ ЧАТА
#СКРЫТАЯ
@bot.message_handler(func=lambda message: message.text.strip().lower() == '.ливни')
def leave_chat(message):
        chat_id = re.search(r'.ливни (.+)', message.text).group(1)

        try:
            bot.leave_chat(chat_id)
            bot.reply_to(message, f"Successfully left the chat {chat_id}.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
        
        
        
        
        
        
        

        
        #ОПРОСЫ
allowed_users = ['6282374712', '5369435686', '5707946795']
        
@bot.message_handler(func=lambda message: message.text.lower().startswith('опрос '))
def create_poll(message):
    if str(message.from_user.id) in allowed_users:
        poll_text = message.text.replace("опрос", "").strip()
        options = poll_text.split("\n")
        question = options[0]
        answers = options[1:]
        if len(answers) > 8:
            bot.reply_to(message, "Максимальное количество вариантов ответа - 8")
            return
        poll = types.Poll(question=question, options=answers, is_anonymous=False)
        sent_poll = bot.send_poll(message.chat.id, question, options=answers, is_anonymous=False)
        bot.pin_chat_message(message.chat.id, sent_poll.message_id, disable_notification=False)
        
        
        

        
                

                                                
                                

                                                
                                                                                     #музыка(ВРЕМЕНО ВЫКЛЮЧЕНО)
SPOTIFY_CLIENT_ID = '4d142088786c487eac0f901facb86ea9'
SPOTIFY_CLIENT_SECRET = 'bb56bdb3a0d34515905d15f23bf8cd4c'

@bot.message_handler(func=lambda message: message.text.lower().startswith('.барананан'))
def music_command(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Ищу трек...") 

    query = message.text.split(' ', 1)[1] 
    track = find_track(query)
    if track:
        bot.delete_message(chat_id, msg.message_id) 
        response_msg = bot.send_message(chat_id, "Название трека: " + track['name'])  
        audio_file = download_audio(track['preview_url']) 
        audio = open(audio_file, 'rb')
        bot.send_audio(chat_id, audio, reply_to_message_id=response_msg.message_id)
        audio.close()
        os.remove(audio_file) 
    else:
        bot.delete_message(chat_id, msg.message_id) 
        bot.send_message(chat_id, "Трек не найден")

def find_track(query):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
    results = sp.search(q='track:' + query, type='track')
    if results['tracks']['items']:
        return results['tracks']['items'][0] 
    else:
        return None

def download_audio(url):
    response = requests.get(url)
    file_name = 'temp_audio.mp3'
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return file_name

        
        
        
        
        
        
#анкетоды               
@bot.message_handler(func=lambda message: message.text.lower() == 'анекдот')
def send_joke(message):
    try:
        response = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1')
        data = response.json()

        if data["content"]:
            bot.reply_to(message, data["content"])
        else:
            bot.reply_to(message, "К сожалению, не удалось получить анекдот. Попробуйте позже.")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Произошла ошибка при получении анекдота.")
        
        
        
        
        
        
        
 #МУТ           
def user_can_restrict_members(user_id, chat_id):
    members = bot.get_chat_administrators(chat_id)
    for member in members:
        if member.user.id == user_id:
            return True
    return False

@bot.message_handler(func=lambda message: message.text.strip().lower() in ['+мут', 'сап мут', '/muted'])
def mute_user(message):
    try:
        args = message.text.split(' ')
        if len(args) < 2:
            duration = 60 
            duration_str = "1 час"
        else:
            duration_str = args[1]
            duration_val = int(duration_str[:-1])
            duration_unit = duration_str[-1]
            if duration_unit not in ['м', 'ч', 'д']:
                bot.send_message(message.chat.id, "время указывать нельзя.")
                return
            if duration_unit == 'м':
                duration = duration_val * 60  # переводим минуты в секунды
            elif duration_unit == 'ч':
                duration = duration_val * 60 * 60 
            else:
                duration = duration_val * 60 * 60 * 24
            
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            bot.send_message(message.chat.id, "Укажите сообщение для мута")
            return

        until_date = int((datetime.now() + timedelta(seconds=duration)).timestamp())
        bot.restrict_chat_member(message.chat.id, user.id, until_date)

        moderator_link = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        user_link = f"[{user.first_name}](tg://user?id={user.id})"
        mute_message = f"👤пользователь {user_link} замучен на {duration_str}\n🧑‍✈️модер: {moderator_link}"
        bot.send_message(message.chat.id, mute_message, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
        

@bot.message_handler(func=lambda message: message.text.lower().startswith('-мут'))
def unmute_user(message):

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if user.username:
            user_mention = f"[{user.first_name}](tg://user?id={user.id})"
        else:
            user_mention = user.first_name
        bot.restrict_chat_member(
            message.chat.id,
            user.id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        unmute_message = f"👤пользователь {user_mention} размучен\n🧑‍✈️модер: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        bot.send_message(message.chat.id, unmute_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Ответьте на сообщение пользователя, которого вы хотите размутить.")

        
        
        
        
        
        
#Админка
allowed_users = ['6282374712', '5369435686', '5707946795']

@bot.message_handler(func=lambda message: message.text.lower() == '+админ')
def promote_to_admin(message):
    if str(message.from_user.id) in allowed_users:
        user = message.from_user
        if user.username:
            user_mention = f"[{user.first_name}](tg://user?id={user.id})"
        else:
            user_mention = user.first_name
        bot.promote_chat_member(message.chat.id, user.id, can_manage_chat=True, can_delete_messages=True, 
                                can_invite_users=True, can_restrict_members=True, 
                                can_pin_messages=True, can_promote_members=True
                               )
        bot.reply_to(message, f"Пользователю {user_mention} были выданы права администратора.", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text.lower() == '-админ')
def demote_from_admin(message):
    if str(message.from_user.id) in allowed_users:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            if user.username:
                user_mention = f"[{user.first_name}](tg://user?id={user.id})"
            else:
                user_mention = user.first_name
            bot.promote_chat_member(message.chat.id, user.id, can_change_info=False, can_post_messages=True,
                                    can_edit_messages=False, can_delete_messages=False, can_invite_users=False,
                                    can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
            bot.send_message(message.chat.id, f"Пользователю {user_mention} сняты админские права.", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "Укажите корректное сообщение для снятия с админки")
            
            
            
            
            
            
            
@bot.message_handler(func=lambda message: message.text.lower().startswith('+бан'))
def ban_user(message):
    chat_id = message.chat.id
    bot_info = bot.get_me()
    bot_member = bot.get_chat_member(chat_id, bot_info.id)
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else None

    if bot_member.status in ["creator", "administrator"]:
        if user_id:
            user_info = bot.get_chat_member(chat_id, message.from_user.id)
            if "administrator" in user_info.status or user_info.status == "creator":
                bot.kick_chat_member(chat_id, user_id)
                banned_user = message.reply_to_message.from_user
                ban_message = f"👤пользователь [{banned_user.first_name}](tg://user?id={banned_user.id}) забанен\n🧑‍✈️модер: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                bot.reply_to(message, ban_message, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Ответьте на сообщение пользователя, которого вы хотите забанить.")
    else:
        bot.reply_to(message, "У меня нет разрешения на удаление пользователей.")

@bot.message_handler(func=lambda message: message.text.lower().startswith('-бан'))
def unban_user(message):
    chat_id = message.chat.id
    bot_info = bot.get_me()
    bot_member = bot.get_chat_member(chat_id, bot_info.id)
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else None

    if bot_member.status in ["creator", "administrator"]:
        if user_id:
            bot.unban_chat_member(chat_id, user_id)
            unbanned_user = message.reply_to_message.from_user
            unban_message = f"👤пользователь [{unbanned_user.first_name}](tg://user?id={unbanned_user.id}) разбанен\n🧑‍✈️модер: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            bot.reply_to(message, unban_message, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Ответьте на сообщение пользователя, которого вы хотите разбанить.")
    else:
        bot.reply_to(message, "У меня нет разрешения на добавление пользователей.")

        
        
        
        
        
        
        
#википедия
wiki_wiki = wikipediaapi.Wikipedia(
    language='ru',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='wikipedia'
)

@bot.message_handler(func=lambda message: message.text.lower().startswith('.вики'))
def wiki_search(message):
    query = message.text[5:].strip() 
    page = wiki_wiki.page(query)
    if page.exists():
        summary = page.summary[:1500]  
        bot.reply_to(message, summary)
    else:
        bot.reply_to(message, "Информация не найдена. Попробуйте изменить запрос.")
        
        
        
        
        
                
#Словарь
@bot.message_handler(func=lambda message: message.text.lower().startswith('.словарь'))
def define_word(message):
    command_parts = message.text.split(' ')
    if len(command_parts) > 1:
        word = command_parts[1]
        response = requests.get(f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20240101T213553Z.26e7fed62e078769.7468573f9cdcb622ca5087c8a063fc37b904dfde&lang=ru-ru&text={word}')

        if response.status_code == 200:
            data = response.json()
            if 'def' in data and data['def']:
                meanings = data['def'][0]['tr']
                response_message = f"📖 Пояснение слова {word}\n"
                for index, meaning in enumerate(meanings, start=1):
                    response_message += f"{index}⃣ {meaning['text']}\n"
                bot.send_message(message.chat.id, response_message)
            else:
                bot.send_message(message.chat.id, f"К сожалению, определение для слова '{word}' не найдено.")
        else:
            bot.send_message(message.chat.id, "Извини, что-то пошло не так. Попробуй позже.")
    else:
        bot.send_message(message.chat.id, "Используйте команду 'словарь' с указанием слова для поиска.")
        
        
        
        
        
        
        
#конкулятор        
@bot.message_handler(func=lambda message: message.text.startswith('.реши'))
def solve_expression(message):
    expression = re.search(r'\.реши (.+)', message.text).group(1)
    try:
        result = eval(expression)
        bot.reply_to(message, f"👨‍🏫 {expression} = {result}")
    except Exception as e:
        bot.reply_to(message, "Кажется, что-то пошло не так. Убедитесь, что пример введен корректно.") 
        
        

                                            
                                                                                     
@bot.message_handler(commands=['название'])
def change_chat_name(message):
    try:
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            new_chat_name = message.text.split(maxsplit=1)[1]  
            global old_chat_name 
            old_chat_name = bot.get_chat(message.chat.id).title 
            bot.set_chat_title(message.chat.id, new_chat_name)
            response = f"🔄Название чата изменено.\n❎Старое название: {old_chat_name}\n✅Новое название: {new_chat_name}"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "У вас недостаточно прав для изменения названия чата.")
    except (IndexError, AttributeError):
        bot.reply_to(message, "Пожалуйста, укажите новое название чата после команды.")

@bot.message_handler(commands=['описание'])
def change_chat_description(message):
    try:
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            new_chat_description = message.text.split(maxsplit=1)[1]  
            global old_chat_description  
            old_chat_description = bot.get_chat(message.chat.id).description  
            bot.set_chat_description(message.chat.id, new_chat_description)  
            response = f"🔄Описание чата изменено.\n❎Старое описание: {old_chat_description}\n✅Новое описание: {new_chat_description}"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "У вас недостаточно прав для изменения описания чата.")
    except (IndexError, AttributeError):
        bot.reply_to(message, "Пожалуйста, укажите новое описание чата после команды.")
        
        
        
        
        


        

         
                        
                                        
                
                                

        
    
    
    
  
        
   
        
             
                  

                       
                                              
                                                                     
chat_states = {}

# Добавляем игру "Мины" в список игр
@bot.message_handler(commands=['игры', 'play@sapcmbot', 'play'])
def show_games(message):
    markup = types.InlineKeyboardMarkup()
    
    rps_button = types.InlineKeyboardButton(text='Камень, ножницы, бумага', callback_data='rps')

    markup.row(rps_button)        
    
    bot.send_message(message.chat.id, "Выбери игру:", reply_markup=markup)
    
    

@bot.message_handler(commands=['start_rps'])
def start_rps_game(message):
    chat_id = message.chat.id
    if chat_id in chat_states and chat_states[chat_id]['game'] == 'rps':
        bot.send_message(chat_id, "Игра в 'Камень, ножницы, бумага' уже начата!")
    else:
        response = "👊✌️🖐 Давай поиграем в 'Камень, ножницы, бумага'! Выбери один из вариантов: камень, ножницы или бумага."
        bot.send_message(chat_id, response)
        chat_states[chat_id] = {'game': 'rps', 'current_player': message.from_user.id}

# Обработчик для игры "камень, ножницы, бумага"
@bot.message_handler(func=lambda message: message.text.lower() in ["камень", "ножницы", "бумага"])
def play_rps(message):
    user_choice = message.text.lower()
    chat_id = message.chat.id
    if chat_id in chat_states and chat_states[chat_id]['game'] == 'rps':
        if message.from_user.id == chat_states[chat_id]['current_player']:
            bot_choice = random.choice(["камень", "ножницы", "бумага"])
            if user_choice == bot_choice:
                result = "Ничья! Я выбрал " + bot_choice + "."
            elif (user_choice == "камень" and bot_choice == "ножницы") or (user_choice == "ножницы" and bot_choice== "бумага") or (user_choice == "бумага" and bot_choice == "камень"):
                result = "Ты победил! Я выбрал " + bot_choice + "."
            else:
                result = "Я победил! Я выбрал " + bot_choice + "."
            bot.send_message(chat_id, result)
            del chat_states[chat_id]  # Очищаем состояние игры
        else:
            bot.reply_to(message, "Сейчас не ваш ход!")    
            
                                                                                               
                                                                                                                                          
                                                                                                                                                                 

def send_welcome(chat_id, message_id):
    bot.send_message(chat_id,
                     '''📌 *Закреплённое сообщение*
                     
Перед тем как начать писать комментарии ознакомьтесь с [правилами](https://teletype.in/@drmotory/chatrules).
Хотите влиться в коллектив?Прочитайте наш [гайд «🫂Как влиться в коллектив».](https://teletype.in/@drmotory/collective-2)\n\n_Спасибо за понимание._''',
                     parse_mode="Markdown",
                     reply_markup=create_markup(),
                     reply_to_message_id=message_id)  # отправка сообщения с указанием id комментария, на который отвечаем

# функция для создания кнопок
def create_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton('Правила', 'https://teletype.in/@drmotory/chatrules'),
        telebot.types.InlineKeyboardButton('мой список команд', 'https://teletype.in/@drmotory/commands_support')
    )
    return markup

# обработчик события 'message' для пересланных сообщений из вашего канала
@bot.message_handler(func=lambda message: message.forward_from_chat is not None)
def handle_forwarded_message(message):
    if message.forward_from_chat.type == 'channel':
        send_welcome(message.chat.id, message.message_id)                                                                           
                                                                                                                
@bot.message_handler(func=lambda message: message.text.lower() == 'как дела?')
def how_are_you(message):
    chance = random.random()  # Генерируем случайное число от 0 до 1
    if chance <= 0.02:  # Шанс 2%, то есть 0.02
        bot.reply_to(message, "У 4 админа точно средненько!")                                                                                                                                            
                                                                                                                                                                        

@bot.message_handler(func=lambda message: message.text.strip().lower() in ['агрессия', 'сап агрессия', '.агрессия', '!агрессия', '/агрессия'])
def handle_aggression(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
        mention = f"<a href='tg://user?id={user_id}'>{user_name}</a>"
        warning_message = f"⛔️<b>Внимание! Специально для {mention} и для всех остальных. Агрессия в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещена.</b>\nСоветуем отказаться от агрессии в наших чатах.\n🤓<i>Агрессия</i> — это поведение, направленное на причинение вреда или проблем другому человеку\n📛За игнорирования предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."

        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Правила сетки", url="https://teletype.in/@drmotory/chatrules")
        url_button2 = types.InlineKeyboardButton(text="Мой список команд", url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button1, url_button2)

        bot.send_message(message.chat.id, warning_message, reply_to_message_id=message.reply_to_message.message_id, reply_markup=keyboard, parse_mode='HTML')
    else:
        warning_message = "⛔️<b>Внимание! Агрессия в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещена.</b>\nСоветуем отказаться от агрессии в наших чатах.\n🤓<i>Агрессия</i> — это поведение, направленное на причинение вреда или проблем другому человеку\n📛За игнорирования предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."

        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Правила сетки", url="https://teletype.in/@drmotory/chatrules")
        url_button2 = types.InlineKeyboardButton(text="Мой список команд", url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button1, url_button2)
        
        bot.send_message(message.chat.id, warning_message, reply_markup=keyboard, parse_mode='HTML')
                                                                                                                                                                                                                               
                              

                                                                                                                                              
                                                                                                                                                                                                                                                                                            


@bot.message_handler(func=lambda message: message.text.strip().lower() in ['ссоры', 'сап ссоры', '.ссоры', '!ссоры', '/ссоры'])
def handle_quarrel(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
        mention = f"<a href='tg://user?id={user_id}'>{user_name}</a>"
        warning_message = f"⛔️<b>Внимание!</b> Специально для {mention} и для всех остальных. Ссоры в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещены.\nсоветуем прекратить ссориться, иначе мы будем вынуждены заглушить вас.\n\n🤓<i>Ссора</i> - это конфликт или разногласие между людьми, организациями или группами, которое часто сопровождается словесными выяснениями, напряженностью и негативными эмоциями.\n\n📛За игнорирование предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."
        bot.send_message(message.chat.id, warning_message, reply_to_message_id=message.reply_to_message.message_id, parse_mode='HTML')
    else:
        warning_message = "⛔️<b>Внимание!</b> Ссоры в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещены.\nсоветуем прекратить ссориться, иначе мы будем вынуждены заглушить вас.\n\n🤓<i>Ссора</i> - это конфликт или разногласие между людьми, организациями или группами, которое часто сопровождается словесными выяснениями, напряженностью и негативными эмоциями.\n\n📛За игнорирование предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."
        bot.send_message(message.chat.id, warning_message, parse_mode='HTML')
        




                                                                                                                                                                                                                                                                                                                                                                                                                                               



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

                                                                                                                                                                                                                                  
                                                     
# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ['administrator', 'creator'] and message.text.startswith('.дел '):
        delete_flag = delete_messages(message)
        if delete_flag:
            bot.delete_message(message.chat.id, message.message_id)

# Обработчик команды .дел
def delete_messages(message):
    try:
        number = int(message.text.split('.дел ')[1])
        if number > 0:
            replied_message_id = message.reply_to_message.message_id
            for i in range(number):
                try:
                    bot.delete_message(message.chat.id, replied_message_id - i)
                except Exception as e:
                    error_message = f"Не удалось удалить сообщение с ID {replied_message_id - i}: {e}"
            if 'error_message' in locals():
                bot.reply_to(message, error_message)
            else:
                bot.reply_to(message, f"Я удалил {number} выбранных сообщений.")
                bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI2nGWFXKEM4_NOSx3PQJUcQuWqFU2RAALMFQACdWepSdykWqEAAVfrBDME")
            return True
        else:
            bot.reply_to(message, "Пожалуйста, введите корректное число и убедитесь, что вы ответили на сообщение, с которого начать удаление.")
    except (ValueError, AttributeError):
        bot.reply_to(message, "Пожалуйста, введите корректное число и убедитесь, что вы ответили на сообщение, с которого начать удаление.")
    
    return False

                                                
        









    
        
admin_chat_id = '-1002129257694'
message_limit = 5
time_window = 10
alert_interval = 300
alert_interval_per_user = 300
user_messages = {}
last_alert_time = {}
flood_detected_users = set()



@bot.message_handler(content_types=['text', 'audio', 'photo', 'voice', 'video', 'document', 'sticker', 'animation'])
def check_message_frequency(message):
    user_id = message.from_user.id
    user_profile = f"[{message.from_user.first_name}](tg://user?id={user_id})"
    current_time = time.time()

    if user_id in user_messages:
        message_times = user_messages[user_id]
        message_times = list(filter(lambda x: current_time - x <= time_window, message_times))

        if len(message_times) > message_limit and user_id not in flood_detected_users:
            if user_id not in last_alert_time or current_time - last_alert_time[user_id] >= alert_interval:
                bot.send_message(admin_chat_id, f"В чате от пользователя {user_profile} замечена активность похожая на флуд. Надо бороться с флудом!", parse_mode="Markdown")
                last_alert_time[user_id] = current_time

                message_url = f"https://t.me/{message.chat.username}/{message.message_id}"
                bot.send_message(admin_chat_id, f"[Посмотреть сообщение]({message_url})", parse_mode="Markdown")

                flood_detected_users.add(user_id)
        elif len(message_times) > message_limit * 1:
            bot.restrict_chat_member(message.chat.id, user_id, until_date=int(time.time()) + 1800)
            bot.send_message(admin_chat_id, f"Флуд от {user_profile} не прекращается. Пользователь получил мут на 30 минут.", parse_mode="Markdown")
            flood_detected_users.add(user_id)

        if user_id in last_alert_time and current_time - last_alert_time[user_id] < alert_interval_per_user:
            last_alert_time[user_id] = current_time
            
    if user_id in user_messages:
        user_messages[user_id].append(current_time)
    else:
        user_messages[user_id] = [current_time]


        
        
        










        
bot.polling()