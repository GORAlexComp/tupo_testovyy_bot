import logging
import os
import secrets
import string
import time
from datetime import datetime

import pymysql
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

application = Application.builder().token(str(os.getenv('BOT_TOKEN'))).build()

timeout = 10
connection = pymysql.connect(
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    db=os.getenv('DB_BASE'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    connect_timeout=int(os.getenv('DB_TIMEOUT')),
    read_timeout=int(os.getenv('DB_TIMEOUT')),
    write_timeout=int(os.getenv('DB_TIMEOUT')),
    autocommit=True
)

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
    connection.close()
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=escape_markdown(str(e), 2),
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = \
                           {update.effective_chat.id}")
            rows = cursor.fetchall()

            if (rows[0]['username'] != ''):
                username = escape_markdown(rows[0]['username'], 2)
            else:
                username = escape_markdown(update.effective_user.full_name, 2)

            tg_link = "tg://user?id=" + str(update.effective_user.id)

            await context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=(f"👋 [{username}]({tg_link}), добро пожаловать в *"
                      f"{str(os.getenv('BOT_NAME'))}*\\!"),
                reply_markup=main_menu,
                parse_mode="MarkdownV2",
                )


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

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM offers")
            rows = cursor.fetchall()

            for row in rows:
                count = escape_markdown(str(row['count']))
                advertiser = escape_markdown(str(row['advertiser']),
                                             2).replace('\\', '')

                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text=(
                        f"🔍\nОффер: *{escape_markdown(str(row['name']))}*\n"
                        f"Источник: *{escape_markdown(str(row['source']))}*\n"
                        f"Тип CAP: *{escape_markdown(str(row['type']))}*\n"
                        f"Колличество: *{count}*\n"
                        f"ID: *{escape_markdown(str(row['offer_id']))}*\n"
                        f"Рекламодатель: *{advertiser}*\n"
                        f"GEO: *{escape_markdown(str(row['geo']))}*\n"
                        f"Link: *{escape_markdown(str(row['link']))}*"
                    ), parse_mode="Markdown",
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
            with connection.cursor() as cursor:
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text='*🧾 Все пользователи*',
                    reply_markup=ReplyKeyboardMarkup([
                        [KeyboardButton('👥 Пользователи'),
                         KeyboardButton('⬅️ Главное меню')]
                    ], resize_keyboard=True),
                    parse_mode="Markdown",
                    )

                cursor.execute("SELECT * FROM users")
                rows = cursor.fetchall()

                for row in rows:
                    if (row['locked'] == 1):
                        locked = "🟢"
                    else:
                        locked = "🔴"

                    if (row['baned'] == 1):
                        baned = "🟢"
                    else:
                        baned = "🔴"

                    if (row['create_timestamp'] == 0):
                        create_ts = "Никогда"
                    else:
                        create_ts = datetime.fromtimestamp(
                            row['create_timestamp']).strftime(
                                "%d/%m/%Y, %H:%M:%S")

                    if (row['auth_timestamp'] == 0):
                        auth_ts = "Никогда"
                    else:
                        auth_ts = datetime.fromtimestamp(
                            row['auth_timestamp']).strftime(
                                "%d/%m/%Y, %H:%M:%S")

                    await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text=(f"👤\nID: <b>' {str(row['id'])} </b>\n"
                              f"Telegram ID: <b> {str(row['tg_id'])} </b>\n"
                              f"Имя: <b> {str(row['username'])} </b>\n"
                              f"Пароль: <b> {str(row['password'])} </b>\n"
                              f"Роль: <b> {str(row['type'])} </b>\n"
                              f"Заблокирован: <b> {str(locked)} </b>\n"
                              f"Забанен: <b> {str(baned)} </b>\n"
                              f"Зарегистрирован: <b> {str(create_ts)} </b>\n"
                              f"Последний вход: <b> {str(auth_ts)} </b>"
                              ), parse_mode="HTML",
                        )
        except pymysql.Error as e:
            await DBError(update, context, e)


async def editUser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (await checkLogin(update, context)):
        try:
            commandText = update.effective_message.text.split(' ')
            await editUserStore(update, context, commandText)
        except Exception as e:
            await DBError(update, context, e)


async def editUserStore(update: Update,
                        context: ContextTypes.DEFAULT_TYPE,
                        commandText):
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
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = \
                           {update.effective_chat.id}")
            rows = cursor.fetchall()
            data = [rows[0]['username'], rows[0]['type']]

            cursor.execute("UPDATE users SET " + f"{str(commandText[1])}" + " \
                = %s WHERE tg_id = %s", (str(commandText[2]),
                                         int(update.effective_chat.id)))

        if (commandText[1] == "username"):
            type = f"*имя* с *{data[0]}* на *{commandText[1]}*!"
        elif (commandText[1] == "password"):
            type = "*пароль*!"
        elif (commandText[1] == "type"):
            type = f"*тип* с *{data[1]}* на *{commandText[2]}*!"

        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text=(f"*✅ Вы успешно изменили {type}"),
            parse_mode="Markdown",
            )


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = \
                           {update.effective_chat.id}")
            rows = cursor.fetchall()

            if (rows[0]['login_now'] == 1):
                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text=("*✅ Вы уже авторизованы!*\nИспользуйте комманду "
                          "*/start* что бы начать."),
                    parse_mode="Markdown",
                    )
            else:
                if (len(rows) >= 1):
                    commandText = update.effective_message.text.split(' ')
                    if (len(commandText) >= 2):
                        if (commandText[1] == rows[0]['password']):
                            cursor.execute(f"UPDATE users SET login_now = 1, \
                                auth_timestamp = {time.time()} WHERE tg_id = \
                                    {update.effective_chat.id}")

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
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = \
                           {update.effective_chat.id} && login_now = 1")
            rows = cursor.fetchall()

            if (len(rows) >= 1):
                cursor.execute(f"UPDATE users SET login_now = 0 WHERE tg_id = \
                               {update.effective_chat.id}")

                await context.bot.sendMessage(
                    chat_id=update.effective_chat.id,
                    text=(
                        "*✅ Вы успешно разлогинились!*\nЧтобы войти снова, "
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
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = \
                           {update.effective_chat.id}")
            rows = cursor.fetchall()

            if (len(rows) >= 1 and rows[0]['login_now'] == 1):
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


async def createUser(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = \
                           {update.effective_chat.id}")
            rows = cursor.fetchall()

            if (len(rows) >= 1):
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

                cursor.execute("INSERT INTO users (`tg_id`, `username`, \
                               `password`, `type`, `create_timestamp`) \
                               VALUES (%s, %s, %s, %s, %s)", (
                                   update.effective_chat.id, str(username),
                                   str(password), "user",
                                   str(time.time()).split('.')[0]))

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
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=("*📘 Помощь!*\n\n"
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

              f"Если Вы забыли пароль, обратитесь за помощью к {tg_support}!"),
        reply_markup=ReplyKeyboardRemove(True),
        parse_mode="Markdown",
        )


def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("edituser", editUser))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("logout", logout))

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
        application.add_handler(MessageHandler(
            filters.Regex("^(" + button + ")$"), func))

    keep_alive()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
