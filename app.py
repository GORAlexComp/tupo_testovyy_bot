import logging
import os

import pymysql
from dotenv import load_dotenv
from telegram import (ForceReply, InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      Update)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler,
                          filters)
from telegram.helpers import escape_markdown

from web import keep_alive

load_dotenv()

logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

timeout = 10
connection = pymysql.connect(
	charset = "utf8mb4",
	cursorclass = pymysql.cursors.DictCursor,
	db = os.getenv('DB_BASE'),
	host = os.getenv('DB_HOST'),
	port = int(os.getenv('DB_PORT')),
	user = os.getenv('DB_USER'),
	password = os.getenv('DB_PASSWORD'),
	connect_timeout = int(os.getenv('DB_TIMEOUT')),
	read_timeout = int(os.getenv('DB_TIMEOUT')),
	write_timeout = int(os.getenv('DB_TIMEOUT')),
)

main_menu = ReplyKeyboardMarkup([
	[
		KeyboardButton("Добавить кампанию"),
		KeyboardButton("✅ Актуальные приложения"),
	], [
		KeyboardButton("Получить NAMING 🗂"),
		KeyboardButton("🔢 CAPS"),
	], [
		KeyboardButton("Меню Фарма 🗄"),
		KeyboardButton("📇 Инфо Баинга"),
	], [
		KeyboardButton("🔔 ВКЛ/ВЫКЛ PUSH о Депозите"),
		KeyboardButton("🤩 Уникализатор"),
	], [
		KeyboardButton("Поставить задачу 📓"),
		KeyboardButton("📝 Сменить Оффер"),
	]
], resize_keyboard = True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "👋 [" + escape_markdown(update.effective_user.full_name, 2) + \
			"](tg://user?id=" + str(update.effective_user.id) + "), добро пожаловать в" + \
			" *" + os.getenv('BOT_NAME') + "* " + escape_markdown("BOT!", 2)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = main_menu,
		parse_mode = "MarkdownV2",
		)

async def allOffers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM offers")
	rows = cursor.fetchall()

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = '*Все офферы*',
		reply_markup = main_menu,
		parse_mode = "MarkdownV2",
		)

	if (rows):
		for row in rows:
			text = 'Оффер: *' + escape_markdown(str(row['name'])) + '*\n'  \
					'Источник: *' + escape_markdown(str(row['source'])) + '*\n'  \
					'Тип CAP: *' + escape_markdown(str(row['type'])) + '*\n'  \
					'Колличество: *' + escape_markdown(str(row['count'])) + '*\n'  \
					'ID: *' + escape_markdown(str(row['offer_id'])) + '*\n'  \
					'Рекламодатель: *' + escape_markdown(str(row['advertiser']), 2).replace('\\', '') + '*\n'  \
					'GEO: *' + escape_markdown(str(row['geo'])) + '*\n'  \
					'Link: *' + escape_markdown(str(row['link'])) + '*'

			await context.bot.sendMessage(
				chat_id = update.effective_chat.id,
				text = text,
				reply_markup = main_menu,
				parse_mode = "Markdown",
				)
	else:
		await context.bot.sendMessage(
			chat_id = update.effective_chat.id,
			text = escape_markdown('Error databese! Please, try again later!', 2),
			reply_markup = main_menu,
			parse_mode = "MarkdownV2",
			)

async def mainMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Что нужно сделать:"

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = main_menu,
		parse_mode = "MarkdownV2",
		)

async def addCampaign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница добавления кампании"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def actualApps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница актуальных приложений"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def getNaming(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница получения нэйминга"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def camp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница КАПС"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def menuFarm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Меню фарма"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def infoBaing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница с инфо Баинга"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def pushDeposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница Пуши о депозите"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def uniqueizer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница уникализатора"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def setTask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Задачи"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

async def changeOffer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	text = "Страница смены оффера"
	menu = ReplyKeyboardMarkup([['⬅️ Main menu']], resize_keyboard = True)

	await context.bot.sendMessage(
		chat_id = update.effective_chat.id,
		text = text,
		reply_markup = menu,
		parse_mode = "MarkdownV2",
		)

def main() -> None:
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("alloffers", allOffers))

	application.add_handler(MessageHandler(filters.Regex("^(⬅️ Main menu)$"), mainMenu))
	application.add_handler(MessageHandler(filters.Regex("^(Добавить кампанию)$"), addCampaign))
	application.add_handler(MessageHandler(filters.Regex("^(✅ Актуальные приложения)$"), actualApps))
	application.add_handler(MessageHandler(filters.Regex("^(Получить NAMING 🗂)$"), getNaming))
	application.add_handler(MessageHandler(filters.Regex("^(🔢 CAPS)$"), camp))
	application.add_handler(MessageHandler(filters.Regex("^(Меню Фарма 🗄)$"), menuFarm))
	application.add_handler(MessageHandler(filters.Regex("^(📇 Инфо Баинга)$"), infoBaing))
	application.add_handler(MessageHandler(filters.Regex("^(🔔 ВКЛ/ВЫКЛ PUSH о Депозите)$"), pushDeposit))
	application.add_handler(MessageHandler(filters.Regex("^(🤩 Уникализатор)$"), uniqueizer))
	application.add_handler(MessageHandler(filters.Regex("^(Поставить задачу 📓)$"), setTask))
	application.add_handler(MessageHandler(filters.Regex("^(📝 Сменить Оффер)$"), changeOffer))

	keep_alive()
	application.run_polling(allowed_updates = Update.ALL_TYPES)

if __name__ == "__main__":
	main()
