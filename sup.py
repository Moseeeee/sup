from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import BotCommandScopeChat, InlineKeyboardMarkup, InlineKeyboardButton, Message
import asyncio, time, re, os, requests, spotipy, wikipediaapi, random, logging
from spotipy.oauth2 import SpotifyClientCredentials
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from sympy import sympify, solve
import re

API_TOKEN = '7017976892:AAG5mjQOCmdoBDXSYG69Y3nhejlKnTzSelQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


# Команды со слешом
async def set_my_commands(bot, commands, scope):
    await bot.set_my_commands(commands, scope=scope)


async def set_commands_for_chat(bot, chat_id, chat_name, commands):
    scope = BotCommandScopeChat(chat_id=chat_id)
    await set_my_commands(bot, commands, scope)


async def setup_commands(bot):
    pass
    chat_id_1 = -1002011140937
    chat_name_1 = "Chat1"
    commands_chat1 = [
    BotCommand('report', '🚫 Пожаловаться на пользователя'),
   BotCommand('commands', '📖 Команды'),
   BotCommand('rules', '📝 Правила чата'),
   BotCommand('grid', '🗂 Чаты сетки')
    ]
    await set_commands_for_chat(bot, chat_id_1, chat_name_1, commands_chat1)

    # Chat 2
    chat_id_2 = -1002129257694
    chat_name_2 = "Chat2"
    commands_chat2 = [
    BotCommand('commands', '📖 Команды'),
    BotCommand('rules', '📝 Правила чата'),
    BotCommand('grid', '🗂 Чаты сетки'),
    BotCommand('addhelper', '✅ Добавиться в список админов'),
    BotCommand('unhelper', '❌ Удалиться из списка админов')
    ]
    await set_commands_for_chat(bot, chat_id_2, chat_name_2, commands_chat2)

# Старт
@dp.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    if message.chat.type == 'private':
        user_id = message.from_user.id
        welcome_message = (
            f"👋Здравствуйте, [{message.from_user.first_name}](tg://user?id={user_id}).\n"
            "🤖Я бот помощник для сетки чатов «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ».\n"
            "💡Если у вас есть идеи для бота, напишите [в этот чат](https://t.me/+LDPqIG1XW7dkNzgy)"
        )

        keyboard = InlineKeyboardMarkup()
        url_button = InlineKeyboardButton(text="Команды", url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button)

        await message.answer(welcome_message, parse_mode='Markdown', reply_markup=keyboard)


# правила

@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['правила', 'сап правила', '.правила', '!правила',
                                                                '/rules@sapcmbot', '/rules', '/правила'])
async def send_rules(message: types.Message):
    rules_link = "https://teletype.in/@drmotory/psc"
    rules_message = f'[Правила чата]({rules_link})'
    await bot.send_message(message.chat.id, rules_message, parse_mode='markdown')


# Репорты
ADMIN_CHATS = [-1002129257694]
MUTE_DURATION = 3600
user_reports = {}


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


@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['репорт', 'сап репорт', '.репорт', '!репорт',
                                                                '/report@sapcmbot', '/report', '.жалоба'])
async def handle_report(message: types.Message):
    if message.chat.type != 'supergroup':
        await message.answer('Репорты работают только в чатах.')
        return

    try:
        user_id = message.from_user.id
        current_time = time.time()

        replied_message = message.reply_to_message
        command, _, report_text = message.text.partition('\n')



        if replied_message and report_text:
            report_content = get_report_content(replied_message)
            reported_user_link = f"[{replied_message.from_user.first_name}](tg://user?id={replied_message.from_user.id})"
            report_message = f'🛑Новая жалоба\n📖Причина: {report_text}\n📝Текст: {report_content}\n🗣Отправитель жалобы: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n👤Жалоба кинули на: {reported_user_link}'
            inline_keyboard = types.InlineKeyboardMarkup()
            goto_button = types.InlineKeyboardButton(text="Перейти к сообщению",
                                                     url=f"https://t.me/{replied_message.chat.username}/{replied_message.message_id}")
            inline_keyboard.row(goto_button)

            for admin_chat_id in ADMIN_CHATS:
                await bot.send_message(admin_chat_id, report_message, parse_mode=types.ParseMode.MARKDOWN,
                                       reply_markup=inline_keyboard)
                await message.answer(f'✅ Жалоба отправлена администраторам.\nПричина:{report_text}')
        elif replied_message:
            report_content = get_report_content(replied_message)
            reported_user_link = f"[{replied_message.from_user.first_name}](tg://user?id={replied_message.from_user.id})"
            report_message = f'🛑Новая жалоба без причины\n📝Текст: {report_content}\n🗣Отправитель жалобы: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n👤Жалоба кинули на: {reported_user_link}'
            inline_keyboard = types.InlineKeyboardMarkup()
            goto_button = types.InlineKeyboardButton(text="Перейти к сообщению",
                                                     url=f"https://t.me/{replied_message.chat.username}/{replied_message.message_id}")
            inline_keyboard.row(goto_button)

            for admin_chat_id in ADMIN_CHATS:
                await bot.send_message(admin_chat_id, report_message, parse_mode=types.ParseMode.MARKDOWN,
                                       reply_markup=inline_keyboard)
                await message.answer('✅ Жалоба отправлена администраторам.')
        else:
            await message.answer(
                'Не удалось обработать вашу жалобу. Укажите причину и ответьте на сообщение, на которое отправляете жалобу.')
    except Exception as e:
        await message.answer('Произошла ошибка при обработке вашей жалобы. Пожалуйста, попробуйте еще раз позже.')


@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['чек', 'сап чек', 'чек.'] and str(message.chat.id) == '-1002129257694')
async def check_report(message: types.Message):
    await message.reply('🌟')
    profile_link = f"tg://user?id={message.from_user.id}"
    await message.reply('[{}]({}) проверил репорты, спасибо!'.format(message.from_user.full_name, profile_link), parse_mode='Markdown')


    


# Команды

@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['команды', 'сап команды', '.команды', '!команды',
                                                                '/commands@sapcmbot', '/commands', '/команды'])
async def send_commands(message: types.Message):
    commands_link = "https://teletype.in/@drmotory/support_commands"
    rules_message = f'[Команды бота]({commands_link})'
    await bot.send_message(message.chat.id, rules_message, parse_mode='markdown')


# Закреплёные сообщения в чатах
allowed_users = ['6282374712']



@dp.message_handler(lambda message: message.text.strip().lower() == '!дорпин')
async def send_and_pin_messages(message: types.Message):
    allowed_users = ['6282374712']
    if str(message.from_user.id) in allowed_users:
        messages_to_send = [
            "[👋](https://teletype.in/@drmotory/collective-2)Добро пожаловать в «[🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чат для общения](https://t.me/drmitory)».\nЗдесь ты можешь найти себе новых знакомых, друзей и может даже пару!\n\nОчень надеемся что вам у нас понравится. Если хотите влиться в коллектив то не надо молчать, а нужно писать и общаться с участниками чата.\n\n[🫂 Как влиться в коллектив](https://teletype.in/@drmotory/collective-2)\n\nℹ️ Мы хотим создать приятную атмосферу в чате. Если вас человек попросил не тегать / отвечать ему на сообщения, то не стоит этого делать, ведь за это вам выдадут мут.\n\nВсе наши чаты:\n[🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чат для общения](https://t.me/drmotory)\n[🎮ᎠᏫᏒᎷᏢᏫᏒᎩ | Игры](https://t.me/drmitory_play)\n\nПеред тем как начать общение ознакомьтесь с правилами чата.\nПравила чатов сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ»🔽",
            "[Правила сетки чатов «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ»](https://teletype.in/@drmotory/psc)\n[Правила голосового чата](https://teletype.in/@drmotory/chatrules#Cgz9)\n❗️ Админы и модеры вправе выдать те наказания, которые посчитают нужным.",
            "Если вы заметили проблемы с поведением других участников или возникли технические трудности, обратитесь к модераторам или администраторам чата для решения проблемы.\n\nПриятного общения 🌺"
        ]

        sent_messages = []
        for text in messages_to_send:
            sent_message = await bot.send_message(message.chat.id, text, parse_mode="Markdown")
            sent_messages.append(sent_message)

        await bot.pin_chat_message(message.chat.id, sent_messages[0].message_id)


@dp.message_handler(lambda message: message.text.strip().lower() == '!плпин')
async def send_and_pin_messages(message: types.Message):
    if str(message.from_user.id) in allowed_users:
        messages_to_send = [
            "[👋](https://teletype.in/@drmotory/chatrules)Добро пожаловать в «[🎮ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | Игры](https://t.me/drmitory_play)»\nЗдесь ты можешь поиграть в игры,при этом не засоряя основной чат.\n\nМы собрали часто используемых ботов для игр,и готовы дать вам сыграть во многие игры!\nЕсли есть предложения то отметьте кого из админов и напишите имя бота и что он делает,а там админы решат,добавлять или нет.\n\nосновной чат для [общения](https://t.me/drmitory),где можно пообщаться без игровых ботов.\n‼️Перед тем как начать общаться,прочитайте [правила сетки.](https://teletype.in/@drmotory/psc)\n[🫂Гайд как влиться в коллектив](https://teletype.in/@drmotory/collective-2)\n\nВсе наши чаты:\n[🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чат для общения](https://t.me/drmitory)\n[🎮ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | Игры](https://t.me/drmitory_play)",
            "Если вы заметили проблемы с поведением других участников или возникли технические трудности, обратитесь к модераторам или администраторам чата для решения проблемы.\n\nПриятных игр🌺"
        ]

        sent_messages = []
        for text in messages_to_send:
            sent_message = await bot.send_message(message.chat.id, text, parse_mode="Markdown")
            sent_messages.append(sent_message)

        await bot.pin_chat_message(message.chat.id, sent_messages[0].message_id)


# Команды для админов:
@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['+пин', 'сап пин'])
async def pin_message(message: Message):
    try:
        chat_admins = await bot.get_chat_administrators(message.chat.id)  

        is_admin = False
        is_admin_can_pin = False
        for admin in chat_admins:
            if admin.user.id == message.from_user.id:
                is_admin = True
                if admin.can_pin_messages:
                    is_admin_can_pin = True
                break



        if is_admin and is_admin_can_pin:
            if message.reply_to_message:
                await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
                reply_message = await bot.send_message(message.chat.id,
                                                       f"📌 [Сообщение](https://t.me/{(await bot.get_chat(chat_id=message.chat.id)).username}/{message.reply_to_message.message_id}) закреплено.",
                                                       parse_mode="Markdown")
            else:
                await message.reply("Чтобы закрепить сообщение, ответьте на него командой '+пин'.",
                                    parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.reply("🔒 У вас недостаточно прав для закрепления сообщений",
                                parse_mode=types.ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply("🚫 У вас недостаточно прав для закрепления сообщений", parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['-пин', 'сап анпин'])
async def unpin_message(message: Message):
    try:
        chat_admins = await bot.get_chat_administrators(message.chat.id)  

        is_admin = False
        for admin in chat_admins:
            if admin.user.id == message.from_user.id:
                is_admin = True
                break

        if is_admin:
            if message.reply_to_message:
                await bot.unpin_chat_message(message.chat.id)
                await message.reply("❌ Сообщение откреплено.", parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.reply("Нет сообщения для открепления.", parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.reply("🔒 У вас недостаточно прав для открепления сообщений.",
                                parse_mode=types.ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply("🚫 У вас недостаточно прав для открепления сообщений", parse_mode=types.ParseMode.MARKDOWN)

        # Муты:


async def user_can_restrict_members(user_id, chat_id):
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)

        if chat_member.status in ['administrator', 'creator']:
            if chat_member.status == 'creator':
                return True
            else:
                chat_permissions = chat_member.chat_permissions
                if 'can_restrict_members' in chat_permissions:
                    return True
    except Exception as e:
        print(f"Error in user_can_restrict_members: {e}")

    return False


@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['+мут', 'сап мут'])
async def process_mute_duration(message: types.Message):
    if await user_can_restrict_members(message.from_user.id, message.chat.id):
        try:
            duration_str = message.text.split('+мут ')[1]
            user = message.reply_to_message.from_user

            duration_val = int(duration_str[:-1])
            duration_unit = duration_str[-1]
            duration = 0

            if duration_unit == 'м':
                duration = duration_val * 60
            elif duration_unit == 'ч':
                duration = duration_val * 60 * 60
            elif duration_unit == 'д':
                duration = duration_val * 60 * 60 * 24

            until_date = int((datetime.now() + timedelta(seconds=duration)).timestamp())



            await bot.restrict_chat_member(message.chat.id, user.id, until_date=until_date,
                                           permissions=types.ChatPermissions())
            admin_link = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            user_link = f"[{user.first_name}](tg://user?id={user.id})"
            await message.answer(f"🔇 Пользователь {user_link} замучен.\n😺 Модератор: {admin_link}",
                                 parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("У вас нет прав на выдачу мута.", parse_mode="Markdown")


@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['-мут', 'сап размут'])
async def unmute(message: types.Message):
    if await user_can_restrict_members(message.from_user.id, message.chat.id):
        try:
            user_id = message.reply_to_message.from_user.id
            user = message.reply_to_message.from_user
            await bot.restrict_chat_member(message.chat.id, user_id,
                                           permissions=types.ChatPermissions(can_send_messages=True,
                                                                             can_send_media_messages=True,
                                                                             can_send_other_messages=True,
                                                                             can_add_web_page_previews=True))
            admin_link = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            user_link = f"[{user.first_name}](tg://user?id={user_id})"
            await message.answer(f"🔊 Пользователь {user_link} размучен.\n😺 Модератор: {admin_link}",
                                 parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("У вас нет прав на размут.", parse_mode="Markdown")

        # Бан:


@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['+бан', 'сап бан'])
async def ban_reply_user(message: types.Message):
    if await user_can_restrict_members(message.from_user.id, message.chat.id) and message.reply_to_message:
        try:
            if len(message.text.split()) <= 1:
                await message.answer("Укажите время и формат (м/ч/д) для бана. Например, '+бан 30д'.")
                return

            ban_params = message.text.split()[1]
            duration_val = int(re.search(r'\d+', ban_params).group())
            duration_unit = re.search(r'[мчд]', ban_params).group()

            user_id = message.reply_to_message.from_user.id
            user = message.reply_to_message.from_user

            duration_seconds = 0
            if duration_unit == 'м':
                duration_seconds = duration_val * 60
            elif duration_unit == 'ч':
                duration_seconds = duration_val * 60 * 60
            elif duration_unit == 'д':
                duration_seconds = duration_val * 60 * 60 * 24

            until_date = int(datetime.now().timestamp()) + duration_seconds
            await bot.kick_chat_member(message.chat.id, user_id, until_date=until_date)

            admin_link = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            user_link = f"[{user.first_name}](tg://user?id={user_id})"
            await message.answer(
                f"🕒 Пользователь {user_link} забанен на {duration_val} {duration_unit}.\n😺 Модератор: {admin_link}",
                parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("У вас нет прав на выдачу бана или это не ответ на сообщение.", parse_mode="Markdown")



# ДОСТУПНО ВСЕМ:
# проверка работоспособности бота
@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['пиу', 'сап пиу', '.пиу', '!пиу', '/пиу', '?пиу'])
async def ping(message: types.Message):
    start_time = time.time()
    sent = await message.answer('Подсчет...')
    end_time = time.time()
    processing_time = round((end_time - start_time) * 1000, 2)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await bot.edit_message_text(f'🔫ПАУ!\n🚀Скорость ответа {processing_time} мс', message.chat.id, sent.message_id)


@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['пинг', 'сап пинг', '.пинг', '!пинг', '/пинг', '?пинг'])
async def ping(message: types.Message):
    start_time = time.time()
    sent = await message.answer('Подсчет...')
    end_time = time.time()
    processing_time = round((end_time - start_time) * 1000, 2)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await bot.edit_message_text(f'🏓ПОНГ!\n🚀Скорость ответа {processing_time} мс', message.chat.id, sent.message_id)


@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['сап', 'сап сап', '.сап', '!сап', '/сап', '?сап'])
async def ping(message: types.Message):
    start_time = time.time()
    sent = await message.answer('Подсчет...')
    end_time = time.time()
    processing_time = round((end_time - start_time) * 1000, 2)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await bot.edit_message_text(f'👋WUSAP\n🚀Скорость ответа {processing_time} мс', message.chat.id, sent.message_id)


# Сетка чатов
@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['сетка', 'сап сетка', '.сетка', '!сетка',
                                                                '/grid@sapcmbot', '/grid'])
async def send_chat_grid(message: types.Message):
    chat_grid_message = "📖Все чаты сетки:"
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="🦦ᎠᏫᏒᎷᏆᎢᏫᏒᎩ | чатик", url="https://t.me/drmitory")
    button2 = types.InlineKeyboardButton(text="Чат закрыт", url="https://t.me/drmitory_play")
    markup.add(button1, button2)
    await bot.send_message(message.chat.id, chat_grid_message, reply_markup=markup)


# Споти
SPOTIFY_CLIENT_ID = '4d142088786c487eac0f901facb86ea9'
SPOTIFY_CLIENT_SECRET = 'bb56bdb3a0d34515905d15f23bf8cd4c'

command_count = {}
command_timestamps = {}


@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['споти', 'сап споти', '.споти', '!споти'])
async def music_command(message: types.Message):
    chat_id = message.chat.id

    if chat_id not in command_count:
        command_count[chat_id] = 0
        command_timestamps[chat_id] = []

    current_time = time.time()
    command_timestamps[chat_id] = [timestamp for timestamp in command_timestamps[chat_id] if
                                   timestamp > current_time - 60]

    if len(command_timestamps[chat_id]) > 5:
        await bot.send_message(chat_id, "Команда отключена на 10 минут из-за частого использования.")
        return

    command_timestamps[chat_id].append(time.time())
    command_count[chat_id] += 1

    msg = await bot.send_message(chat_id, "Ищу трек...")

    try:
        query = message.text.split(' ', 1)[1]
        track = find_track(query)
        if track:
            await bot.delete_message(chat_id, msg.message_id)
            audio_file = download_audio(track['preview_url'])
            audio = open(audio_file, 'rb')
            response_msg = await bot.send_audio(chat_id, audio, title="трек: " + track['name'])
            audio.close()
            os.remove(audio_file)
        else:
            await bot.delete_message(chat_id, msg.message_id)
            await bot.send_message(chat_id, "Трек не найден")
    except Exception as e:
        await bot.send_message(chat_id,
                               f"Произошла ошибка при обработке запроса: {str(e)}. Пожалуйте, попробуйте снова.")



def find_track(query):
    try:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                                 client_secret=SPOTIFY_CLIENT_SECRET))
        results = sp.search(q='track:' + query, type='track')
        if results and 'tracks' in results and 'items' in results['tracks'] and results['tracks']['items']:
            return results['tracks']['items'][0]
        else:
            return None
    except Exception as e:
        print(f"Error finding track: {str(e)}")
        return None


def download_audio(url):
    response = requests.get(url)
    file_name = 'temp_audio.mp3'
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return file_name


# Ссоры
@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['ссоры', 'сап ссоры', '.ссоры', '!ссоры', '/ссоры'])
async def handle_quarrel(message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
        mention = f"<a href='tg://user?id={user_id}'>{user_name}</a>"
        warning_message = f"⛔️<b>Внимание!</b> Специально для {mention} и для всех остальных. Ссоры в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещены.nсоветуем прекратить ссориться, иначе мы будем вынуждены заглушить вас.\n\n🤓<i>Ссора</i> - это конфликт или разногласие между людьми, организациями или группами, которое часто сопровождается словесными выяснениями, напряженностью и негативными эмоциями.\n\n📛За игнорирование предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Правила сетки", url="https://teletype.in/@drmotory/chatrules")
        url_button2 = types.InlineKeyboardButton(text="Мой список команд",
                                                 url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button1, url_button2)

        await message.reply(warning_message, reply=False, reply_markup=keyboard, parse_mode='HTML')
    else:
        warning_message = "⛔️<b>Внимание!</b> Ссоры в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещены.nсоветуем прекратить ссориться, иначе мы будем вынуждены заглушить вас.\n\n🤓<i>Ссора</i> - это конфликт или разногласие между людьми, организациями или группами, которое часто сопровождается словесными выяснениями, напряженностью и негативными эмоциями.\n\n📛За игнорирование предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."

        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Правила сетки", url="https://teletype.in/@drmotory/chatrules")
        url_button2 = types.InlineKeyboardButton(text="Мой список команд",
                                                 url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button1, url_button2)

        await message.reply(warning_message, reply=False, reply_markup=keyboard, parse_mode='HTML')


# Агрессия
@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['агрессия', 'сап агрессия', '.агрессия', '!агрессия', '/агрессия'])
async def handle_aggression(message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
        mention = f"<a href='tg://user?id={user_id}'>{user_name}</a>"
        warning_message = f"⛔️<b>Внимание! Специально для {mention} и для всех остальных. Агрессия в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещена.</b>nСоветуем отказаться от агрессии в наших чатах.n🤓<i>Агрессия</i> — это поведение, направленное на причинение вреда или проблем другому человекуn📛За игнорирования предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."



        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Правила сетки", url="https://teletype.in/@drmotory/chatrules")
        url_button2 = types.InlineKeyboardButton(text="Мой список команд",
                                                 url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button1, url_button2)

        await message.reply(warning_message, reply=False, reply_markup=keyboard, parse_mode='HTML')
    else:
        warning_message = "⛔️<b>Внимание! Агрессия в чатах сетки «ᎠᏫᏒᎷᏆᎢᏫᏒᎩ» запрещена.</b>\nСоветуем отказаться от агрессии в наших чатах.\n\n🤓<i>Агрессия</i> — это поведение, направленное на причинение вреда или проблем другому человеку.\n\n📛За игнорирования предупреждения админы имеют полное право выдать наказание, которое посчитают нужным."

        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Правила сетки", url="https://teletype.in/@drmotory/chatrules")
        url_button2 = types.InlineKeyboardButton(text="Мой список команд",
                                                 url="https://teletype.in/@drmotory/commands_support")
        keyboard.add(url_button1, url_button2)

        await message.reply(warning_message, reply=False, reply_markup=keyboard, parse_mode='HTML')


# Вики
wiki_wiki = wikipediaapi.Wikipedia(
    language='ru',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='wikipedia')


@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['вики', 'сап вики', '.вики', '!вики'])
async def wiki_search(message: types.Message):
    query = message.text[5:].strip()
    page = wiki_wiki.page(query)
    if page.exists():
        summary = page.summary[:1500]
        await message.reply(summary)
    else:
        await message.reply("Информация не найдена. Попробуйте изменить запрос.")


# Словарь
@dp.message_handler(
    lambda message: message.text.split()[0].strip().lower() in ['словарь', 'сап словарь', '.словарь', '!словарь'])
async def define_word(message: types.Message):
    command_parts = message.text.split(' ')
    if len(command_parts) > 1:
        word = command_parts[1]
        response = requests.get(
            f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20240101T213553Z.26e7fed62e078769.7468573f9cdcb622ca5087c8a063fc37b904dfde&lang=ru-ru&text={word}')

        if response.status_code == 200:
            data = response.json()
            if 'def' in data and data['def']:
                meanings = data['def'][0]['tr']
                response_message = f"📖 Пояснение слова {word}\n"
                for index, meaning in enumerate(meanings, start=1):
                    response_message += f"{index}⃣ {meaning['text']}\n"
                await message.reply(response_message)
            else:
                await message.reply(f"К сожалению, определение для слова '{word}' не найдено.")
        else:
            await message.reply("Извини, что-то пошло не так. Попробуй позже.")
    else:
        await message.reply("Используйте команду 'словарь' с указанием слова для поиска.")


# Реши
@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['реши', 'сап реши', '.реши', '!реши'])
async def solve_expression(message: types.Message):
    expression = re.search(r'\.реши (.+)', message.text).group(1)
    try:
        expr = sympify(expression)
        result = solve(expr)
        if len(result) == 0:
            solution = expr.evalf()
            await message.reply(f"👨‍🏫 {expression} = {solution}")
        else:
            await message.reply(f"👨‍🏫 {expression} = {result}")
    except Exception as e:
        await message.reply("Кажется, что-то пошло не так. Убедитесь, что пример введен корректно.")


# Пасхалки

@dp.message_handler(lambda message: message.text.lower() == 'как дела?')
async def how_are_you(message: Message):
    chance = random.random()
    if chance <= 0.09:
        await message.reply("У 4 админа точно средненько!")



# Автоматические штучки:
async def block_user(chat_id, user_id, user, message_id):
    try:
        await bot.restrict_chat_member(chat_id, user_id, types.ChatPermissions(can_send_messages=False), until_date=int(time.time()) + 86400)
        
        user_link = f"[{user.full_name}](tg://user?id={user.id})"
        block_message = f"🆘 Обнаружена подозрительная ссылка. Пользователь {user_link} заблокирован на сутки."

        unblock_button = InlineKeyboardButton(text="Разблокировать", callback_data=f"unblock_{user.id}")
        keyboard = InlineKeyboardMarkup().add(unblock_button)

        message = await bot.send_message(chat_id=chat_id, text=block_message, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)
        
        return message.message_id, message_id  # Возвращаем идентификаторы обоих сообщений

    except Exception as e:
        print(f"Ошибка при блокировке пользователя: {e}")

async def unblock_user(chat_id, user_id, moderator_id, block_message_id):
    try:
        moderator_chat_member = await bot.get_chat_member(chat_id, moderator_id)
        
        if moderator_chat_member.status not in ['administrator', 'creator']:
            return          
        user_chat_member = await bot.get_chat_member(chat_id, user_id)

        if user_chat_member.status not in ['administrator', 'creator']:
            await bot.restrict_chat_member(chat_id, user_id, types.ChatPermissions(can_send_messages=True))
        else:
            return
        
        user_link = f"[{user_chat_member.user.full_name}](tg://user?id={user_id})"
        admin_link = f"[{moderator_chat_member.user.full_name}](tg://user?id={moderator_id}"
        
        block_message = f"🆘 Обнаружена подозрительная ссылка. Пользователь {user_link} заблокирован на сутки.\n\n☑️ Пользователь разблокирован\nМодератор: {admin_link}"
        
        await bot.edit_message_text(chat_id=chat_id, message_id=block_message_id, text=block_message, parse_mode=types.ParseMode.MARKDOWN)
        
    except Exception as e:
        print(f"Ошибка при разблокировке пользователя: {e}")

@dp.message_handler()
async def check_message(message: types.Message):
    chat_id = message.chat.id  
    if re.search(r't(?:elegram)?\.me\/(.+)', message.text):
        user = message.from_user
        chat_member = await bot.get_chat_member(chat_id, user.id)
        
        if chat_member.status in ['administrator', 'creator']:
            return  # Если пользователь - администратор, не обрабатываем ссылку
        
        await bot.delete_message(chat_id, message.message_id)
        
        link_message_id = message.message_id  
        block_message_id, link_message_id = await block_user(chat_id, user.id, user, link_message_id)
        
        await asyncio.sleep(5)
        
        if block_message_id:
            await unblock_user(chat_id, user.id, user.id, block_message_id)

@dp.callback_query_handler(lambda query: query.data.startswith('unblock'))
async def process_unblock_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = int(callback_query.data.split('_')[1])
    block_message_id = callback_query.message.message_id
    
    user = await bot.get_chat_member(chat_id, user_id)
    if user.status in ['administrator', 'creator']:
        return
    
    moderator_id = callback_query.from_user.id
    moderator = await bot.get_chat_member(chat_id, moderator_id)
    
    if moderator.status not in ['administrator', 'creator']:
        return
    
    await unblock_user(chat_id, user_id, moderator_id, block_message_id)

    await bot.answer_callback_query(callback_query.id, text="Пользователь разблокирован.")









async def send_message():
    channel_message = await bot.send_message('-1001996822806', "проверка активности⬇️")
    return channel_message

@dp.message_handler(lambda message: message.text.split()[0].strip().lower() in ['.актив', 'сап актив', '.актив', '!актив'])
async def send_activity(message: types.Message):
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['creator', 'administrator']:
        await message.answer("У вас нет прав для использования этой функции.")
        return
    
    sent_message = await message.answer("проверяйте просмотры в сообщении ниже.")
    channel_message = await send_message()
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_message.chat.id, message_id=channel_message.message_id)





async def send_welcome(chat_id, message_id):
    await bot.send_message(chat_id,
                           '''📌 Закреплённое сообщение
      
      Перед тем как начать писать комментарии ознакомьтесь с [правилами](https://teletype.in/@drmotory/chatrules).
      Хотите влиться в коллектив?Прочитайте наш гайд «[🫂Как влиться в коллектив](https://teletype.in/@drmotory/collective-2)».\n\n_Спасибо за понимание._''',
                           parse_mode="Markdown",
                           reply_markup=create_markup(),
                           reply_to_message_id=message_id)  


def create_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Правила', url='https://teletype.in/@drmotory/chatrules'),
        types.InlineKeyboardButton('мой список команд', url='https://teletype.in/@drmotory/commands_support')
    )
    return markup


@dp.message_handler(content_types=types.ContentType.TEXT, is_forwarded=True)
async def handle_forwarded_message(message: types.Message):
    if message.forward_from_chat.type == 'channel':
        await send_welcome(message.chat.id, message.message_id)


@dp.message_handler()
async def handle_messages(message: types.Message):
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    if chat_member.status in ['administrator', 'creator'] and message.text.startswith('.дел '):
        chat_permissions = chat_member.can_delete_messages

        if chat_permissions:
            await delete_messages(message)
        else:
            await bot.send_message(message.chat.id, "У вас нет разрешения на удаление сообщений.")


async def delete_messages(message: types.Message):
    error_message = None

    try:
        number = int(message.text.split('.дел ')[1])

        if number > 0:
            replied_message_id = message.reply_to_message.message_id

            for i in range(number):
                try:
                    await bot.delete_message(message.chat.id, replied_message_id - i)
                except Exception as e:
                    error_message = f"Не удалось удалить сообщение с ID {replied_message_id - i}: {e}"

            if not error_message:
                await bot.send_message(message.chat.id, f"Я удалил {number} выбранных сообщений.")
                await bot.send_sticker(message.chat.id,
                                       "CAACAgIAAxkBAAI2nGWFXKEM4_NOSx3PQJUcQuWqFU2RAALMFQACdWepSdykWqEAAVfrBDME")

        else:
            await bot.send_message(message.chat.id,
                                   "Пожалуйста, введите корректное число и убедитесь, что вы ответили на сообщение, с которого начать удаление.")
    except (ValueError, AttributeError, IndexError):
        await bot.send_message(message.chat.id,
                               "Пожалуйста, введите корректное число и убедитесь, что вы ответили на сообщение, с которого начать удаление.")


admin_chat_id = '-1002129257694'
message_limit = 5
time_window = 10
alert_interval = 300
alert_interval_per_user = 300
user_messages = {}
last_alert_time = {}
flood_detected_users = set()


@dp.message_handler(content_types=['text', 'audio', 'photo', 'voice', 'video', 'document', 'sticker', 'animation'])
async def check_message_frequency(message: types.Message):
    user_id = message.from_user.id
    user_profile = f"[{message.from_user.first_name}](tg://user?id={user_id})"
    current_time = time.time()

    if user_id in user_messages:
        message_times = user_messages[user_id]
        message_times = list(filter(lambda x: current_time - x <= time_window, message_times))



        if len(message_times) > message_limit and user_id not in flood_detected_users:
            if user_id not in last_alert_time or current_time - last_alert_time[user_id] >= alert_interval:
                await bot.send_message(admin_chat_id,
                                       f"В чате от пользователя {user_profile} замечена активность похожая на флуд. Надо бороться с флудом!",
                                       parse_mode="Markdown")
                last_alert_time[user_id] = current_time

                message_url = f"https://t.me/{message.chat.username}/{message.message_id}"
                await bot.send_message(admin_chat_id, f"[Посмотреть сообщение]({message_url})", parse_mode="Markdown")

                flood_detected_users.add(user_id)
        elif len(message_times) > message_limit - 1:
            permissions = types.ChatPermissions(can_send_messages=False)
            await bot.restrict_chat_member(message.chat.id, user_id, permissions, until_date=int(time.time()) + 1800)
            await bot.send_message(admin_chat_id,
                                   f"Флуд от {user_profile} не прекращается. Пользователь получил мут на 30 минут.",
                                   parse_mode="Markdown")
            flood_detected_users.add(user_id)

        if user_id in last_alert_time and current_time - last_alert_time[user_id] < alert_interval_per_user:
            last_alert_time[user_id] = current_time

    if user_id in user_messages:
        user_messages[user_id].append(current_time)
    else:
        user_messages[user_id] = [current_time]


bot_stopped = False


async def on_startup(dp: Dispatcher):
    pass

#async def on_shutdown(dp: Dispatcher):
#    global bot_stopped
#    if not bot_stopped:
#        await bot.send_message(chat_id='your_chat_id', text="Бот выключен")
#        await bot.close()
#        bot_stopped = True


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await on_startup(dp)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Произошла притическая ошибка --> {e}')


if __name__ == "__main__":
    asyncio.run(main())