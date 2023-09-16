import logging
import os
import secrets
import string
import time
from datetime import datetime

import pymysql.cursors
from dotenv import load_dotenv
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      Update)
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)
from telegram.helpers import escape_markdown

from web import keep_alive

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot = Application.builder().token(str(os.getenv('BOT_TOKEN'))).build()

db = pymysql.connect(
    db=os.getenv('DB_BASE'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    cursorclass=pymysql.cursors.DictCursor,
    charset="utf8mb4",
    autocommit=True
)
cursor = db.cursor()

main_menu = ReplyKeyboardMarkup(
    [[
        KeyboardButton("❇️ Добавить кампанию"),
        KeyboardButton("✅ Актуальные приложения"),
    ], [
        KeyboardButton("🗂 Получить NAMING"),
        KeyboardButton("🔢 CAPS"),
    ], [
        KeyboardButton("🗄 Меню Фарма"),
        KeyboardButton("📇 Инфо Баинга"),
    ], [
        KeyboardButton("🔔 ВКЛ/ВЫКЛ PUSH о Депозите"),
        KeyboardButton("🤩 Уникализатор"),
    ], [
        KeyboardButton("📓 Поставить задачу"),
        KeyboardButton("🔖 Офферы"),
    ], [
        KeyboardButton("👥 Пользователи")
    ]],
    resize_keyboard=True
)
back_to_mm = ReplyKeyboardMarkup([['⬅️ Главное меню']], resize_keyboard=True)

tg_support = str(os.getenv('BOT_SUPPORT'))


async def DBError(update, context, e):
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=str(e)
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        try:
            cursor.execute(("SELECT * FROM users WHERE tg_id = "
                            f"{update.effective_chat.id}"))
            user = cursor.fetchone()
            db.commit()

            if (user['username'] != ''):
                username = escape_markdown(user['username'])
            else:
                username = escape_markdown(update.effective_user.full_name)

            tg_link = "tg://user?id=" + str(update.effective_user.id)

            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=(f"👋 [{username}]({tg_link}), добро пожаловать в *"
                      f"{str(os.getenv('BOT_NAME'))}*!"),
                reply_markup=main_menu,
                parse_mode="Markdown",
                )

        except pymysql.Error as e:
            await DBError(update, context, e)
            return False


async def mainMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*📜 Что нужно сделать:*",
            reply_markup=main_menu,
            parse_mode="Markdown",
            )


async def addCampaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*❇️ Добавление кампании*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def actualApps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*✅ Актуальные приложения*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def getNaming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*🗂 Получения нэйминга*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def camp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*🔢 КАПС*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def menuFarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*🗄 Меню фарма*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def infoBaing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*📇 Инфо Баинга*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def pushDeposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*🔔 Пуши о депозите*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def uniqueizer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*🤩 Уникализатор*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def setTask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*📓 Задачи*",
            reply_markup=back_to_mm,
            parse_mode="Markdown",
            )


async def menuOffers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*🔖 Что делать с офферами?*",
            reply_markup=ReplyKeyboardMarkup([[
                KeyboardButton("🗒 Все Офферы"),
                KeyboardButton("📝 Сменить Оффер")],
                [KeyboardButton("⬅️ Главное меню")]
            ], resize_keyboard=True),
            parse_mode="Markdown",
            )


async def allOffers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        try:
            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text='*🗒 Все офферы*',
                reply_markup=ReplyKeyboardMarkup([[
                    KeyboardButton('🔖 Офферы'),
                    KeyboardButton('⬅️ Главное меню')]
                ], resize_keyboard=True),
                parse_mode="Markdown",
                )

            cursor.execute("SELECT * FROM offers")
            offers = cursor.fetchall()
            db.commit()

            if (len(offers) >= 1):
                for offer in offers:
                    name = escape_markdown(str(offer['name']))
                    source = escape_markdown(str(offer['source']))
                    type_cap = escape_markdown(str(offer['type']))
                    count = escape_markdown(str(offer['count']))
                    offer_id = escape_markdown(str(offer['offer_id']))
                    advertiser = escape_markdown(str(offer['advertiser']),
                                                 2).replace('\\', '')

                    await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text=(
                            f"🔍\nОффер: *{name}*\n"
                            f"Источник: *{source}*\n"
                            f"Тип CAP: *{type_cap}*\n"
                            f"Колличество: *{count}*\n"
                            f"ID: *{offer_id}*\n"
                            f"Рекламодатель: *{advertiser}*\n"
                            f"GEO: *{escape_markdown(str(offer['geo']))}*\n"
                            f"Link: *{escape_markdown(str(offer['link']))}*"
                        ), parse_mode="Markdown",
                        )
            else:
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text="❌ Офферов не найдено!", parse_mode="Markdown",
                    )

        except pymysql.Error as e:
            await DBError(update, context, e)


async def changeOffer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*📝 Смена оффера*",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton('🔖 Офферы'),
                 KeyboardButton('⬅️ Главное меню')]
            ], resize_keyboard=True),
            parse_mode="Markdown",
            )


async def menuUsers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="*👥 Что делать с пользователями?*",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("🧾 Все пользователи"),
                 KeyboardButton("⬅️ Главное меню")]
            ], resize_keyboard=True),
            parse_mode="Markdown",
            )


async def allUsers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        try:
            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text='*🧾 Все пользователи*',
                reply_markup=ReplyKeyboardMarkup([
                    [KeyboardButton('👥 Пользователи'),
                        KeyboardButton('⬅️ Главное меню')]
                ], resize_keyboard=True),
                parse_mode="Markdown",
                )

            cursor.execute((
                "SELECT * FROM users WHERE type NOT IN "
                "('mainadmin', 'admin')"))
            users = cursor.fetchall()
            db.commit()

            if (len(users) >= 1):
                for user in users:
                    if (user['locked'] == 1):
                        locked = "🟢"
                    else:
                        locked = "🔴"

                    if (user['baned'] == 1):
                        baned = "🟢"
                    else:
                        baned = "🔴"

                    if (user['create_timestamp'] == 0):
                        create_ts = "Никогда"
                    else:
                        create_ts = datetime.fromtimestamp(
                            user['create_timestamp']).strftime(
                                "%d/%m/%Y, %H:%M:%S")

                    if (user['auth_timestamp'] == 0):
                        auth_ts = "Никогда"
                    else:
                        auth_ts = datetime.fromtimestamp(
                            user['auth_timestamp']).strftime(
                                "%d/%m/%Y, %H:%M:%S")

                    await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text=(f"👤\nID: <b>{str(user['id'])}</b>\n"
                              f"Telegram ID: <b>{str(user['tg_id'])}</b>\n"
                              f"Имя: <b>{str(user['username'])}</b>\n"
                              f"Пароль: <b>{str(user['password'])}</b>\n"
                              f"Роль: <b>{str(user['type'])}</b>\n"
                              f"Заблокирован: <b>{str(locked)}</b>\n"
                              f"Забанен: <b>{str(baned)}</b>\n"
                              f"Зарегистрирован: <b>{str(create_ts)}</b>\n"
                              f"Последний вход: <b>{str(auth_ts)} </b>"
                              ), parse_mode="HTML",
                        )
            else:
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text='*❌ Пользователи не найдены!',
                    parse_mode="Markdown",
                    )

        except pymysql.Error as e:
            await DBError(update, context, e)


async def editUser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        try:
            commandText = update.effective_message.text.split(' ')
            await editUserStore(update, context, commandText)

        except pymysql.Error as e:
            await DBError(update, context, e)


async def editUserStore(update: Update,
                        context: ContextTypes.DEFAULT_TYPE,
                        commandText):
    try:
        if (len(commandText) == 1):
            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text='*❌ Ошибка 1:* Нужно указать _TYPE_',
                parse_mode="Markdown",
                )
        elif (len(commandText) == 2):
            types = ['username', 'password', 'type']
            if (commandText[1] in types):
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text='*❌ Ошибка 2:* Нужно указать _NEW VALUE_',
                    parse_mode="Markdown",
                    )
            else:
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text=(f"*❌ Ошибка 1.1: * _TYPE_ [{', '.join(types)}] не "
                          "найден в базе!"),
                    parse_mode="Markdown",
                    )

        elif (len(commandText) == 3):
            cursor.execute(("SELECT * FROM users WHERE tg_id = "
                            f"{update.effective_chat.id}"))
            rows = cursor.fetchone()
            db.commit()

            data = [rows['username'], rows['type']]

            sql = ((f"UPDATE users SET {commandText[1]} = "
                    f"'{commandText[2]}' WHERE tg_id = "
                    f"{update.effective_chat.id}"))

            cursor.execute(sql)
            db.commit()

            if (commandText[1] == "username"):
                text = ("✅ Вы успешно изменили *имя* с *"
                        f"{data[0]}* на *{commandText[2]}*!")
            elif (commandText[1] == "password"):
                text = "✅ Вы успешно изменили *пароль*!"
            elif (commandText[1] == "type"):
                text = ("✅ Вы успешно изменили *тип* с *"
                        f"{data[1]}* на *{commandText[2]}*!")
            else:
                text = "❌ Не удалось изменить данные пользователя!"

            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode="Markdown",
                )

    except pymysql.Error as e:
        await DBError(update, context, e)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cursor.execute(("SELECT * FROM users WHERE tg_id = "
                        f"{update.effective_chat.id}"))
        user = cursor.fetchone()
        db.commit()

        if (user['login_now'] == 1):
            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=("*✅ Вы уже авторизованы!*\nИспользуйте комманду "
                      "*/start* что бы начать."),
                parse_mode="Markdown",
                )
        else:
            if (user):
                commandText = update.effective_message.text.split(' ')
                if (len(commandText) >= 2):
                    if (commandText[1] == user['password']):
                        cursor.execute(("UPDATE users SET login_now = "
                                        "1, auth_timestamp = "
                                        f"{time.time()} WHERE tg_id = "
                                        f"{update.effective_chat.id}"))
                        db.commit()

                        await context.bot.deleteMessage(
                            chat_id=update.effective_chat.id,
                            message_id=update.message._id_attrs[0],
                            )

                        await context.bot.sendMessage(
                            chat_id=update.effective_chat.id,
                            text="*✅ Вы успешно авторизовались!*",
                            reply_markup=main_menu,
                            parse_mode="Markdown",
                            )

                        await start(update, context)

                    else:
                        await context.bot.sendMessage(
                            chat_id=update.effective_chat.id,
                            text=("*⛔️ Неверный пароль!*\nЕсли Вы забыли "
                                  "пароль, обратитесь за помощью "
                                  "к {tg_support}!"),
                            parse_mode="Markdown",
                        )
                else:
                    await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text=("*❌ Не указан пароль!*\nКомманда должна "
                              "быть /login _ВашПароль_.\nЕсли Вы забыли "
                              f"пароль, обратитесь за помощью к "
                              f"{tg_support}!"),
                        parse_mode="Markdown",
                        )
            else:
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text=("*⛔️ Вы не зарегистрированы!*\nОбратитесь к "
                          f"{tg_support} за помощью!"),
                    parse_mode="Markdown",
                    )

    except pymysql.Error as e:
        await DBError(update, context, e)


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cursor.execute(("SELECT * FROM users WHERE tg_id = "
                        f"{update.effective_chat.id} && login_now = 1"))
        db.commit()

        if (cursor.fetchone()):
            cursor.execute(("UPDATE users SET login_now = 0 WHERE tg_id = "
                            f"{update.effective_chat.id}"))
            db.commit()

            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=("*✅ Вы успешно разлогинились!*\nЧтобы войти снова, "
                      "введите комманду /login _ВашПароль_."),
                reply_markup=ReplyKeyboardRemove(True),
                parse_mode="Markdown",
                )

        else:
            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=("*✅ Нужно авторизоваться!*\nВведите комманду /login "
                      "_ВашПароль_.\nЕсли Вы забыли пароль, обратитесь за "
                      f"помощью к {tg_support}!"),
                parse_mode="Markdown",
                )

    except pymysql.Error as e:
        await DBError(update, context, e)


async def checkLogin(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        cursor.execute(("SELECT * FROM users WHERE tg_id = "
                        f"{update.effective_chat.id}"))
        user = cursor.fetchone()
        db.commit()

        if (user and user['login_now'] == 1):
            return True
        else:
            if (await createUser(update, context)):
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text=("*✅ Нужно авторизоваться!*\nВведите комманду "
                          "/login _ВашПароль_.\nЕсли Вы забыли пароль, "
                          f"обратитесь за помощью к {tg_support}!"),
                    reply_markup=ReplyKeyboardRemove(True),
                    parse_mode="Markdown",
                    )
                return False

        return False

    except pymysql.Error as e:
        await DBError(update, context, e)
        return False


async def checkRole(update: Update,
                    context: ContextTypes.DEFAULT_TYPE, roles) -> bool:
    try:
        cursor.execute(("SELECT type FROM users WHERE tg_id = "
                        f"{update.effective_chat.id}"))
        role = cursor.fetchone()
        db.commit()

        if (role['type'] in roles):
            return True
        else:
            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=("❌ Вам недоступно выполнение данной операции!\n"
                      f"Вы можете запросить доступ у {tg_support}."),
                parse_mode="Markdown",
                )
            return False

    except pymysql.Error as e:
        await DBError(update, context, e)
        return False


async def createUser(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        cursor.execute(("SELECT * FROM users WHERE tg_id = "
                        f"{update.effective_chat.id}"))
        db.commit()

        if (cursor.fetchone()):
            return True
        else:
            if (update.effective_chat.first_name):
                username = update.effective_chat.first_name
            else:
                username = "UserName"

            password = ''
            for i in range(8):
                password += ''.join(secrets.choice(
                    string.ascii_letters + string.digits +
                    string.punctuation))

            cursor.execute(("INSERT INTO users (tg_id, username, "
                            "password, type, create_timestamp) "
                            "VALUES (%s, %s, %s, %s, %s)", (
                                update.effective_chat.id,
                                str(username), str(password), "user",
                                str(time.time()).split('.')[0])))
            db.commit()

            text = ("*✅ Вы успешно зарегистрированы!*\n\n🔑 Ваш пароль: `"
                    f"{escape_markdown(password, 2)}"
                    "`\nЧтобы авторизоваться, введите комманду /login "
                    "_ВашПароль_.\n\n*❗️ В целях безопасности, "
                    "рекомендуем запомнить Ваш пароль и удалить данное "
                    "сообщение!*")

            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode="MarkdownV2",
                )

            return False

    except pymysql.Error as e:
        await DBError(update, context, e)
        return False


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text=(
                "*📘 Помощь!*\n\n"
                "📍 /login - команда для авторизации в боте\n"
                "  `Например:` /login *password*\n\n"

                "📍 /edituser - команда для изменения своих данных\n"
                "  `Параметры:` \n"
                "    *тип* - может быть _username_, _password_ или _type_;\n"
                "    *новоеЗначение* - должно содержать строчный тип данных.\n"
                "  `Например:` /edituser *username* *НовоеИмя*\n\n"

                "📍 /admins - команда для вывода списка админов\n\n"
                "📍 /logout - команда для завершения сессии в боте\n\n"
                "📍 /help - команда для вывода этого сообщения\n\n"

                "Если Вы забыли пароль, обратитесь за помощью к "
                f"{tg_support}!"),
            parse_mode="Markdown",
            )


async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        if (await checkRole(update, context, roles=["mainadmin", "admin"])):
            try:
                cursor.execute("SELECT * FROM users WHERE type IN "
                               "('mainadmin', 'admin')")
                admins = cursor.fetchall()
                db.commit()

                if (len(admins) >= 1):
                    await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text="*👑 Админы!*\n\n",
                        parse_mode="Markdown",
                        )

                    for admin in admins:
                        if (admin['type'] == 'mainadmin'):
                            type = "Главный админ"
                        elif (admin['type'] == 'admin'):
                            type = "Админ"

                        if (admin['locked'] == 1):
                            locked = "🟢"
                        else:
                            locked = "🔴"

                        if (admin['baned'] == 1):
                            baned = "🟢"
                        else:
                            baned = "🔴"

                        if (admin['create_timestamp'] == 0):
                            create_ts = "Никогда"
                        else:
                            create_ts = datetime.fromtimestamp(
                                admin['create_timestamp']).strftime(
                                    "%d/%m/%Y, %H:%M:%S")

                        if (admin['auth_timestamp'] == 0):
                            auth_ts = "Никогда"
                        else:
                            auth_ts = datetime.fromtimestamp(
                                admin['auth_timestamp']).strftime(
                                    "%d/%m/%Y, %H:%M:%S")

                        tg_id = str(admin['tg_id'])

                        await context.bot.sendMessage(
                            chat_id=update.effective_chat.id,
                            text=(f"👤\nID: <b>{str(admin['id'])}</b>\n"
                                  f"Telegram ID: <b>{tg_id}</b>\n"
                                  f"Имя: <b>{str(admin['username'])}</b>\n"
                                  f"Роль: <b>{str(type)}</b>\n"
                                  f"Заблокирован: <b>{str(locked)}</b>\n"
                                  f"Забанен: <b>{str(baned)}</b>\n"
                                  f"Зарегистрирован: <b>{str(create_ts)}</b>\n"
                                  f"Последний вход: <b>{str(auth_ts)}</b>"
                                  ), parse_mode="HTML",
                            )
                else:
                    await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text=("*👑 Админы!*\n\n"
                              " ❌ Администраторов не найдено!"),
                        parse_mode="Markdown",
                        )

            except pymysql.Error as e:
                await DBError(update, context, e)
                return False


def main():
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help))
    bot.add_handler(CommandHandler("edituser", editUser))
    bot.add_handler(CommandHandler("admins", admins))
    bot.add_handler(CommandHandler("login", login))
    bot.add_handler(CommandHandler("logout", logout))

    mh = [
        ("⬅️ Главное меню", mainMenu),

        ("❇️ Добавить кампанию", addCampaign),
        ("✅ Актуальные приложения", actualApps),
        ("🗂 Получить NAMING", getNaming),
        ("🔢 CAPS", camp),
        ("🗄 Меню Фарма", menuFarm),
        ("📇 Инфо Баинга", infoBaing),
        ("🔔 ВКЛ/ВЫКЛ PUSH о Депозите", pushDeposit),
        ("🤩 Уникализатор", uniqueizer),
        ("📓 Поставить задачу", setTask),

        ("🔖 Офферы", menuOffers),
        ("🗒 Все Офферы", allOffers),
        ("📝 Сменить Оффер", changeOffer),

        ("👥 Пользователи", menuUsers),
        ("🧾 Все пользователи", allUsers),
    ]

    for button, func in mh:
        bot.add_handler(MessageHandler(
            filters.Regex("^(" + button + ")$"), func))

    keep_alive()
    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
